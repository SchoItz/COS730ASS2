"""
database.py - Database component (Optimised).
Key improvement: saveScoresBatch() replaces N individual saveScore() calls,
reducing database round-trips from O(reviewers) to O(1).
"""
import time
from .metrics import tracker


class Database:
    """Optimised persistence layer with batch score saving.

    Changes vs baseline:
      - saveScore()       (called N times in loop) REPLACED BY
      - saveScoresBatch() (called once with all scores)
    """

    def __init__(self, simulation_delay: float = 0.0):
        self._simulation_delay = simulation_delay
        self._submissions: dict = {}
        self._scores: dict = {}
        self._submission_counter = 0
        self._reviewers = [
            {"id": 1, "name": "Dr. Alice Smith",   "workload": 2, "conflicts": []},
            {"id": 2, "name": "Dr. Bob Jones",      "workload": 5, "conflicts": []},
            {"id": 3, "name": "Prof. Carol Brown",  "workload": 1, "conflicts": ["author_x"]},
            {"id": 4, "name": "Dr. David Wilson",   "workload": 3, "conflicts": []},
            {"id": 5, "name": "Prof. Eve Davis",    "workload": 4, "conflicts": []},
        ]

    def _delay(self):
        if self._simulation_delay > 0:
            time.sleep(self._simulation_delay)

    @tracker.track
    def saveSubmission(self, data: dict) -> dict:
        self._delay()
        self._submission_counter += 1
        submission_id = f"SUB{self._submission_counter:04d}"
        self._submissions[submission_id] = {
            **data,
            "submission_id": submission_id,
            "status": "pending",
        }
        return {"submission_id": submission_id, "status": "saved"}

    @tracker.track
    def fetchReviewers(self) -> list:
        self._delay()
        return list(self._reviewers)

    @tracker.track
    def saveScoresBatch(self, submission_id: str, scores: dict) -> dict:
        """
        Persists all reviewer scores in a single operation.
        Optimisation: replaces N individual saveScore() calls with one batch call.
        """
        self._delay()
        for reviewer_id, score in scores.items():
            key = f"{submission_id}_{reviewer_id}"
            self._scores[key] = score
        return {"status": "saved", "count": len(scores)}
