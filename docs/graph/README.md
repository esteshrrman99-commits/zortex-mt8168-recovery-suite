# ZORTEX v1.2 Knowledge Graph

The knowledge graph converts repository files, modules, tests, workflows,
documentation, reports, artifacts, and Python imports into a deterministic
read-only graph.

## Commands

```bash
python scripts/zortex_graph.py build
python scripts/zortex_graph.py summary
python scripts/zortex_graph.py query orchestrator
python scripts/zortex_graph.py export
python scripts/zortex_graph.py missing-evidence
```

## Default export

```text
artifacts/graph/knowledge-graph.json
```

## Current relationships

- repository `contains` path
- directory `contains` file
- Python module `imports` module

## Safety

The graph performs repository inspection only. It does not write to devices,
modify firmware, bypass access controls, or authorize restoration.
