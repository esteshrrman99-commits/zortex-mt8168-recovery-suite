#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.assistant import AssistantEngine


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ZORTEX v1.3 local-first assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask")
    ask.add_argument("query", nargs="+")
    explain = sub.add_parser("explain")
    explain.add_argument("text", nargs="+")
    plan = sub.add_parser("plan")
    plan.add_argument("goal", nargs="+")
    sub.add_parser("status")
    return parser


def main() -> int:
    args = make_parser().parse_args()
    engine = AssistantEngine(ROOT, os.environ.get("ZORTEX_AI_PROVIDER", "mock"))

    if args.command == "ask":
        print(json.dumps(engine.ask(" ".join(args.query)).to_dict(), indent=2))
    elif args.command == "explain":
        print(json.dumps(engine.explain(" ".join(args.text)).to_dict(), indent=2))
    elif args.command == "plan":
        print(json.dumps([x.to_dict() for x in engine.plan(" ".join(args.goal))], indent=2))
    else:
        print(json.dumps(engine.status(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
