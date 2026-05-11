"""
validator.py - Validator component (Optimised).
Functionally identical to the baseline — validation logic does not change.
"""
from .metrics import tracker


class Validator:
    @tracker.track
    def validateFormat(self, data: dict) -> bool:
        required_fields = ["title", "content", "author"]
        return all(field in data and bool(data[field]) for field in required_fields)
