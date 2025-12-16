from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from datetime import datetime, timedelta
import time
import logging

from ..config.settings import settings

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)  # Store request timestamps by identifier
        self.ip_requests = defaultdict(list)  # Track requests by IP

    async def dispatch(self, request: Request, call_next):
        # Get client IP address
        client_ip = request.client.host

        # Determine rate limit based on endpoint and user
        rate_limit = self._get_rate_limit(request, client_ip)

        # Get current timestamp
        now = time.time()

        # Clean old requests (older than 1 hour)
        self._clean_old_requests(now)

        # Get identifier for this request (IP + endpoint or user ID if authenticated)
        identifier = self._get_identifier(request, client_ip)

        # Get requests for this identifier
        request_times = self.requests[identifier]

        # Count requests in the last hour
        recent_requests = [t for t in request_times if now - t < 3600]  # 1 hour = 3600 seconds

        if len(recent_requests) >= rate_limit:
            logger.warning(f"Rate limit exceeded for {identifier}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )

        # Add current request timestamp
        self.requests[identifier].append(now)

        # Process the request
        response = await call_next(request)

        return response

    def _get_rate_limit(self, request: Request, client_ip: str) -> int:
        """Determine the appropriate rate limit based on the request"""
        # Check if this is an AI-related endpoint
        if "/chat" in request.url.path or "/search" in request.url.path:
            # Check if we have a session identifier
            session_id = request.query_params.get("session_id") or request.cookies.get("session_id")
            if session_id:
                # AI endpoints have a per-session limit
                return settings.rate_limit_ai_requests
            else:
                # If no session, use IP-based limit
                return min(settings.rate_limit_anonymous_requests, settings.rate_limit_ai_requests)
        elif request.method in ["POST", "PUT", "DELETE"]:
            # For authenticated users (if we had auth)
            # For now, use anonymous limit as default
            return settings.rate_limit_anonymous_requests
        else:
            # For GET requests and other endpoints
            return settings.rate_limit_anonymous_requests

    def _get_identifier(self, request: Request, client_ip: str) -> str:
        """Get a unique identifier for rate limiting"""
        # If we had user authentication, we could use user ID
        # For now, use IP address as identifier
        # Could also consider using session ID for more granular control
        session_id = request.query_params.get("session_id") or request.cookies.get("session_id")

        if session_id:
            return f"session_{session_id}"
        else:
            return f"ip_{client_ip}"

    def _clean_old_requests(self, now: float):
        """Remove request timestamps older than 1 hour"""
        cutoff = now - 3600  # 1 hour ago

        # Clean requests by identifier
        identifiers_to_remove = []
        for identifier, timestamps in self.requests.items():
            # Keep only recent requests
            self.requests[identifier] = [t for t in timestamps if t > cutoff]
            # If no recent requests left, mark for removal
            if not self.requests[identifier]:
                identifiers_to_remove.append(identifier)

        # Remove empty entries
        for identifier in identifiers_to_remove:
            del self.requests[identifier]

# Additional validation utilities
def validate_content_length(content: str, max_length: int = settings.max_content_length) -> bool:
    """Validate content length"""
    if len(content) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Content exceeds maximum length of {max_length} characters"
        )
    return True

def validate_query_length(query: str, max_length: int = settings.max_query_length) -> bool:
    """Validate query length"""
    if len(query) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Query exceeds maximum length of {max_length} characters"
        )
    return True