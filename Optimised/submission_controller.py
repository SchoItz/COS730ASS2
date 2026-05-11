"""
submission_controller.py - SubmissionController component (Optimised).
Key improvement: reduced responsibilities — no longer manages reviewer
assignment loop or knows about individual Reviewer objects.
"""
from .metrics import tracker
from .validator import Validator
from .database import Database
from .reviewer_manager import ReviewerManager
from .evaluation_manager import EvaluationManager


class SubmissionController:
    """Lean orchestrator — delegates to cohesive collaborators.

    Changes vs baseline:
      - No longer depends on Reviewer class directly (removed dependency)
      - No longer controls the reviewer assignment loop (delegated to ReviewerManager)
      - submit() is simpler: validate → save → select+assign → evaluate
    """

    def __init__(
        self,
        validator: Validator,
        database: Database,
        reviewer_manager: ReviewerManager,
        evaluation_manager: EvaluationManager,
    ):
        # Reduced from 5 collaborators (baseline) to 4
        self._validator = validator
        self._database = database
        self._reviewer_manager = reviewer_manager
        self._evaluation_manager = evaluation_manager

    @tracker.track
    def submit(self, data: dict) -> dict:
        """
        Simplified submission pipeline:
          1. Validate format
          2. Save submission
          3. Delegate reviewer selection + assignment to ReviewerManager
          4. Delegate full evaluation to EvaluationManager
        """
        if not self._validator.validateFormat(data):
            return {"status": "error", "message": "Invalid submission format"}

        confirmation = self._database.saveSubmission(data)
        submission_id = confirmation["submission_id"]

        # ReviewerManager handles both selection and assignment
        reviewers = self._reviewer_manager.selectAndAssignReviewers(
            submission_id, data.get("author", "")
        )

        if not reviewers:
            return {"status": "error", "message": "No reviewers available"}

        # EvaluationManager handles scoring, persistence, decision, notification
        outcome = self._evaluation_manager.evaluate(submission_id, reviewers)

        return {
            "status": "success",
            "submission_id": submission_id,
            "outcome": outcome,
        }
