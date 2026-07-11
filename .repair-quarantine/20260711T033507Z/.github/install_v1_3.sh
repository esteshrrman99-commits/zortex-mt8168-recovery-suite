#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
python -m pip install -e .
pytest -q tests/test_assistant.py
python scripts/zortex_assistant.py status
python scripts/zortex_assistant.py ask "knowledge graph orchestrator"
python scripts/zortex_assistant.py explain "FileNotFoundError"
python scripts/zortex_assistant.py plan "check repository health"
pytest -q --maxfail=1
git status
