"""
validator.py - Validator component (Baseline).
Corresponds to the Validator lifeline in the sequence diagram.
Responsibility: validate the format of submitted data.
"""
from .metrics import tracker


class Validator:
    """Validates submission data format.
    Sequence diagram interaction: SubmissionController -> validateFormat(data) -> Validator
    """

    @tracker.track
    def validateFormat(self, data: dict) -> bool:
        """
        Checks that all required fields are present and non-empty.
        Returns True (valid) or False (invalid).
        """
        required_fields = ["title", "content", "author"]
        return all(field in data and bool(data[field]) for field in required_fields)
