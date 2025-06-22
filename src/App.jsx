import React, { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import StoryPage from './pages/StoryPage'
import GalleryPage from './pages/GalleryPage'
import AboutPage from './pages/AboutPage'
import { AppProvider } from './context/AppContext'

function App() {
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate app initialization
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-cinematic-bg">
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="text-6xl mb-4">🎬</div>
          <h1 className="text-4xl font-cinematic gradient-text mb-4">
            DreamDirector
          </h1>
          <div className="loading-dots text-lg">Loading your cinematic experience</div>
        </motion.div>
      </div>
    )
  }

  return (
    <AppProvider>
      <div className="min-h-screen bg-cinematic-bg text-white">
        <Navbar />
        
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/story" element={<StoryPage />} />
            <Route path="/gallery" element={<GalleryPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </AnimatePresence>
      </div>
    </AppProvider>
  )
}

export default App 