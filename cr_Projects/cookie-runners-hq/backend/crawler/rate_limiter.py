"""Rate limiter for crawl operations.

Token-bucket rate limiting with per-source and global limits.
"""
from __future__ import annotations

import threading
import time
from collections import defaultdict

from config.settings import get_config


class RateLimiter:
    """Token-bucket rate limiter for crawl sources.

    Parameters
    ----------
    requests_per_minute : int
        Maximum requests per source per minute.
    global_rpm : int
        Global request cap across all sources.
    """

    def __init__(self, requests_per_minute: int = 10, global_rpm: int = 60) -> None:
        self.requests_per_minute = requests_per_minute
        self.global_rpm = global_rpm
        self._source_buckets: dict[int, list[float]] = defaultdict(list)
        self._global_bucket: list[float] = []
        self._lock = threading.Lock()

    def _clean_bucket(self, bucket: list[float]) -> None:
        """Remove timestamps older than 60 seconds."""
        cutoff = time.time() - 60.0
        while bucket and bucket[0] < cutoff:
            bucket.pop(0)

    def acquire(self, source_id: int) -> bool:
        """Attempt to acquire a slot for a source.

        Returns True if the request is allowed, False if it must wait.
        """
        with self._lock:
            now = time.time()
            self._clean_bucket(self._source_buckets[source_id])
            self._clean_bucket(self._global_bucket)

            if len(self._source_buckets[source_id]) >= self.requests_per_minute:
                return False
            if len(self._global_bucket) >= self.global_rpm:
                return False

            self._source_buckets[source_id].append(now)
            self._global_bucket.append(now)
            return True

    def wait_time(self, source_id: int) -> float:
        """Return seconds to wait before the next request is allowed."""
        with self._lock:
            self._clean_bucket(self._source_buckets[source_id])
            self._clean_bucket(self._global_bucket)

            source_wait = 0.0
            if self._source_buckets[source_id]:
                oldest = self._source_buckets[source_id][0]
                source_wait = max(0.0, 60.0 - (time.time() - oldest))

            global_wait = 0.0
            if self._global_bucket:
                oldest = self._global_bucket[0]
                global_wait = max(0.0, 60.0 - (time.time() - oldest))

            return max(source_wait, global_wait)

    def acquire_blocking(self, source_id: int, timeout: float = 30.0) -> bool:
        """Block until a slot is available or timeout is reached."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.acquire(source_id):
                return True
            wait = min(self.wait_time(source_id), deadline - time.time())
            if wait > 0:
                time.sleep(wait)
        return False


# Singleton instance shared across the app
_rate_limiter: RateLimiter | None = None
_init_lock = threading.Lock()


def get_rate_limiter() -> RateLimiter:
    """Return the global RateLimiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        with _init_lock:
            if _rate_limiter is None:
                cfg = get_config()
                _rate_limiter = RateLimiter(
                    requests_per_minute=cfg.rate_limit_rpm,
                    global_rpm=cfg.rate_limit_global_rpm,
                )
    return _rate_limiter
