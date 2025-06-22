## Inspiration
We love immersive games but always felt constrained by text-only interfaces. We dreamed of a platform where you could not just imagine the story, but see it unfold like a movie with adaptive music that responds to your emotions. The latest advances in multimodal AI from Google—including Gemini, Imagen 3.0, Veo 2.0, and Lyria RealTime—gave us the tools to finally build it: a true AI storyteller that weaves narrative, visuals, and dynamic audio together in real time.

## What it does
DreamDirector is your personal AI Cinematic Director for any adventure you can imagine. You start with a simple story idea—cyberpunk mystery, space opera, fantasy quest—and our sophisticated multi-agent AI system collaborates to build a rich, interactive world. The system generates stunning 4K images with visual consistency tracking, produces cinematic 8-second video sequences for dramatic moments, and creates adaptive music that evolves with your story's emotional tone. Every choice you make matters, with the AI maintaining persistent memory of characters, locations, and world state across your entire journey.

## How we built it

### Architecture & Technology Stack
**Frontend (React 18 + Modern Web)**
- React 18 with Vite for lightning-fast development
- Tailwind CSS with custom cinematic themes
- Framer Motion for advanced animations and transitions
- React Router Dom for seamless navigation
- Axios for API communication

**Backend (FastAPI + Python)**
- FastAPI with async/await for high-performance API handling
- Uvicorn ASGI server with real-time capabilities
- Pydantic for data validation and type safety
- Python-multipart for media file handling
- CORS middleware for cross-origin support

**AI & Multi-Agent System (Google ADK + GenAI)**
- Google ADK (Application Development Kit) for agent orchestration
- Google GenAI SDK with Gemini models for intelligent reasoning
- Google Imagen 3.0 for consistent visual generation
- Google Veo 2.0 for cinematic video sequences
- Google Lyria RealTime for streaming adaptive music

### Multi-Agent Workflow
We architected DreamDirector as a team of specialized AI agents working through the Google ADK framework:

**🎭 Story Director Agent**
- Orchestrates narrative flow using Gemini's reasoning capabilities
- Manages three-act story structure and pacing
- Generates meaningful user choices with preview consequences
- Maintains character development and plot consistency

**🎨 Visual Consistency Agent**
- Uses Imagen 3.0 with character/location reference tracking
- Maintains visual DNA across all generated content
- Ensures professional cinematographic composition
- Applies consistent artistic style and color palettes

**🎵 Adaptive Music Composer**
- Leverages Lyria RealTime for streaming audio generation
- Creates layered compositions (atmospheric, character, action themes)
- Responds to emotional tone and story tension in real-time
- Supports multiple genres from cyberpunk synthwave to orchestral fantasy

**🎬 Media Orchestrator**
- Coordinates multi-modal generation timing
- Optimizes resource usage across Google's APIs
- Handles video generation with image seeds for consistency
- Manages media balance for optimal user experience

### User Choice System
Our choice system goes beyond simple branching narratives:
- **Dynamic Choice Generation**: AI creates contextual choices based on current story state
- **Visual Preview System**: Users see potential outcomes through generated imagery
- **Persistent Consequences**: Every decision affects character relationships and world state
- **Adaptive Difficulty**: Story complexity adjusts to user engagement patterns
- **Memory Integration**: Choices influence future scene generation and character interactions

## Challenges we ran into
Orchestrating multiple cutting-edge AI models in real-time presented significant challenges. Ensuring visual consistency across Imagen 3.0 generations required sophisticated prompt engineering and reference image tracking. Integrating Lyria RealTime's streaming audio with FastAPI's async architecture demanded careful threading and session management. The most complex challenge was building a coherent multi-agent system where each AI agent could communicate through structured function calls while maintaining narrative coherence and user experience fluidity.

## Accomplishments that we're proud of
We successfully created the first truly multimodal storytelling engine that combines Gemini's reasoning, Imagen's visuals, Veo's cinematography, and Lyria's music into a seamless experience. Our multi-agent architecture represents a breakthrough in AI collaboration—each agent specializes in its domain while contributing to a unified creative vision. We're especially proud of our visual consistency system that maintains character appearance and world continuity across an entire story session, and our adaptive music system that creates Hollywood-quality soundtracks in real-time.

## What we learned
This hackathon was a masterclass in practical multimodal AI engineering. We learned how to architect complex agent systems using Google ADK's tool framework, mastered advanced prompt engineering for consistent visual generation, and discovered the nuances of real-time audio streaming. Most importantly, we proved that sophisticated AI agent collaboration can create experiences far richer than any single model—the whole truly becomes greater than the sum of its parts.

## What's next for DreamDirector
We envision expanding DreamDirector into a comprehensive creative platform. Our roadmap includes:
- **Multiplayer Adventures**: Shared AI-crafted worlds for collaborative storytelling
- **Creator Tools**: Allow users to define custom genres and fine-tune agent behaviors
- **Extended Media Support**: Integration with more Google AI APIs as they become available
- **Mobile Experience**: Native iOS/Android apps with offline story caching
- **Community Features**: Story sharing, remixing, and collaborative world-building

## Submission for the UC Berkeley AI Hackathon 2025 - Creativity Track
DreamDirector represents the future of AI-powered interactive entertainment, showcasing how multiple specialized agents can collaborate to create magical user experiences.

### Problem and Market Opportunity
The creator economy demands high-quality multimedia content, but individual creators face immense time and cost barriers. DreamDirector democratizes cinematic storytelling by turning weeks of traditional production into seconds of AI-powered generation, making professional-quality interactive media accessible to everyone.

### Multi-Agent Innovation and Technical Excellence
Our core innovation is a sophisticated multi-agent system built on Google ADK that goes far beyond simple prompt chaining. Each agent maintains specialized knowledge domains and communicates through structured function calls with persistent state management. This architecture enables complex creative workflows while maintaining reliability and coherence.

### Scalability and Impact
Built on Google's cloud-native APIs with async FastAPI architecture, DreamDirector is designed for massive scale. Our vision is to keep the core storytelling experience free for creators, students, and hobbyists while building sustainable revenue through enterprise API licensing for professional studios seeking to integrate our multi-agent creative engine into their workflows.

**DreamDirector isn't just an app—it's the foundation for the next generation of interactive entertainment.**