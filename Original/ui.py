"""
ui.py - UI component (Baseline).
Corresponds to the UI lifeline in the sequence diagram.
Responsibility: entry point for researcher interactions; delegates to SubmissionController.
"""
from .metrics import tracker
from .submission_controller import SubmissionController


class UI:
    """User interface layer.

    Sequence diagram interactions:
      - Researcher -> submitResearchOutput(data) -> UI
      - UI         -> submit(data)               -> SubmissionController
      - UI         -> sendNotification()         -> Researcher
    """

    def __init__(self, submission_controller: SubmissionController):
        self._submission_controller = submission_controller

    @tracker.track
    def submitResearchOutput(self, data: dict, researcher_id: str = "anonymous") -> dict:
        """Top-level entry point called by the Researcher actor."""
        result = self.submit(data)
        self.sendNotification(researcher_id, result)
        return result

    @tracker.track
    def submit(self, data: dict) -> dict:
        """Delegates to SubmissionController."""
        return self._submission_controller.submit(data)

    @tracker.track
    def sendNotification(self, researcher_id: str, result: dict) -> dict:
        """Notifies the researcher of the final outcome via the UI."""
        outcome = result.get("outcome", "error")
        return {
            "researcher_id": researcher_id,
            "notification": f"Your submission outcome: {outcome.upper()}",
            "delivered": True,
        }
