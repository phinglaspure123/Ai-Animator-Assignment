# Dummy Endpoints Documentation

This document provides information about the dummy endpoints available in the `dummy_endpoint.py` file. These endpoints mimic the behavior of real endpoints but return hardcoded responses, making them suitable for development and testing.

## Authentication Endpoints

### 1. User Signup
- **Endpoint**: `/signup` (POST)
- **Input**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password",
    "confirm_password": "secure_password"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "User created successfully",
    "user_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```

### 2. User Login
- **Endpoint**: `/login` (POST)
- **Input**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "token": "JWT_TOKEN_HERE",
    "user": {
      "email": "user@example.com",
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "credits_remaining": 100,
      "subscription_tier": "premium"
    }
  }
  ```

### 3. User Logout
- **Endpoint**: `/logout` (POST)
- **Input**: No body required, uses session/token
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Logged out successfully"
  }
  ```

### 4. Verify Token
- **Endpoint**: `/verify-token` (GET)
- **Input**: No body required, token in header or cookies
- **Output**:
  ```json
  {
    "valid": true,
    "user": {
      "email": "user@example.com",
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "credits_remaining": 100,
      "subscription_tier": "premium"
    }
  }
  ```

### 5. Forgot Password
- **Endpoint**: `/forgot-password` (POST)
- **Input**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Password reset email sent"
  }
  ```

### 6. Verify OTP
- **Endpoint**: `/verify-otp` (POST)
- **Input**:
  ```json
  {
    "email": "user@example.com",
    "otp": "123456"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "OTP verified successfully",
    "reset_token": "reset_token_12345"
  }
  ```

### 7. Reset Password
- **Endpoint**: `/reset-password` (POST)
- **Input**:
  ```json
  {
    "email": "user@example.com",
    "reset_token": "reset_token_12345",
    "new_password": "new_secure_password",
    "confirm_password": "new_secure_password"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Password reset successfully"
  }
  ```

### 8. Google Auth
- **Endpoint**: `/auth/google` (GET)
- **Input**: OAuth flow, no direct input
- **Output**: Redirects to `/?token=JWT_TOKEN_HERE`

## Payment Endpoints

### 1. Create Checkout Session
- **Endpoint**: `/create-checkout-session` (POST)
- **Input**:
  ```json
  {
    "price_id": "price_1OvnMnSHuGJaxdvpOYxeKBwW"
  }
  ```
- **Output**:
  ```json
  {
    "sessionId": "cs_test_[UUID]",
    "credits": 1000
  }
  ```

### 2. Stripe Webhook
- **Endpoint**: `/webhook` (POST)
- **Input**: Stripe webhook event data
- **Output**:
  ```json
  {
    "status": "success"
  }
  ```

### 3. Get Prices
- **Endpoint**: `/get-prices` (GET)
- **Input**: No input required
- **Output**:
  ```json
  {
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
    "pro plan": { ... },
    "enterprise": { ... }
  }
  ```

### 4. Get Stripe Config
- **Endpoint**: `/config` (GET)
- **Input**: No input required
- **Output**:
  ```json
  {
    "publishableKey": "pk_test_dummy_key"
  }
  ```

## Text to Video Endpoints

### 1. Generate Video Prompts
- **Endpoint**: `/text-segmentor` (POST)
- **Input**:
  ```json
  {
    "text": "A beautiful sunrise over mountains with golden light. Birds flying across the clear blue sky. A flowing river through a lush green forest.",
    "video_length": 15
  }
  ```
- **Output**:
  ```json
  {
    "prompts": [
      "A beautiful sunrise over mountains with golden light",
      "Birds flying across the clear blue sky",
      "A flowing river through a lush green forest"
    ],
    "s3_location": "user@example.com/text_to_video/[UUID]/prompts.json",
    "generation_id": "[UUID]"
  }
  ```

### 2. Text to Video WebSocket
- **Endpoint**: `/text-to-video/ws/{user_email}` (WebSocket)
- **Input**: WebSocket connection
- **Output**: Series of WebSocket messages with status updates and finally:
  ```json
  {
    "status": "completed",
    "message": "Video generation completed",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/text_to_video/[UUID]/output.mp4"
  }
  ```

## Image to Video Endpoints

### 1. Process Images
- **Endpoint**: `/process_images` (POST)
- **Input**: Form data with up to 5 image files
- **Output**:
  ```json
  {
    "status": "success",
    "images": ["image1.jpg", "image2.jpg", ...],
    "message": "Successfully processed N images",
    "combined_image_path": "user@example.com/processed_images/[UUID]/combined.png"
  }
  ```

### 2. Upload Custom Background
- **Endpoint**: `/upload_custom_background` (POST)
- **Input**: Form data with background_image file
- **Output**:
  ```json
  {
    "status": "success",
    "path": "user@example.com/backgrounds/[UUID]/background.jpg"
  }
  ```

### 3. Generate AI Background
- **Endpoint**: `/generate_ai_background` (POST)
- **Input**:
  ```json
  {
    "prompt": "Sunny beach with palm trees"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "background_path": "user@example.com/backgrounds/[UUID]/generated.jpg",
    "background_url": "https://vidgencraft-media.s3.amazonaws.com/user@example.com/backgrounds/[UUID]/generated.jpg"
  }
  ```

### 4. Colorize Image
- **Endpoint**: `/colorize-image` (POST)
- **Input**: Form data with image file
- **Output**:
  ```json
  {
    "status": "success",
    "colorized_image_path": "user@example.com/colorized/[UUID]/colorized.jpg",
    "colorized_image_url": "https://vidgencraft-media.s3.amazonaws.com/user@example.com/colorized/[UUID]/colorized.jpg"
  }
  ```

### 5. Merge Background
- **Endpoint**: `/merge_background` (POST)
- **Input**:
  ```json
  {
    "background": {"path": "path/to/background.jpg", "url": "https://example.com/background.jpg"},
    "emotion": "happy",
    "combinedImagePath": "path/to/combined/image.jpg",
    "numberOfImages": 2
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "merged_image_path": "user@example.com/merged/[UUID]/merged.jpg",
    "merged_image_url": "https://vidgencraft-media.s3.amazonaws.com/user@example.com/merged/[UUID]/merged.jpg"
  }
  ```

### 6. Generate Prompt
- **Endpoint**: `/generate_prompt` (POST)
- **Input**:
  ```json
  {
    "background": "beach",
    "emotion": "happy",
    "mergedImagePath": "path/to/merged/image.jpg",
    "numberOfImages": 2
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "prompt": "A happy scene showing beach"
  }
  ```

### 7. Save Preferences
- **Endpoint**: `/save_preferences` (POST)
- **Input**:
  ```json
  {
    "backgroundPrompt": "beach sunset",
    "expressionPrompt": "peaceful scene",
    "selectedBackground": "path/to/background.jpg",
    "mergedImagePath": "path/to/merged/image.jpg",
    "selectedModel": "kling",
    "numberOfImages": 2
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Preferences saved successfully",
    "preferences_id": "[UUID]"
  }
  ```

### 8. Test Image Path
- **Endpoint**: `/api/test-path/{user_id}/{image_name}` (GET)
- **Input**: Path parameters user_id and image_name
- **Output**:
  ```json
  {
    "path": "user_id/image_name",
    "exists": true
  }
  ```

### 9. Image to Video WebSocket
- **Endpoint**: `/ws/{user_email}` (WebSocket)
- **Input**: WebSocket connection
- **Output**: Series of WebSocket messages with status updates and finally:
  ```json
  {
    "status": "completed",
    "message": "Video generation completed",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/image_to_video/[UUID]/output.mp4"
  }
  ```

### 10. Generate Video Thread
- **Endpoint**: `/generate_video_thread` (POST)
- **Input**: JSON object with video generation parameters
- **Output**:
  ```json
  {
    "status": "processing",
    "message": "Video generation started in background",
    "video_id": "[UUID]"
  }
  ```

### 11. Generate Video
- **Endpoint**: `/api/video/generate` (POST)
- **Input**: JSON object with video generation parameters
- **Output**:
  ```json
  {
    "status": "processing",
    "message": "Video generation started",
    "video_id": "[UUID]"
  }
  ```

## MM Audio Endpoints

### 1. Upload Video
- **Endpoint**: `/api/upload_video` (POST)
- **Input**: Form data with video file and optional watermark flag
- **Output**:
  ```json
  {
    "status": "success",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[UUID]/input.mp4",
    "s3_key": "user@example.com/sound_effects/[UUID]/input.mp4",
    "creation_id": "[UUID]",
    "duration": 8.0
  }
  ```

### 2. Generate Audio
- **Endpoint**: `/api/generate_audio` (POST)
- **Input**:
  ```json
  {
    "video_url": "https://example.com/video.mp4",
    "prompt": "Indian holy music",
    "negative_prompt": "human voice, speech, talking, vocals, singing",
    "num_steps": 25,
    "duration": 8.0,
    "cfg_strength": 4.5,
    "creation_id": null
  }
  ```
- **Output**:
  ```json
  {
    "status": "processing",
    "message": "Audio generation started",
    "creation_id": "[UUID]"
  }
  ```

### 3. Get Audio Status
- **Endpoint**: `/api/audio_status/{creation_id}` (GET)
- **Input**: Path parameter creation_id
- **Output**:
  ```json
  {
    "status": "completed",
    "creation_id": "[creation_id]",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[creation_id]/output.mp4"
  }
  ```

### 4. Audio Generation WebSocket
- **Endpoint**: `/api/ws/generation/{user_email}` (WebSocket)
- **Input**: WebSocket connection
- **Output**: Series of WebSocket messages with status updates and finally:
  ```json
  {
    "status": "completed",
    "message": "Audio generation completed",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[creation_id]/output.mp4",
    "creation_id": "[creation_id]"
  }
  ```

### 5. Extract Audio
- **Endpoint**: `/api/extract_audio/{creation_id}` (GET)
- **Input**: Path parameter creation_id
- **Output**:
  ```json
  {
    "status": "success",
    "audio_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[creation_id]/audio.mp3"
  }
  ```

### 6. Get Audio Status by ID
- **Endpoint**: `/api/status/{creation_id}` (GET)
- **Input**: Path parameter creation_id
- **Output**:
  ```json
  {
    "status": "completed",
    "creation_id": "[creation_id]",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[creation_id]/output.mp4"
  }
  ```

### 7. Get Output Video
- **Endpoint**: `/api/get_output_video/{creation_id}` (GET)
- **Input**: Path parameter creation_id
- **Output**:
  ```json
  {
    "status": "success",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[creation_id]/output.mp4"
  }
  ```

### 8. Get S3 File
- **Endpoint**: `/api/get_s3_file` (POST)
- **Input**:
  ```json
  {
    "key": "user@example.com/sound_effects/[creation_id]/output.mp4"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/sound_effects/[creation_id]/output.mp4"
  }
  ```

## Library Endpoints

### 1. Get User Library
- **Endpoint**: `/library/{user_id}` (GET)
- **Input**: Path parameter user_id
- **Output**:
  ```json
  {
    "creations": [
      {
        "id": "[UUID]",
        "type": "text_to_video",
        "created_at": "2023-07-01T12:00:00.000Z",
        "url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/text_to_video/[UUID]/output.mp4",
        "thumbnail": "https://vidgencraft-media.s3.amazonaws.com/user@example.com/text_to_video/[UUID]/thumbnail.jpg",
        "metadata": {
          "prompt": "A beautiful sunset over mountains"
        }
      },
      ...additional creation objects
    ]
  }
  ```

### 2. Delete Creation
- **Endpoint**: `/library/{creation_id}` (DELETE)
- **Input**: Path parameter creation_id
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Creation [creation_id] deleted successfully"
  }
  ```

## Watermark Endpoints

### 1. Add Watermark
- **Endpoint**: `/watermark` (POST)
- **Input**:
  ```json
  {
    "video_url": "https://example.com/video.mp4",
    "watermark_text": "Vidgencraft",
    "watermark_position": "bottom-right"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Watermark added successfully",
    "video_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/watermarked/[UUID]/output.mp4"
  }
  ```

## Movie Maker Endpoints

### 1. Combine Clips
- **Endpoint**: `/movie/clips` (POST)
- **Input**:
  ```json
  {
    "clips": [
      {"url": "https://example.com/clip1.mp4", "start": 0, "end": 5},
      {"url": "https://example.com/clip2.mp4", "start": 0, "end": 10}
    ],
    "output_name": "my_movie"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "message": "Clips combined successfully",
    "movie_url": "https://vidgencraft-videos.s3.amazonaws.com/user@example.com/movies/[UUID]/my_movie.mp4"
  }
  ```

## Utils Endpoints

### 1. Health Check
- **Endpoint**: `/utils/health` (GET)
- **Input**: No input required
- **Output**:
  ```json
  {
    "status": "ok",
    "version": "2.0.0"
  }
  ```

## Character Score Endpoints

### 1. Get Character Score
- **Endpoint**: `/character/score/{user_id}` (GET)
- **Input**: Path parameter user_id
- **Output**:
  ```json
  {
    "character_score": 75,
    "usage_stats": {
      "videos_generated": 10,
      "total_duration": 120,
      "favorite_type": "text_to_video"
    }
  }
  ```

## Referral Endpoints

### 1. Generate Referral Code
- **Endpoint**: `/referral/generate` (POST)
- **Input**: No body required, uses session/token
- **Output**:
  ```json
  {
    "status": "success",
    "referral_code": "USER12345678",
    "referral_url": "https://vidgencraft.com/signup?ref=USER12345678"
  }
  ```

### 2. Verify Referral Code
- **Endpoint**: `/referral/verify` (POST)
- **Input**:
  ```json
  {
    "referral_code": "USER12345678"
  }
  ```
- **Output**:
  ```json
  {
    "status": "success",
    "valid": true,
    "referrer": "referring_user@example.com",
    "bonus_credits": 10
  }
  ```

## Main API Endpoints

### 1. API Health Check
- **Endpoint**: `/api/health` (GET)
- **Input**: No input required
- **Output**:
  ```json
  {
    "status": "ok"
  }
  ```

### 2. Root Redirect
- **Endpoint**: `/` (GET)
- **Input**: No input required
- **Output**: Redirects to `/docs`

### 3. API Redirect
- **Endpoint**: `/api` (GET)
- **Input**: No input required
- **Output**: Redirects to `/docs` 