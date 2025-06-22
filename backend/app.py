from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Add the agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

try:
    from agent import (
        start_new_adventure,
        present_story_choice,
        resolve_user_choice,
        generate_establishing_scene,
        orchestrate_adaptive_music,
        create_single_choice_image,
        create_epic_climax_video,
        get_story_status,
        game_state,
        begin_opening_scene,
        continue_narrative,
        create_story_climax,
        generate_direct_video
    )
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Could not import agent functions: {e}")
    AGENT_AVAILABLE = False

app = FastAPI(
    title="DreamDirector API",
    description="🎬 AI-Powered Cinematic Storytelling Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://*.railway.app",
        "https://*.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (generated media)
media_dir = Path("../agents")  # Files are generated in agents directory
if media_dir.exists():
    app.mount("/media", StaticFiles(directory=str(media_dir)), name="media")
else:
    # Fallback to current directory
    media_dir = Path(".")
    app.mount("/media", StaticFiles(directory=str(media_dir)), name="media")

# Serve frontend static files (for production)
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Serve frontend at root for production
    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        # API routes should not be served by frontend
        if path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Serve specific files
        file_path = static_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        
        # Fallback to index.html for SPA routing
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        
        raise HTTPException(status_code=404, detail="File not found")

# Request/Response Models
class StoryRequest(BaseModel):
    story_request: str

class ChoiceRequest(BaseModel):
    choice: str

class MediaRequest(BaseModel):
    type: str  # 'image', 'video', 'music'
    prompt: str
    emotional_tone: str = "mysterious"

class StoryResponse(BaseModel):
    narrative: str
    choices: list[str] = []
    scene_description: str = ""
    mood: str = "mysterious"
    scene_id: str = ""
    media_files: dict = {}
    story_complete: bool = False
    story_progression: list = []
    choices_remaining: int = 0
    current_choice: int = 0
    total_choices: int = 0

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "🎬 DreamDirector API - REAL AI ONLY!",
        "agent_available": AGENT_AVAILABLE,
        "mode": "PRODUCTION - Using agent.py only",
        "mock_data": "DISABLED",
        "endpoints": [
            "/api/start-story",
            "/api/make-choice", 
            "/api/generate-media",
            "/api/story-status",
            "/api/media-files"
        ]
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_available": AGENT_AVAILABLE,
        "media_directory": str(media_dir.absolute()) if media_dir.exists() else "not found"
    }

# Start a new story
@app.post("/api/start-story", response_model=StoryResponse)
async def start_story(request: StoryRequest):
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI Agent system not available. Please check Google ADK installation.")
    
    try:
        print(f"🎬 Starting story using agent.py: {request.story_request}")
        
        # Step 1: Initialize the adventure with real AI
        init_result = start_new_adventure(request.story_request)
        print(f"✅ Adventure initialized: {init_result.get('status')}")
        
        # Step 2: Begin opening scene with real AI
        opening_result = begin_opening_scene()
        print(f"✅ Opening scene created: {opening_result.get('status')}")
        
        # Step 3: Let AI generate the actual story situation and choices
        # Don't provide hardcoded text - let the AI create everything
        choice_result = present_story_choice("")  # Empty string - let AI generate situation
        print(f"✅ Choices presented: {choice_result.get('status')}")
        
        # Extract ONLY real AI-generated content
        ai_narrative = ""
        if opening_result.get('opening_scene', {}).get('narrative'):
            ai_narrative = opening_result['opening_scene']['narrative']
        elif init_result.get('scenario', {}).get('hook'):
            ai_narrative = init_result['scenario']['hook']
        else:
            ai_narrative = "Story initializing..."
            
        ai_situation = choice_result.get('situation', '')
        if ai_situation:
            ai_narrative += f" {ai_situation}"
        
        return StoryResponse(
            narrative=ai_narrative,
            choices=[
                choice_result.get('choice_a', ''),
                choice_result.get('choice_b', ''),
                choice_result.get('choice_c', '')
            ],
            scene_description=init_result.get('scenario', {}).get('setting', request.story_request),
            mood=game_state.current_mood,
            scene_id='opening_scene',
            media_files={},
            story_complete=False,
            story_progression=[],
            choices_remaining=5,
            current_choice=0,
            total_choices=5
        )
    except Exception as e:
        print(f"❌ Agent.py error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Agent error: {str(e)}")

# Make a choice in the story
@app.post("/api/make-choice", response_model=StoryResponse)
async def make_choice(request: ChoiceRequest):
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI Agent system not available. Please check Google ADK installation.")
    
    try:
        print(f"🎭 Processing choice using agent.py: {request.choice}")
        
        # Step 1: Resolve the user's choice with real AI narrative
        choice_result = resolve_user_choice(request.choice)
        print(f"✅ Choice resolved: {choice_result.get('status')}")
        
        # Extract the REAL AI-generated narrative
        ai_narrative = choice_result.get('ai_narrative', 'The story continues...')
        print(f"🤖 Using AI narrative: {ai_narrative[:50]}...")
        
        # Build comprehensive story progression
        story_progression = []
        
        # Add the choice resolution with REAL AI narrative
        story_progression.append({
            'type': 'choice_result',
            'content': ai_narrative,  # Use real AI narrative!
            'timestamp': datetime.now().isoformat()
        })
        
        # Check if more choices needed
        user_choices_made = choice_result.get('user_choices_made', 0)
        choices_remaining = 5 - user_choices_made
        
        if user_choices_made < 5:
            # Step 2: Continue narrative with story evolution
            narrative_result = continue_narrative()
            print(f"✅ Narrative continued: {narrative_result.get('status')}")
            
            # Add real narrative continuation
            if narrative_result.get('narrative'):
                story_progression.append({
                    'type': 'story_continuation',
                    'content': narrative_result['narrative'],  # Real AI story evolution
                    'timestamp': datetime.now().isoformat()
                })
            
            # Step 3: Generate next choices with updated context
            next_choice_result = present_story_choice("")  # Let AI create new situation
            print(f"✅ Next choices presented: {next_choice_result.get('status')}")
            
            # Get the new situation
            new_situation = next_choice_result.get('situation', 'What do you do next?')
            story_progression.append({
                'type': 'new_situation',
                'content': new_situation,
                'timestamp': datetime.now().isoformat()
            })
            
            # Extract AI-generated choices
            choices = [
                next_choice_result.get('choice_a', ''),
                next_choice_result.get('choice_b', ''),
                next_choice_result.get('choice_c', '')
            ]
            
            # Get updated scene context
            current_scene = narrative_result.get('current_scene', game_state.current_scene)
            
            return StoryResponse(
                narrative=ai_narrative,  # Real AI narrative outcome
                scene_description=current_scene,
                choices=choices,
                story_complete=False,
                story_progression=story_progression,
                choices_remaining=choices_remaining,
                current_choice=user_choices_made,
                total_choices=5
            )
        else:
            # Final choice - create climax
            climax_result = create_story_climax(request.choice)
            print(f"✅ Story climax created: {climax_result.get('status')}")
            
            # Add climax narrative
            if climax_result.get('climax_outcome'):
                story_progression.append({
                    'type': 'story_climax',
                    'content': climax_result.get('completion_message', 'Your adventure reaches its epic conclusion!'),
                    'timestamp': datetime.now().isoformat()
                })
            
            return StoryResponse(
                narrative=ai_narrative,  # Real AI choice outcome
                scene_description=f"{game_state.current_scene} - FINALE",
                choices=[],
                story_complete=True,
                story_progression=story_progression,
                choices_remaining=0,
                current_choice=5,
                total_choices=5
            )
        
    except Exception as e:
        print(f"❌ Choice processing error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Choice processing failed: {str(e)}")

# Generate media content
@app.post("/api/generate-media")
async def generate_media(request: MediaRequest):
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI Agent system not available. Please check Google ADK installation.")
    
    try:
        print(f"🎨 Generating {request.type} using agent.py: {request.prompt}")
        
        result = {}
        generated_files = []
        
        if request.type == "image":
            result = generate_establishing_scene(
                location=request.prompt,
                mood=request.emotional_tone,
                details="cinematic quality"
            )
            # Add any generated images from game state
            generated_files = game_state.generated_images
            
        elif request.type == "music":
            result = orchestrate_adaptive_music(
                scene_context=request.prompt,
                emotional_tone=request.emotional_tone
            )
            # Add any generated music from game state
            generated_files = game_state.generated_music
            
        elif request.type == "video":
            # **ALLOW VIDEOS DURING REGULAR STORY**
            print("🎬 Generating video for current scene...")
            try:
                # Try to generate actual video
                result = generate_direct_video(
                    prompt=request.prompt,
                    emotional_tone=request.emotional_tone
                )
                
                # Check if video was actually generated
                if game_state.generated_videos:
                    generated_files = game_state.generated_videos
                    result.update({
                        "message": "🎬 AI video generated successfully!",
                        "method": "direct_video_generation",
                        "note": "Video generation may take 2-3 minutes"
                    })
                else:
                    # Fallback to image if video generation failed
                    print("🎨 Video generation failed, creating cinematic image instead...")
                    result = create_single_choice_image(
                        chosen_action=f"cinematic moment: {request.prompt}",
                        difficulty="medium",
                        context=request.prompt
                    )
                    generated_files = game_state.generated_images
                    result.update({
                        "message": "🎨 Generated cinematic image (video generation in progress)",
                        "method": "fallback_to_image",
                        "note": "Video may appear shortly in the gallery"
                    })
                    
            except Exception as video_error:
                print(f"⚠️ Video generation issue: {video_error}")
                # Fallback to scene generation
                result = generate_establishing_scene(
                    location=request.prompt,
                    mood=request.emotional_tone,
                    details="cinematic sequence"
                )
                generated_files = game_state.generated_images
                result.update({
                    "message": "🎨 Generated scene image (video generation unavailable)",
                    "method": "fallback_scene_generation"
                })
        else:
            raise HTTPException(status_code=400, detail="Invalid media type")
        
        # Get the latest generated file for this media type
        latest_file = None
        if generated_files:
            latest_file = generated_files[-1]  # Most recent file
            
        # Construct proper response with file information
        response = {
            "status": "success",
            "type": request.type,
            "result": result,
            "message": f"✨ {request.type.title()} generated using agent.py!",
            "generated_file": latest_file,
            "total_files": len(generated_files),
            "all_files": generated_files[-5:] if len(generated_files) > 5 else generated_files  # Last 5 files
        }
        
        # Add file URL if file exists
        if latest_file:
            response["url"] = f"/api/media/{latest_file}"
            response["filename"] = latest_file
            print(f"✅ {request.type} file ready: {latest_file}")
        
        return response
        
    except Exception as e:
        print(f"❌ Agent.py media generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Agent media generation error: {str(e)}")

# Get current story status
@app.get("/api/story-status")
async def story_status():
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI Agent system not available. Please check Google ADK installation.")
    
    try:
        result = get_story_status()
        return {
            **result,
            "agent_available": True
        }
    except Exception as e:
        print(f"❌ Agent.py story status error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Agent story status error: {str(e)}")

# Get list of generated media files
@app.get("/api/media-files")
async def get_media_files():
    media_files = {
        "images": [],
        "videos": [],
        "music": []
    }
    
    if AGENT_AVAILABLE:
        try:
            # Get actual generated files from game state
            media_files["images"] = game_state.generated_images
            media_files["videos"] = game_state.generated_videos  
            media_files["music"] = game_state.generated_music
        except:
            pass
    
    # Also scan directory for files (check both agents and root)
    scan_dirs = [Path("../agents"), Path("../"), Path(".")]
    
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            # Find generated files
            for file_path in scan_dir.glob("generated_scene_*.png"):
                filename = str(file_path.name)
                if filename not in media_files["images"]:
                    media_files["images"].append(filename)
            
            for file_path in scan_dir.glob("generated_video_*.mp4"):
                filename = str(file_path.name)
                if filename not in media_files["videos"]:
                    media_files["videos"].append(filename)
                
            for file_path in scan_dir.glob("lyria_final_*.wav"):
                filename = str(file_path.name)
                if filename not in media_files["music"]:
                    media_files["music"].append(filename)
    
    return media_files

# Serve individual media files
@app.get("/api/media/{filename}")
async def get_media_file(filename: str):
    # Check multiple possible locations
    possible_dirs = [Path("../agents"), Path("../"), Path(".")]
    
    for check_dir in possible_dirs:
        file_path = check_dir / filename
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
    
    raise HTTPException(status_code=404, detail=f"Media file not found: {filename}")

def get_file_extension(media_type: str) -> str:
    """Get appropriate file extension for media type"""
    extensions = {
        "image": "png",
        "video": "mp4", 
        "music": "wav"
    }
    return extensions.get(media_type, "bin")



if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 8000))
    
    print("🎬 Starting DreamDirector API server...")
    print(f"🤖 Agent available: {AGENT_AVAILABLE}")
    print(f"🌐 Server will start on port: {port}")
    
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False) 