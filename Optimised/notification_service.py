"""
notification_service.py - NotificationService component (Optimised).
Key improvement: single notify(outcome) method replaces three separate
outcome-specific methods (notifyAcceptance / notifyRejection / notifyRevision).
"""
from .metrics import tracker

_MESSAGES = {
    "accepted": "has been ACCEPTED.",
    "rejected": "has been REJECTED.",
    "revision": "requires REVISION.",
}


class NotificationService:
    """Unified notification dispatcher.

    Changes vs baseline:
      - notifyAcceptance() + notifyRejection() + notifyRevision()
        REPLACED BY
      - notify(submission_id, outcome)
    """

    @tracker.track
    def notify(self, submission_id: str, outcome: str) -> dict:
        """
        Dispatches the appropriate notification based on outcome.
        Eliminates the scattered ALT branching from the baseline sequence diagram.
        """
        message = _MESSAGES.get(outcome, "has an unknown outcome.")
        return {
            "submission_id": submission_id,
            "message": f"Submission {submission_id} {message}",
            "type": outcome,
        }
