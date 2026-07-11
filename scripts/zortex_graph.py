#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zortex.graph import KnowledgeGraph


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="ZORTEX v1.2 knowledge graph")
    sub = root.add_subparsers(dest="command", required=True)

    sub.add_parser("build")
    sub.add_parser("summary")

    query = sub.add_parser("query")
    query.add_argument("term")

    export = sub.add_parser("export")
    export.add_argument(
        "--output",
        default="artifacts/graph/knowledge-graph.json",
    )

    sub.add_parser("missing-evidence")
    return root


def main() -> int:
    args = parser().parse_args()
    graph = KnowledgeGraph(ROOT)
    graph.build()

    if args.command == "build":
        path = graph.export(ROOT / "artifacts/graph/knowledge-graph.json")
        print(path)
        return 0

    if args.command == "summary":
        print(json.dumps(graph.summary(), indent=2))
        return 0

    if args.command == "query":
        print(json.dumps(graph.query(args.term), indent=2))
        return 0

    if args.command == "export":
        path = graph.export(ROOT / args.output)
        print(path)
        return 0

    if args.command == "missing-evidence":
        print(json.dumps(graph.missing_evidence(), indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
