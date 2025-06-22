"""
Middleware for the Sleep Science Explainer Bot.
"""

import time
from typing import Dict, Any
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
import structlog

from backend.core.config import settings


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests."""
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = structlog.get_logger(__name__)
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Log request details and timing."""
        start_time = time.time()
        
        # Log request
        self.logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        self.logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration=duration,
        )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests."""
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = structlog.get_logger(__name__)
        self.request_counts: Dict[str, Dict[str, Any]] = {}
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Apply rate limiting to requests."""
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries
        self._cleanup_old_entries(current_time)
        
        # Check rate limit
        if not self._check_rate_limit(client_ip, current_time):
            self.logger.warning(
                "Rate limit exceeded",
                client_ip=client_ip,
                limit=settings.rate_limit_requests,
                window=settings.rate_limit_window,
            )
            return Response(
                content={"detail": "Rate limit exceeded"},
                status_code=429,
                media_type="application/json"
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
        response.headers["X-RateLimit-Window"] = str(settings.rate_limit_window)
        
        return response
    
    def _check_rate_limit(self, client_ip: str, current_time: float) -> bool:
        """Check if client has exceeded rate limit."""
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {
                "count": 0,
                "window_start": current_time
            }
        
        client_data = self.request_counts[client_ip]
        
        # Reset window if expired
        if current_time - client_data["window_start"] > settings.rate_limit_window:
            client_data["count"] = 0
            client_data["window_start"] = current_time
        
        # Check limit
        if client_data["count"] >= settings.rate_limit_requests:
            return False
        
        # Increment count
        client_data["count"] += 1
        return True
    
    def _cleanup_old_entries(self, current_time: float) -> None:
        """Remove old rate limit entries."""
        expired_ips = []
        for client_ip, client_data in self.request_counts.items():
            if current_time - client_data["window_start"] > settings.rate_limit_window:
                expired_ips.append(client_ip)
        
        for client_ip in expired_ips:
            del self.request_counts[client_ip] 