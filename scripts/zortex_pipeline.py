#!/usr/bin/env python3
"""Run the complete ZORTEX read-only analysis pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.pipeline.runner import (  # noqa: E402
    BLOCK_MESSAGE,
    execute_pipeline,
    save_pipeline_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="ZORTEX analysis pipeline")
    parser.add_argument(
        "command",
        choices=["run", "status", "deploy-check"],
    )
    args = parser.parse_args()

    if args.command == "deploy-check":
        print(BLOCK_MESSAGE)
        return 2

    report_path = ROOT / "artifacts" / "pipeline-report.json"

    if args.command == "status":
        if not report_path.exists():
            print("No pipeline report exists. Run: python scripts/zortex_pipeline.py run")
            return 1

        print(report_path.read_text(encoding="utf-8"))
        return 0

    report = execute_pipeline()
    path = save_pipeline_report(report)

    print(json.dumps(report, indent=2))
    print(f"\nSaved: {path}")

    return 0 if report["pipeline_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
