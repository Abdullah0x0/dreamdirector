import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Image as ImageIcon, 
  Music, 
  Video, 
  Loader, 
  Sparkles,
  ChevronRight,
  Volume2,
  VolumeX
} from 'lucide-react'
import { useApp } from '../context/AppContext'

function StoryPage() {
  const { 
    currentStory, 
    isStoryActive, 
    isGenerating, 
    generationProgress,
    generatedImages,
    generatedVideos, 
    generatedMusic,
    startNewStory, 
    makeChoice,
    generateMedia,
    dispatch
  } = useApp()
  
  const [storyInput, setStoryInput] = useState('')
  const [storyEvents, setStoryEvents] = useState([]) // Track all story events
  const [isPlaying, setIsPlaying] = useState(false)
  const [choiceAnimation, setChoiceAnimation] = useState(false)
  const [screenShake, setScreenShake] = useState(false)
  const [dramaticFlash, setDramaticFlash] = useState(false)
  const [pulseEffect, setPulseEffect] = useState(false)
  const [choiceGlow, setChoiceGlow] = useState(-1) // Which choice is glowing

  // Add new story events to the progression
  const addStoryEvent = (event) => {
    setStoryEvents(prev => [...prev, {
      id: Date.now(),
      timestamp: new Date().toLocaleTimeString(),
      ...event
    }])
  }

  // Function to clean markdown asterisks from text
  const cleanMarkdown = (text) => {
    if (!text) return text
    return text.replace(/\*\*(.*?)\*\*/g, '$1').replace(/\*(.*?)\*/g, '$1')
  }

  const handleStartStory = async () => {
    if (!storyInput.trim()) return
    
    // DRAMATIC SCREEN EFFECTS
    setDramaticFlash(true)
    setScreenShake(true)
    setPulseEffect(true)
    
    setTimeout(() => {
      setDramaticFlash(false)
      setScreenShake(false)
      setPulseEffect(false)
    }, 1000)
    
    const startEvent = {
      type: 'story_start',
      content: `🎬 Starting: ${storyInput}`,
      timestamp: new Date().toLocaleTimeString()
    }
    setStoryEvents([startEvent])
    
    try {
      const result = await startNewStory(storyInput)
      
      // Add narrative to timeline if present
      if (result.story_progression) {
        const narrativeEvents = result.story_progression.map((event, index) => ({
          id: Date.now() + index + 1,
          type: event.type || 'narrative',
          content: event.type === 'story_opening' 
            ? cleanMarkdown(`📖 ${event.content}`)
            : cleanMarkdown(event.content),
          timestamp: new Date().toLocaleTimeString()
        }))
        setStoryEvents(prev => [...prev, ...narrativeEvents])
      }
      
      // Add scene description
      if (result.scene_description) {
        const sceneEvent = {
          id: Date.now() + 100,
          type: 'scene',
          content: cleanMarkdown(`📍 ${result.scene_description}`),
          timestamp: new Date().toLocaleTimeString()
        }
        setStoryEvents(prev => [...prev, sceneEvent])
      }
      
      // **AUTO-FETCH MEDIA** - After 2 seconds, check for newly generated media
      setTimeout(async () => {
        try {
          await fetchLatestMedia()
        } catch (error) {
          console.log('Media fetch error:', error)
        }
      }, 2000)
      
      console.log('Story started successfully:', result)
      
    } catch (error) {
      console.error('Story start error:', error)
      const errorEvent = {
        id: Date.now(),
        type: 'error',
        content: `❌ Failed to start story: ${error.message}`,
        timestamp: new Date().toLocaleTimeString()
      }
      setStoryEvents(prev => [...prev, errorEvent])
    }
  }

  const handleChoice = async (choice, choiceIndex) => {
    if (!choice || isGenerating) return
    
    try {
      const result = await makeChoice(choice)
      
      // Add user choice to timeline
      const choiceEvent = {
        id: Date.now(),
        type: 'user_choice',
        content: cleanMarkdown(`🎭 You chose: ${choice}`),
        timestamp: new Date().toLocaleTimeString()
      }
      setStoryEvents(prev => [...prev, choiceEvent])
      
      // Add story progression events with dramatic effect
      if (result.story_progression) {
        const progressionEvents = result.story_progression.map((event, index) => ({
          id: Date.now() + index + 1,
          type: event.type,
          content: event.type === 'choice_result' 
            ? cleanMarkdown(`🎭 Your Choice Result: ${event.content}`)
            : event.type === 'story_continuation'
            ? cleanMarkdown(`📖 Story Continues: ${event.content}`)
            : event.type === 'new_situation'
            ? cleanMarkdown(`🎯 New Situation: ${event.content}`)
            : cleanMarkdown(event.content),
          timestamp: new Date().toLocaleTimeString()
        }))
        setStoryEvents(prev => [...prev, ...progressionEvents])
      }
      
      // Add scene update
      if (result.scene_description) {
        const sceneEvent = {
          id: Date.now() + 100,
          type: 'scene',
          content: cleanMarkdown(`📍 Scene: ${result.scene_description}`),
          timestamp: new Date().toLocaleTimeString()
        }
        setStoryEvents(prev => [...prev, sceneEvent])
      }
      
      // **AUTO-FETCH NEW MEDIA** - Fetch media generated during choice processing
      setTimeout(async () => {
        try {
          await fetchLatestMedia()
          
          // If story completed, fetch again in case epic video was generated
          if (result.story_complete) {
            console.log('🎬 Story completed! Fetching epic finale video...')
            setTimeout(async () => {
              try {
                await fetchLatestMedia()
              } catch (error) {
                console.log('Epic video fetch error:', error)
              }
            }, 5000) // Wait additional 5 seconds for epic video generation
          }
        } catch (error) {
          console.log('Media fetch after choice:', error)
        }
      }, 3000) // Wait 3 seconds for video/music generation to complete
      
      console.log('Choice processed successfully:', result) // Debug log
      
    } catch (error) {
      console.error('Choice error:', error)
      const errorEvent = {
        id: Date.now(),
        type: 'error',
        content: `❌ Error processing choice: ${error.message}`,
        timestamp: new Date().toLocaleTimeString()
      }
      setStoryEvents(prev => [...prev, errorEvent])
    }
  }

  const handleGenerateMedia = async (type) => {
    const prompt = currentStory?.scene_description || storyInput || 'mysterious adventure scene'
    
    addStoryEvent({
      type: 'media_generation',
      content: `🎨 Generating ${type} for current scene...`
    })
    
    try {
      await generateMedia(type, prompt)
      
      addStoryEvent({
        type: 'media_complete',
        content: `✨ ${type.charAt(0).toUpperCase() + type.slice(1)} generated successfully!`
      })
    } catch (error) {
      addStoryEvent({
        type: 'error',
        content: `❌ Error generating ${type}: ${error.message}`
      })
    }
  }

  // **NEW FUNCTION**: Fetch latest media and update displays - NO VIDEOS DURING REGULAR STORY
  const fetchLatestMedia = async () => {
    try {
      const response = await fetch('/api/media-files')
      const mediaFiles = await response.json()
      
      // Update the generated media in context
      if (mediaFiles.images && mediaFiles.images.length > 0) {
        const latestImage = mediaFiles.images[mediaFiles.images.length - 1]
        dispatch({ 
          type: 'ADD_GENERATED_IMAGE', 
          payload: {
            id: Date.now(),
            url: `/api/media/${latestImage}`,
            filename: latestImage,
            type: 'image',
            title: 'AI Generated Scene',
            timestamp: new Date().toISOString()
          }
        })
      }
      
      // **VIDEOS: Allow during regular gameplay too**
      if (mediaFiles.videos && mediaFiles.videos.length > 0) {
        const latestVideo = mediaFiles.videos[mediaFiles.videos.length - 1]
        dispatch({ 
          type: 'ADD_GENERATED_VIDEO', 
          payload: {
            id: Date.now(),
            url: `/api/media/${latestVideo}`,
            filename: latestVideo,
            type: 'video',
            title: currentStory?.story_complete ? '🎬 EPIC FINALE VIDEO' : '🎬 AI Generated Video',
            timestamp: new Date().toISOString()
          }
        })
      }
      
      if (mediaFiles.music && mediaFiles.music.length > 0) {
        const latestMusic = mediaFiles.music[mediaFiles.music.length - 1]
        dispatch({ 
          type: 'ADD_GENERATED_MUSIC', 
          payload: {
            id: Date.now(),
            url: `/api/media/${latestMusic}`,
            filename: latestMusic,
            type: 'music',
            title: 'AI Generated Music',
            timestamp: new Date().toISOString()
          }
        })
      }
      
      console.log('📱 Auto-fetched media:', {
        images: mediaFiles.images?.length || 0,
        videos: 'ONLY IN CLIMAX',
        music: mediaFiles.music?.length || 0
      })
      
    } catch (error) {
      console.error('Auto-fetch media error:', error)
    }
  }

  const resetStory = () => {
    if (confirm('Are you sure you want to start a new story? This will clear your current progress.')) {
      setStoryEvents([])
      setStoryInput('')
      dispatch({ type: 'SET_STORY_ACTIVE', payload: false })
      dispatch({ type: 'SET_CURRENT_STORY', payload: null })
      dispatch({ type: 'RESET_STATE' })
      
      // Clear localStorage as well
      localStorage.removeItem('dreamdirector-state')
      
      // Show confirmation
      dispatch({ type: 'ADD_NOTIFICATION', payload: {
        type: 'success',
        message: '✨ Story cleared! Ready for a new adventure.'
      }})
    }
  }



  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8, ease: "easeInOut" }}
      className={`min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white transition-all duration-500 ${
        screenShake ? 'animate-pulse transform scale-[1.02] rotate-1 shadow-2xl shadow-purple-500/50' : ''
      } ${
        dramaticFlash ? 'bg-gradient-to-br from-white via-purple-200 to-blue-200 shadow-[0_0_100px_rgba(147,51,234,0.8)]' : ''
      } ${
        pulseEffect ? 'animate-pulse shadow-inner shadow-purple-400/40' : ''
      }`}
    >
      {/* Enhanced Background particles with more dynamic movement */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {[...Array(100)].map((_, i) => (
          <motion.div
            key={i}
            className={`absolute rounded-full ${
              i < 30 ? 'w-1 h-1 bg-purple-400' : 
              i < 60 ? 'w-2 h-2 bg-pink-400' : 
              i < 85 ? 'w-1.5 h-1.5 bg-blue-400' :
              'w-3 h-3 bg-yellow-400'
            } ${
              dramaticFlash ? 'bg-white shadow-2xl scale-150' : ''
            }`}
            animate={{
              y: [Math.random() * window.innerHeight, -50],
              x: [
                Math.random() * window.innerWidth, 
                Math.random() * window.innerWidth + (Math.random() - 0.5) * 200
              ],
              opacity: [0, dramaticFlash ? 1 : Math.random() * 0.6 + 0.2, 0],
              scale: [0.3, dramaticFlash ? 2 : 1.2, 0.3],
              rotate: [0, 360, 720]
            }}
            transition={{
              duration: Math.random() * 20 + 10,
              repeat: Infinity,
              delay: Math.random() * 10,
              ease: "easeInOut",
              type: "tween"
            }}
            style={{
              left: Math.random() * 100 + '%',
              top: Math.random() * 100 + '%'
            }}
          />
        ))}
      </div>

      <div className="relative z-10 container mx-auto px-6 py-8 pt-24">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Story Panel - Left Side with enhanced animations */}
          <div className="lg:col-span-3">
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ 
                duration: 0.8, 
                ease: "easeOut",
                type: "spring",
                stiffness: 100,
                damping: 20
              }}
              className="bg-white/15 backdrop-blur-xl rounded-3xl p-8 border border-white/25 shadow-2xl"
            >
              <motion.div 
                className="flex items-center gap-4 mb-8"
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.6 }}
              >
                <motion.div
                  animate={{ 
                    rotate: [0, 360],
                    scale: [1, 1.2, 1]
                  }}
                  transition={{ 
                    rotate: { duration: 8, repeat: Infinity, ease: "linear" },
                    scale: { duration: 2, repeat: Infinity, ease: "easeInOut" }
                  }}
                >
                  <Sparkles className="w-8 h-8 text-purple-400" />
                </motion.div>
                <div>
                  <motion.h1 
                    className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-yellow-400 bg-clip-text text-transparent"
                    animate={{ 
                      backgroundPosition: ["0%", "100%", "0%"]
                    }}
                    transition={{ 
                      duration: 3, 
                      repeat: Infinity, 
                      ease: "linear" 
                    }}
                    style={{ backgroundSize: "200% 100%" }}
                  >
                    Interactive Story
                  </motion.h1>
                  <motion.p 
                    className="text-purple-200"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    Experience dynamic storytelling powered by AI. Your choices shape the narrative in real-time.
                  </motion.p>
                </div>
              </motion.div>

              {/* Story Input with enhanced animations */}
              {!isStoryActive && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8, y: 30 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.8, y: -30 }}
                  transition={{ 
                    duration: 0.6, 
                    type: "spring",
                    stiffness: 120,
                    damping: 15
                  }}
                  className="mb-8"
                >
                  <motion.label 
                    className="block text-lg font-semibold text-purple-200 mb-4"
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                  >
                    What story would you like to experience?
                  </motion.label>
                  <div className="flex gap-4">
                    <motion.input
                      type="text"
                      value={storyInput}
                      onChange={(e) => setStoryInput(e.target.value)}
                      placeholder="e.g., A space adventure on Mars, A magical quest in an enchanted forest..."
                      className="flex-1 px-4 py-3 bg-white/15 border border-purple-300/40 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:ring-4 focus:ring-purple-400/50 focus:border-purple-400/80 transition-all duration-300"
                      onKeyPress={(e) => e.key === 'Enter' && handleStartStory()}
                      whileFocus={{ scale: 1.02 }}
                      transition={{ type: "spring", stiffness: 300 }}
                    />
                    <motion.button
                      whileHover={{ 
                        scale: 1.08,
                        boxShadow: "0 10px 30px rgba(147, 51, 234, 0.4)",
                        backgroundColor: "rgba(147, 51, 234, 0.9)"
                      }}
                      whileTap={{ 
                        scale: 0.95,
                        backgroundColor: "rgba(147, 51, 234, 1)"
                      }}
                      onClick={handleStartStory}
                      disabled={isGenerating || !storyInput.trim()}
                      className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-semibold hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-all duration-300"
                    >
                      <motion.div
                        animate={isGenerating ? { rotate: 360 } : {}}
                        transition={isGenerating ? { duration: 1, repeat: Infinity, ease: "linear" } : {}}
                      >
                        {isGenerating ? <Loader className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                      </motion.div>
                      {isGenerating ? 'Starting...' : 'Begin Story'}
                    </motion.button>
                  </div>
                </motion.div>
              )}

              {/* Story Timeline with enhanced animations */}
              <div className="space-y-4 mb-8 max-h-96 overflow-y-auto">
                <AnimatePresence mode="popLayout">
                  {storyEvents.map((event, index) => (
                    <motion.div
                      key={event.id}
                      layout
                      initial={{ 
                        opacity: 0, 
                        x: -60, 
                        scale: 0.8,
                        rotateY: -15
                      }}
                      animate={{ 
                        opacity: 1, 
                        x: 0, 
                        scale: 1,
                        rotateY: 0,
                        boxShadow: [
                          '0 0 0px rgba(147, 51, 234, 0)',
                          '0 8px 25px rgba(147, 51, 234, 0.4)',
                          '0 4px 15px rgba(147, 51, 234, 0.2)'
                        ]
                      }}
                      exit={{ 
                        opacity: 0, 
                        x: 30, 
                        scale: 0.8,
                        transition: { duration: 0.3 }
                      }}
                      transition={{ 
                        delay: index * 0.1,
                        duration: 0.7,
                        type: "spring",
                        stiffness: 120,
                        damping: 18
                      }}
                      whileHover={{
                        scale: 1.03,
                        x: 10,
                        boxShadow: '0 12px 35px rgba(147, 51, 234, 0.3)',
                        rotateY: 2
                      }}
                      className={`p-4 rounded-xl border-l-4 cursor-pointer transition-all duration-400 ${
                        event.type === 'story_start' ? 'bg-green-500/25 border-l-green-400 hover:bg-green-500/35' :
                        event.type === 'narrative' ? 'bg-blue-500/25 border-l-blue-400 hover:bg-blue-500/35' :
                        event.type === 'user_choice' ? 'bg-purple-500/25 border-l-purple-400 hover:bg-purple-500/35' :
                        event.type === 'scene' ? 'bg-yellow-500/25 border-l-yellow-400 hover:bg-yellow-500/35' :
                        event.type === 'error' ? 'bg-red-500/25 border-l-red-400 hover:bg-red-500/35' :
                        'bg-gray-500/25 border-l-gray-400 hover:bg-gray-500/35'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <motion.span 
                          className="text-sm text-gray-300"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: index * 0.1 + 0.3 }}
                        >
                          {event.timestamp}
                        </motion.span>
                      </div>
                      <motion.div 
                        className="text-white leading-relaxed"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 + 0.4 }}
                      >
                        {event.content}
                      </motion.div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>



              {/* Choices Section - DRAMATICALLY IMPROVED */}
              {isStoryActive && currentStory && currentStory.choices && currentStory.choices.length > 0 && !currentStory.story_complete && (
                <motion.div
                  initial={{ opacity: 0, y: 40, scale: 0.9 }}
                  animate={{ 
                    opacity: 1, 
                    y: 0,
                    scale: choiceAnimation ? [1, 1.05, 1] : 1,
                    rotateX: choiceAnimation ? [0, 8, 0] : 0
                  }}
                  transition={{ 
                    duration: 0.6,
                    type: "spring",
                    stiffness: 100
                  }}
                  className={`bg-gradient-to-r from-purple-600/30 to-pink-600/30 rounded-2xl p-6 border border-purple-400/40 backdrop-blur-lg ${
                    choiceAnimation ? 'ring-4 ring-purple-400/60 shadow-2xl shadow-purple-500/40' : ''
                  }`}
                >
                  <motion.h3 
                    className="text-xl font-bold text-purple-200 mb-4 flex items-center gap-2"
                    animate={{
                      textShadow: [
                        "0 0 0px rgba(147, 51, 234, 0)",
                        "0 0 20px rgba(147, 51, 234, 0.8)",
                        "0 0 0px rgba(147, 51, 234, 0)"
                      ]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <motion.div
                      animate={{ x: [0, 5, 0] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                    >
                      <ChevronRight className="w-5 h-5" />
                    </motion.div>
                    What do you do?
                  </motion.h3>
                  <div className="space-y-3">
                    {currentStory.choices.map((choice, index) => {
                      // More robust choice filtering
                      const cleanChoice = choice ? choice.trim() : ''
                      if (!cleanChoice) return null
                      
                      return (
                        <motion.button
                          key={index}
                          layout
                          initial={{ opacity: 0, x: -30, scale: 0.9 }}
                          animate={{ 
                            opacity: 1, 
                            x: 0, 
                            scale: choiceGlow === index ? [1, 1.08, 1.02, 1] : 1,
                            boxShadow: choiceGlow === index 
                              ? [
                                  '0 0 0px rgba(147, 51, 234, 0)', 
                                  '0 0 60px rgba(255, 215, 0, 1)', 
                                  '0 0 30px rgba(147, 51, 234, 0.8)',
                                  '0 0 0px rgba(147, 51, 234, 0)'
                                ]
                              : '0 0 0px rgba(147, 51, 234, 0)',
                            borderColor: choiceGlow === index
                              ? [
                                  'rgba(147, 51, 234, 0.5)', 
                                  'rgba(255, 215, 0, 1)', 
                                  'rgba(147, 51, 234, 0.8)',
                                  'rgba(147, 51, 234, 0.5)'
                                ]
                              : 'rgba(255, 255, 255, 0.15)',
                            backgroundColor: choiceGlow === index
                              ? [
                                  'rgba(255, 255, 255, 0.1)',
                                  'rgba(255, 215, 0, 0.3)',
                                  'rgba(147, 51, 234, 0.4)',
                                  'rgba(255, 255, 255, 0.1)'
                                ]
                              : 'rgba(255, 255, 255, 0.1)'
                          }}
                          transition={{ 
                            delay: choiceGlow === index ? 0 : index * 0.1,
                            duration: choiceGlow === index ? 0.4 : 0.3,
                            repeat: choiceGlow === index ? 3 : 0,
                            type: "spring",
                            stiffness: choiceGlow === index ? 200 : 150
                          }}
                          whileHover={{ 
                            scale: 1.04, 
                            x: 20,
                            backgroundColor: 'rgba(147, 51, 234, 0.5)',
                            borderColor: 'rgba(147, 51, 234, 1)',
                            boxShadow: '0 15px 40px rgba(147, 51, 234, 0.4)',
                            rotateY: 3
                          }}
                          whileTap={{ 
                            scale: 0.96,
                            backgroundColor: 'rgba(147, 51, 234, 0.7)',
                            boxShadow: '0 0 50px rgba(147, 51, 234, 0.8)'
                          }}
                          onClick={() => handleChoice(cleanChoice, index)}
                          disabled={isGenerating}
                          className={`w-full text-left p-4 bg-white/15 hover:bg-white/25 rounded-xl border border-white/15 hover:border-purple-400/60 transition-all duration-400 disabled:opacity-50 disabled:cursor-not-allowed backdrop-blur-sm ${
                            choiceGlow === index ? 'ring-2 ring-gold-400 ring-opacity-80' : ''
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <motion.span 
                              className="flex-shrink-0 w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold"
                              animate={{
                                backgroundColor: choiceGlow === index 
                                  ? ['rgba(147, 51, 234, 1)', 'rgba(255, 215, 0, 1)', 'rgba(147, 51, 234, 1)']
                                  : 'rgba(147, 51, 234, 1)',
                                scale: choiceGlow === index ? [1, 1.3, 1] : 1
                              }}
                              transition={{ duration: 0.4, repeat: choiceGlow === index ? 3 : 0 }}
                            >
                              {String.fromCharCode(65 + index)}
                            </motion.span>
                            <span className="text-white">{cleanMarkdown(cleanChoice)}</span>
                          </div>
                        </motion.button>
                      )
                    })}
                  </div>
                  
                  {isGenerating && (
                    <motion.div 
                      initial={{ opacity: 0, y: 20, scale: 0.9 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      transition={{ type: "spring", stiffness: 150 }}
                      className="mt-4 text-center"
                    >
                      <motion.div 
                        className="inline-flex items-center gap-2 text-purple-300 bg-purple-900/40 px-6 py-3 rounded-xl backdrop-blur-sm"
                        animate={{
                          boxShadow: [
                            '0 0 0px rgba(147, 51, 234, 0)',
                            '0 0 30px rgba(147, 51, 234, 0.6)',
                            '0 0 0px rgba(147, 51, 234, 0)'
                          ]
                        }}
                        transition={{ duration: 2, repeat: Infinity }}
                      >
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        >
                          <Loader className="w-4 h-4" />
                        </motion.div>
                        <span>Processing your choice...</span>
                      </motion.div>
                      <motion.div 
                        className="mt-2 text-sm text-purple-400"
                        animate={{ opacity: [0.5, 1, 0.5] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                      >
                        ✨ AI is crafting your story outcome...
                      </motion.div>
                    </motion.div>
                  )}
                </motion.div>
              )}

              {/* Story Complete Message with enhanced animation */}
              {isStoryActive && currentStory?.story_complete && (
                <motion.div
                  initial={{ opacity: 0, y: 30, scale: 0.8 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ 
                    type: "spring", 
                    stiffness: 120,
                    damping: 15
                  }}
                  className="bg-gradient-to-r from-green-600/30 to-blue-600/30 rounded-2xl p-6 border border-green-400/40 text-center backdrop-blur-lg"
                >
                  <motion.h3 
                    className="text-xl font-bold text-green-200 mb-2"
                    animate={{
                      textShadow: [
                        "0 0 0px rgba(34, 197, 94, 0)",
                        "0 0 20px rgba(34, 197, 94, 0.8)",
                        "0 0 0px rgba(34, 197, 94, 0)"
                      ]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    🎬 Story Complete!
                  </motion.h3>
                  <p className="text-green-100">Your adventure has reached its conclusion. Start a new story to continue exploring!</p>
                </motion.div>
              )}

              {/* Reset Button with enhanced animation */}
              {isStoryActive && (
                <div className="mt-6 text-center">
                  <motion.button
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    whileHover={{ 
                      scale: 1.08,
                      boxShadow: "0 8px 25px rgba(107, 114, 128, 0.4)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    onClick={resetStory}
                    className="px-6 py-2 bg-gray-600 hover:bg-gray-700 rounded-xl font-semibold flex items-center gap-2 mx-auto transition-all duration-300"
                  >
                    <motion.div
                      whileHover={{ rotate: -180 }}
                      transition={{ duration: 0.3 }}
                    >
                      <RotateCcw className="w-4 h-4" />
                    </motion.div>
                    New Story
                  </motion.button>
                </div>
              )}
            </motion.div>
          </div>

          {/* Media Panel - Right Side with enhanced animations and NO MUSIC TRACKS */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 50, scale: 0.9 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              transition={{ 
                duration: 0.8, 
                delay: 0.2,
                type: "spring",
                stiffness: 100
              }}
              className="bg-white/15 backdrop-blur-xl rounded-3xl p-4 border border-white/25 shadow-2xl"
            >
              <motion.h2 
                className="text-lg font-bold text-purple-200 mb-4 flex items-center gap-2"
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <motion.div
                  animate={{ 
                    rotate: [0, 360],
                    scale: [1, 1.3, 1]
                  }}
                  transition={{ 
                    rotate: { duration: 8, repeat: Infinity, ease: "linear" },
                    scale: { duration: 3, repeat: Infinity, ease: "easeInOut" }
                  }}
                >
                  <Sparkles className="w-5 h-5" />
                </motion.div>
                {currentStory?.story_complete && generatedVideos.length > 0 
                  ? `Epic Adventure Complete (${generatedImages.length} scenes + finale video)` 
                  : `Generated Visuals (${generatedImages.length})`}
              </motion.h2>
              
              {/* **ONLY IMAGES - NO MUSIC TRACKS DISPLAYED** */}
              <div className="max-h-96 overflow-y-auto space-y-4 pr-2">
                {/* Show message if no content */}
                {generatedImages.length === 0 && (
                  <motion.div 
                    className="text-center py-8 text-purple-300"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.6 }}
                  >
                    <motion.div 
                      className="w-16 h-16 mx-auto mb-4 rounded-xl bg-purple-900/40 flex items-center justify-center"
                      animate={{
                        boxShadow: [
                          '0 0 0px rgba(147, 51, 234, 0)',
                          '0 0 20px rgba(147, 51, 234, 0.4)',
                          '0 0 0px rgba(147, 51, 234, 0)'
                        ]
                      }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      <ImageIcon className="w-8 h-8" />
                    </motion.div>
                    <p className="text-sm">Visuals will appear here as your story progresses</p>
                  </motion.div>
                )}

                {/* **ONLY IMAGES - Enhanced animations for each image** */}
                <AnimatePresence>
                  {generatedImages.map((image, index) => (
                    <motion.div
                      key={image.id}
                      layout
                      initial={{ opacity: 0, y: 30, scale: 0.8, rotateY: -20 }}
                      animate={{ opacity: 1, y: 0, scale: 1, rotateY: 0 }}
                      exit={{ opacity: 0, scale: 0.8, x: 30 }}
                      transition={{
                        duration: 0.6,
                        delay: index * 0.1,
                        type: "spring",
                        stiffness: 120
                      }}
                      whileHover={{
                        scale: 1.05,
                        rotateY: 5,
                        boxShadow: '0 15px 35px rgba(59, 130, 246, 0.3)'
                      }}
                      className="mb-4"
                    >
                      <motion.div 
                        className="flex items-center gap-2 mb-2"
                        initial={{ x: -20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: index * 0.1 + 0.2 }}
                      >
                        <ImageIcon className="w-4 h-4 text-blue-400" />
                        <span className="text-xs font-semibold text-blue-300">Scene {index + 1}</span>
                        <span className="text-xs text-gray-400">{new Date(image.timestamp).toLocaleTimeString()}</span>
                      </motion.div>
                      <motion.div 
                        className="relative aspect-video bg-gray-800 rounded-xl overflow-hidden shadow-lg"
                        whileHover={{
                          boxShadow: '0 10px 30px rgba(59, 130, 246, 0.4)'
                        }}
                      >
                        <motion.img
                          src={image.url}
                          alt={`Generated scene ${index + 1}`}
                          className="w-full h-full object-cover"
                          initial={{ scale: 1.1, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          transition={{ duration: 0.5 }}
                          whileHover={{ scale: 1.1 }}
                          onError={(e) => {
                            e.target.style.display = 'none'
                            e.target.nextSibling.style.display = 'flex'
                          }}
                        />
                        <motion.div 
                          className="hidden absolute inset-0 flex items-center justify-center text-gray-400 text-sm bg-gray-800"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                        >
                          Loading...
                        </motion.div>
                      </motion.div>
                    </motion.div>
                  ))}
                </AnimatePresence>

                {/* **EPIC FINALE VIDEO - Only shows when story is complete** */}
                {currentStory?.story_complete && generatedVideos.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 40, scale: 0.8 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
                    className="mt-6 p-4 bg-gradient-to-r from-gold-600/20 to-yellow-600/20 rounded-xl border border-gold-400/40"
                  >
                    <motion.div 
                      className="flex items-center gap-2 mb-3"
                      animate={{
                        textShadow: [
                          "0 0 0px rgba(255, 215, 0, 0)",
                          "0 0 20px rgba(255, 215, 0, 0.8)",
                          "0 0 0px rgba(255, 215, 0, 0)"
                        ]
                      }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      <Video className="w-5 h-5 text-gold-400" />
                      <span className="text-gold-200 font-bold">🎬 EPIC FINALE VIDEO</span>
                    </motion.div>
                    <motion.div 
                      className="aspect-video bg-gray-900 rounded-lg overflow-hidden"
                      whileHover={{ scale: 1.02 }}
                      transition={{ type: "spring", stiffness: 300 }}
                    >
                      <video
                        src={generatedVideos[generatedVideos.length - 1]?.url}
                        controls
                        autoPlay
                        muted
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          console.error('Video failed to load:', e)
                        }}
                      >
                        Your browser does not support the video tag.
                      </video>
                    </motion.div>
                    <motion.p 
                      className="text-xs text-gold-300 mt-2 text-center"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.5 }}
                    >
                      ✨ The cinematic conclusion to your adventure
                    </motion.p>
                  </motion.div>
                )}
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default StoryPage 