"""In-process sliding window rate limiting for RakshaScan MVP.

Provides lightweight protection against flood attacks, repeated expensive OCR requests,
and URL scanning abuse without requiring external Redis/distributed dependencies.
Configurable via settings.RATE_LIMITING_ENABLED.
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Dict, List, Optional, Tuple

from fastapi import HTTPException, Request, status

from app.core.config import settings


class InMemoryRateLimiter:
    """Thread-safe sliding-window in-memory rate limiter."""

    def __init__(self, window_seconds: int = 60) -> None:
        self.window_seconds = window_seconds
        # Maps (client_key, bucket) -> list of request timestamps
        self._history: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        self._lock = Lock()

    def get_client_ip(self, request: Request) -> str:
        """Extracts the client IP from X-Forwarded-For or socket host."""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            # First IP in the comma-separated proxy chain
            return forwarded_for.split(",")[0].strip()
        if request.client and request.client.host:
            return request.client.host
        return "127.0.0.1"

    def is_allowed(self, key: str, bucket: str, limit: int) -> Tuple[bool, int]:
        """Checks if a request under `bucket` is permitted within the sliding window.

        Args:
            key: Client identifier (e.g. IP address).
            bucket: Action bucket identifier (e.g. "url", "message", "screenshot").
            limit: Maximum allowed requests within `window_seconds`.

        Returns:
            Tuple of (is_allowed: bool, retry_after_seconds: int)
        """
        if not settings.RATE_LIMITING_ENABLED:
            return True, 0

        now = time.time()
        window_start = now - self.window_seconds

        with self._lock:
            timestamps = self._history[(key, bucket)]
            # Prune expired timestamps older than the sliding window
            self._history[(key, bucket)] = [ts for ts in timestamps if ts > window_start]
            active_requests = self._history[(key, bucket)]

            if len(active_requests) >= limit:
                oldest_in_window = active_requests[0]
                retry_after = max(1, int(oldest_in_window + self.window_seconds - now))
                return False, retry_after

            # Record current request
            self._history[(key, bucket)].append(now)
            return True, 0

    def reset(self) -> None:
        """Clears all rate limit history (primarily for test isolation)."""
        with self._lock:
            self._history.clear()


# Global in-process rate limiter singleton
rate_limiter = InMemoryRateLimiter(window_seconds=60)


def rate_limit_guard(bucket: str, limit: int):
    """FastAPI dependency for endpoint-level rate enforcement."""

    async def _dependency(request: Request) -> None:
        client_ip = rate_limiter.get_client_ip(request)
        allowed, retry_after = rate_limiter.is_allowed(client_ip, bucket, limit)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error_type": "RATE_LIMIT_EXCEEDED",
                    "message": (
                        f"Too many requests for {bucket} analysis. "
                        f"Please wait {retry_after} seconds before submitting again."
                    ),
                },
                headers={"Retry-After": str(retry_after)},
            )

    return _dependency
