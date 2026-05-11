# COS 730 – Assignment 2: From Behavioural Models to Optimised Implementation

## Repository Structure

```
COS730ASS2/
├── Original/               # Task 1 – Baseline implementation (exact sequence diagram)
│   ├── __init__.py
│   ├── ui.py
│   ├── submission_controller.py
│   ├── validator.py
│   ├── database.py
│   ├── reviewer_manager.py
│   ├── reviewer.py
│   ├── evaluation_manager.py
│   ├── notification_service.py
│   ├── metrics.py
│   └── main.py
│
├── Optimised/              # Tasks 4 & 5 – Redesigned implementation
│   ├── __init__.py
│   ├── ui.py
│   ├── submission_controller.py
│   ├── validator.py
│   ├── database.py
│   ├── reviewer_manager.py
│   ├── reviewer.py
│   ├── evaluation_manager.py
│   ├── notification_service.py
│   ├── decision_engine.py  # Decision table (Task 3)
│   ├── metrics.py
│   └── main.py
│
├── benchmark.py            # Task 6 – Empirical comparison
├── benchmark_results.json  # Generated benchmark output
└── report.md               # Full technical report (Tasks 1–6)
```

## System Description

An **Intelligent Submission and Review System** that models:
- Artefact submission and format validation
- Conflict-of-interest and workload-aware reviewer assignment
- Multi-reviewer peer evaluation
- Decision-table-driven outcome determination (accepted / revision / rejected)
- Outcome notification

## Running the Code

> Requires Python 3.12+. No external dependencies.

```bash
# Run the original (baseline) system demo
python -m Original.main

# Run the optimised system demo
python -m Optimised.main

# Run the empirical benchmark (200 iterations per system)
python benchmark.py
```

## Key Results (Task 6)

| Metric                 | Original | Optimised | Improvement  |
|------------------------|----------|-----------|--------------|
| Method calls / run     | 24       | 17        | −29.2%       |
| Avg execution time     | 6.96 ms  | 4.24 ms   | −39.4%       |
| Speedup                | 1.0x     | 1.64x     |              |
| Public methods         | 20       | 14        | −30%         |
| DB calls / submission  | 5        | 3         | −2           |

## Design Improvements (Tasks 2–4)

| Issue in Original Design           | Fix in Optimised                                      |
|------------------------------------|-------------------------------------------------------|
| Two separate reviewer filter passes | Single-pass combined filter in `selectAndAssignReviewers` |
| Assignment loop in SubmissionController | Moved to `ReviewerManager` (GRASP: Creator)       |
| 4 fragmented evaluation methods    | 1 `evaluate()` method + `DecisionEngine` (decision table) |
| 3 notification methods (brittle)   | 1 `notify(outcome)` with data-driven dispatch         |
| N database calls in scoring loop   | 1 batch call `saveScoresBatch()`                      |

## Report

See [report.md](report.md) for the full technical report covering all 6 tasks, including sequence diagrams, decision tables, code comparisons, and empirical evaluation.
