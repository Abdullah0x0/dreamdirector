import React from 'react'
import { motion } from 'framer-motion'
import { 
  Zap, 
  Brain, 
  Sparkles, 
  Users, 
  Award, 
  Code, 
  Palette, 
  Music,
  Image as ImageIcon,
  Video,
  Globe,
  Github,
  ExternalLink
} from 'lucide-react'

function AboutPage() {
  const technologies = [
    {
      name: 'Google ADK',
      description: 'Agent Development Kit for multi-agent orchestration',
      icon: Brain,
      color: 'text-blue-400'
    },
    {
      name: 'Gemini 2.5 Pro',
      description: 'Advanced reasoning for story orchestration',
      icon: Sparkles,
      color: 'text-purple-400'
    },
    {
      name: 'Imagen 3.0',
      description: 'Consistent visual generation',
      icon: ImageIcon,
      color: 'text-green-400'
    },
    {
      name: 'Veo 2.0',
      description: 'Cinematic video generation',
      icon: Video,
      color: 'text-red-400'
    },
    {
      name: 'Lyria RealTime',
      description: 'Adaptive music composition',
      icon: Music,
      color: 'text-yellow-400'
    },
    {
      name: 'React + Vite',
      description: 'Modern web interface',
      icon: Code,
      color: 'text-cyan-400'
    }
  ]

  const features = [
    {
      title: 'Multi-Agent AI Collaboration',
      description: 'Specialized AI agents work together to create cohesive storytelling experiences.',
      icon: Users
    },
    {
      title: 'Real-time Generation',
      description: 'Dynamic content creation that responds instantly to your choices.',
      icon: Zap
    },
    {
      title: 'Visual Consistency',
      description: 'Maintains character and world consistency across all generated content.',
      icon: Palette
    },
    {
      title: 'Infinite Possibilities',
      description: 'Every story is unique with meaningful player agency and choices.',
      icon: Globe
    }
  ]

  const stats = [
    { label: 'AI Models', value: '5+' },
    { label: 'Media Types', value: '3' },
    { label: 'Code Lines', value: '1735+' },
    { label: 'Real-time', value: '100%' }
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="pt-16 min-h-screen"
    >
      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <div className="text-6xl mb-6">🎬</div>
            <h1 className="text-5xl font-cinematic gradient-text mb-6">
              About DreamDirector
            </h1>
            <p className="text-xl text-gray-300 leading-relaxed">
              A revolutionary storytelling experience where you become both the director and star 
              of your own cinematic adventure, powered by cutting-edge AI collaboration.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Technologies Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-cinematic-accent/5 via-transparent to-cinematic-gold/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-cinematic gradient-text mb-6">
              Powered by Google AI
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Built using the latest Google AI technologies for unprecedented creative collaboration
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {technologies.map((tech, index) => (
              <motion.div
                key={tech.name}
                initial={{ y: 50, opacity: 0 }}
                whileInView={{ y: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card-cinematic p-6 hover:scale-105 transition-transform duration-300"
              >
                <tech.icon className={`${tech.color} mb-4`} size={48} />
                <h3 className="text-xl font-cinematic text-white mb-3">
                  {tech.name}
                </h3>
                <p className="text-gray-400">
                  {tech.description}
                </p>
              </motion.div>
            ))}
          </div>
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
            <h2 className="text-4xl font-cinematic gradient-text mb-6">
              Key Features
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Advanced capabilities that make every story unique and engaging
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ x: index % 2 === 0 ? -50 : 50, opacity: 0 }}
                whileInView={{ x: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="card-cinematic p-8"
              >
                <feature.icon className="text-cinematic-accent mb-4" size={48} />
                <h3 className="text-2xl font-cinematic text-white mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-400 text-lg">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-cinematic-accent/10 via-transparent to-cinematic-gold/10">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-cinematic gradient-text mb-4">
              By the Numbers
            </h2>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-4xl font-bold gradient-text mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-400">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Hackathon Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            className="card-cinematic p-8 text-center"
          >
            <Award className="text-cinematic-gold mx-auto mb-6" size={64} />
            <h2 className="text-3xl font-cinematic gradient-text mb-4">
              UC Berkeley AI Hackathon 2025
            </h2>
            <p className="text-xl text-gray-300 mb-6">
              Built for the Creativity Track, showcasing the future of human-AI creative collaboration
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 mt-8">
              <div className="text-center">
                <Brain className="text-cinematic-accent mx-auto mb-3" size={32} />
                <h4 className="font-semibold text-white mb-2">Technical Innovation</h4>
                <p className="text-sm text-gray-400">
                  First multi-agent storytelling system using Google ADK
                </p>
              </div>
              <div className="text-center">
                <Sparkles className="text-cinematic-accent mx-auto mb-3" size={32} />
                <h4 className="font-semibold text-white mb-2">Creative Excellence</h4>
                <p className="text-sm text-gray-400">
                  Infinite storytelling possibilities with meaningful agency
                </p>
              </div>
              <div className="text-center">
                <Globe className="text-cinematic-accent mx-auto mb-3" size={32} />
                <h4 className="font-semibold text-white mb-2">Real-World Impact</h4>
                <p className="text-sm text-gray-400">
                  Educational, therapeutic, and entertainment applications
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Links Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-cinematic gradient-text mb-8">
              Explore More
            </h2>
            
            <div className="flex flex-col md:flex-row gap-6 justify-center">
              <a
                href="https://github.com/Abdullah0x0/dreamdirector"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary flex items-center justify-center space-x-3"
              >
                <Github size={20} />
                <span>View Source Code</span>
                <ExternalLink size={16} />
              </a>
              
              <a
                href="https://google.github.io/adk-docs/"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary flex items-center justify-center space-x-3"
              >
                <Brain size={20} />
                <span>Google ADK Docs</span>
                <ExternalLink size={16} />
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </motion.div>
  )
}

export default AboutPage 