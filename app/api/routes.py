from fastapi import APIRouter

# Create router
router = APIRouter()

# Import and include health check routes
from .health import router as health_router
router.include_router(health_router, tags=["health"])

@router.get('/ping')
async def ping_pong():
    """A simple ping endpoint."""
    return {"message": "pong!"}

# Add additional API routes here using the @router decorator
