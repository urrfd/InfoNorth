from __future__ import annotations

import threading

import pytest

from fortnox.ratelimit import SlidingWindowRateLimiter


class FakeClock:
    """A monotonic clock that only advances when someone sleeps."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def test_allows_burst_up_to_limit_without_sleeping():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(25, 5.0, monotonic=clock.monotonic, sleep=clock.sleep)
    for _ in range(25):
        assert limiter.acquire() == 0.0
    assert clock.sleeps == []


def test_sleeps_once_the_window_is_full():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(3, 5.0, monotonic=clock.monotonic, sleep=clock.sleep)
    for _ in range(3):
        limiter.acquire()

    waited = limiter.acquire()

    assert waited == pytest.approx(5.0)
    assert clock.now == pytest.approx(5.0)


def test_slots_free_up_as_the_window_slides():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(2, 5.0, monotonic=clock.monotonic, sleep=clock.sleep)
    limiter.acquire()  # t=0
    clock.now = 3.0
    limiter.acquire()  # t=3

    clock.now = 6.0  # the t=0 slot has aged out
    assert limiter.acquire() == 0.0
    assert clock.sleeps == []


def test_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        SlidingWindowRateLimiter(0, 5.0)
    with pytest.raises(ValueError):
        SlidingWindowRateLimiter(5, 0)


def test_is_thread_safe():
    limiter = SlidingWindowRateLimiter(50, 0.01)
    errors: list[BaseException] = []

    def worker():
        try:
            for _ in range(20):
                limiter.acquire()
        except BaseException as exc:  # pragma: no cover - only on a real bug
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    assert not errors
