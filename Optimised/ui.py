"""
ui.py - UI component (Optimised).
Simplified: notification is handled by NotificationService; UI only relays result.
"""
from .metrics import tracker
from .submission_controller import SubmissionController


class UI:
    def __init__(self, submission_controller: SubmissionController):
        self._submission_controller = submission_controller

    @tracker.track
    def submitResearchOutput(self, data: dict, researcher_id: str = "anonymous") -> dict:
        result = self.submit(data)
        self.sendNotification(researcher_id, result)
        return result

    @tracker.track
    def submit(self, data: dict) -> dict:
        return self._submission_controller.submit(data)

    @tracker.track
    def sendNotification(self, researcher_id: str, result: dict) -> dict:
        outcome = result.get("outcome", "error")
        return {
            "researcher_id": researcher_id,
            "notification": f"Your submission outcome: {outcome.upper()}",
            "delivered": True,
        }
