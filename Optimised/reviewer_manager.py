"""
reviewer_manager.py - ReviewerManager component (Optimised).
Key improvements:
  1. Combines filterConflicts + checkWorkload into a single-pass filter
     (eliminates 2 separate method calls from the baseline).
  2. Handles reviewer assignment internally, removing that responsibility
     from SubmissionController (better GRASP responsibility allocation).
"""
from .metrics import tracker
from .database import Database
from .reviewer import Reviewer


class ReviewerManager:
    """Manages the full reviewer selection and assignment pipeline.

    Changes vs baseline:
      - getAvailableReviewers() + filterConflicts() + checkWorkload() + assignment loop
        REPLACED BY
      - selectAndAssignReviewers()  (single cohesive method)
    """

    MAX_WORKLOAD = 4
    MIN_REVIEWERS = 3

    def __init__(self, database: Database):
        self._database = database

    @tracker.track
    def selectAndAssignReviewers(
        self, submission_id: str, submission_author: str
    ) -> list:
        """
        Fetches reviewers, applies a single-pass eligibility filter
        (conflict-of-interest AND workload in one pass), assigns eligible
        reviewers, and returns the assigned Reviewer instances.

        Optimisations:
          - Single filter pass replaces two separate filterConflicts/checkWorkload calls
          - Assignment responsibility moved here from SubmissionController
        """
        all_reviewers = self._database.fetchReviewers()

        # Single-pass eligibility filter (combines conflict + workload checks)
        eligible = [
            r for r in all_reviewers
            if submission_author not in r.get("conflicts", [])
            and r["workload"] <= self.MAX_WORKLOAD
        ]

        selected = eligible[: self.MIN_REVIEWERS]

        # Assign and return reviewer instances
        reviewer_instances = []
        for data in selected:
            reviewer = Reviewer(data)
            reviewer.assignReview(submission_id)
            reviewer_instances.append(reviewer)

        return reviewer_instances
