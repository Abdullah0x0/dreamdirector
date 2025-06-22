import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Film, 
  Home, 
  BookOpen, 
  Image, 
  Info, 
  Menu, 
  X,
  Sparkles 
} from 'lucide-react'

function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/story', label: 'Story', icon: BookOpen },
    { path: '/gallery', label: 'Gallery', icon: Image },
    { path: '/about', label: 'About', icon: Info },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 bg-cinematic-card/90 backdrop-blur-lg border-b border-gray-800"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.6 }}
              className="text-3xl"
            >
              🎬
            </motion.div>
            <div>
              <h1 className="text-xl font-cinematic gradient-text group-hover:text-glow transition-all duration-300">
                DreamDirector
              </h1>
              <p className="text-xs text-gray-400">AI Cinematic Storytelling</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-300 ${
                  isActive(path)
                    ? 'text-cinematic-accent bg-cinematic-accent/10 border border-cinematic-accent/30'
                    : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
                }`}
              >
                <Icon size={18} />
                <span className="font-medium">{label}</span>
                {isActive(path) && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="w-2 h-2 bg-cinematic-accent rounded-full"
                  />
                )}
              </Link>
            ))}
            
            {/* AI Status Indicator */}
            <div className="flex items-center space-x-2 px-3 py-2 bg-green-500/10 border border-green-500/30 rounded-lg">
              <Sparkles size={16} className="text-green-400" />
              <span className="text-sm text-green-400 font-medium">AI Ready</span>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 rounded-lg bg-gray-800/50 hover:bg-gray-700/50 transition-colors"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        <motion.div
          initial={false}
          animate={{
            height: isOpen ? 'auto' : 0,
            opacity: isOpen ? 1 : 0
          }}
          className="md:hidden overflow-hidden"
        >
          <div className="py-4 space-y-2">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-300 ${
                  isActive(path)
                    ? 'text-cinematic-accent bg-cinematic-accent/10 border border-cinematic-accent/30'
                    : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{label}</span>
              </Link>
            ))}
            
            <div className="flex items-center space-x-3 px-4 py-3 bg-green-500/10 border border-green-500/30 rounded-lg">
              <Sparkles size={20} className="text-green-400" />
              <span className="text-green-400 font-medium">AI System Ready</span>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.nav>
  )
}

export default Navbar 