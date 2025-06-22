"""
Main application entry point for the Sleep Science Explainer Bot.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.core.config import settings
from backend.core.logging import setup_logging
from backend.database.connection import db_manager

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Sleep Science Explainer Bot...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Initialize database
    try:
        db_manager.create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        # Continue without database for demo purposes
    
    yield
    
    # Shutdown
    logger.info("Shutting down Sleep Science Explainer Bot...")
    db_manager.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="A conversational AI for explaining sleep science research",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    
    # Import routes after middleware setup
    try:
        from backend.api.routes import chat, papers, analytics, health
        from backend.core.middleware import RequestLoggingMiddleware, RateLimitMiddleware
        
        app.add_middleware(RequestLoggingMiddleware)
        app.add_middleware(RateLimitMiddleware)
        
        # Include routers
        app.include_router(health.router, prefix=settings.API_PREFIX, tags=["health"])
        app.include_router(chat.router, prefix=settings.API_PREFIX, tags=["chat"])
        app.include_router(papers.router, prefix=settings.API_PREFIX, tags=["papers"])
        app.include_router(analytics.router, prefix=settings.API_PREFIX, tags=["analytics"])
        
    except ImportError as e:
        logger.warning(f"Some routes could not be loaded: {e}")
        # Add basic health check
        @app.get("/health")
        async def health_check():
            return {"status": "healthy", "message": "Basic health check"}
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 