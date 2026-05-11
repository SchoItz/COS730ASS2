"""
notification_service.py - NotificationService component (Baseline).
Corresponds to the NotificationService lifeline in the sequence diagram.
Responsibility: send outcome-specific notifications.
NOTE: Three separate methods for acceptance/rejection/revision — an identified
      inefficiency (scattered conditional notification logic).
"""
from .metrics import tracker


class NotificationService:
    """Dispatches outcome notifications.

    Sequence diagram interactions (ALT block):
      - EvaluationManager -> notifyAcceptance() -> NotificationService  [if accepted]
      - EvaluationManager -> notifyRejection()  -> NotificationService  [if rejected]
      - EvaluationManager -> notifyRevision()   -> NotificationService  [if revision]
    """

    @tracker.track
    def notifyAcceptance(self, submission_id: str) -> dict:
        return {
            "submission_id": submission_id,
            "message": f"Submission {submission_id} has been ACCEPTED.",
            "type": "acceptance",
        }

    @tracker.track
    def notifyRejection(self, submission_id: str) -> dict:
        return {
            "submission_id": submission_id,
            "message": f"Submission {submission_id} has been REJECTED.",
            "type": "rejection",
        }

    @tracker.track
    def notifyRevision(self, submission_id: str) -> dict:
        return {
            "submission_id": submission_id,
            "message": f"Submission {submission_id} requires REVISION.",
            "type": "revision",
        }
