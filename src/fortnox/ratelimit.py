"""Client-side rate limiting.

Fortnox applies a sliding window of 25 requests per 5 seconds per access token
(300 per minute per client-id and tenant). Bursting past it earns HTTP 429 and
the limiter stays engaged until the average falls back under the limit, so it is
cheaper to pace requests here than to absorb 429s.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable


class SlidingWindowRateLimiter:
    """Blocks until a request may be sent without exceeding the window.

    Thread-safe. Only covers this process - if you run several workers against
    the same Fortnox tenant, size each worker's limit accordingly or put a
    shared limiter in front of them.
    """

    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
        *,
        monotonic: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be at least 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._monotonic = monotonic
        self._sleep = sleep
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> float:
        """Reserve a slot, sleeping if needed. Returns seconds spent waiting."""
        waited = 0.0
        while True:
            with self._lock:
                now = self._monotonic()
                self._prune(now)
                if len(self._timestamps) < self.max_requests:
                    self._timestamps.append(now)
                    return waited
                sleep_for = self._timestamps[0] + self.window_seconds - now
            # Sleep outside the lock so other threads can make progress.
            sleep_for = max(sleep_for, 0.001)
            self._sleep(sleep_for)
            waited += sleep_for

    def _prune(self, now: float) -> None:
        cutoff = now - self.window_seconds
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()
