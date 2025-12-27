"""
Health check endpoint router.

Provides system health status endpoint.
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns system health status and current timestamp.
    
    Returns:
        dict: Health status with timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

