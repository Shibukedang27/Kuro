#!/usr/bin/env python3
"""Retain bounded closure-transition evidence without changing production.

  .venv/bin/python scripts/record_normalized_audit.py --output /tmp/normalized-audit.json
Use --full-output for the larger report with all expanded event witnesses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def compact_report(report):
    """Keep all changed-merge classifications; hash repeated normalized maps."""
    for case in report["cases"]:
        comparison = case["production_vs_normalized"]
        events = []
        for event in comparison.pop("production_changed_merge_witnesses"):
            before, after = event.pop("current_normalized"), event.pop("merged_normalized")
            pending = event["queue_before"]
            expected = tuple(pending) + (event["successor"],)
            evidence = event.pop("matching_append_queue_evidence")
            event["matching_append_observed"] = any(tuple(item["queue"]) == expected for item in evidence)
            assert event["matching_append_observed"], "changed merge lacks matching queue append"
            event["normalized_equal"] = before == after
            event["current_normalized_sha256"] = hashlib.sha256(json.dumps(before).encode()).hexdigest()
            event["merged_normalized_sha256"] = hashlib.sha256(json.dumps(after).encode()).hexdigest()
            events.append(event)
        comparison["all_changed_merge_events"] = events
        for name in ("queue_differences", "visit_differences", "merge_differences"):
            differences = comparison.pop(name)
            comparison[name + "_invocation_count"] = len(differences)
        # First differences and every aligned-prefix transition mismatch remain.
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--full-output", type=Path)
    args = parser.parse_args()
    import compiler.native as native
    from scripts.audit_normalized_closures import audit_corpus
    files = [Path(native.__file__), ROOT / "scripts/audit_normalized_closures.py",
             ROOT / "scripts/profile_sparse_closures.py", Path(__file__)]
    metadata = {"python": sys.version, "platform": platform.platform(),
                "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "compiler_dirty": bool(subprocess.check_output(["git", "status", "--porcelain", "--", "compiler"], cwd=ROOT, text=True).strip()),
                "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    audit = audit_corpus(native)
    if args.full_output:
        args.full_output.parent.mkdir(parents=True, exist_ok=True)
        args.full_output.write_text(json.dumps({"metadata": metadata, "audit": audit}, indent=2) + "\n")
    result = {"metadata": metadata, "audit": compact_report(audit)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for check in ("all_outcomes_equal", "all_shared_legacy_traces_equal", "all_outer_transitions_equal",
                  "all_exact_invocation_summaries_equal", "all_trace_validations_pass"):
        assert audit[check], f"audit failed: {check}; evidence retained at {args.output}"
    print(args.output, flush=True)


if __name__ == "__main__":
    main()
