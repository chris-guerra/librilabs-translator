"""
FastAPI application entry point.

Main application setup with CORS, routers, and error handling.
"""
import uuid
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import health

app = FastAPI(
    title="Librilabs Translator API",
    version="1.0.0",
    description="Document translation and review workflow API",
)

# CORS configuration
# Production: Set ALLOWED_ORIGINS environment variable with comma-separated origins
# Example: ALLOWED_ORIGINS=https://app.librilabs.com,https://www.librilabs.com
# Never use allow_origins=["*"] in production for security reasons
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Supports production via environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTPException with structured error response.
    
    Preserves HTTP status code from the exception.
    """
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail if isinstance(exc.detail, str) else "An error occurred",
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
            }
        }
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle Starlette HTTPException (including FastAPI's default 404).
    
    Ensures all HTTP exceptions, including 404 Not Found, use structured error format.
    """
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail if isinstance(exc.detail, str) else "An error occurred",
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
            }
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.
    
    Returns structured error response with 500 status code.
    Ensures no sensitive information (API keys, stack traces) is exposed.
    """
    request_id = str(uuid.uuid4())
    # Log the exception for debugging (without exposing to client)
    # In production, this would go to a logging service
    print(f"Unhandled exception [request_id={request_id}]: {type(exc).__name__}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
            }
        }
    )


# Unversioned routes
app.include_router(health.router)

