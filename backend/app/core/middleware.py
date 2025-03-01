import time
from datetime import datetime, timedelta

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.caching import clear_expired_cache


class CacheCleanupMiddleware(BaseHTTPMiddleware):
    """
    Middleware to periodically clean up expired cache entries.
    """
    
    def __init__(self, app, cleanup_interval=300):  # 5 minutes by default
        super().__init__(app)
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = datetime.now()
    
    async def dispatch(self, request: Request, call_next):
        """
        Dispatch method called for each request.
        
        Args:
            request: FastAPI request
            call_next: Next middleware or route handler
            
        Returns:
            Response: FastAPI response
        """
        # Check if it's time to clean up the cache
        now = datetime.now()
        if (now - self.last_cleanup).total_seconds() > self.cleanup_interval:
            # Clear expired cache entries
            clear_expired_cache()
            self.last_cleanup = now
        
        # Continue with the request
        response = await call_next(request)
        return response
