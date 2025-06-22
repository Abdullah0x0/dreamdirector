import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Play, 
  Sparkles, 
  Image, 
  Music, 
  Video, 
  BookOpen,
  ArrowRight,
  Star,
  Zap,
  Globe
} from 'lucide-react'

function HomePage() {
  const features = [
    {
      icon: BookOpen,
      title: 'Infinite Stories',
      description: 'AI-powered narratives that adapt to your choices, creating unique adventures every time.',
      color: 'text-blue-400'
    },
    {
      icon: Image,
      title: 'Visual Generation',
      description: 'Stunning images created in real-time using Google Imagen 3.0 for visual consistency.',
      color: 'text-purple-400'
    },
    {
      icon: Video,
      title: 'Cinematic Videos',
      description: 'Dynamic video sequences generated with Veo 2.0, bringing your story to life.',
      color: 'text-green-400'
    },
    {
      icon: Music,
      title: 'Adaptive Music',
      description: 'Real-time music composition with Google Lyria that responds to story emotions.',
      color: 'text-yellow-400'
    }
  ]

  const stats = [
    { label: 'Unique Stories', value: '∞', icon: Globe },
    { label: 'AI Agents', value: '4+', icon: Zap },
    { label: 'Media Types', value: '3', icon: Star },
    { label: 'Real-time', value: '100%', icon: Sparkles }
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="pt-16"
    >
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-cinematic-bg via-cinematic-card/20 to-cinematic-bg"></div>
        
        <div className="relative z-10 text-center max-w-6xl mx-auto px-4">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mb-8"
          >
            <div className="text-8xl mb-6 animate-float">🎬</div>
            <h1 className="text-6xl md:text-8xl font-cinematic gradient-text text-glow mb-6">
              DreamDirector
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Direct your dreams, live your story. Experience AI-powered cinematic storytelling 
              where every choice matters and every moment is epic.
            </p>
          </motion.div>

          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col md:flex-row gap-6 justify-center items-center mb-12"
          >
            <Link to="/story" className="btn-primary text-lg px-8 py-4 flex items-center space-x-3">
              <Play size={24} />
              <span>Start Your Story</span>
              <ArrowRight size={20} />
            </Link>
            
            <Link to="/gallery" className="btn-secondary text-lg px-8 py-4 flex items-center space-x-3">
              <Image size={24} />
              <span>View Gallery</span>
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto"
          >
            {stats.map(({ label, value, icon: Icon }, index) => (
              <div key={label} className="card-cinematic p-6 text-center">
                <Icon className="mx-auto mb-3 text-cinematic-accent" size={32} />
                <div className="text-3xl font-bold gradient-text mb-2">{value}</div>
                <div className="text-gray-400">{label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-cinematic gradient-text mb-6">
              Multi-Agent AI Collaboration
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Powered by Google's latest AI technologies, working together to create 
              your perfect cinematic experience.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ y: 50, opacity: 0 }}
                whileInView={{ y: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card-cinematic p-8 hover:scale-105 transition-transform duration-300"
              >
                <feature.icon className={`${feature.color} mb-6`} size={48} />
                <h3 className="text-xl font-cinematic text-white mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-cinematic-accent/10 via-transparent to-cinematic-gold/10">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-cinematic gradient-text mb-6">
              Ready to Direct Your Dreams?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join the future of interactive storytelling. Every adventure is unique, 
              every choice is yours, and every story is unforgettable.
            </p>
            
            <div className="flex flex-col md:flex-row gap-6 justify-center">
              <Link to="/story" className="btn-primary text-lg px-10 py-4 flex items-center justify-center space-x-3">
                <Sparkles size={24} />
                <span>Begin Your Adventure</span>
              </Link>
              
              <Link to="/about" className="btn-secondary text-lg px-10 py-4 flex items-center justify-center space-x-3">
                <BookOpen size={24} />
                <span>Learn More</span>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </motion.div>
  )
}

export default HomePage 