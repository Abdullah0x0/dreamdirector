import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Image as ImageIcon, 
  Video, 
  Music, 
  Download, 
  Play, 
  Pause,
  Grid,
  List,
  Filter,
  Search,
  Eye
} from 'lucide-react'
import { useApp } from '../context/AppContext'

function GalleryPage() {
  const { generatedImages, generatedVideos, generatedMusic } = useApp()
  const [viewMode, setViewMode] = useState('grid')
  const [filterType, setFilterType] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedItem, setSelectedItem] = useState(null)
  const [isPlaying, setIsPlaying] = useState(false)

  // Convert real AI-generated media to unified format
  const createGalleryItem = (item, type, index) => ({
    id: `${type}-${index}`,
    type: type,
    filename: item.filename || item.url?.split('/').pop() || `${type}_${index}`,
    title: item.title || item.description || `AI Generated ${type.charAt(0).toUpperCase() + type.slice(1)}`,
    description: item.description || item.prompt || `Generated ${type} content`,
    timestamp: item.timestamp || item.created_at || new Date().toISOString(),
    mood: item.mood || item.tone || 'creative',
    url: item.url || item.file_path || item.path,
    prompt: item.prompt || item.scene_description || `AI ${type} generation`
  })

  // Combine all real AI-generated media
  const allItems = [
    ...generatedImages.map((img, idx) => createGalleryItem(img, 'image', idx)),
    ...generatedVideos.map((vid, idx) => createGalleryItem(vid, 'video', idx)),
    ...generatedMusic.map((music, idx) => createGalleryItem(music, 'music', idx))
  ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)) // Sort by newest first

  const filteredItems = allItems.filter(item => {
    const matchesType = filterType === 'all' || item.type === filterType
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.prompt.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesType && matchesSearch
  })

  const getTypeIcon = (type) => {
    switch (type) {
      case 'image': return ImageIcon
      case 'video': return Video
      case 'music': return Music
      default: return ImageIcon
    }
  }

  const getTypeColor = (type) => {
    switch (type) {
      case 'image': return 'text-purple-400'
      case 'video': return 'text-green-400'
      case 'music': return 'text-yellow-400'
      default: return 'text-gray-400'
    }
  }

  const getTypeLabel = (type) => {
    switch (type) {
      case 'image': return 'Imagen 3'
      case 'video': return 'Veo 2'
      case 'music': return 'Lyria'
      default: return type
    }
  }

  const handleItemClick = (item) => {
    setSelectedItem(item)
  }

  const closePreview = () => {
    setSelectedItem(null)
    setIsPlaying(false)
  }

  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleString()
    } catch {
      return timestamp
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="pt-16 min-h-screen"
    >
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-4xl font-cinematic gradient-text mb-2">
              🎨 AI Media Gallery
            </h1>
            <p className="text-gray-400">
              Explore all your AI-generated content from your storytelling adventures
            </p>
          </div>

          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            {/* View Mode Toggle */}
            <div className="flex bg-gray-800 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-cinematic-accent text-white' : 'text-gray-400'}`}
              >
                <Grid size={18} />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-cinematic-accent text-white' : 'text-gray-400'}`}
              >
                <List size={18} />
              </button>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search AI-generated media..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-cinematic-accent"
              />
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Filter size={20} className="text-gray-400" />
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:border-cinematic-accent"
            >
              <option value="all">All AI Media</option>
              <option value="image">Imagen 3 (Images)</option>
              <option value="video">Veo 2 (Videos)</option>
              <option value="music">Lyria (Music)</option>
            </select>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total AI Media', value: allItems.length, icon: Eye },
            { label: 'Imagen 3 Images', value: generatedImages.length, icon: ImageIcon },
            { label: 'Veo 2 Videos', value: generatedVideos.length, icon: Video },
            { label: 'Lyria Music', value: generatedMusic.length, icon: Music },
          ].map((stat, index) => (
            <div key={stat.label} className="card-cinematic p-4 text-center">
              <stat.icon className="mx-auto mb-2 text-cinematic-accent" size={24} />
              <div className="text-2xl font-bold gradient-text">{stat.value}</div>
              <div className="text-sm text-gray-400">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Gallery Content */}
        {filteredItems.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🤖</div>
            <h3 className="text-2xl font-cinematic text-gray-400 mb-2">
              {allItems.length === 0 ? 'No AI media generated yet' : 'No media found'}
            </h3>
            <p className="text-gray-500">
              {allItems.length === 0 
                ? 'Start creating stories and generate images, videos, and music to see them here!'
                : 'Try adjusting your search terms or filters'
              }
            </p>
          </div>
        ) : (
          <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6' : 'space-y-4'}>
            {filteredItems.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`card-cinematic overflow-hidden cursor-pointer hover:scale-105 transition-all duration-300 ${
                  viewMode === 'list' ? 'flex items-center p-4' : 'aspect-square'
                }`}
                onClick={() => handleItemClick(item)}
              >
                {viewMode === 'grid' ? (
                  <>
                    <div className="aspect-square bg-gray-800 flex items-center justify-center relative group">
                      {item.type === 'image' && item.url ? (
                        <img 
                          src={item.url} 
                          alt={item.title}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.style.display = 'none'
                            e.target.nextSibling.style.display = 'flex'
                          }}
                        />
                      ) : null}
                      <div className="flex items-center justify-center w-full h-full" style={{ display: item.type === 'image' && item.url ? 'none' : 'flex' }}>
                        {React.createElement(getTypeIcon(item.type), {
                          size: 48,
                          className: `${getTypeColor(item.type)} group-hover:scale-110 transition-transform`
                        })}
                      </div>
                      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <Eye size={32} className="text-white" />
                      </div>
                      {/* AI Badge */}
                      <div className="absolute top-2 right-2 bg-cinematic-accent/80 text-white text-xs px-2 py-1 rounded">
                        {getTypeLabel(item.type)}
                      </div>
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-white mb-1 truncate">{item.title}</h3>
                      <p className="text-sm text-gray-400 mb-2 line-clamp-2">{item.description}</p>
                      <div className="flex justify-between items-center text-xs text-gray-500">
                        <span className={`px-2 py-1 rounded ${getTypeColor(item.type)} bg-current bg-opacity-20`}>
                          {getTypeLabel(item.type)}
                        </span>
                        <span>{item.mood}</span>
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="w-16 h-16 bg-gray-800 rounded-lg flex items-center justify-center mr-4 relative">
                      {item.type === 'image' && item.url ? (
                        <img 
                          src={item.url} 
                          alt={item.title}
                          className="w-full h-full object-cover rounded-lg"
                          onError={(e) => {
                            e.target.style.display = 'none'
                            e.target.nextSibling.style.display = 'flex'
                          }}
                        />
                      ) : null}
                      <div className="flex items-center justify-center w-full h-full" style={{ display: item.type === 'image' && item.url ? 'none' : 'flex' }}>
                        {React.createElement(getTypeIcon(item.type), {
                          size: 24,
                          className: getTypeColor(item.type)
                        })}
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white mb-1">{item.title}</h3>
                      <p className="text-sm text-gray-400 mb-1">{item.description}</p>
                      <div className="flex items-center space-x-2 text-xs text-gray-500">
                        <span className={`px-2 py-1 rounded ${getTypeColor(item.type)} bg-current bg-opacity-20`}>
                          {getTypeLabel(item.type)}
                        </span>
                        <span>{item.mood}</span>
                        <span>•</span>
                        <span>{formatTimestamp(item.timestamp)}</span>
                      </div>
                    </div>
                    <button className="p-2 bg-gray-800 hover:bg-gray-700 rounded-lg">
                      <Download size={18} />
                    </button>
                  </>
                )}
              </motion.div>
            ))}
          </div>
        )}

        {/* Preview Modal */}
        {selectedItem && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4"
            onClick={closePreview}
          >
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              className="card-cinematic max-w-4xl w-full max-h-[90vh] overflow-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-2xl font-cinematic text-white mb-2">
                      {selectedItem.title}
                    </h2>
                    <p className="text-gray-400 mb-2">{selectedItem.description}</p>
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <span className={`px-2 py-1 rounded ${getTypeColor(selectedItem.type)} bg-current bg-opacity-20`}>
                        {getTypeLabel(selectedItem.type)} AI
                      </span>
                      <span>•</span>
                      <span>{selectedItem.mood}</span>
                    </div>
                  </div>
                  <button
                    onClick={closePreview}
                    className="p-2 bg-gray-800 hover:bg-gray-700 rounded-lg"
                  >
                    ✕
                  </button>
                </div>

                <div className="bg-gray-800 rounded-lg p-8 mb-4">
                  {selectedItem.type === 'image' && selectedItem.url ? (
                    <img 
                      src={selectedItem.url} 
                      alt={selectedItem.title}
                      className="w-full max-h-96 object-contain rounded-lg mx-auto"
                      onError={(e) => {
                        e.target.style.display = 'none'
                        e.target.nextSibling.style.display = 'block'
                      }}
                    />
                  ) : null}
                  {selectedItem.type === 'video' && selectedItem.url ? (
                    <video controls className="w-full max-h-96 rounded-lg mx-auto">
                      <source src={selectedItem.url} type="video/mp4" />
                      Your browser doesn't support video playback.
                    </video>
                  ) : null}
                  {selectedItem.type === 'music' && selectedItem.url ? (
                    <div className="text-center">
                      <Music className="text-yellow-400 mx-auto mb-4" size={64} />
                      <audio controls className="w-full max-w-md mx-auto">
                        <source src={selectedItem.url} type="audio/mpeg" />
                        <source src={selectedItem.url} type="audio/wav" />
                        Your browser doesn't support audio playback.
                      </audio>
                    </div>
                  ) : null}
                  
                  {/* Fallback for items without URL or failed loads */}
                  <div className="text-center text-gray-400" style={{ display: selectedItem.url ? 'none' : 'block' }}>
                    {React.createElement(getTypeIcon(selectedItem.type), {
                      size: 64,
                      className: `${getTypeColor(selectedItem.type)} mx-auto mb-4`
                    })}
                    <p>AI-generated {selectedItem.type} content</p>
                    <p className="text-sm mt-2">File: {selectedItem.filename}</p>
                  </div>
                </div>

                {selectedItem.prompt && (
                  <div className="bg-gray-900/50 rounded-lg p-4 mb-4">
                    <h4 className="text-sm font-medium text-gray-400 mb-2">🎭 AI Prompt:</h4>
                    <p className="text-gray-300 text-sm">{selectedItem.prompt}</p>
                  </div>
                )}

                <div className="flex justify-between items-center">
                  <div className="text-sm text-gray-400">
                    Generated: {formatTimestamp(selectedItem.timestamp)}
                  </div>
                  <div className="flex space-x-2">
                    {selectedItem.type === 'music' && selectedItem.url && (
                      <button className="btn-secondary flex items-center space-x-2">
                        {isPlaying ? <Pause size={18} /> : <Play size={18} />}
                        <span>{isPlaying ? 'Pause' : 'Play'}</span>
                      </button>
                    )}
                    {selectedItem.url && (
                      <a 
                        href={selectedItem.url} 
                        download={selectedItem.filename}
                        className="btn-primary flex items-center space-x-2"
                      >
                        <Download size={18} />
                        <span>Download</span>
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default GalleryPage 