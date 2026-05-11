"""
evaluation_manager.py - EvaluationManager component (Optimised).
Key improvements:
  1. Single evaluate() method replaces startEvaluation + calculateAverage +
     checkConsensus + applyRules (4 calls → 1 call).
  2. Uses DecisionEngine (decision table) for outcome determination.
  3. Batch score persistence via saveScoresBatch() (N calls → 1 call).
  4. Single notification call via NotificationService.notify().
"""
from .metrics import tracker
from .database import Database
from .notification_service import NotificationService
from .decision_engine import DecisionEngine


class EvaluationManager:
    """Cohesive evaluation manager using a decision table.

    Changes vs baseline:
      - startEvaluation() + calculateAverage() + checkConsensus() + applyRules()
        REPLACED BY
      - evaluate()  (delegates decision logic to DecisionEngine)
    """

    def __init__(self, database: Database, notification_service: NotificationService):
        self._database = database
        self._notification_service = notification_service
        self._decision_engine = DecisionEngine()

    @tracker.track
    def evaluate(self, submission_id: str, reviewers: list) -> str:
        """
        Full evaluation pipeline:
          1. Collect all reviewer scores
          2. Persist all scores in a single batch call
          3. Determine outcome via DecisionEngine (decision table)
          4. Dispatch unified notification
        """
        # Collect scores from each reviewer
        scores: dict = {}
        for reviewer in reviewers:
            result = reviewer.submitScore(submission_id)
            scores[reviewer.id] = result["score"]

        # Batch persist all scores — single DB call instead of N
        self._database.saveScoresBatch(submission_id, scores)

        # Determine outcome using decision table (replaces 3 separate calls)
        outcome = self._decision_engine.evaluate(list(scores.values()))

        # Single unified notification call (replaces 3 conditional calls)
        self._notification_service.notify(submission_id, outcome)

        return outcome
