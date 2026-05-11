"""
reviewer_manager.py - ReviewerManager component (Baseline).
Corresponds to the ReviewerManager lifeline in the sequence diagram.
Responsibility: retrieve, filter (conflicts), and filter (workload) reviewers.
NOTE: filterConflicts and checkWorkload are separate method calls — an identified
      inefficiency (two passes over the reviewer list instead of one).
"""
from .metrics import tracker
from .database import Database


class ReviewerManager:
    """Manages the reviewer pool for a submission.

    Sequence diagram interactions:
      - SubmissionController -> getAvailableReviewers()         -> ReviewerManager
      - ReviewerManager      -> fetchReviewers()                -> Database
      - ReviewerManager      -> filterConflicts(reviewerList)   -> self  [separate call]
      - ReviewerManager      -> checkWorkload(reviewerList)     -> self  [separate call]
    """

    MAX_WORKLOAD = 4

    def __init__(self, database: Database):
        self._database = database

    @tracker.track
    def getAvailableReviewers(self, submission_author: str) -> list:
        """
        Orchestrates reviewer selection:
          1. Fetch full list from database
          2. Filter by conflict-of-interest  (separate call)
          3. Filter by workload capacity     (separate call)
        """
        reviewer_list = self._database.fetchReviewers()
        # Two separate filtering passes — baseline design inefficiency
        filtered = self.filterConflicts(reviewer_list, submission_author)
        checked = self.checkWorkload(filtered)
        return checked

    @tracker.track
    def filterConflicts(self, reviewer_list: list, submission_author: str) -> list:
        """Removes reviewers who have a declared conflict with the submission author."""
        return [
            r for r in reviewer_list
            if submission_author not in r.get("conflicts", [])
        ]

    @tracker.track
    def checkWorkload(self, reviewer_list: list) -> list:
        """Removes reviewers whose current workload exceeds the permitted maximum."""
        return [r for r in reviewer_list if r["workload"] <= self.MAX_WORKLOAD]
