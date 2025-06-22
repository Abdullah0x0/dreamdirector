# 🎬 DreamDirector - AI-Powered Cinematic Storytelling

> **"Tell me your dream story and I'll make you live it"**

DreamDirector is a revolutionary multimodal storytelling experience that combines cutting-edge AI technologies to create infinite, interactive narratives with real-time visual, audio, and video generation. Built for the UC Berkeley AI Hackathon 2025, this project represents the future of immersive digital storytelling.

<p align="center">
  <img src="https://github.com/user-attachments/assets/46ac8eb6-4c1e-4730-b716-030f5e903c44" alt="DreamDirector Landing Page" width="800">
  <br>
  <em>The main landing page, inviting users to start their cinematic adventure.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/6170e172-9fac-4c37-a00d-860a548e777e" alt="About DreamDirector" width="800">
  <br>
  <em>A breakdown of the key features and the Google AI tech stack.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/54bbbda5-a042-4949-9fb7-bf0cb616ca87" alt="Empty Media Gallery" width="800">
  <br>
  <em>The user's personal media gallery, ready to be filled with generated content.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/58b5273b-774a-4882-8b44-9be1133a976f" alt="Starting a Story" width="800">
  <br>
  <em>The user's journey begins with a simple prompt for any world they can imagine.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/6b956dc9-0ad3-4b77-96f2-2163be59d4ad" alt="Gameplay Loop" width="800">
  <br>
  <em>Our core experience: the AI drives the story, generates visuals, and presents choices.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b4006d78-3ca0-4f16-a678-8099d0d327c7" alt="AI Generated Video" width="800">
  <br>
  <em>Cinematic videos are generated in real-time for key story moments.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/1478ca2a-901b-4c8b-bf42-10fa5ebdecc6" alt="Filled Media Gallery" width="800">
  <br>
  <em>The gallery automatically saves every image, video, and music track from the story.</em>
</p>



## ✨ Key Features

### 🤖 Multi-Agent AI System
- **Story Director Agent** - Orchestrates narrative flow and pacing
- **Visual Consistency Agent** - Maintains character and location coherence
- **Music Composer Agent** - Creates adaptive, emotionally-responsive soundtracks
- **Media Generation Agent** - Coordinates real-time content creation

### 🎭 Real-Time Media Generation
- **Cinematic Images** - Google Imagen 3.0 with visual consistency tracking
- **Dynamic Videos** - Google Veo 2.0 for scene-to-scene transitions
- **Adaptive Music** - Google Lyria RealTime for contextual soundscapes
- **Professional Quality** - 4K visuals, 48kHz audio, cinematic composition

### 🎯 Interactive Storytelling
- **Choice-Driven Narratives** - Every decision shapes your unique story
- **Persistent Memory** - Characters and world state maintained across scenes
- **Emotional Intelligence** - AI responds to user personality and preferences
- **Infinite Replayability** - No two adventures are ever the same

## 🛠️ Technology Stack

### Frontend Technologies
- **React 18** - Modern component-based UI framework
- **Vite** - Lightning-fast build tool and development server
- **React Router Dom** - Client-side routing and navigation
- **Framer Motion** - Advanced animations and interactive transitions  
- **Tailwind CSS** - Utility-first styling with custom cinematic theme
- **Lucide React** - Beautiful, customizable icon library
- **Axios** - Promise-based HTTP client for API communication

### Backend Technologies
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - Lightning-fast ASGI server with async support
- **Pydantic** - Data validation and settings management
- **Python Multipart** - File upload and media handling
- **Python-dotenv** - Environment configuration management
- **CORS Middleware** - Cross-origin resource sharing support

### AI
- **Google ADK (Application Development Kit)** - Core AI agent orchestration
- **Google GenAI SDK** - Multimodal content generation APIs
- **Google Imagen 3.0** - State-of-the-art image generation with consistency
- **Google Veo 2.0** - Advanced video generation from image seeds  
- **Google Lyria RealTime** - Streaming music composition and generation
- **Streamlit** - Interactive AI demonstrations and prototyping

### Development & Build Tools
- **PostCSS** - CSS transformation and optimization
- **Autoprefixer** - Automatic vendor prefix management
- **Git** - Version control and collaboration
- **Node.js** - JavaScript runtime for frontend tooling

## 🎨 AI Agents & Capabilities

### 📖 Narrative Director
- **Story Architecture** - Creates compelling three-act structures
- **Character Development** - Maintains personality consistency
- **Plot Progression** - Balances pacing and dramatic tension
- **Choice Generation** - Crafts meaningful decision points

### 🎬 Visual Consistency Engine  
- **Character References** - Maintains visual identity across scenes
- **Location Memory** - Ensures environmental continuity
- **Style Coherence** - Applies consistent artistic direction
- **Scene Composition** - Professional cinematographic framing

### 🎵 Adaptive Music Composer
- **Emotional Scoring** - Music responds to story mood and tension
- **Real-Time Generation** - Seamless audio streaming during gameplay
- **Layered Composition** - Combines atmospheric, character, and action themes
- **Genre Adaptation** - Matches musical style to story setting

### 🎯 Media Orchestrator
- **Generation Optimization** - Balances quality with performance
- **Content Synchronization** - Coordinates multi-modal generation
- **Resource Management** - Efficient GPU and API usage
- **Quality Assurance** - Ensures professional-grade output

## 🌟 Project Highlights

### Innovation
- **Multi-Modal AI Collaboration** - First-of-its-kind agent orchestration
- **Real-Time Generation** - Live content creation during user interaction
- **Visual Consistency** - Breakthrough character/location memory system
- **Adaptive Soundscapes** - Dynamic music that evolves with narrative

### Technical Excellence
- **Async Architecture** - Non-blocking, high-performance backend
- **Streaming APIs** - Real-time audio/video generation pipeline
- **State Management** - Persistent game world across sessions
- **Error Resilience** - Graceful handling of AI generation failures

### User Experience
- **Cinematic Interface** - Movie-quality visual design and animations
- **Intuitive Navigation** - Seamless story progression and choice making
- **Performance Optimized** - Fast loading, smooth interactions
- **Accessibility** - Responsive design for all device types

## 🏆 Competition Context

**UC Berkeley AI Hackathon 2025 - Creativity Track**

DreamDirector represents a new paradigm in interactive entertainment, combining Google's most advanced AI technologies into a cohesive, magical user experience. The project showcases the potential of multi-agent AI systems working in harmony to create something greater than the sum of their parts.

## 🚀 Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Backend │    │  AI Agent System │
│                 │    │                  │    │                 │  
│ • Story UI      │◄──►│ • API Routes     │◄──►│ • Story Director│
│ • Media Gallery │    │ • Media Serving  │    │ • Visual Agent  │
│ • Choice System │    │ • State Mgmt     │    │ • Music Agent   │
│ • Animations    │    │ • File Handling  │    │ • Media Agent   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Google AI APIs │ 
                       │                 │
                       │ • Imagen 3.0    │
                       │ • Veo 2.0       │ 
                       │ • Lyria RT      │
                       │ • GenAI SDK     │
                       └─────────────────┘
```

---

*Showcasing the future of AI-powered interactive entertainment*
