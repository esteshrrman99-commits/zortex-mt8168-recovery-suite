#!/usr/bin/env python3
"""ZORTEX v0.9 dashboard terminal interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.dashboard.engine import (  # noqa: E402
    BLOCK_MESSAGE,
    build_all_reports,
    build_dashboard_data,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="ZORTEX ROM dashboard")
    parser.add_argument(
        "command",
        choices=["summary", "build", "deploy-check"],
    )
    args = parser.parse_args()

    if args.command == "summary":
        print(json.dumps(build_dashboard_data()["statistics"], indent=2))
        return 0

    if args.command == "build":
        json_path, html_path, md_path = build_all_reports()
        print(f"Saved JSON: {json_path}")
        print(f"Saved HTML: {html_path}")
        print(f"Saved Markdown: {md_path}")
        return 0

    print(BLOCK_MESSAGE)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
