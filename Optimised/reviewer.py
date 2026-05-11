"""
reviewer.py - Reviewer component (Optimised).
Functionally identical to the baseline Reviewer — no change needed here.
"""
import random
from .metrics import tracker


class Reviewer:
    def __init__(self, reviewer_data: dict):
        self.id: int = reviewer_data["id"]
        self.name: str = reviewer_data["name"]
        self.workload: int = reviewer_data["workload"]
        self.conflicts: list = reviewer_data.get("conflicts", [])
        self.assigned_submission: str | None = None

    @tracker.track
    def assignReview(self, submission_id: str) -> dict:
        self.assigned_submission = submission_id
        self.workload += 1
        return {
            "reviewer_id": self.id,
            "submission_id": submission_id,
            "status": "assigned",
        }

    @tracker.track
    def submitScore(self, submission_id: str) -> dict:
        rng = random.Random(self.id * 31337)
        score = round(rng.uniform(5.0, 10.0), 2)
        return {
            "reviewer_id": self.id,
            "submission_id": submission_id,
            "score": score,
        }
