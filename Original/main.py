"""
main.py - Baseline system entry point.
Wires all components together and provides a demo run.
Run from project root: python -m baseline.main
"""
import json
from .validator import Validator
from .database import Database
from .reviewer_manager import ReviewerManager
from .notification_service import NotificationService
from .evaluation_manager import EvaluationManager
from .submission_controller import SubmissionController
from .ui import UI
from . import metrics


def create_system(simulation_delay: float = 0.0) -> UI:
    """Factory function: constructs and wires all baseline components."""
    validator = Validator()
    database = Database(simulation_delay=simulation_delay)
    notification_service = NotificationService()
    reviewer_manager = ReviewerManager(database)
    evaluation_manager = EvaluationManager(database, notification_service)
    submission_controller = SubmissionController(
        validator, database, reviewer_manager, evaluation_manager
    )
    return UI(submission_controller)


def run_demo():
    metrics.tracker.reset()
    ui = create_system()

    print("=" * 55)
    print("   BASELINE SYSTEM DEMO")
    print("=" * 55)

    # --- Valid submission ---
    valid_data = {
        "title": "AI Ethics in Modern Systems",
        "content": "This paper explores ethical considerations in AI...",
        "author": "researcher_001",
    }
    print("\n[1] Valid submission:")
    result = ui.submitResearchOutput(valid_data, researcher_id="researcher_001")
    print(json.dumps(result, indent=2))

    # --- Invalid submission (missing fields) ---
    invalid_data = {"title": "Incomplete Paper"}
    print("\n[2] Invalid submission (missing content and author):")
    result_invalid = ui.submitResearchOutput(invalid_data, researcher_id="researcher_002")
    print(json.dumps(result_invalid, indent=2))

    # --- Metrics ---
    print("\n" + "=" * 55)
    print("   METRICS REPORT")
    print("=" * 55)
    report = metrics.tracker.report()
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    run_demo()
