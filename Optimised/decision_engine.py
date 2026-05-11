"""
decision_engine.py - Decision Table engine (Optimised).
Replaces the scattered calculateAverage / checkConsensus / applyRules calls
in the baseline EvaluationManager with a single, explicit decision table.

Decision Table: Submission Outcome
════════════════════════════════════════════════════════════════════
 Rule │ Avg ≥ 7.0 │ Avg ≥ 5.0 │ Consensus │ Outcome
──────┼───────────┼───────────┼───────────┼────────────────────────
  R1  │     Y     │     Y     │     Y     │ accepted
  R2  │     Y     │     Y     │     N     │ revision
  R3  │     N     │     Y     │     Y     │ revision
  R4  │     N     │     Y     │     N     │ revision
  R5  │     N     │     N     │    N/A    │ rejected
════════════════════════════════════════════════════════════════════
Note: R1 + R2 cover avg >= 7.0 (accept threshold).
      R3 + R4 cover 5.0 <= avg < 7.0 (revision threshold).
      R5 covers avg < 5.0 (rejection threshold).
      Consensus only gates acceptance; low consensus still allows revision.
"""


class DecisionEngine:
    """
    Encapsulates all outcome decision logic as an explicit decision table.
    Improves: clarity, testability, maintainability, single responsibility.
    """

    ACCEPT_THRESHOLD = 7.0
    REVISION_THRESHOLD = 5.0
    CONSENSUS_TOLERANCE = 2.0

    # Decision table represented as ordered rules:
    # Each rule: (requires_high_score, requires_mid_score, requires_consensus, outcome)
    # None for requires_consensus means "don't care"
    _RULES = [
        (True,  True,  True,  "accepted"),   # R1
        (True,  True,  False, "revision"),   # R2
        (False, True,  True,  "revision"),   # R3
        (False, True,  False, "revision"),   # R4
        (False, False, None,  "rejected"),   # R5
    ]

    def evaluate(self, scores: list) -> str:
        """
        Evaluates a list of reviewer scores against the decision table
        and returns the submission outcome: 'accepted', 'revision', or 'rejected'.
        """
        if not scores:
            return "rejected"

        average = sum(scores) / len(scores)
        consensus = all(abs(s - average) <= self.CONSENSUS_TOLERANCE for s in scores)

        high_score = average >= self.ACCEPT_THRESHOLD
        mid_score = average >= self.REVISION_THRESHOLD

        for req_high, req_mid, req_consensus, outcome in self._RULES:
            high_match = req_high == high_score
            mid_match = req_mid == mid_score
            consensus_match = (req_consensus is None) or (req_consensus == consensus)
            if high_match and mid_match and consensus_match:
                return outcome

        return "rejected"  # Fallback (should not be reached)

    def get_table_representation(self) -> dict:
        """Returns a structured representation of the decision table for reporting."""
        return {
            "thresholds": {
                "accept": self.ACCEPT_THRESHOLD,
                "revision": self.REVISION_THRESHOLD,
                "consensus_tolerance": self.CONSENSUS_TOLERANCE,
            },
            "conditions": [
                "C1: Average score >= accept threshold (7.0)",
                "C2: Average score >= revision threshold (5.0)",
                "C3: Reviewer consensus achieved (max deviation <= 2.0)",
            ],
            "rules": [
                {"id": "R1", "C1": "Y", "C2": "Y", "C3": "Y", "action": "accepted"},
                {"id": "R2", "C1": "Y", "C2": "Y", "C3": "N", "action": "revision"},
                {"id": "R3", "C1": "N", "C2": "Y", "C3": "Y", "action": "revision"},
                {"id": "R4", "C1": "N", "C2": "Y", "C3": "N", "action": "revision"},
                {"id": "R5", "C1": "N", "C2": "N", "C3": "-", "action": "rejected"},
            ],
        }
