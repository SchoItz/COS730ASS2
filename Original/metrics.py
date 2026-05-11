"""
metrics.py - Call tracking module for the Baseline system.
Provides a decorator-based call counter and timer for empirical evaluation.
"""
import time
import functools


class CallTracker:
    """Tracks method call counts and cumulative execution times."""

    def __init__(self):
        self.call_counts: dict = {}
        self.call_times: dict = {}

    def track(self, func):
        """Decorator that instruments a function for call counting and timing."""
        tracker_ref = self

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = func.__qualname__
            tracker_ref.call_counts[key] = tracker_ref.call_counts.get(key, 0) + 1
            t0 = time.perf_counter()
            result = func(*args, **kwargs)
            tracker_ref.call_times[key] = (
                tracker_ref.call_times.get(key, 0.0) + (time.perf_counter() - t0)
            )
            return result

        return wrapper

    def reset(self):
        """Clears all recorded metrics."""
        self.call_counts.clear()
        self.call_times.clear()

    def total_calls(self) -> int:
        return sum(self.call_counts.values())

    def total_time_ms(self) -> float:
        return sum(self.call_times.values()) * 1000.0

    def report(self) -> dict:
        return {
            "total_calls": self.total_calls(),
            "total_time_ms": round(self.total_time_ms(), 4),
            "per_method": {
                k: {
                    "calls": v,
                    "time_ms": round(self.call_times.get(k, 0.0) * 1000, 6),
                }
                for k, v in sorted(self.call_counts.items())
            },
        }


# Module-level singleton tracker used by all baseline classes
tracker = CallTracker()
