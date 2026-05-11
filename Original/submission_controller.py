"""
submission_controller.py - SubmissionController component (Baseline).
Corresponds to the SubmissionController lifeline in the sequence diagram.
Responsibility: orchestrate the full submission pipeline.
NOTE: This class has too many responsibilities and is tightly coupled to many
      collaborators — an identified design inefficiency (violation of SRP/GRASP).
"""
from .metrics import tracker
from .validator import Validator
from .database import Database
from .reviewer_manager import ReviewerManager
from .reviewer import Reviewer
from .evaluation_manager import EvaluationManager

NUM_REVIEWERS_REQUIRED = 3


class SubmissionController:
    """Central orchestrator for the submission workflow.

    Sequence diagram interactions:
      - UI                  -> submit(data)                  -> SubmissionController
      - SubmissionController -> validateFormat(data)          -> Validator
      - SubmissionController -> saveSubmission(data)          -> Database
      - SubmissionController -> getAvailableReviewers()       -> ReviewerManager
      - LOOP: SubmissionController -> assignReview()          -> Reviewer
      - SubmissionController -> startEvaluation()             -> EvaluationManager
    """

    def __init__(
        self,
        validator: Validator,
        database: Database,
        reviewer_manager: ReviewerManager,
        evaluation_manager: EvaluationManager,
    ):
        # NOTE: SubmissionController depends on 4 collaborators — high coupling
        self._validator = validator
        self._database = database
        self._reviewer_manager = reviewer_manager
        self._evaluation_manager = evaluation_manager

    @tracker.track
    def submit(self, data: dict) -> dict:
        """
        Full submission pipeline as specified in the sequence diagram:
          1. Validate format
          2. ALT [invalid]: return error
          3. [valid]: save submission
          4. Get available reviewers
          5. LOOP [assign reviewers]: assign each reviewer
          6. Start evaluation
        """
        # Step 1-2: Validate format — ALT [invalid] returns error
        is_valid = self._validator.validateFormat(data)
        if not is_valid:
            return {"status": "error", "message": "Invalid submission format"}

        # Step 3: Save submission to database
        confirmation = self._database.saveSubmission(data)
        submission_id = confirmation["submission_id"]

        # Step 4: Get filtered available reviewers
        filtered_reviewers_data = self._reviewer_manager.getAvailableReviewers(
            data.get("author", "")
        )

        # Step 5: LOOP [assign reviewers] — SubmissionController directly controls
        # reviewer instantiation and assignment (poor responsibility allocation)
        count = min(NUM_REVIEWERS_REQUIRED, len(filtered_reviewers_data))
        reviewer_instances: list[Reviewer] = []
        for reviewer_data in filtered_reviewers_data[:count]:
            reviewer = Reviewer(reviewer_data)
            reviewer.assignReview(submission_id)
            reviewer_instances.append(reviewer)

        if not reviewer_instances:
            return {"status": "error", "message": "No reviewers available"}

        # Step 6: Start evaluation
        outcome = self._evaluation_manager.startEvaluation(submission_id, reviewer_instances)

        return {
            "status": "success",
            "submission_id": submission_id,
            "outcome": outcome,
        }
