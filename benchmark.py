"""
benchmark.py - Empirical evaluation comparing Baseline vs Optimised systems.
Run from project root: python benchmark.py

Metrics collected:
  - Total method calls per submission
  - Per-method call breakdown
  - Average / min / max execution time over N runs
  - Speedup factor and call reduction percentage
"""
import json
import time
import statistics

# ── Original (Baseline) ─────────────────────────────────────────────────────
from Original.main import create_system as create_baseline
import Original.metrics as baseline_metrics

# ── Optimised ────────────────────────────────────────────────────────────────
from Optimised.main import create_system as create_optimised
import Optimised.metrics as optimised_metrics

# ── Configuration ────────────────────────────────────────────────────────────
N_RUNS = 200              # number of benchmark iterations per system
DB_DELAY = 0.001          # 1 ms simulated I/O latency per database operation

SAMPLE_SUBMISSION = {
    "title": "Advanced Machine Learning Techniques for Scientific Review",
    "content": "This paper presents novel approaches to automated review workflows...",
    "author": "researcher_001",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _run_system(create_fn, metrics_module, delay, data):
    """Creates a fresh system, runs one submission, returns (elapsed_ms, report)."""
    metrics_module.tracker.reset()
    ui = create_fn(simulation_delay=delay)
    t0 = time.perf_counter()
    ui.submitResearchOutput(data.copy(), researcher_id="researcher_001")
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, metrics_module.tracker.report()


def run_benchmark(create_fn, metrics_module, label, n_runs=N_RUNS, delay=DB_DELAY):
    """Runs n_runs iterations and aggregates timing + call statistics."""
    times = []
    last_report = None

    for _ in range(n_runs):
        elapsed, report = _run_system(create_fn, metrics_module, delay, SAMPLE_SUBMISSION)
        times.append(elapsed)
        last_report = report

    return {
        "system": label,
        "n_runs": n_runs,
        "calls_per_run": last_report["total_calls"],
        "avg_time_ms": round(statistics.mean(times), 4),
        "median_time_ms": round(statistics.median(times), 4),
        "stdev_time_ms": round(statistics.stdev(times), 4) if len(times) > 1 else 0.0,
        "min_time_ms": round(min(times), 4),
        "max_time_ms": round(max(times), 4),
        "method_breakdown": last_report["per_method"],
    }


# ── Reporting ────────────────────────────────────────────────────────────────

def print_summary(b: dict, o: dict):
    W = 70
    print("=" * W)
    print("  EMPIRICAL EVALUATION: BASELINE vs OPTIMISED")
    print(f"  (n={b['n_runs']} runs each, DB delay={DB_DELAY*1000:.1f} ms/op)")
    print("=" * W)

    rows = [
        ("Method calls per run",    "calls_per_run",    ""),
        ("Average execution time",  "avg_time_ms",      " ms"),
        ("Median execution time",   "median_time_ms",   " ms"),
        ("Std deviation",           "stdev_time_ms",    " ms"),
        ("Min execution time",      "min_time_ms",      " ms"),
        ("Max execution time",      "max_time_ms",      " ms"),
    ]

    print(f"\n{'Metric':<32} {'Baseline':>12} {'Optimised':>12} {'Delta':>12}")
    print("-" * W)
    for label, key, unit in rows:
        b_val = b[key]
        o_val = o[key]
        if isinstance(b_val, float):
            delta = f"{((b_val - o_val) / b_val * 100):+.1f}%" if b_val else "N/A"
            print(f"{label:<32} {str(b_val)+unit:>12} {str(o_val)+unit:>12} {delta:>12}")
        else:
            delta = f"-{b_val - o_val} ({(b_val - o_val)/b_val*100:.1f}%)" if b_val else "N/A"
            print(f"{label:<32} {str(b_val)+unit:>12} {str(o_val)+unit:>12} {delta:>12}")

    speedup = b["avg_time_ms"] / o["avg_time_ms"] if o["avg_time_ms"] else float("inf")
    print(f"\n  Speedup factor: {speedup:.2f}x")

    print("\n" + "=" * W)
    print("  METHOD CALL BREAKDOWN")
    print("=" * W)

    all_methods = sorted(
        set(b["method_breakdown"]) | set(o["method_breakdown"])
    )
    print(f"\n{'Method':<48} {'Baseline':>10} {'Optimised':>10}")
    print("-" * W)
    for m in all_methods:
        b_calls = b["method_breakdown"].get(m, {}).get("calls", 0)
        o_calls = o["method_breakdown"].get(m, {}).get("calls", 0)
        # Shorten display name: ClassName.method_name
        parts = m.split(".")
        short = f"{parts[-2]}.{parts[-1]}" if len(parts) >= 2 else m
        diff = ""
        if b_calls != o_calls:
            diff = f"  ({'new' if b_calls == 0 else 'removed' if o_calls == 0 else f'Δ{o_calls-b_calls:+d}'})"
        print(f"{short:<48} {str(b_calls):>10} {str(o_calls):>10}{diff}")

    print("\n" + "=" * W)
    print("  COMPLEXITY METRICS (static analysis)")
    print("=" * W)
    print_complexity_table()


def print_complexity_table():
    """Prints a static complexity comparison derived from source code analysis."""
    rows = [
        # (Component,              Baseline methods, Optimised methods, Note)
        ("Validator",              1, 1, "unchanged"),
        ("Database",               3, 3, "saveScore→saveScoresBatch"),
        ("Reviewer",               2, 2, "unchanged"),
        ("ReviewerManager",        3, 1, "3 methods merged to 1"),
        ("EvaluationManager",      4, 1, "4 methods merged to 1 + DecisionEngine"),
        ("NotificationService",    3, 1, "3 notify methods merged to 1"),
        ("SubmissionController",   1, 1, "fewer dependencies (5→4)"),
        ("UI",                     3, 3, "unchanged"),
        ("DecisionEngine",         0, 1, "new: centralises decision logic"),
    ]
    print(f"\n{'Component':<28} {'B methods':>10} {'O methods':>10}  Note")
    print("-" * 70)
    for comp, b_m, o_m, note in rows:
        print(f"{comp:<28} {b_m:>10} {o_m:>10}  {note}")

    total_b = sum(r[1] for r in rows)
    total_o = sum(r[2] for r in rows)
    reduction = (total_b - total_o) / total_b * 100
    print("-" * 70)
    print(f"{'TOTAL':<28} {total_b:>10} {total_o:>10}  -{total_b-total_o} methods ({reduction:.1f}% reduction)")

    print("\n  Coupling (direct class dependencies per controller):")
    print(f"    SubmissionController baseline dependencies : 5")
    print(f"    SubmissionController optimised dependencies: 4  (Reviewer removed)")


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Running {N_RUNS} iterations per system...\n")

    print("  [1/2] Benchmarking baseline system...")
    baseline_result = run_benchmark(create_baseline, baseline_metrics, "Baseline")
    print("  [2/2] Benchmarking optimised system...")
    optimised_result = run_benchmark(create_optimised, optimised_metrics, "Optimised")

    print_summary(baseline_result, optimised_result)

    # Save raw results to JSON for report inclusion
    with open("benchmark_results.json", "w") as f:
        json.dump(
            {"baseline": baseline_result, "optimised": optimised_result},
            f, indent=2,
        )
    print("\n  Raw results saved to benchmark_results.json")
