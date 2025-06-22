import React, { createContext, useContext, useReducer, useEffect } from 'react'
import axios from 'axios'

const AppContext = createContext()

const initialState = {
  // Story state
  currentStory: null,
  storyHistory: [],
  isStoryActive: false,
  
  // Media state
  generatedImages: [],
  generatedVideos: [],
  generatedMusic: [],
  isGenerating: false,
  generationProgress: 0,
  
  // UI state
  currentPage: 'home',
  notifications: [],
  
  // Settings
  autoplayMusic: true,
  showVisuals: true,
  storyComplexity: 'medium'
}

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_CURRENT_STORY':
      return { ...state, currentStory: action.payload }
    case 'SET_STORY_ACTIVE':
      return { ...state, isStoryActive: action.payload }
    case 'SET_GENERATING':
      return { ...state, isGenerating: action.payload }
    case 'SET_GENERATION_PROGRESS':
      return { ...state, generationProgress: action.payload }
    case 'ADD_GENERATED_IMAGE':
      return { 
        ...state, 
        generatedImages: [...state.generatedImages, action.payload] 
      }
    case 'ADD_GENERATED_VIDEO':
      return { 
        ...state, 
        generatedVideos: [...state.generatedVideos, action.payload] 
      }
    case 'ADD_GENERATED_MUSIC':
      return { 
        ...state, 
        generatedMusic: [...state.generatedMusic, action.payload] 
      }
    case 'CLEAR_GENERATED_VIDEOS':
      return { 
        ...state, 
        generatedVideos: [] 
      }
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [...state.notifications, {
          id: Date.now(),
          ...action.payload
        }]
      }
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload)
      }
    case 'RESET_STATE':
      return {
        ...initialState,
        notifications: state.notifications
      }
    default:
      return state
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState)

  // API functions
  const startNewStory = async (storyRequest) => {
    try {
      dispatch({ type: 'SET_GENERATING', payload: true })
      dispatch({ type: 'SET_GENERATION_PROGRESS', payload: 0 })
      
      const response = await axios.post('/api/start-story', { 
        story_request: storyRequest 
      })
      
      dispatch({ type: 'SET_CURRENT_STORY', payload: response.data })
      dispatch({ type: 'SET_STORY_ACTIVE', payload: true })
      dispatch({ type: 'ADD_NOTIFICATION', payload: {
        type: 'success',
        message: 'Real AI story generated! 🎬'
      }})
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to start story'
      dispatch({ type: 'ADD_NOTIFICATION', payload: {
        type: 'error',
        message: `AI Agent Error: ${errorMessage}`
      }})
      throw error
    } finally {
      dispatch({ type: 'SET_GENERATING', payload: false })
    }
  }

  const makeChoice = async (choice) => {
    try {
      dispatch({ type: 'SET_GENERATING', payload: true })
      
      const response = await axios.post('/api/make-choice', { 
        choice: choice 
      })
      
      dispatch({ type: 'ADD_TO_STORY_HISTORY', payload: response.data })
      dispatch({ type: 'SET_CURRENT_STORY', payload: response.data })
      // Keep story active unless it's marked as complete
      if (!response.data.story_complete) {
        dispatch({ type: 'SET_STORY_ACTIVE', payload: true })
      } else {
        dispatch({ type: 'SET_STORY_ACTIVE', payload: false })
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to process choice'
      dispatch({ type: 'ADD_NOTIFICATION', payload: {
        type: 'error',
        message: `AI Agent Error: ${errorMessage}`
      }})
      throw error
    } finally {
      dispatch({ type: 'SET_GENERATING', payload: false })
    }
  }

  const generateMedia = async (type, prompt) => {
    try {
      dispatch({ type: 'SET_GENERATING', payload: true })
      dispatch({ type: 'SET_GENERATION_PROGRESS', payload: 0 })
      
      const response = await axios.post('/api/generate-media', { 
        type: type,
        prompt: prompt,
        emotional_tone: 'mysterious'
      })
      
      // Handle the new response format with actual file information
      const mediaData = {
        id: Date.now(),
        type: type,
        title: `AI Generated ${type.charAt(0).toUpperCase() + type.slice(1)}`,
        description: prompt,
        timestamp: new Date().toISOString(),
        mood: 'mysterious',
        filename: response.data.filename || response.data.generated_file || `${type}_${Date.now()}`,
        url: response.data.url || response.data.generated_file,
        prompt: prompt
      }
      
      // Add generated media to state based on type
      switch (type) {
        case 'image':
          dispatch({ type: 'ADD_GENERATED_IMAGE', payload: mediaData })
          break
        case 'video':
          dispatch({ type: 'ADD_GENERATED_VIDEO', payload: mediaData })
          break
        case 'music':
          dispatch({ type: 'ADD_GENERATED_MUSIC', payload: mediaData })
          break
      }
      
      dispatch({ type: 'ADD_NOTIFICATION', payload: {
        type: 'success',
        message: `🎨 Real AI ${type} generated! ${response.data.generated_file ? '✅ File ready' : '🎭 Processing...'}`
      }})
      
      console.log(`✨ ${type} generated:`, response.data)
      return response.data
      
    } catch (error) {
      const errorMessage = error.response?.data?.detail || `Failed to generate ${type}`
      dispatch({ type: 'ADD_NOTIFICATION', payload: {
        type: 'error',
        message: `AI Agent Error: ${errorMessage}`
      }})
      console.error(`❌ ${type} generation failed:`, error)
      throw error
    } finally {
      dispatch({ type: 'SET_GENERATING', payload: false })
      dispatch({ type: 'SET_GENERATION_PROGRESS', payload: 0 })
    }
  }

  const contextValue = {
    ...state,
    dispatch,
    startNewStory,
    makeChoice,
    generateMedia
  }

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
} 