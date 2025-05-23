from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring and auto-scaling.
    
    This endpoint is used by fly.io to determine if the application is healthy
    and to make decisions about auto-scaling and machine shutdown.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("APP_ENV", "development"),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }