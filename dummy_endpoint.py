from fastapi import APIRouter, Request, Depends, File, Form, UploadFile, WebSocket, BackgroundTasks, Query, Body
from fastapi.responses import JSONResponse, RedirectResponse, Response
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import base64
import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import time
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

# Router setup
router = APIRouter()

# Mock data for all endpoints
class MockDatabase:
    def __init__(self):
        self.users = {
            "user@example.com": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "credits_remaining": 100,
                "subscription_tier": "premium",
                "subscription_start_date": datetime.now(),
                "subscription_end_date": datetime.now() + timedelta(days=30)
            }
        }
        self.creations = {}
        self.libraries = {}
        self.preferences = {}
        self.watermarks = {}
        self.generations = {}
        
    def get_user_by_email(self, email):
        return self.users.get(email)
    
    def update_user(self, email, data):
        if email in self.users:
            self.users[email].update(data)
            return True
        return False

# Initialize mock database
mock_db = MockDatabase()

# Mock DB dependency
def get_mock_db():
    return mock_db

# Helper functions
def get_mock_token_from_request(request):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ")[1] if " " in auth_header else ""
    return token, None

def get_mock_current_user(request):
    return mock_db.get_user_by_email("user@example.com")

def generate_mock_id():
    return str(uuid.uuid4())

# Dummy JWT token for testing
DUMMY_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwidXNlcklkIjoiMTIzZTQ1NjctZTg5Yi0xMmQzLWE0NTYtNDI2NjE0MTc0MDAwIiwiZXhwIjoxNzE2OTc2MTI3fQ.Qj2wjBxZGRxTwWcDfCYpjEIEdiQZZhsOtUUG5qf0YQA"

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
    async def send_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)

manager = ConnectionManager()

# Auth endpoints
class SignupRequest(BaseModel):
    email: str
    password: str
    confirm_password: str

@router.post("/signup")
async def signup(request: SignupRequest):
    return JSONResponse({
        "status": "success",
        "message": "User created successfully",
        "user_id": "123e4567-e89b-12d3-a456-426614174000"
    })

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    return JSONResponse({
        "status": "success",
        "token": DUMMY_TOKEN,
        "user": {
            "email": request.email,
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "credits_remaining": 100,
            "subscription_tier": "premium"
        }
    })

@router.post("/logout")
async def logout(request: Request):
    return JSONResponse({
        "status": "success",
        "message": "Logged out successfully"
    })

@router.get("/verify-token")
async def verify_token(request: Request):
    return JSONResponse({
        "valid": True,
        "user": {
            "email": "user@example.com",
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "credits_remaining": 100,
            "subscription_tier": "premium"
        }
    })

class ResetPasswordRequest(BaseModel):
    email: str

@router.post("/forgot-password")
async def forgot_password(request: ResetPasswordRequest):
    return JSONResponse({
        "status": "success",
        "message": "Password reset email sent"
    })

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str

@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest):
    return JSONResponse({
        "status": "success",
        "message": "OTP verified successfully",
        "reset_token": "reset_token_12345"
    })

class ResetPasswordWithTokenRequest(BaseModel):
    email: str
    reset_token: str
    new_password: str
    confirm_password: str

@router.post("/reset-password")
async def reset_password(request: ResetPasswordWithTokenRequest):
    return JSONResponse({
        "status": "success",
        "message": "Password reset successfully"
    })

@router.get("/auth/google")
async def google_auth():
    return RedirectResponse(url="/?token=" + DUMMY_TOKEN)

# Payment endpoints
@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    mock_request_data = await request.json()
    return JSONResponse({
        "sessionId": "cs_test_" + generate_mock_id(),
        "credits": 1000
    })

@router.post("/webhook")
async def stripe_webhook(request: Request):
    return JSONResponse({
        "status": "success"
    })

@router.get("/get-prices")
async def get_prices():
    return JSONResponse({
        "basic plan": {
            "usd": {
                "month": {
                    "id": "price_1OvnMnSHuGJaxdvpOYxeKBwW",
                    "amount": 9.99,
                    "interval": "month",
                    "currency": "usd"
                },
                "year": {
                    "id": "price_1OvnMnSHuGJaxdvpOsLw6wA6",
                    "amount": 99.99,
                    "interval": "year",
                    "currency": "usd"
                }
            }
        },
        "pro plan": {
            "usd": {
                "month": {
                    "id": "price_1OvnNaSHuGJaxdvpDXPqMV5I",
                    "amount": 19.99,
                    "interval": "month",
                    "currency": "usd"
                },
                "year": {
                    "id": "price_1OvnNaSHuGJaxdvpBCrYdOK8",
                    "amount": 199.99,
                    "interval": "year", 
                    "currency": "usd"
                }
            }
        },
        "enterprise": {
            "usd": {
                "month": {
                    "id": "price_1OvnOGSHuGJaxdvpjkHHtJLp",
                    "amount": 49.99,
                    "interval": "month",
                    "currency": "usd"
                },
                "year": {
                    "id": "price_1OvnOGSHuGJaxdvpknIldRGv",
                    "amount": 499.99,
                    "interval": "year",
                    "currency": "usd"
                }
            }
        }
    })

@router.get("/config")
async def get_stripe_config():
    return JSONResponse({
        "publishableKey": "pk_test_dummy_key"
    })

# Text to Video endpoints
class TextPromptRequest(BaseModel):
    text: str
    video_length: int

class TextPromptResponse(BaseModel):
    prompts: List[str]
    s3_location: str
    generation_id: str

@router.post("/text-segmentor", response_model=TextPromptResponse)
async def generate_video_prompts(request: Request, text_prompt_request: TextPromptRequest):
    generation_id = generate_mock_id()
    return JSONResponse({
        "prompts": [
            "A beautiful sunrise over mountains with golden light",
            "Birds flying across the clear blue sky",
            "A flowing river through a lush green forest"
        ],
        "s3_location": f"user@example.com/text_to_video/{generation_id}/prompts.json",
        "generation_id": generation_id
    })

@router.websocket("/text-to-video/ws/{user_email}")
async def text_to_video_websocket(websocket: WebSocket, user_email: str):
    await websocket.accept()
    
    try:
        # Send mock status updates
        await websocket.send_json({"status": "initializing", "message": "Starting text to video generation"})
        await asyncio.sleep(1)
        
        await websocket.send_json({"status": "processing", "message": "Processing prompts", "completed": 0, "total": 3})
        await asyncio.sleep(1)
        
        await websocket.send_json({"status": "processing", "message": "Processing prompts", "completed": 1, "total": 3})
        await asyncio.sleep(1)
        
        await websocket.send_json({"status": "processing", "message": "Processing prompts", "completed": 2, "total": 3})
        await asyncio.sleep(1)
        
        await websocket.send_json({"status": "processing", "message": "Processing prompts", "completed": 3, "total": 3})
        await asyncio.sleep(1)
        
        # Final message with video URL
        video_id = generate_mock_id()
        await websocket.send_json({
            "status": "completed",
            "message": "Video generation completed",
            "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/text_to_video/{video_id}/output.mp4"
        })
    except WebSocketDisconnect:
        print(f"Client disconnected: {user_email}")

# Image to Video endpoints
@router.post("/process_images")
async def process_images_endpoint(
    request: Request,
    image1: Optional[UploadFile] = File(None),
    image2: Optional[UploadFile] = File(None),
    image3: Optional[UploadFile] = File(None),
    image4: Optional[UploadFile] = File(None),
    image5: Optional[UploadFile] = File(None)
):
    images = [img for img in [image1, image2, image3, image4, image5] if img is not None]
    num_images = len(images)
    
    return JSONResponse({
        "status": "success",
        "images": [f"image{i+1}.jpg" for i in range(num_images)],
        "message": f"Successfully processed {num_images} images",
        "combined_image_path": f"user@example.com/processed_images/{generate_mock_id()}/combined.png"
    })

@router.post("/upload_custom_background")
async def upload_custom_background(
    request: Request,
    background_image: UploadFile = File(...)
):
    return JSONResponse({
        "status": "success", 
        "path": f"user@example.com/backgrounds/{generate_mock_id()}/background.jpg"
    })

class BackgroundPromptRequest(BaseModel):
    prompt: str

@router.post("/generate_ai_background")
async def generate_ai_background(
    request: Request,
    background_request: BackgroundPromptRequest
):
    background_id = generate_mock_id()
    return JSONResponse({
        "status": "success",
        "background_path": f"user@example.com/backgrounds/{background_id}/generated.jpg",
        "background_url": f"https://vidgencraft-media.s3.amazonaws.com/user@example.com/backgrounds/{background_id}/generated.jpg"
    })

@router.post("/colorize-image")
async def colorize_image(
    request: Request,
    image: UploadFile = File(...)
):
    colorized_id = generate_mock_id()
    return JSONResponse({
        "status": "success",
        "colorized_image_path": f"user@example.com/colorized/{colorized_id}/colorized.jpg",
        "colorized_image_url": f"https://vidgencraft-media.s3.amazonaws.com/user@example.com/colorized/{colorized_id}/colorized.jpg"
    })

class BackgroundMergeRequest(BaseModel):
    background: dict
    emotion: str
    combinedImagePath: Optional[str] = None
    numberOfImages: Optional[int] = 2

@router.post("/merge_background")
async def merge_background(
    request: Request,
    merge_request: BackgroundMergeRequest
):
    merged_id = generate_mock_id()
    return JSONResponse({
        "status": "success",
        "merged_image_path": f"user@example.com/merged/{merged_id}/merged.jpg",
        "merged_image_url": f"https://vidgencraft-media.s3.amazonaws.com/user@example.com/merged/{merged_id}/merged.jpg"
    })

class PromptRequest(BaseModel):
    background: str
    emotion: str
    mergedImagePath: str
    numberOfImages: Optional[int] = None

@router.post("/generate_prompt")
async def generate_prompt_endpoint(
    request: Request,
    prompt_request: PromptRequest
):
    return JSONResponse({
        "status": "success",
        "prompt": f"A {prompt_request.emotion} scene showing {prompt_request.background}"
    })

class PreferencesData(BaseModel):
    backgroundPrompt: str
    expressionPrompt: str
    selectedBackground: str
    mergedImagePath: Optional[str] = None
    selectedModel: str
    numberOfImages: Optional[int] = None

@router.post("/save_preferences")
async def save_preferences(
    request: Request,
    preferences: PreferencesData
):
    preferences_id = generate_mock_id()
    return JSONResponse({
        "status": "success",
        "message": "Preferences saved successfully",
        "preferences_id": preferences_id
    })

@router.get("/api/test-path/{user_id}/{image_name}")
async def test_image_path(user_id: str, image_name: str):
    return JSONResponse({
        "path": f"{user_id}/{image_name}",
        "exists": True
    })

@router.websocket("/ws/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str):
    await websocket.accept()
    
    try:
        # Send mock status updates
        await websocket.send_json({"status": "initializing", "message": "Starting image to video generation"})
        await asyncio.sleep(1)
        
        await websocket.send_json({
            "status": "processing", 
            "message": "Processing image", 
            "progress": 25
        })
        await asyncio.sleep(1)
        
        await websocket.send_json({
            "status": "processing", 
            "message": "Generating video", 
            "progress": 50
        })
        await asyncio.sleep(1)
        
        await websocket.send_json({
            "status": "processing", 
            "message": "Finalizing", 
            "progress": 75
        })
        await asyncio.sleep(1)
        
        # Final message with video URL
        video_id = generate_mock_id()
        await websocket.send_json({
            "status": "completed",
            "message": "Video generation completed",
            "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/image_to_video/{video_id}/output.mp4"
        })
    except WebSocketDisconnect:
        print(f"Client disconnected: {user_email}")

@router.post("/generate_video_thread")
async def generate_video_thread(request: Request, data: dict):
    return JSONResponse({
        "status": "processing",
        "message": "Video generation started in background",
        "video_id": generate_mock_id()
    })

@router.post("/api/video/generate")
async def generate_video(
    request: Request,
    background_tasks: BackgroundTasks
):
    video_id = generate_mock_id()
    return JSONResponse({
        "status": "processing",
        "message": "Video generation started",
        "video_id": video_id
    })

# MM Audio endpoints
class AudioGenerationRequest(BaseModel):
    video_url: Optional[str] = None
    prompt: Optional[str] = ""
    negative_prompt: Optional[str] = "human voice, speech, talking, vocals, singing"
    seed: Optional[int] = None
    num_steps: Optional[int] = 25
    duration: Optional[float] = 8.0
    cfg_strength: Optional[float] = 4.5
    mask_away_clip: Optional[bool] = False
    creation_id: Optional[str] = None

class VideoUploadResponse(BaseModel):
    status: str
    video_url: str
    s3_key: str
    creation_id: str
    duration: float

@router.post("/api/upload_video", response_model=VideoUploadResponse)
async def upload_video(
    request: Request,
    video: UploadFile = File(...),
    watermark: bool = Form(False)
):
    creation_id = generate_mock_id()
    return JSONResponse({
        "status": "success",
        "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{creation_id}/input.mp4",
        "s3_key": f"user@example.com/sound_effects/{creation_id}/input.mp4",
        "creation_id": creation_id,
        "duration": 8.0
    })

@router.post("/api/generate_audio")
async def generate_audio(
    request: Request,
    generation_request: AudioGenerationRequest,
    background_tasks: BackgroundTasks
):
    creation_id = generation_request.creation_id or generate_mock_id()
    return JSONResponse({
        "status": "processing",
        "message": "Audio generation started",
        "creation_id": creation_id
    })

@router.get("/api/audio_status/{creation_id}")
async def get_audio_status(
    request: Request,
    creation_id: str
):
    return JSONResponse({
        "status": "completed",
        "creation_id": creation_id,
        "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{creation_id}/output.mp4"
    })

@router.websocket("/api/ws/generation/{user_email}")
async def websocket_generation_endpoint(websocket: WebSocket, user_email: str):
    await websocket.accept()
    
    try:
        creation_id = generate_mock_id()
        # Send mock status updates
        await websocket.send_json({
            "status": "initializing", 
            "message": "Starting audio generation",
            "creation_id": creation_id
        })
        await asyncio.sleep(1)
        
        await websocket.send_json({
            "status": "processing", 
            "message": "Generating audio for video", 
            "progress": 30,
            "creation_id": creation_id
        })
        await asyncio.sleep(1)
        
        await websocket.send_json({
            "status": "processing", 
            "message": "Applying audio to video", 
            "progress": 70,
            "creation_id": creation_id
        })
        await asyncio.sleep(1)
        
        # Final message with video URL
        await websocket.send_json({
            "status": "completed",
            "message": "Audio generation completed",
            "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{creation_id}/output.mp4",
            "creation_id": creation_id
        })
    except WebSocketDisconnect:
        print(f"Client disconnected: {user_email}")

@router.get("/api/extract_audio/{creation_id}")
async def extract_audio(
    request: Request,
    creation_id: str
):
    return JSONResponse({
        "status": "success",
        "audio_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{creation_id}/audio.mp3"
    })

@router.get("/api/status/{creation_id}")
async def get_audio_status_by_id(creation_id: str):
    return JSONResponse({
        "status": "completed",
        "creation_id": creation_id,
        "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{creation_id}/output.mp4"
    })

@router.get("/api/get_output_video/{creation_id}")
async def get_output_video(
    request: Request,
    creation_id: str
):
    return JSONResponse({
        "status": "success",
        "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{creation_id}/output.mp4"
    })

@router.post("/api/get_s3_file")
async def get_s3_file(
    request: Request,
    body: dict = Body(...)
):
    return JSONResponse({
        "status": "success",
        "url": f"https://vidgencraft-videos.s3.amazonaws.com/{body.get('key', 'file.mp4')}"
    })

# Library endpoints
@router.get("/library/{user_id}")
async def get_user_library(request: Request, user_id: str):
    return JSONResponse({
        "creations": [
            {
                "id": generate_mock_id(),
                "type": "text_to_video",
                "created_at": datetime.now().isoformat(),
                "url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/text_to_video/{generate_mock_id()}/output.mp4",
                "thumbnail": f"https://vidgencraft-media.s3.amazonaws.com/user@example.com/text_to_video/{generate_mock_id()}/thumbnail.jpg",
                "metadata": {
                    "prompt": "A beautiful sunset over mountains"
                }
            },
            {
                "id": generate_mock_id(),
                "type": "image_to_video",
                "created_at": datetime.now().isoformat(),
                "url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/image_to_video/{generate_mock_id()}/output.mp4",
                "thumbnail": f"https://vidgencraft-media.s3.amazonaws.com/user@example.com/image_to_video/{generate_mock_id()}/thumbnail.jpg",
                "metadata": {
                    "prompt": "Beach scene with waves"
                }
            },
            {
                "id": generate_mock_id(),
                "type": "sound_effects",
                "created_at": datetime.now().isoformat(),
                "url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/{generate_mock_id()}/output.mp4",
                "thumbnail": f"https://vidgencraft-media.s3.amazonaws.com/user@example.com/sound_effects/{generate_mock_id()}/thumbnail.jpg",
                "metadata": {
                    "prompt": "Forest sounds with birds"
                }
            }
        ]
    })

@router.delete("/library/{creation_id}")
async def delete_creation(request: Request, creation_id: str):
    return JSONResponse({
        "status": "success",
        "message": f"Creation {creation_id} deleted successfully"
    })

# Watermark endpoints
@router.post("/watermark")
async def add_watermark(request: Request):
    data = await request.json()
    return JSONResponse({
        "status": "success",
        "message": "Watermark added successfully",
        "video_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/watermarked/{generate_mock_id()}/output.mp4"
    })

# Movie maker endpoints
class ClipRequest(BaseModel):
    clips: List[dict]
    output_name: str

@router.post("/movie/clips")
async def combine_clips(request: Request, clip_request: ClipRequest):
    movie_id = generate_mock_id()
    return JSONResponse({
        "status": "success",
        "message": "Clips combined successfully",
        "movie_url": f"https://vidgencraft-videos.s3.amazonaws.com/user@example.com/movies/{movie_id}/{clip_request.output_name}.mp4"
    })

# Utils endpoints
@router.get("/utils/health")
async def health_check():
    return JSONResponse({
        "status": "ok",
        "version": "2.0.0"
    })

# Character score endpoints
@router.get("/character/score/{user_id}")
async def get_character_score(user_id: str):
    return JSONResponse({
        "character_score": 75,
        "usage_stats": {
            "videos_generated": 10,
            "total_duration": 120,
            "favorite_type": "text_to_video"
        }
    })

# Referral endpoints
@router.post("/referral/generate")
async def generate_referral_code(request: Request):
    return JSONResponse({
        "status": "success",
        "referral_code": "USER" + generate_mock_id()[:8].upper(),
        "referral_url": "https://vidgencraft.com/signup?ref=USER12345678"
    })

@router.post("/referral/verify")
async def verify_referral_code(request: Request):
    data = await request.json()
    return JSONResponse({
        "status": "success",
        "valid": True,
        "referrer": "referring_user@example.com",
        "bonus_credits": 10
    })

# Main API endpoints
@router.get("/api/health")
async def api_health_check():
    return JSONResponse({
        "status": "ok"
    })

@router.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@router.get("/api")
async def redirect_to_api_docs():
    return RedirectResponse(url="/docs")

# Import asyncio for websocket simulations
import asyncio 