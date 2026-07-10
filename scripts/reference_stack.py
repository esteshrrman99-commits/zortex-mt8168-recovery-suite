#!/usr/bin/env python3
"""Terminal interface for the ZORTEX reference-stack laboratory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.reference_stack.catalog import (  # noqa: E402
    BLOCK_MESSAGE,
    audit,
    components,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="ZORTEX reference-stack lab")
    parser.add_argument(
        "command",
        choices=["list", "audit", "deploy-check", "sources"],
    )
    args = parser.parse_args()

    if args.command == "list":
        for item in components():
            print(
                f"{item.id:24} "
                f"{item.classification:28} "
                f"{item.package}"
            )
        return 0

    if args.command == "sources":
        for item in components():
            print(f"{item.id}: {item.source}")
        return 0

    if args.command == "audit":
        report = audit()
        output = ROOT / "reference-stack/reports/audit.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        print(f"Saved: {output}")
        return 0

    print(BLOCK_MESSAGE)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
