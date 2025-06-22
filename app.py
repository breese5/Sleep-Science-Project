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

from backend.api.routes import analytics, chat, health, papers, monitoring
from backend.core.config import settings
from backend.core.logging import get_logger, setup_logging
from backend.core.middleware import RequestLoggingMiddleware
from backend.database.connection import db_manager

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Sleep Science Explainer Bot...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {'on' if settings.debug else 'off'}")
    
    # Connect to database
    db_manager.create_tables()
    
    yield
    
    # Close database connections
    db_manager.close()
    logger.info("Sleep Science Explainer Bot shut down.")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        lifespan=lifespan
    )
    
    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    
    # Import routes after middleware setup
    try:
        from backend.core.middleware import RateLimitMiddleware
        
        app.add_middleware(RequestLoggingMiddleware)
        app.add_middleware(RateLimitMiddleware)
        
        # Include routers
        app.include_router(health.router, tags=["Health"])
        app.include_router(chat.router, prefix=settings.api_prefix, tags=["Chat"])
        app.include_router(papers.router, prefix=settings.api_prefix, tags=["Papers"])
        app.include_router(analytics.router, prefix=settings.api_prefix, tags=["Analytics"])
        app.include_router(monitoring.router, prefix=settings.api_prefix, tags=["Monitoring"])
        
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
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 