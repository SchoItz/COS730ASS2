"""
evaluation_manager.py - EvaluationManager component (Baseline).
Corresponds to the EvaluationManager lifeline in the sequence diagram.
Responsibility: orchestrate evaluation loop, calculate average, check consensus,
                apply rules, dispatch notifications.
NOTE: calculateAverage, checkConsensus, and applyRules are separate method calls
      — an identified inefficiency (fragmented evaluation logic).
"""
from .metrics import tracker
from .database import Database
from .notification_service import NotificationService


class EvaluationManager:
    """Manages the full evaluation lifecycle for a submission.

    Sequence diagram interactions:
      - SubmissionController -> startEvaluation()         -> EvaluationManager
      - LOOP: Reviewer       -> submitScore(score)        -> EvaluationManager
      - EvaluationManager    -> saveScore(score)          -> Database   [in loop]
      - EvaluationManager    -> calculateAverage()        -> self
      - EvaluationManager    -> checkConsensus()          -> self
      - EvaluationManager    -> applyRules(avg, consensus)-> self
      - ALT: EvaluationManager -> notifyAcceptance/Rejection/Revision -> NotificationService
    """

    ACCEPT_THRESHOLD = 7.0
    REVISION_THRESHOLD = 5.0
    CONSENSUS_TOLERANCE = 2.0

    def __init__(self, database: Database, notification_service: NotificationService):
        self._database = database
        self._notification_service = notification_service
        self._scores: list = []
        self._submission_id: str = ""

    @tracker.track
    def startEvaluation(self, submission_id: str, reviewers: list) -> str:
        """
        Drives the evaluation process:
          1. Collects scores from each reviewer (LOOP in diagram)
          2. Persists each score individually (Database.saveScore in loop)
          3. Calculates average (separate call)
          4. Checks consensus (separate call)
          5. Applies decision rules (separate call)
          6. Dispatches outcome-specific notification
        """
        self._submission_id = submission_id
        self._scores = []

        # LOOP [each reviewer]: reviewer submits score, database saves it
        for reviewer in reviewers:
            result = reviewer.submitScore(submission_id)
            score = result["score"]
            self._database.saveScore(submission_id, reviewer.id, score)
            self._scores.append(score)

        # Separate evaluation method calls — baseline design inefficiency
        average = self.calculateAverage()
        consensus = self.checkConsensus()
        outcome = self.applyRules(average, consensus)

        # ALT block: three separate notification paths
        if outcome == "accepted":
            self._notification_service.notifyAcceptance(submission_id)
        elif outcome == "rejected":
            self._notification_service.notifyRejection(submission_id)
        else:
            self._notification_service.notifyRevision(submission_id)

        return outcome

    @tracker.track
    def calculateAverage(self) -> float:
        """Computes the arithmetic mean of collected scores."""
        if not self._scores:
            return 0.0
        return sum(self._scores) / len(self._scores)

    @tracker.track
    def checkConsensus(self) -> bool:
        """Returns True if all scores deviate <= CONSENSUS_TOLERANCE from the mean."""
        if not self._scores:
            return False
        avg = sum(self._scores) / len(self._scores)
        return all(abs(s - avg) <= self.CONSENSUS_TOLERANCE for s in self._scores)

    @tracker.track
    def applyRules(self, average: float, consensus: bool) -> str:
        """
        Applies decision rules to determine the submission outcome.
        Scattered conditional logic — identified as a design inefficiency.
        """
        if average >= self.ACCEPT_THRESHOLD and consensus:
            return "accepted"
        if average < self.REVISION_THRESHOLD:
            return "rejected"
        return "revision"
