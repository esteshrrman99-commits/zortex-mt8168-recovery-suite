#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.orchestrator import Orchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ZORTEX v2.0 repository orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("plan", "dry-run", "run", "resume", "status", "report", "bundle"):
        sub.add_parser(name)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    engine = Orchestrator(ROOT)

    if args.command == "plan":
        print(json.dumps(
            [{"name": name, "command": command} for name, command in engine.plan()],
            indent=2,
        ))
        return 0

    if args.command == "dry-run":
        state = engine.execute(dry_run=True)
        print(json.dumps(state.to_dict(), indent=2))
        return 0

    if args.command in {"run", "resume"}:
        state = engine.execute(dry_run=False)
        print(json.dumps(state.to_dict(), indent=2))
        return 0 if state.status == "passed" else 1

    if args.command == "status":
        print(json.dumps(engine.status(), indent=2))
        return 0

    if args.command == "report":
        status = engine.status()
        path = engine.report_dir / "acceptance.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        print(path)
        return 0

    if args.command == "bundle":
        print(engine.bundle())
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
