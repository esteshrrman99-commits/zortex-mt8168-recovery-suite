#!/usr/bin/env python3
"""Terminal interface for ZORTEX v0.8 ROM knowledge tools."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.rom_knowledge.catalog import (  # noqa: E402
    locked_target_profile,
    reference_profile,
    save_profile,
    save_source_report,
    scan_public_sources,
)
from zortex.rom_knowledge.compare import compare_profiles  # noqa: E402
from zortex.rom_knowledge.reporting import save_comparison  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="ZORTEX ROM knowledge engine")
    parser.add_argument(
        "command",
        choices=[
            "build-profiles",
            "sources",
            "compare",
            "report",
            "deploy-check",
        ],
    )
    args = parser.parse_args()

    reference = reference_profile()
    target = locked_target_profile()

    if args.command == "build-profiles":
        print(f"Saved: {save_profile(reference)}")
        print(f"Saved: {save_profile(target)}")
        return 0

    if args.command == "sources":
        print(json.dumps(scan_public_sources(), indent=2))
        print(f"Saved: {save_source_report()}")
        return 0

    result = compare_profiles(reference, target)

    if args.command == "compare":
        print(result.model_dump_json(indent=2))
        return 0

    if args.command == "report":
        json_path, markdown_path = save_comparison(result)
        print(f"Saved: {json_path}")
        print(f"Saved: {markdown_path}")
        return 0

    print(result.decision)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
