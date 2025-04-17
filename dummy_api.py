from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dummy_endpoint import router

app = FastAPI(
    title="AI Animator API (Dummy)",
    description="Dummy API for AI video and audio generation for development and testing",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("dummy_api:app", host="0.0.0.0", port=8001, reload=True) 