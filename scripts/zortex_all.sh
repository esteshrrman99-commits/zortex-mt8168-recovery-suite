#!/usr/bin/env bash
set -euo pipefail

echo "Running ZORTEX full read-only analysis..."
python scripts/zortex_pipeline.py run

echo
echo "Generated reports:"
find \
  artifacts \
  dashboard/reports \
  rom-analysis/reports \
  reference-stack/reports \
  reports \
  -type f 2>/dev/null | sort

echo
echo "ZORTEX analysis complete."
