"""
database.py - Database component (Baseline).
Corresponds to the Database lifeline in the sequence diagram.
Responsibility: persist submissions, return reviewer lists, persist scores.
NOTE: simulation_delay simulates I/O latency for benchmarking purposes.
"""
import time
from .metrics import tracker


class Database:
    """Simulated persistence layer.

    Sequence diagram interactions:
      - SubmissionController -> saveSubmission(data) -> Database
      - ReviewerManager      -> fetchReviewers()     -> Database
      - EvaluationManager    -> saveScore(score)     -> Database  [called in loop]
    """

    def __init__(self, simulation_delay: float = 0.0):
        self._simulation_delay = simulation_delay
        self._submissions: dict = {}
        self._scores: dict = {}
        self._submission_counter = 0
        # Pre-populated reviewer registry
        self._reviewers = [
            {"id": 1, "name": "Dr. Alice Smith",   "workload": 2, "conflicts": []},
            {"id": 2, "name": "Dr. Bob Jones",      "workload": 5, "conflicts": []},
            {"id": 3, "name": "Prof. Carol Brown",  "workload": 1, "conflicts": ["author_x"]},
            {"id": 4, "name": "Dr. David Wilson",   "workload": 3, "conflicts": []},
            {"id": 5, "name": "Prof. Eve Davis",    "workload": 4, "conflicts": []},
        ]

    def _delay(self):
        """Simulates I/O latency (configurable for benchmarking)."""
        if self._simulation_delay > 0:
            time.sleep(self._simulation_delay)

    @tracker.track
    def saveSubmission(self, data: dict) -> dict:
        """Persists a new submission and returns a confirmation with the generated ID."""
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
        """Returns the full list of registered reviewers."""
        self._delay()
        return list(self._reviewers)

    @tracker.track
    def saveScore(self, submission_id: str, reviewer_id: int, score: float) -> dict:
        """
        Persists a single reviewer's score.
        NOTE: Called once per reviewer inside a loop — an identified inefficiency.
        """
        self._delay()
        key = f"{submission_id}_{reviewer_id}"
        self._scores[key] = score
        return {"status": "saved", "key": key}
