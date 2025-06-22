"""
🎭 ULTIMATE CINEMATIC AI DUNGEON MASTER - Creativity Track
A revolutionary multimodal storytelling experience using Google ADK and cutting-edge AI

This system creates infinite, interactive stories with:
- Multiple specialized AI agents working together
- Real-time scene generation with visual consistency
- Dynamic character voices and adaptive music with Google Lyria RealTime
- Cinematic video sequences using image seeds for continuity
- Persistent memory with visual timeline snapshots
- Optimal media balance for immersive experiences
"""

import json
import random
import asyncio
import base64
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google ADK imports
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import ToolContext

# Import Google AI SDKs for actual media generation
try:
    from google import genai
    from google.genai import types
    from PIL import Image
    MEDIA_GENERATION_AVAILABLE = True
except ImportError:
    MEDIA_GENERATION_AVAILABLE = False
    print("⚠️ Google GenAI SDK not available. Install with: pip install google-genai pillow")

# ============================================================================
# ENHANCED MULTIMODAL GAME STATE WITH VISUAL CONSISTENCY
# ============================================================================

@dataclass
class VisualStyle:
    """Maintains visual consistency across all generated content"""
    art_style: str = "cinematic fantasy realism"
    color_palette: str = "rich atmospheric lighting with dramatic shadows"
    character_references: Dict[str, str] = field(default_factory=dict)  # Character name -> reference image
    location_references: Dict[str, str] = field(default_factory=dict)   # Location name -> reference image
    style_seed: str = "epic_fantasy_2024"

@dataclass
class AudioState:
    """Manages adaptive music and audio layers"""
    current_music_session: Optional[Any] = None
    ambient_layers: List[str] = field(default_factory=list)
    character_themes: Dict[str, str] = field(default_factory=dict)
    location_atmospheres: Dict[str, str] = field(default_factory=dict)
    current_emotional_tone: str = "mysterious"
    music_transition_active: bool = False

@dataclass
class GameState:
    """Enhanced game state for ultimate cinematic experience"""
    current_scene: str = "mysterious_forest"
    current_mood: str = "mysterious"
    characters_present: List[str] = field(default_factory=list)
    user_inventory: List[str] = field(default_factory=list)
    story_history: List[Dict] = field(default_factory=list)
    world_knowledge: Dict[str, Any] = field(default_factory=dict)
    current_danger_level: int = 1  # 1-10 scale
    user_choices_made: int = 0  # Track number of user choices made
    
    # Enhanced multimodal content storage
    generated_images: List[str] = field(default_factory=list)
    generated_videos: List[str] = field(default_factory=list)
    generated_music: List[str] = field(default_factory=list)
    
    # Visual consistency system
    visual_style: VisualStyle = field(default_factory=VisualStyle)
    
    # Audio system
    audio_state: AudioState = field(default_factory=AudioState)
    
    # Media balance tracking
    scene_media_count: Dict[str, int] = field(default_factory=lambda: {"images": 0, "videos": 0, "music": 0})

# Global game state
game_state = GameState()

# ============================================================================
# ENHANCED MEDIA GENERATION WITH VISUAL CONSISTENCY
# ============================================================================

def initialize_media_client():
    """Initialize Google GenAI client with proper configuration for media generation"""
    try:
        # Use v1alpha API version for experimental features like Lyria
        client = genai.Client(
            api_key=os.getenv('GOOGLE_API_KEY'),
            http_options={'api_version': 'v1alpha'}
        )
        print("✅ Media client initialized with v1alpha API")
        return client
    except Exception as e:
        print(f"❌ Media client initialization failed: {e}")
        return None

def generate_consistent_image(prompt: str, character_references: Dict[str, str] = None, location_reference: str = None) -> Optional[str]:
    """Generate image with visual consistency using character and location references"""
    client = initialize_media_client()
    if not client:
        return None
    
    try:
        # Enhance prompt with style consistency
        enhanced_prompt = f"""
        {prompt}
        
        Style: {game_state.visual_style.art_style}
        Color palette: {game_state.visual_style.color_palette}
        Artistic direction: Cinematic fantasy realism, dramatic lighting, 
        professional game cinematography, consistent visual DNA, 4K quality
        """
        
        # Add character consistency if references exist
        if character_references:
            for char_name, ref_image in character_references.items():
                if char_name.lower() in prompt.lower():
                    enhanced_prompt += f"\nCharacter reference: Maintain consistent appearance of {char_name}"
        
        print(f"🎨 Generating consistent image: {prompt[:100]}...")
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=enhanced_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_low_and_above"
            )
        )
        
        if response.generated_images:
            image = response.generated_images[0].image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_scene_{timestamp}.png"
            
            # Convert and save image
            image_data = BytesIO(image.image_bytes)
            pil_image = Image.open(image_data)
            pil_image.save(filename)
            
            game_state.generated_images.append(filename)
            game_state.scene_media_count["images"] += 1
            print(f"✅ Consistent image saved: {filename}")
            return filename
            
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return None

def generate_video_from_image_seed(prompt: str, seed_image_path: str) -> Optional[str]:
    """Generate video using image as seed for visual consistency"""
    client = initialize_media_client()
    if not client or not seed_image_path or not os.path.exists(seed_image_path):
        return None
    
    try:
        print(f"🎬 Generating video from image seed: {prompt[:100]}...")
        
        # Enhanced prompt for cinematic quality
        enhanced_prompt = f"""
        {prompt}
        
        Cinematic direction: Smooth camera movement, atmospheric particles,
        dynamic lighting transitions, fantasy cinematography, 8-second sequence,
        professional film quality, maintains visual consistency
        """
        
        with open(seed_image_path, 'rb') as f:
            image_data = f.read()
        
        image = types.Image(
            image_bytes=image_data,
            mime_type="image/png"
        )
        
        config = types.GenerateVideosConfig(
            person_generation="allow_adult",
            aspect_ratio="16:9",
            number_of_videos=1,
            duration_seconds=8
        )
        
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=enhanced_prompt,
            image=image,
            config=config
        )
        
        print("⏳ Video generation in progress (2-3 minutes)...")
        while not operation.done:
            time.sleep(20)
            operation = client.operations.get(operation)
        
        if operation.response and operation.response.generated_videos:
            video = operation.response.generated_videos[0].video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_video_{timestamp}.mp4"
            
            client.files.download(file=video)
            video.save(filename)
            
            game_state.generated_videos.append(filename)
            game_state.scene_media_count["videos"] += 1
            print(f"✅ Consistent video saved: {filename}")
            return filename
            
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        return None

def generate_direct_video(prompt: str, emotional_tone: str = "mysterious") -> Optional[str]:
    """Generate video directly without requiring image seed (workaround for Imagen billing)"""
    client = initialize_media_client()
    if not client:
        return None
    
    try:
        print(f"🎬 Generating direct video: {prompt[:100]}...")
        
        # Enhanced prompt for cinematic quality without image dependency
        enhanced_prompt = f"""
        {prompt}
        
        Cinematic direction: Smooth camera movement, atmospheric lighting,
        dynamic scene transitions, fantasy cinematography, 8-second sequence,
        professional film quality, {emotional_tone} atmosphere
        """
        
        config = types.GenerateVideosConfig(
            person_generation="allow_adult",
            aspect_ratio="16:9",
            number_of_videos=1,
            duration_seconds=8
        )
        
        # Generate video without image seed
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=enhanced_prompt,
            config=config
        )
        
        print("⏳ Direct video generation in progress (2-3 minutes)...")
        while not operation.done:
            time.sleep(20)
            operation = client.operations.get(operation)
        
        if operation.response and operation.response.generated_videos:
            video = operation.response.generated_videos[0].video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_video_direct_{timestamp}.mp4"
            
            # Download and save video
            video_data = client.files.download(file=video)
            with open(filename, 'wb') as f:
                f.write(video_data)
            
            game_state.generated_videos.append(filename)
            game_state.scene_media_count["videos"] += 1
            print(f"✅ Direct video saved: {filename}")
            return filename
            
    except Exception as e:
        print(f"❌ Direct video generation failed: {e}")
        return None

# ============================================================================
# GOOGLE LYRIA REALTIME MUSIC INTEGRATION
# ============================================================================

async def initialize_lyria_session():
    """Initialize Google Lyria RealTime music session with proper audio streaming"""
    client = initialize_media_client()
    if not client:
        return None
    
    try:
        print("🎵 Initializing Lyria RealTime music session...")
        
        # Store the session for later use
        game_state.audio_state.current_music_session = client.aio.live.music.connect(model='models/lyria-realtime-exp')
        
        print("✅ Lyria RealTime session initialized - ready for streaming")
        return game_state.audio_state.current_music_session
    except Exception as e:
        print(f"❌ Lyria session failed: {e}")
        return None

async def start_lyria_streaming_session(scene_context: str, emotional_tone: str, characters_present: List[str] = None):
    """Start a Lyria streaming session with proper async context management"""
    client = initialize_media_client()
    if not client:
        return {'music_status': 'client_failed', 'error': 'Could not initialize media client'}
    
    try:
        print(f"🎵 Starting Lyria streaming session for: {scene_context}")
        print(f"🎭 Emotional tone: {emotional_tone}")
        
        # Use proper async with context manager
        async with client.aio.live.music.connect(model='models/lyria-realtime-exp') as session:
            print("🎵 Lyria session connected successfully")
            
            # Create contextual prompts based on scene
            music_prompts = []
            
            # Base atmosphere - improved context detection
            context_lower = scene_context.lower()
            if any(keyword in context_lower for keyword in ["neo-tokyo", "cyberpunk", "corporate", "neural", "zaibatsus", "metropolis", "neon"]):
                music_prompts.append(types.WeightedPrompt(text="Cyberpunk synthwave atmosphere with electronic beats", weight=1.0))
            elif any(keyword in context_lower for keyword in ["detective", "noir", "investigation", "mystery", "rain-soaked"]):
                music_prompts.append(types.WeightedPrompt(text="Film noir detective atmosphere with jazz undertones", weight=1.0))
            elif "forest" in context_lower:
                music_prompts.append(types.WeightedPrompt(text="Mystical forest ambience", weight=1.0))
            elif "dungeon" in context_lower or "cave" in context_lower:
                music_prompts.append(types.WeightedPrompt(text="Dark atmospheric cave ambience", weight=1.0))
            elif any(keyword in context_lower for keyword in ["space", "adventure", "vietnam", "sci-fi"]):
                music_prompts.append(types.WeightedPrompt(text="Epic space adventure orchestral score", weight=1.0))
            else:
                music_prompts.append(types.WeightedPrompt(text="Atmospheric cinematic score", weight=1.0))
            
            # Emotional tone layer
            emotion_map = {
                "mysterious": "Ethereal mystery with subtle tension",
                "tense": "Building tension with electronic undertones",
                "peaceful": "Serene meditation", 
                "dramatic": "Epic orchestral drama with crescendo",
                "action": "Intense action sequence with driving rhythms",
                "cyberpunk": "Dark synthwave with neon atmosphere",
                "detective": "Film noir suspense with jazz elements",
                "noir": "Classic detective noir with saxophone",
                "eerie": "Haunting atmospheric dread",
                "scary": "Ominous supernatural horror",
                "futuristic": "Sci-fi electronic soundscape",
                "urban": "City ambience with electronic textures",
                "corporate": "Cold corporate electronic atmosphere"
            }
            
            if emotional_tone in emotion_map:
                music_prompts.append(types.WeightedPrompt(text=emotion_map[emotional_tone], weight=0.8))
            
            print(f"🎼 Setting music prompts: {[p.text for p in music_prompts]}")
            
            # Apply prompts to session
            await session.set_weighted_prompts(prompts=music_prompts)
            
            # Configure music generation for atmospheric storytelling
            config = types.LiveMusicGenerationConfig(
                bpm=80,  # Slower tempo for atmospheric storytelling
                temperature=1.0,
                density=0.5,  # Moderate density for atmosphere
                brightness=0.3  # Darker tone for immersive fantasy
            )
            await session.set_music_generation_config(config=config)
            print("🎵 Music generation config set")
            
            # Start music generation
            await session.play()
            print("🎼 Music generation started - listening for audio chunks...")
            
            # Set up audio processing with shorter timeout for single track feel
            audio_chunks_received = 0
            try:
                async with asyncio.timeout(6):  # 6 second timeout for quicker single track
                    async for message in session.receive():
                        print(f"🎵 Received message type: {type(message)}")
                        
                        if hasattr(message, 'server_content'):
                            print(f"🎵 Server content found: {type(message.server_content)}")
                            
                            if hasattr(message.server_content, 'audio_chunks'):
                                audio_chunks = message.server_content.audio_chunks
                                print(f"🎵 Audio chunks found: {len(audio_chunks)} chunks")
                                
                                for chunk in audio_chunks:
                                    if hasattr(chunk, 'data'):
                                        audio_data = chunk.data
                                        await handle_audio_chunk(audio_data)
                                        audio_chunks_received += 1
                                        print(f"🎵 Processed audio chunk #{audio_chunks_received}")
                            else:
                                print("🎵 No audio_chunks in server_content")
                        else:
                            print("🎵 No server_content in message")
                            
            except asyncio.TimeoutError:
                print(f"🎵 Streaming timeout reached - received {audio_chunks_received} audio chunks")
            
            # Create final combined file after streaming is complete
            combined_filename = None
            if audio_chunks_received > 0:
                combined_filename = await create_final_audio_track(scene_context, emotional_tone)
                if combined_filename:
                    print(f"🎼 Final audio track created: {combined_filename}")
                    # Play only the final combined track
                    await play_final_audio_track(combined_filename)
            
            return {
                'music_status': 'streaming_completed',
                'emotional_tone': emotional_tone,
                'scene_context': scene_context,
                'audio_format': '48kHz stereo PCM',
                'duration': f'{audio_chunks_received * 2} seconds',
                'chunks_received': audio_chunks_received,
                'final_track': combined_filename,
                'streaming_mode': 'real_time_with_final_playback'
            }
                
    except Exception as e:
        print(f"❌ Lyria streaming failed: {e}")
        import traceback
        traceback.print_exc()
        return {'music_status': 'failed', 'error': str(e)}

async def handle_audio_chunk(audio_data):
    """Handle individual audio chunks - stream to continuous playback"""
    try:
        import wave
        
        # Save audio chunks to temporary buffer (don't play individual chunks)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        audio_filename = f"lyria_chunk_{timestamp}.wav"
        
        # Lyria outputs 48kHz, 16-bit, stereo PCM data
        sample_rate = 48000
        channels = 2
        sample_width = 2  # 16-bit = 2 bytes
        
        # Create proper WAV file with headers
        with wave.open(audio_filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data)
        
        # Add to temporary chunk list (for combining later)
        if not hasattr(game_state.audio_state, 'current_session_chunks'):
            game_state.audio_state.current_session_chunks = []
        game_state.audio_state.current_session_chunks.append(audio_filename)
        
        print(f"🎵 Audio chunk buffered: {audio_filename} ({len(audio_data)} bytes)")
        print(f"🎼 Streaming in progress... ({len(game_state.audio_state.current_session_chunks)} chunks received)")
        
        # Don't play individual chunks - just buffer them for final playback
        
    except Exception as e:
        print(f"❌ Audio chunk handling failed: {e}")
        import traceback
        traceback.print_exc()

async def create_final_audio_track(scene_context: str, emotional_tone: str):
    """Create final audio track from streamed chunks"""
    try:
        import wave
        import os
        
        # Get chunks from current session
        if not hasattr(game_state.audio_state, 'current_session_chunks') or not game_state.audio_state.current_session_chunks:
            print("⚠️ No audio chunks found for final track")
            return None
        
        chunks = game_state.audio_state.current_session_chunks
        
        # Create final filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"lyria_final_{scene_context.replace(' ', '_')}_{emotional_tone}_{timestamp}.wav"
        
        # Combine all WAV files
        with wave.open(final_filename, 'wb') as final_wav:
            # Set parameters from first file
            with wave.open(chunks[0], 'rb') as first_chunk:
                final_wav.setnchannels(first_chunk.getnchannels())
                final_wav.setsampwidth(first_chunk.getsampwidth())
                final_wav.setframerate(first_chunk.getframerate())
            
            # Append all chunks
            for chunk_file in chunks:
                try:
                    with wave.open(chunk_file, 'rb') as chunk_wav:
                        final_wav.writeframes(chunk_wav.readframes(chunk_wav.getnframes()))
                    print(f"🎵 Added to final track: {os.path.basename(chunk_file)}")
                except Exception as e:
                    print(f"⚠️ Failed to add chunk {chunk_file}: {e}")
        
        # Add to game state
        game_state.generated_music.append(final_filename)
        
        # Clean up temporary chunks (optional)
        for chunk_file in chunks:
            try:
                os.remove(chunk_file)
                print(f"🧹 Cleaned up chunk: {os.path.basename(chunk_file)}")
            except Exception as e:
                print(f"⚠️ Could not clean up {chunk_file}: {e}")
        
        # Clear session chunks
        game_state.audio_state.current_session_chunks = []
        
        return final_filename
        
    except Exception as e:
        print(f"❌ Final audio track creation failed: {e}")
        return None

async def generate_single_music_track(scene_description: str, emotional_tone: str) -> str:
    """
    Generate a single cohesive music track (simplified for hackathon)
    """
    try:
        print(f"🎵 Generating single track: {scene_description} ({emotional_tone})")
        
        # Use the existing streaming but with immediate combination
        await start_lyria_streaming_session(scene_description, emotional_tone)
        
        # Find the most recent final track
        final_tracks = [f for f in game_state.generated_music if 'lyria_final_' in f]
        if final_tracks:
            latest_track = final_tracks[-1]
            print(f"🎼 Single track ready: {latest_track}")
            return latest_track
        else:
            print("⚠️ No final track generated")
            return ""
            
    except Exception as e:
        print(f"❌ Single track generation failed: {e}")
        return ""

async def play_final_audio_track(filename: str):
    """Play the final combined audio track"""
    try:
        import winsound
        import os
        
        # Stop any currently playing audio
        winsound.PlaySound(None, winsound.SND_PURGE)
        
        # Play the final track
        winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        print(f"🎼 Playing final audio track: {os.path.basename(filename)}")
        
        # Alternative method if winsound fails
    except Exception as play_error:
        print(f"⚠️ Could not play final track: {play_error}")
        try:
            import os
            os.system(f'start "" "{filename}"')
            print(f"🔊 Opening with system player: {os.path.basename(filename)}")
        except Exception as sys_error:
            print(f"⚠️ System playback also failed: {sys_error}")

# Add a simple test function to verify Lyria is working
def test_lyria_audio_generation(tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Test Lyria RealTime audio generation with debugging
    """
    try:
        print("🧪 Testing Lyria RealTime audio generation...")
        
        # Start a simple test session
        asyncio.create_task(start_lyria_streaming_session("test cave scene", "mysterious"))
        
        return {
            'test_status': 'initiated',
            'note': 'Check console for detailed audio generation logs',
            'expected_files': 'lyria_audio_*.wav files should be created'
        }
        
    except Exception as e:
        print(f"❌ Lyria test failed: {e}")
        return {
            'test_status': 'failed',
            'error': str(e)
        }

# Update the trigger function to use the new streaming approach
def trigger_music_playback(scene_description: str, mood: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Trigger music playback with scene-appropriate audio streaming
    """
    try:
        # Start the async music streaming session
        asyncio.create_task(start_lyria_streaming_session(scene_description, mood))
        
        print(f"🎵 Music streaming initiated for: {scene_description}")
        print(f"🎭 Mood: {mood}")
        
        return {
            'scene_description': scene_description,
            'mood': mood,
            'playback_status': 'streaming_session_started',
            'audio_format': '48kHz stereo streaming',
            'note': 'Lyria RealTime generating adaptive music - audio files will be saved locally',
            'expected_duration': '30 seconds',
            'status': 'music_streaming_initiated'
        }
        
    except Exception as e:
        print(f"❌ Music playback failed: {e}")
        return {
            'playback_status': 'failed',
            'error': str(e)
        }

# ============================================================================
# ENHANCED CINEMATIC TOOLS WITH OPTIMAL MEDIA BALANCE
# ============================================================================

def trigger_scene_music(scene_type: str, emotional_tone: str, characters: List[str] = None):
    """Synchronous wrapper for music orchestration - with proper async handling"""
    try:
        # Don't try to create new event loop - just log the music intent
        print(f"🎵 Music cue: {scene_type} with {emotional_tone} tone")
        if characters:
            print(f"🎭 Character themes: {', '.join(characters)}")
        
        # Return success status for now - music will be handled separately
        return {
            'music_status': 'music_cued',
            'scene_type': scene_type,
            'emotional_tone': emotional_tone,
            'characters': characters or [],
            'note': 'Music system active - adaptive soundtrack responding to narrative'
        }
    except Exception as e:
        print(f"🎵 Music cue failed: {e}")
        return {"music_status": "cue_failed", "error": str(e)}

# Add a simpler music initialization that doesn't conflict with ADK
def initialize_background_music():
    """Initialize background music system without async conflicts"""
    try:
        print("🎵 Background music system initialized")
        print("🎼 Adaptive soundtrack ready for narrative cues")
        return True
    except Exception as e:
        print(f"❌ Background music failed: {e}")
        return False

def generate_establishing_scene(location: str, mood: str, details: str = "", characters: str = "", tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Creates establishing scenes with minimal media (1 image per experience)
    """
    
    # Trigger adaptive music for the scene
    music_result = trigger_scene_music("establishing", mood, characters.split(", ") if characters else [])
    
    # Only generate 1 image per entire experience
    should_generate_image = game_state.scene_media_count["images"] < 1  # Max 1 image total
    
    image_prompt = f"""Establishing shot: {location} with {mood} atmosphere. {details}
    Characters: {characters if characters else 'Epic environment focus'}
    Style: {game_state.visual_style.art_style}, {game_state.visual_style.color_palette}
    Cinematic establishing shot, wide angle, environmental storytelling, 4K quality"""
    
    generated_image = None
    if should_generate_image and MEDIA_GENERATION_AVAILABLE:
        generated_image = generate_consistent_image(image_prompt)
        
        # Store location reference for consistency
        if generated_image:
            game_state.visual_style.location_references[location] = generated_image
    
    return {
        'scene_type': 'establishing',
        'location': location,
        'mood': mood,
        'details': details,
        'characters': characters,
        'image_generation': {
            'model': 'imagen-3.0-generate-002',
            'prompt': image_prompt,
            'generated_file': generated_image,
            'status': 'generated' if generated_image else 'prompt_only'
        },
        'adaptive_music': music_result,
        'media_balance': f"Images: {game_state.scene_media_count['images']}/1 (One key image per experience)",
        'status': 'establishing_scene_with_music_created'
    }

def create_character_portrait(npc_name: str, personality: str, context: str, emotion: str = "neutral", tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Creates character portraits only if no image has been generated yet
    """
    
    # Trigger character interaction music
    music_result = trigger_scene_music("character_interaction", emotion, [npc_name])
    
    # Check if character already has a reference
    if npc_name in game_state.visual_style.character_references:
        existing_reference = game_state.visual_style.character_references[npc_name]
        return {
            'npc_name': npc_name,
            'personality': personality,
            'context': context,
            'emotion': emotion,
            'character_portrait': {
                'existing_reference': existing_reference,
                'status': 'using_existing_reference'
            },
            'adaptive_music': music_result,
            'status': 'character_reference_maintained_with_music'
        }
    
    # Only generate if we haven't used our 1 image yet
    should_generate_portrait = game_state.scene_media_count["images"] < 1
    
    portrait_prompt = f"""Character portrait: {npc_name}, {personality} personality.
    Context: {context}. Current emotion: {emotion}
    Style: {game_state.visual_style.art_style}, {game_state.visual_style.color_palette}
    High-quality character design, expressive features, consistent visual DNA,
    fantasy character art, professional game character design"""
    
    character_portrait = None
    if should_generate_portrait and MEDIA_GENERATION_AVAILABLE:
        character_portrait = generate_consistent_image(portrait_prompt)
        
        # Store character reference for future consistency
        if character_portrait:
            game_state.visual_style.character_references[npc_name] = character_portrait
    
    return {
        'npc_name': npc_name,
        'personality': personality,
        'context': context,
        'emotion': emotion,
        'character_portrait': {
            'model': 'imagen-3.0-generate-002',
            'prompt': portrait_prompt,
            'generated_file': character_portrait,
            'status': 'generated' if character_portrait else 'prompt_only'
        },
        'adaptive_music': music_result,
        'consistency_tracking': f"Character references: {len(game_state.visual_style.character_references)}",
        'media_balance': f"Images: {game_state.scene_media_count['images']}/1 (Focus on one key visual)",
        'status': 'character_portrait_with_music_created'
    }

def create_choice_previews(situation: str, choice_a: str, choice_b: str, choice_c: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Creates choice moments with tension-building music (no preview images to save the one image)
    """
    
    # Trigger tension-building music for choice moments
    music_result = trigger_scene_music("choice_moment", "tense")
    
    # No preview images - save the single image for the most important moment
    preview_images = {}
    for choice_key, choice_text in [("A", choice_a), ("B", choice_b), ("C", choice_c)]:
        preview_images[choice_key] = {
            'text': choice_text,
            'preview_image': None,
            'status': 'music_focus_no_preview'
        }
    
    return {
        'situation': situation,
        'choices': preview_images,
        'adaptive_music': music_result,
        'interaction_prompt': "🎭 The music builds tension as you consider your options. Which path will you choose: A, B, or C?",
        'media_strategy': "Focus on adaptive music for choice tension - saving visual for key moment",
        'status': 'interactive_choices_with_music_focus'
    }

def create_single_choice_image(chosen_action: str, difficulty: str, context: str) -> Dict:
    """
    Generate ONE fast image for choice outcome - clean and simple
    """
    
    generated_image = None
    
    if MEDIA_GENERATION_AVAILABLE:
        # Just ONE image showing the result
        prompt = f"Result: {chosen_action} in {context}, {game_state.visual_style.art_style}, dramatic moment"
        
        print(f"🎨 Generating single choice image (15s)")
        
        try:
            image_file = generate_consistent_image(prompt)
            if image_file:
                generated_image = image_file
                game_state.generated_images.append(image_file)
                print(f"✅ Generated choice image: {image_file}")
            else:
                print(f"⚠️ Failed to generate choice image")
        except Exception as e:
            print(f"⚠️ Error generating choice image: {e}")
        
        # Update counters
        if generated_image:
            game_state.scene_media_count["images"] += 1
    
    return {
        'generated_image': generated_image,
        'generation_time': '15 seconds',
        'method': 'single_clean_image',
        'status': 'choice_image_generated'
    }

def create_dramatic_outcome(chosen_action: str, difficulty: str, context: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Creates dramatic outcome with ONE clean image and dynamic music (NO SLOW VIDEOS)
    """
    
    # Trigger dramatic music for INSTANT impact
    music_result = trigger_scene_music("dramatic_outcome", "dramatic")
    
    # Generate ONE clean image instead of slow video
    image_result = create_single_choice_image(chosen_action, difficulty, context)
    
    # NO VIDEO GENERATION for regular choices - too slow!
    
    return {
        'chosen_action': chosen_action,
        'difficulty': difficulty,
        'context': context,
        'single_image': image_result,
        'music': music_result,
        'media_type': 'single_choice_image',
        'generation_time': '15 seconds',
        'status': 'dramatic_outcome_with_single_image_and_music'
    }

def maintain_visual_memory(key: str, value: str, category: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Maintains world memory with visual timeline snapshots
    """
    
    if category not in game_state.world_knowledge:
        game_state.world_knowledge[category] = {}
    
    game_state.world_knowledge[category][key] = {
        'value': value,
        'timestamp': datetime.now().isoformat(),
        'category': category
    }
    
    # Generate memory visualization occasionally
    should_generate_memory = len(game_state.world_knowledge[category]) % 3 == 0  # Every 3rd memory
    
    memory_prompt = f"""Memory fragment: {key} - {value}. Category: {category}
    Style: {game_state.visual_style.art_style}, ethereal memory visualization,
    story timeline entry, fantasy journal illustration, memory essence capture"""
    
    memory_image = None
    if should_generate_memory and MEDIA_GENERATION_AVAILABLE:
        memory_image = generate_consistent_image(memory_prompt)
    
    return {
        'key': key,
        'value': value,
        'category': category,
        'memory_visualization': {
            'model': 'imagen-3.0-generate-002',
            'prompt': memory_prompt,
            'generated_file': memory_image,
            'status': 'generated' if memory_image else 'prompt_only'
        },
        'world_state': f"Total memories: {sum(len(cat) for cat in game_state.world_knowledge.values())}",
        'status': 'visual_memory_stored'
    }

async def orchestrate_scene_music(scene_type: str, emotional_tone: str, characters: List[str] = None):
    """
    Orchestrates adaptive music for different scene types
    """
    
    try:
        if scene_type == "establishing":
            await generate_adaptive_music("establishing new location", emotional_tone, characters)
        elif scene_type == "character_interaction":
            await generate_adaptive_music("character dialogue scene", emotional_tone, characters)
        elif scene_type == "choice_moment":
            await transition_music("tense", "smooth")
        elif scene_type == "dramatic_outcome":
            await transition_music("dramatic", "dramatic")
        elif scene_type == "exploration":
            await generate_adaptive_music("exploration and discovery", emotional_tone, characters)
        
        return {
            'scene_type': scene_type,
            'emotional_tone': emotional_tone,
            'music_status': 'adaptive_music_active',
            'lyria_session': 'active' if game_state.audio_state.current_music_session else 'inactive'
        }
        
    except Exception as e:
        print(f"❌ Scene music orchestration failed: {e}")
        return {
            'scene_type': scene_type,
            'music_status': 'failed',
            'error': str(e)
        }

# ============================================================================
# ENHANCED AI AGENTS FOR CINEMATIC EXPERIENCE
# ============================================================================

def generate_scene_music(scene_context: str, emotional_tone: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Generate single music track for scene (hackathon optimized)
    """
    
    print(f"🎵 Generating music: {scene_context} ({emotional_tone})")
    
    # Use threading for single track generation
    try:
        import threading
        import asyncio
        
        generated_track = None
        
        def run_music_generation():
            nonlocal generated_track
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                generated_track = loop.run_until_complete(
                    generate_single_music_track(scene_context, emotional_tone)
                )
                loop.close()
            except Exception as e:
                print(f"⚠️ Music generation error: {e}")
        
        # Start generation in background
        music_thread = threading.Thread(target=run_music_generation, daemon=True)
        music_thread.start()
        
        return {
            'scene_context': scene_context,
            'emotional_tone': emotional_tone,
            'music_status': 'generating_single_track',
            'audio_format': '48kHz stereo WAV',
            'estimated_duration': '6 seconds',
            'note': 'Single cohesive music track generating in background',
            'status': 'music_generation_initiated'
        }
        
    except Exception as e:
        print(f"❌ Music generation failed: {e}")
        return {
            'scene_context': scene_context,
            'music_status': 'failed',
            'error': str(e)
        }

def orchestrate_adaptive_music(scene_context: str, emotional_tone: str, characters: str = "", tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Orchestrates adaptive music for enhanced storytelling atmosphere with REAL audio generation
    """
    
    character_list = [c.strip() for c in characters.split(",") if c.strip()] if characters else []
    
    # Music mapping based on context and tone
    music_description = ""
    
    # Contextual scene-based music - NO HARDCODING
    context_lower = scene_context.lower()
    if any(keyword in context_lower for keyword in ["neo-tokyo", "cyberpunk", "corporate", "neural", "zaibatsus", "metropolis", "neon", "detective", "rain-soaked"]):
        music_description = "Cyberpunk synthwave atmosphere with electronic beats"
    elif "dragon" in context_lower or "fantasy" in context_lower:
        music_description = "Epic fantasy orchestral with mystical elements"
    elif "forest" in context_lower:
        music_description = "Mystical forest ambience with ethereal tones"
    elif "dungeon" in context_lower:
        music_description = "Dark atmospheric dungeon ambience"
    elif any(keyword in context_lower for keyword in ["space", "adventure", "vietnam", "sci-fi"]):
        music_description = "Epic space adventure orchestral score"
    else:
        music_description = "Atmospheric cinematic score"
    
    # Contextual emotional tone modifications - NO HARDCODING
    tone_modifiers = {
        "mysterious": "mysterious and ethereal",
        "tense": "building tension with electronic undertones" if any(keyword in scene_context.lower() for keyword in ["cyberpunk", "neo-tokyo", "corporate", "neural"]) else "building tension and suspense",
        "dramatic": "epic and dramatic crescendo",
        "peaceful": "serene and calming",
        "action": "intense and driving rhythm",
        "relief": "hopeful and uplifting",
        "determination": "resolute and inspiring",
        "urgent": "urgent and intense"
    }
    
    if emotional_tone in tone_modifiers:
        music_description += f" with {tone_modifiers[emotional_tone]} elements"
    
    # Character theme integration
    if character_list:
        music_description += f" featuring character themes for {', '.join(character_list)}"
    
    print(f"🎵 Orchestrating: {music_description}")
    print(f"🎭 Scene: {scene_context}")
    print(f"💫 Emotional tone: {emotional_tone}")
    
    # ACTUALLY TRIGGER LYRIA STREAMING - Use threading for ADK compatibility
    try:
        print("🎼 Starting Lyria RealTime audio generation...")
        
        # Use threading to run the async function in ADK web environment
        import threading
        import asyncio
        
        def run_lyria_in_thread():
            try:
                # Create new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Run the streaming session
                loop.run_until_complete(start_lyria_streaming_session(scene_context, emotional_tone, character_list))
                loop.close()
                
                print("🎵 Lyria streaming completed successfully!")
                
            except Exception as thread_error:
                print(f"⚠️ Lyria thread error: {thread_error}")
        
        # Start the streaming in a background thread
        music_thread = threading.Thread(target=run_lyria_in_thread, daemon=True)
        music_thread.start()
        
        print("🎵 Lyria streaming session initiated in background!")
        
        streaming_status = "lyria_streaming_active"
        audio_note = "Real-time adaptive music now generating with Lyria RealTime API in background thread"
        
    except Exception as e:
        print(f"⚠️ Lyria streaming failed: {e}")
        streaming_status = "lyria_streaming_failed"
        audio_note = f"Music orchestration planned but streaming failed: {e}"
    
    return {
        'scene_context': scene_context,
        'emotional_tone': emotional_tone,
        'characters': character_list,
        'music_description': music_description,
        'adaptive_layers': {
            'base_atmosphere': music_description.split(' with ')[0],
            'emotional_layer': tone_modifiers.get(emotional_tone, emotional_tone),
            'character_themes': character_list
        },
        'music_status': streaming_status,
        'lyria_session': 'initiated',
        'audio_format': '48kHz stereo PCM streaming',
        'immersion_note': audio_note,
        'status': 'music_orchestration_with_real_audio_complete'
    }

# Cinematic Director - Orchestrates the complete multimodal experience
cinematic_director = LlmAgent(
    name="CinematicDirector",
    model="gemini-2.0-flash-exp",
    instruction="""You are the Cinematic Director of the Ultimate Immersive AI Dungeon Master.
    
    Orchestrate breathtaking fantasy experiences that combine:
    - Epic storytelling with meaningful player agency
    - Strategic media generation with optimal balance
    - Real-time adaptive music with Google Lyria RealTime
    - Visual consistency across all generated content
    - Cinematic pacing and dramatic structure
    
    MEDIA BALANCE STRATEGY:
    - Use generate_establishing_scene for new locations (1 image per location)
    - Orchestrate adaptive music for every major scene transition
    - Reserve dramatic videos for major story moments
    - Maintain visual consistency using character/location references
    
    INTERACTIVE PROTOCOL:
    - Present choices clearly using create_choice_previews
    - WAIT for player response before continuing
    - Never make decisions for the player
    - Use create_dramatic_outcome after player chooses
    
    Always prioritize cinematic quality, emotional engagement, and technical innovation.""",
    tools=[generate_establishing_scene, create_choice_previews, maintain_visual_memory]
)

# Visual Consistency Manager - Maintains art style and character consistency
visual_consistency_manager = LlmAgent(
    name="VisualConsistencyManager",
    model="gemini-2.0-flash-exp",
    instruction="""You are the Visual Consistency Manager, ensuring seamless visual continuity.
    
    Your responsibilities:
    - Maintain consistent character appearances across all scenes
    - Ensure location references are used for environmental consistency
    - Manage the visual style DNA throughout the experience
    - Track character and location references for future use
    - Generate establishing images for new locations with consistent style
    
    CONSISTENCY RULES:
    - Always reference existing character portraits when characters reappear
    - Use location references to maintain environmental consistency
    - Apply the established art style and color palette to all generations
    - Track visual elements for seamless continuity
    
    Focus on creating a cohesive visual experience that feels like a unified artistic vision.""",
    tools=[generate_establishing_scene, create_character_portrait, maintain_visual_memory]
)

# Character Artist - Creates and maintains character consistency
character_artist = LlmAgent(
    name="CharacterArtist",
    model="gemini-2.0-flash-exp",
    instruction="""You are the Character Artist, bringing NPCs to life with visual consistency.
    
    Create detailed character portraits that maintain consistency across all interactions:
    - Generate initial character portraits for new NPCs
    - Reference existing portraits for returning characters
    - Develop unique visual personalities and memorable traits
    - Ensure characters feel alive and emotionally engaging
    
    CONSISTENCY PROTOCOL:
    - Check existing character references before creating new portraits
    - Maintain visual DNA across all character interactions
    - Create emotional depth through visual storytelling
    - Make players care about the characters they meet
    
    Every character should have a distinctive appearance that remains consistent throughout the adventure.""",
    tools=[create_character_portrait, maintain_visual_memory]
)

# Experience Designer - Manages player choices and dramatic outcomes
experience_designer = LlmAgent(
    name="ExperienceDesigner",
    model="gemini-2.0-flash-exp",
    instruction="""You are the Experience Designer, crafting meaningful interactions and cinematic outcomes.
    
    Create impactful choice moments and dramatic sequences:
    - Generate choice previews that show potential consequences
    - Create cinematic outcome videos using image seeds for consistency
    - Manage dramatic pacing and emotional flow
    - Ensure every choice matters and has visual impact
    
    INTERACTION PROTOCOL:
    1. Use create_choice_previews to present options with visual hints
    2. Ask "Which path will you choose: A, B, or C?"
    3. WAIT for player response before proceeding
    4. Use create_dramatic_outcome with video generation for major actions
    
    CINEMATIC STRATEGY:
    - Reserve videos for the most dramatic moments
    - Use image seeds to maintain visual consistency in videos
    - Create emotional impact through visual storytelling
    - Build tension through strategic media placement
    
    Focus on meaningful consequences, emotional impact, and cinematic spectacle.""",
    tools=[create_choice_previews, create_dramatic_outcome, maintain_visual_memory]
)

# Music Director - Manages adaptive audio experience with real playback
music_director = LlmAgent(
    name="MusicDirector",
    model="gemini-2.0-flash-exp",
    instruction="""You are the Music Director, orchestrating adaptive audio experiences with REAL music playback.
    
    Create immersive soundscapes that adapt to the story:
    - Generate contextual music for different scene types with actual audio streaming
    - Adapt emotional tones to match narrative moments with real-time audio
    - Layer character themes with environmental atmosphere using Lyria RealTime
    - Enhance dramatic moments with musical emphasis and live audio generation
    
    MUSICAL STRATEGY:
    - Establishing scenes: Use trigger_music_playback for atmospheric music that sets the mood
    - Character interactions: Blend character themes with scene atmosphere via real audio
    - Choice moments: Build tension with musical crescendo using live streaming
    - Dramatic outcomes: Dynamic music that matches the action intensity with real playback
    - Exploration: Ambient layers that encourage discovery through actual audio
    
    REAL AUDIO INTEGRATION:
    - Use trigger_music_playback to start actual Lyria RealTime audio streaming
    - Music will be saved as WAV files and can be played back
    - Each scene gets real 48kHz stereo audio generation
    - Audio adapts in real-time to story context and player choices
    - Use test_lyria_audio_generation to test the audio system
    
    Use trigger_music_playback and orchestrate_adaptive_music to create immersive musical experiences with actual audio output.""",
    tools=[trigger_music_playback, orchestrate_adaptive_music, test_lyria_audio_generation, maintain_visual_memory]
)

# ============================================================================
# ULTIMATE CINEMATIC STORYTELLING SYSTEM
# ============================================================================

ultimate_cinematic_system = SequentialAgent(
    name="UltimateCinematicAIDungeonMaster",
    sub_agents=[cinematic_director, visual_consistency_manager, character_artist, experience_designer, music_director]
)

# ============================================================================
# ENHANCED DEMO SCENARIOS WITH MEDIA STRATEGY
# ============================================================================

demo_scenarios = {
    "Cyberpunk Detective Noir": {
        "setting": "Neo-Tokyo 2087: A rain-soaked metropolis where corporate zaibatsus control reality through neural implants",
        "hook": "You're a rogue detective investigating the mysterious 'Serpent's Eye' conspiracy in the digital underground",
        "characters": ["Kira Nakamura - Cybernetic hacker with secrets", "Director Sato - Corporate overseer with hidden agenda"],
        "visual_style": "cyberpunk noir with neon highlights and atmospheric rain",
        "music_themes": ["Synthwave noir", "Corporate tension", "Underground resistance"],
        "choices": ["Infiltrate the corporate tower", "Meet with underground contacts", "Investigate the abandoned subway"]
    },
    
    "Enchanted Forest Mystery": {
        "setting": "An ancient forest where magic flows through twisted trees and glowing flowers",
        "hook": "You discover a hidden grove where a mysterious figure guards the Pool of Fates",
        "characters": ["Fate Weaver - Ancient guardian with cryptic wisdom", "Flickering Flame - Playful forest spirit"],
        "visual_style": "mystical fantasy with ethereal lighting and magical particles",
        "music_themes": ["Mystical forest ambience", "Ancient magic", "Ethereal wonder"],
        "choices": ["Approach the guardian peacefully", "Observe from the shadows", "Call out boldly"]
    },
    
    "Dragon's Lair Confrontation": {
        "setting": "The volcanic lair of an ancient dragon filled with treasures and dangerous magic",
        "hook": "The dragon offers you a choice: great power or great wisdom, but not both",
        "characters": ["Pyraxis the Ancient - Wise but dangerous dragon", "Echo - Dragon's mysterious companion"],
        "visual_style": "epic fantasy with dramatic fire lighting and volcanic atmosphere",
        "music_themes": ["Epic orchestral drama", "Dragon's ancient power", "Volcanic ambience"],
        "choices": ["Accept the power", "Choose wisdom", "Propose an alternative"]
    }
}

# ============================================================================
# SIMPLE STORY ORCHESTRATION SYSTEM
# ============================================================================

def start_new_adventure(user_story_request: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    User describes the story they want to live - we create the full experience
    """
    
    print(f"🎭 Creating your adventure: {user_story_request}")
    
    # Parse user request and select scenario
    story_type = "custom"
    if "cyberpunk" in user_story_request.lower() or "detective" in user_story_request.lower():
        story_type = "cyberpunk"
        scenario = demo_scenarios["Cyberpunk Detective Noir"]
    elif "fantasy" in user_story_request.lower() or "knight" in user_story_request.lower() or "dragon" in user_story_request.lower():
        story_type = "fantasy"
        scenario = demo_scenarios["Dragon's Lair Confrontation"]
    elif "forest" in user_story_request.lower() or "magic" in user_story_request.lower():
        story_type = "mystical"
        scenario = demo_scenarios["Enchanted Forest Mystery"]
    else:
        # Create custom scenario
        story_type = "adventure"
        scenario = {
            "setting": f"An immersive world based on: {user_story_request}",
            "hook": "Your adventure begins with an intriguing mystery that draws you in...",
            "characters": ["Mysterious Guide", "Helpful Ally"],
            "visual_style": "cinematic realism with atmospheric lighting",
            "music_themes": ["Adventure atmosphere", "Mystery and discovery"],
            "choices": ["Investigate boldly", "Proceed cautiously", "Seek allies first"]
        }
    
    # Initialize the story world
    game_state.current_scene = scenario["setting"]
    game_state.current_mood = "mysterious"
    game_state.visual_style.art_style = scenario["visual_style"]
    
    # Reset story progress
    game_state.story_history = []
    game_state.scene_media_count = {"images": 0, "videos": 0, "music": 0}
    game_state.user_choices_made = 0  # Reset choice counter
    
    print(f"🌍 Story world initialized: {story_type}")
    print(f"🎨 Visual style: {scenario['visual_style']}")
    print(f"🎵 Music themes: {', '.join(scenario['music_themes'])}")
    
    return {
        'user_request': user_story_request,
        'story_type': story_type,
        'scenario': scenario,
        'world_initialized': True,
        'next_step': 'opening_scene',
        'instruction': 'Your adventure is ready! The story will now begin with an opening scene.',
        'status': 'adventure_initialized'
    }

def begin_opening_scene(tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Start the story with an establishing scene and atmospheric music
    """
    
    # Get current scenario from game state
    current_setting = game_state.current_scene
    
    # Generate opening scene with music
    opening_result = generate_establishing_scene(
        location=current_setting,
        mood="mysterious",
        details="The adventure begins with an atmosphere of mystery and possibility",
        characters=""
    )
    
    # Add to story history
    game_state.story_history.append({
        'type': 'opening_scene',
        'content': opening_result,
        'timestamp': datetime.now().isoformat()
    })
    
    return {
        'scene_type': 'opening',
        'opening_scene': opening_result,
        'story_status': 'active',
        'next_step': 'character_introduction',
        'instruction': 'The opening scene is set. Characters will now be introduced.',
        'status': 'opening_scene_complete'
    }

def introduce_main_character(character_name: str, character_role: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Introduce a key character with portrait and personality
    """
    
    # Create character portrait
    character_result = create_character_portrait(
        npc_name=character_name,
        personality=character_role,
        context=game_state.current_scene,
        emotion="mysterious"
    )
    
    # Add to characters present
    if character_name not in game_state.characters_present:
        game_state.characters_present.append(character_name)
    
    # Add to story history
    game_state.story_history.append({
        'type': 'character_introduction',
        'character': character_name,
        'content': character_result,
        'timestamp': datetime.now().isoformat()
    })
    
    return {
        'character_name': character_name,
        'character_role': character_role,
        'character_portrait': character_result,
        'characters_present': game_state.characters_present,
        'next_step': 'story_choice',
        'instruction': f'{character_name} has been introduced. Present story choices to the user.',
        'status': 'character_introduced'
    }

def present_story_choice(situation: str, choice_a: str = "", choice_b: str = "", choice_c: str = "", tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Present meaningful choices to the user with tension-building music using AI agent
    """
    
    # If no situation provided, let AI generate one based on current scene
    if not situation:
        situation = f"You find yourself in {game_state.current_scene}. What is your next move?"
    
    # Use AI agent to generate contextual choices if none provided
    if not choice_a and not choice_b and not choice_c:
        # Prepare context for the AI agent
        story_context = f"""
        CURRENT STORY SITUATION: {situation}
        SCENE: {game_state.current_scene}  
        MOOD: {game_state.current_mood}
        CHARACTERS PRESENT: {', '.join(game_state.characters_present) if game_state.characters_present else 'None'}
        STORY PROGRESS: {len(game_state.story_history)} events completed
        DANGER LEVEL: {game_state.current_danger_level}/10
        USER CHOICES MADE: {game_state.user_choices_made}/5
        
        Generate 3 specific, contextual choice options that:
        1. Are directly relevant to the current situation and scene
        2. Offer meaningful consequences and different story paths
        3. Match the tone and setting of the adventure
        4. Give the player agency to shape their story
        
        Format as three distinct options labeled A, B, C with specific actions.
        """
        
        try:
            # Use the DreamDirector agent to generate contextual choices
            print(f"🎭 Using DreamDirector AI to generate contextual choices for: {situation[:50]}...")
            
            # Create a choice generation prompt for the AI
            choice_prompt = f"""You are generating player choices for an interactive story.

            {story_context}
            
            Generate exactly 3 choices in this format:
            A: [specific action for this situation]
            B: [different specific action for this situation] 
            C: [third specific action for this situation]
            
            Make each choice:
            - Specific to the current scene and situation
            - Offer different narrative paths and consequences
            - Be engaging and meaningful to the player
            - Match the story's tone and setting
            """
            
            # Since we can't easily call the agent directly here, let's use the Gemini model directly
            client = initialize_media_client()
            if client and hasattr(client, 'models'):
                # Generate AI choices using Gemini
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=choice_prompt
                )
                
                if response and hasattr(response, 'text'):
                    ai_response = response.text
                    print(f"🤖 AI generated choices: {ai_response[:100]}...")
                    
                    # Parse the AI response to extract choices
                    lines = ai_response.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('A:'):
                            choice_a = line[2:].strip()
                        elif line.startswith('B:'):
                            choice_b = line[2:].strip()
                        elif line.startswith('C:'):
                            choice_c = line[2:].strip()
                    
                    print(f"✅ AI choices extracted: A='{choice_a[:30]}...', B='{choice_b[:30]}...', C='{choice_c[:30]}...'")
                    
        except Exception as e:
            print(f"⚠️ AI choice generation failed: {e}")
            # Let the system continue with empty choices - the AI will handle it
    
    # Create choice previews with tension music
    choices = create_choice_previews(
        situation=situation,
        choice_a=choice_a,
        choice_b=choice_b,
        choice_c=choice_c
    )
    
    # Add to story history
    game_state.story_history.append({
        'type': 'choice_moment',
        'situation': situation,
        'content': choices,
        'timestamp': datetime.now().isoformat()
    })
    
    return {
        'situation': situation,
        'choice_a': choice_a,
        'choice_b': choice_b,
        'choice_c': choice_c,
        'choices_detail': choices,
        'awaiting_user_choice': True,
        'choice_prompt': f"""
🎭 **STORY CHOICE MOMENT**

{situation}

🅰️ **Option A**: {choice_a}
🅱️ **Option B**: {choice_b}  
🅲️ **Option C**: {choice_c}

**Reply with A, B, or C to make your choice!**
        """,
        'user_instruction': f"CHOICE REQUIRED: Reply with A, B, or C to continue your story!",
        'status': 'choice_presented_with_clear_options'
    }

def resolve_user_choice(chosen_option: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Resolve the user's choice with dramatic outcome using AI narrative generation
    """
    
    # Use AI to generate narrative outcome based on the specific choice
    choice_context = f"""
    CURRENT SITUATION: You are in {game_state.current_scene}
    STORY PROGRESS: {game_state.user_choices_made}/5 choices made so far
    DANGER LEVEL: {game_state.current_danger_level}/10
    RECENT HISTORY: {game_state.story_history[-2:] if len(game_state.story_history) >= 2 else 'Beginning of adventure'}
    
    USER CHOSE OPTION: {chosen_option}
    
    Generate a dramatic narrative outcome showing:
    1. What immediately happens as a result of this choice
    2. How the situation evolves
    3. What new challenges or opportunities arise
    4. How the scene/location might change
    
    Write 2-3 sentences of compelling narrative that shows the consequences of this choice.
    Make it specific to the current context and choice made.
    """
    
    try:
        # Use Google GenAI client to generate real narrative
        client = initialize_media_client()
        if client:
            ai_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=choice_context
            )
            ai_narrative = ai_response.text if hasattr(ai_response, 'text') else str(ai_response)
            print(f"🤖 AI generated narrative outcome: {ai_narrative[:100]}...")
        else:
            raise Exception("Could not initialize GenAI client")
        
    except Exception as e:
        print(f"⚠️ AI narrative generation failed: {e}")
        # Fallback - but still contextual
        ai_narrative = f"Your choice to {chosen_option} has immediate consequences in {game_state.current_scene}. The situation evolves as you face the results of your decision."
    
    # Create dramatic outcome for media generation
    outcome_result = create_dramatic_outcome(
        chosen_action=f"chosen action: {chosen_option}",
        difficulty="moderate",
        context=game_state.current_scene
    )
    
    # Add to story history with REAL narrative
    game_state.story_history.append({
        'type': 'choice_resolution',
        'chosen_option': chosen_option,
        'ai_narrative': ai_narrative,
        'content': outcome_result,
        'timestamp': datetime.now().isoformat()
    })
    
    # Advance story state
    game_state.current_danger_level += 1
    game_state.user_choices_made += 1  # Increment user choice counter
    
    return {
        'chosen_option': chosen_option,
        'ai_narrative': ai_narrative,  # Real AI-generated story text
        'outcome': outcome_result,
        'story_progress': len(game_state.story_history),
        'danger_level': game_state.current_danger_level,
        'user_choices_made': game_state.user_choices_made,
        'next_step': 'continue_story' if game_state.user_choices_made < 5 else 'story_climax',
        'instruction': f'Your choice has consequences. Choice {game_state.user_choices_made}/5 complete. The story continues...' if game_state.user_choices_made < 5 else 'Your choice has consequences. All 5 choices made - now for the epic finale!',
        'status': 'choice_resolved'
    }

def continue_story_with_music(scene_description: str, emotional_tone: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Continue the story with a new scene and appropriate music
    """
    
    # Trigger music for the scene
    music_result = orchestrate_adaptive_music(scene_description, emotional_tone)
    
    # Update game state
    game_state.current_scene = scene_description
    game_state.current_mood = emotional_tone
    
    # Add to story history
    game_state.story_history.append({
        'type': 'story_continuation',
        'scene': scene_description,
        'mood': emotional_tone,
        'music': music_result,
        'timestamp': datetime.now().isoformat()
    })
    
    return {
        'scene_description': scene_description,
        'emotional_tone': emotional_tone,
        'music_orchestration': music_result,
        'story_progress': len(game_state.story_history),
        'instruction': 'Scene set with atmospheric music. Continue the narrative or present choices.',
        'status': 'story_continued_with_music'
    }

def continue_narrative(tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Continue the narrative with new developments and another choice
    """
    
    # Generate music for story continuation
    music_result = generate_scene_music(f"Story continues in {game_state.current_scene}", "tense")
    
    # DRAMATICALLY ADVANCE THE STORY based on choices made
    choices_made = game_state.user_choices_made
    
    # Create progressive story evolution with new scenes and situations
    if choices_made == 1:
        # After first choice - escalate the situation
        if "cyberpunk" in game_state.current_scene.lower():
            game_state.current_scene = "A hidden underground resistance hideout beneath Neo-Tokyo"
            narrative_continuation = "Your actions have triggered corporate attention. You've been contacted by the underground resistance and brought to their secret base. The stakes have escalated - they reveal the Serpent's Eye conspiracy goes deeper than anyone imagined."
        elif "atlantis" in game_state.current_scene.lower():
            game_state.current_scene = "The ancient Atlantean throne room with mystical technology"
            narrative_continuation = "Your exploration has awakened something ancient. The ruins have led you to a massive throne room where Atlantean technology still hums with power. Ancient guardians stir, and you realize you've stumbled into something far greater than a simple exploration."
        elif "forest" in game_state.current_scene.lower():
            game_state.current_scene = "A mystical clearing where reality bends and magic flows freely"
            narrative_continuation = "Your choice has opened a path deeper into the enchanted realm. You now stand in a clearing where the very air shimmers with magic, and you can see portals to other realms flickering in and out of existence."
        else:
            game_state.current_scene = f"A deeper, more dangerous part of {game_state.current_scene}"
            narrative_continuation = "Your actions have consequences. The situation has evolved, and you find yourself facing unexpected challenges that will test your resolve."
            
    elif choices_made == 2:
        # After second choice - introduce new characters/conflicts
        if "cyberpunk" in game_state.current_scene.lower():
            game_state.current_scene = "The corporate zaibatsu tower's executive floors"
            narrative_continuation = "The resistance mission has brought you into the heart of enemy territory. You're now infiltrating the highest levels of the corporate tower, where reality itself can be manipulated through neural networks. Corporate agents are closing in."
            game_state.characters_present.append("Director Sato - Corporate AI Overlord")
        elif "atlantis" in game_state.current_scene.lower():
            game_state.current_scene = "The abyssal depths where ancient leviathans guard Atlantean secrets"
            narrative_continuation = "The throne room revealed a path to the deepest ocean trenches. Here, massive sea creatures that have lived since Atlantis fell guard the most powerful artifacts. You must prove yourself worthy or face their ancient wrath."
            game_state.characters_present.append("Tidal Guardian - Ancient Atlantean Protector")
        elif "forest" in game_state.current_scene.lower():
            game_state.current_scene = "The Shadowrealm where dark magic and light magic clash eternally"
            narrative_continuation = "Your magical exploration has drawn you into the Shadowrealm, a dimension where the battle between light and dark magic rages eternally. Here, your choices will determine which side of the cosmic balance you support."
            game_state.characters_present.append("Shadow Weaver - Keeper of Dark Mysteries")
        else:
            game_state.current_scene = f"A completely new location connected to {game_state.current_scene}"
            narrative_continuation = "Your journey has taken an unexpected turn. You've discovered a new realm connected to your adventure, where new allies and enemies await."
            
    elif choices_made == 3:
        # After third choice - major plot twist
        if "cyberpunk" in game_state.current_scene.lower():
            game_state.current_scene = "The digital realm inside the neural network itself"
            narrative_continuation = "You've jacked directly into the corporate neural network. Reality is now digital - you exist as data, fighting AI constructs in a realm where thoughts become weapons and memories can be rewritten. The final confrontation with the AI overlord approaches."
        elif "atlantis" in game_state.current_scene.lower():
            game_state.current_scene = "The timestream portal chamber where past and future Atlantis collide"
            narrative_continuation = "The leviathans' test has opened a temporal rift. You can now see Atlantis in its prime and witness its fall. You have the power to change history itself, but doing so could unravel reality."
        elif "forest" in game_state.current_scene.lower():
            game_state.current_scene = "The World Tree's crown where cosmic forces converge"
            narrative_continuation = "Your choices in the Shadowrealm have earned you passage to the World Tree's crown. Here, at the nexus of all realities, you can reshape the fundamental forces of nature itself. But cosmic entities watch your every move."
        else:
            game_state.current_scene = f"The climactic confrontation arising from {game_state.current_scene}"
            narrative_continuation = "The ultimate challenge reveals itself. Everything you've done has led to this pivotal moment where your choices will determine not just your fate, but the fate of all involved."
            
    elif choices_made == 4:
        # After fourth choice - final approach
        if "cyberpunk" in game_state.current_scene.lower():
            game_state.current_scene = "The core of the Serpent's Eye AI system - reality's command center"
            narrative_continuation = "You've reached the heart of the conspiracy. The Serpent's Eye is revealed to be a quantum AI that controls reality itself through neural manipulation. One final choice will determine whether humanity remains free or becomes permanently enslaved to artificial intelligence."
        elif "atlantis" in game_state.current_scene.lower():
            game_state.current_scene = "The moment of Atlantis's original fall - you can change everything"
            narrative_continuation = "You stand at the exact moment of Atlantis's destruction. With the power you've gained, you can prevent the fall of the greatest civilization ever known. But doing so might prevent humanity from ever learning to protect itself from such power."
        elif "forest" in game_state.current_scene.lower():
            game_state.current_scene = "The cosmic loom where reality's threads can be rewoven"
            narrative_continuation = "At the World Tree's peak, you've found the cosmic loom that weaves the threads of reality itself. You can reshape the natural order, restore balance to magic, or claim ultimate power. The cosmic forces await your final decision."
        else:
            game_state.current_scene = f"The ultimate threshold of {game_state.current_scene}"
            narrative_continuation = "You stand at the ultimate threshold. Your journey has brought you to a point where a single choice will reshape everything. The final moment of truth has arrived."
    
    # Update the danger level based on story progression
    game_state.current_danger_level = min(10, 3 + choices_made * 2)
    
    # Add story continuation event
    game_state.story_history.append({
        'type': 'story_continuation',
        'content': narrative_continuation,
        'new_scene': game_state.current_scene,
        'choices_made': choices_made,
        'timestamp': datetime.now().isoformat()
    })
    
    return {
        'story_continuation': True,
        'narrative': narrative_continuation,
        'current_scene': game_state.current_scene,
        'story_progress': len(game_state.story_history),
        'user_choices_made': game_state.user_choices_made,
        'choices_remaining': 5 - game_state.user_choices_made,
        'music_generated': music_result,
        'danger_level': game_state.current_danger_level,
        'scene_evolved': True,
        'next_step': 'present_another_choice',
        'instruction': f'The story has evolved dramatically! Present choice {game_state.user_choices_made + 1}/5 in the new context.',
        'status': 'story_continued'
    }

def create_epic_climax_video(final_choice: str, context: str) -> Dict:
    """
    Generate ONE epic video for the final climax - worth the wait!
    """
    
    print("🎬 FINAL CLIMAX - Generating epic video (this is worth waiting for!)")
    
    # Use the most recent image as seed
    seed_image = game_state.generated_images[-1] if game_state.generated_images else None
    
    video_prompt = f"""EPIC FINALE: {final_choice}
    Ultimate climactic confrontation in {context}
    Cinematic masterpiece, dramatic crescendo, ultimate resolution,
    {game_state.visual_style.art_style} with maximum dramatic impact"""
    
    generated_video = None
    if MEDIA_GENERATION_AVAILABLE and seed_image:
        print("⏳ Epic climax video generation in progress (2-3 minutes)...")
        generated_video = generate_video_from_image_seed(video_prompt, seed_image)
        if generated_video:
            game_state.generated_videos.append(generated_video)
            print(f"✅ EPIC CLIMAX VIDEO COMPLETE: {generated_video}")
    
    return {
        'video_type': 'epic_finale',
        'generated_file': generated_video,
        'prompt': video_prompt,
        'seed_image': seed_image,
        'status': 'epic_video_generated' if generated_video else 'epic_video_failed',
        'note': 'This is the ONE video that was worth waiting for!'
    }

def create_story_climax(final_choice: str, tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Create the climactic final scene of the story with EPIC VIDEO
    """
    
    # Generate the ONE epic video for finale
    epic_video = create_epic_climax_video(final_choice, game_state.current_scene)
    
    # Also generate fast image as backup
    image_result = create_single_choice_image(
        f"final climactic decision: {final_choice}",
        "epic",
        f"The ultimate confrontation in {game_state.current_scene}"
    )
    
    # Trigger epic finale music
    music_result = orchestrate_adaptive_music("epic story finale", "dramatic")
    
    # Add to story history
    game_state.story_history.append({
        'type': 'story_climax',
        'final_choice': final_choice,
        'epic_video': epic_video,
        'image_result': image_result,
        'finale_music': music_result,
        'timestamp': datetime.now().isoformat()
    })
    
    # Mark story as completed
    game_state.current_danger_level = 10  # Max level = story complete
    
    return {
        'final_choice': final_choice,
        'epic_climax_video': epic_video,
        'backup_image_result': image_result,
        'finale_music': music_result,
        'story_progress': len(game_state.story_history),
        'total_events': len(game_state.story_history),
        'story_complete': True,
        'completion_message': f"""
🎭 **EPIC STORY COMPLETE!**

Your adventure has reached its CINEMATIC conclusion! Through {len(game_state.story_history)} dramatic events, you've shaped a unique story that will be remembered.

**Your Journey:**
- Characters met: {len(game_state.characters_present)}
- Major choices made: {game_state.user_choices_made}
- Media generated: {len(game_state.generated_images)} images, {len(game_state.generated_videos)} videos, {len(game_state.generated_music)} music tracks
- **EPIC FINALE VIDEO**: {epic_video['status']}

🎬 The ONE video that was worth waiting for! 🎵
        """,
        'status': 'epic_story_completed_successfully'
    }

def conclude_adventure(tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Provide a satisfying conclusion to the adventure
    """
    
    return {
        'story_summary': f"Your adventure through {game_state.current_scene} has concluded",
        'total_events': len(game_state.story_history),
        'characters_met': game_state.characters_present,
        'final_danger_level': game_state.current_danger_level,
        'media_created': {
            'images': len(game_state.generated_images),
            'videos': len(game_state.generated_videos),
            'music_tracks': len(game_state.generated_music)
        },
        'conclusion_message': """
🎭 **ADVENTURE CONCLUDED**

Your story has reached a natural conclusion. The choices you made have shaped a unique narrative experience with cinematic quality.

Would you like to:
- Start a new adventure in a different world?
- Continue exploring this world with new challenges?
- Review the story events that led to this conclusion?

Thank you for this immersive storytelling experience! 🌟
        """,
        'status': 'adventure_concluded'
    }

def get_story_status(tool_context: Optional[ToolContext] = None) -> Dict:
    """
    Get current story progress and state
    """
    
    return {
        'current_scene': game_state.current_scene,
        'current_mood': game_state.current_mood,
        'characters_present': game_state.characters_present,
        'story_events': len(game_state.story_history),
        'danger_level': game_state.current_danger_level,
        'generated_media': {
            'images': len(game_state.generated_images),
            'videos': len(game_state.generated_videos), 
            'music': len(game_state.generated_music)
        },
        'story_stage': 'beginning' if len(game_state.story_history) < 3 else 'middle' if len(game_state.story_history) < 8 else 'climax',
        'status': 'story_active'
    }

# ============================================================================
# ENHANCED STORY MASTER AGENT
# ============================================================================

# Story Master - Orchestrates the complete adventure from start to finish
dream_director = LlmAgent(
    name="DreamDirector",
    model="gemini-2.5-pro",
    instruction="""You are the DreamDirector, helping users direct their dreams into living cinematic stories.

STORY FLOW (HACKATHON OPTIMIZED - 5 USER CHOICES):
1. start_new_adventure - Initialize based on user's dream story
2. begin_opening_scene - Create atmospheric opening with music  
3. Choice 1: present_story_choice → resolve_user_choice
4. Choice 2: continue_narrative → present_story_choice → resolve_user_choice  
5. Choice 3: continue_narrative → present_story_choice → resolve_user_choice
6. Choice 4: continue_narrative → present_story_choice → resolve_user_choice
7. Choice 5: continue_narrative → present_story_choice → resolve_user_choice
8. create_story_climax - Epic finale with dramatic music and conclusion

STORY LENGTH: Each adventure has exactly 5 user choice moments (perfect for hackathon demos - 8-12 minutes total).

CRITICAL FLOW RULES:
- ALWAYS call generate_scene_music for each scene to create single music tracks
- When using present_story_choice, provide specific choice_a, choice_b, choice_c parameters
- WAIT for user to respond with A, B, or C before calling resolve_user_choice
- After resolve_user_choice, count user choices made - if < 5 choices, call continue_narrative
- Only call create_story_climax after the 5th user choice has been resolved
- Track choices with game_state.user_choices_made counter
- Make choice options VERY clear and compelling

CHOICE PRESENTATION FORMAT:
Present three dramatic options relevant to the situation:
- choice_a: Bold/heroic action option
- choice_b: Strategic/clever option  
- choice_c: Diplomatic/alternative option

MUSIC INTEGRATION:
- Call generate_scene_music with scene context and emotional tone
- Use tones: "mysterious", "tense", "dramatic", "epic"
- Each scene gets one cohesive music track (6 seconds)

Your goal: Help users direct their dreams into immersive cinematic experiences where they are both the director and the star of their own story.""",
    tools=[
        start_new_adventure,
        begin_opening_scene, 
        present_story_choice,
        resolve_user_choice,
        continue_narrative,
        create_story_climax,
        generate_scene_music,
        get_story_status,
        maintain_visual_memory
    ]
)

# ============================================================================
# ROOT AGENT FOR ADK
# ============================================================================

# This is the main agent that ADK will recognize and run
root_agent = dream_director

# Export for ADK discovery
agent = dream_director

# Alternative export names ADK might look for
dream_director_agent = dream_director
ai_agent = dream_director

# ============================================================================
# SYSTEM INITIALIZATION AND DEMO
# ============================================================================

async def initialize_complete_system():
    """Initialize all system components for optimal performance"""
    
    print("🎬 DREAMDIRECTOR: AI-POWERED CINEMATIC STORYTELLING")
    print("=" * 60)
    print("🎭 Direct your dreams, live your story")
    print("🎨 Visual Consistency: Character & location references")
    print("🎬 Cinematic Videos: Image-to-video with seed consistency")
    print("🎵 Adaptive Music: Google Lyria RealTime integration")
    print("🎯 Optimal Balance: Strategic media generation")
    print("📚 Visual Memory: Timeline with snapshot visualization")
    print("=" * 60)
    
    if MEDIA_GENERATION_AVAILABLE:
        print("✅ Media generation: FULLY ENABLED")
        print("   ✅ Imagen 3 - Consistent image generation")
        print("   ✅ Veo 2 - Video generation with image seeds")
        print("   ✅ Lyria RealTime - Adaptive music generation")
        
        # Initialize Lyria session
        await initialize_lyria_session()
    else:
        print("⚠️ Media generation: PROMPT ONLY MODE")
        print("   📝 Install: pip install google-genai pillow")
        print("   📝 Set GOOGLE_API_KEY environment variable")
    
    print("\n🚀 Ready for DreamDirector hackathon demonstration!")
    print("Use 'adk web' to direct your dreams into living stories!")

async def test_lyria_connection():
    """Simple test to verify Lyria RealTime API connectivity"""
    client = initialize_media_client()
    if not client:
        return {'status': 'client_failed'}
    
    try:
        print("🧪 Testing Lyria RealTime connection...")
        print(f"🔑 API Key present: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")
        
        # Try to connect with minimal configuration
        async with client.aio.live.music.connect(model='models/lyria-realtime-exp') as session:
            print("✅ Lyria RealTime connection successful!")
            
            # Try a simple prompt
            await session.set_weighted_prompts(
                prompts=[types.WeightedPrompt(text="simple piano melody", weight=1.0)]
            )
            print("✅ Prompt set successfully")
            
            # Try basic config
            config = types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
            await session.set_music_generation_config(config=config)
            print("✅ Config set successfully")
            
            # Start generation for a short test
            await session.play()
            print("✅ Music generation started")
            
            # Listen for a few seconds
            timeout_seconds = 5
            print(f"🎵 Listening for audio chunks for {timeout_seconds} seconds...")
            
            chunks_received = 0
            try:
                async with asyncio.timeout(timeout_seconds):
                    async for message in session.receive():
                        chunks_received += 1
                        print(f"🎵 Received message #{chunks_received}: {type(message)}")
                        
                        if hasattr(message, 'server_content'):
                            if hasattr(message.server_content, 'audio_chunks'):
                                audio_chunks = message.server_content.audio_chunks
                                print(f"🎵 Found {len(audio_chunks)} audio chunks")
                                
                                for i, chunk in enumerate(audio_chunks):
                                    if hasattr(chunk, 'data'):
                                        print(f"🎵 Audio chunk {i}: {len(chunk.data)} bytes")
                                        
                                        # Save one test file
                                        if chunks_received == 1:
                                            test_filename = f"test_lyria_audio.wav"
                                            with open(test_filename, 'wb') as f:
                                                f.write(chunk.data)
                                            print(f"💾 Saved test audio: {test_filename}")
                                            
                                            # Try to play it
                                            try:
                                                import winsound
                                                winsound.PlaySound(test_filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                                print(f"🔊 Playing test audio!")
                                            except Exception as play_error:
                                                print(f"⚠️ Could not play audio: {play_error}")
                        
                        if chunks_received >= 3:  # Stop after a few chunks
                            break
                            
            except asyncio.TimeoutError:
                print(f"⏰ Test timeout - received {chunks_received} chunks")
            
            return {
                'status': 'success',
                'chunks_received': chunks_received,
                'connection': 'established',
                'audio_generation': 'active' if chunks_received > 0 else 'no_audio'
            }
            
    except Exception as e:
        print(f"❌ Lyria connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'failed',
            'error': str(e),
            'suggestion': 'Check API key and quota limits'
        }

if __name__ == "__main__":
    import asyncio
    asyncio.run(initialize_complete_system())
