#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
touch src/zortex/__init__.py
python -m pip install -e .
pytest -q tests/test_sdk_dashboard.py
python scripts/zortex_sdk_dashboard.py profile-add --id score7t-711 --manufacturer Keefe --model 711 --chipset MT8168 --architecture arm64-v8a --android 10
python scripts/zortex_sdk_dashboard.py timeline-add --type milestone --summary "SDK dashboard installed"
python scripts/zortex_sdk_dashboard.py kb-add --title "SCORE 7T Profile" --category device --content "Model 711, MT8168, Android 10" --tags score7t,mt8168
python scripts/zortex_sdk_dashboard.py dashboard-build
python scripts/zortex_sdk_dashboard.py health
git status --short
