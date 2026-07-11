#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
touch src/zortex/__init__.py
python -m pip install -e .
pytest -q tests/test_elite_diagnostics.py
python scripts/zortex_elite.py compatibility-demo
python scripts/zortex_elite.py provenance-demo
python scripts/zortex_elite.py report-demo
git status --short
