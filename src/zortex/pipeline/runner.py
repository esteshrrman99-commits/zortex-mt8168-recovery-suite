"""ZORTEX v1.0 read-only analysis pipeline."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
ARTIFACT_DIR = ROOT / "artifacts"
BLOCK_MESSAGE = (
    "BLOCKED: analysis pipeline does not authorize firmware deployment."
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    return {
        "command": command,
        "return_code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "passed": result.returncode == 0,
    }


def hash_file(path: Path) -> dict[str, str]:
    data = path.read_bytes()

    return {
        "path": str(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "sha512": hashlib.sha512(data).hexdigest(),
    }


def collect_report_files() -> list[Path]:
    patterns = [
        "reports/**/*.json",
        "reports/**/*.html",
        "reports/**/*.md",
        "rom-analysis/reports/**/*.json",
        "rom-analysis/reports/**/*.md",
        "dashboard/reports/**/*.json",
        "dashboard/reports/**/*.html",
        "dashboard/reports/**/*.md",
        "reference-stack/reports/**/*.json",
    ]

    paths: list[Path] = []

    for pattern in patterns:
        paths.extend(ROOT.glob(pattern))

    return sorted({path for path in paths if path.is_file()})


def execute_pipeline() -> dict[str, Any]:
    steps = [
        {
            "name": "reference-audit",
            "command": [sys.executable, "scripts/reference_stack.py", "audit"],
        },
        {
            "name": "build-rom-profiles",
            "command": [sys.executable, "scripts/rom_knowledge.py", "build-profiles"],
        },
        {
            "name": "source-inventory",
            "command": [sys.executable, "scripts/rom_knowledge.py", "sources"],
        },
        {
            "name": "rom-comparison",
            "command": [sys.executable, "scripts/rom_knowledge.py", "report"],
        },
        {
            "name": "dashboard-build",
            "command": [sys.executable, "scripts/zortex_dashboard.py", "build"],
        },
        {
            "name": "tests",
            "command": [sys.executable, "-m", "pytest", "-q"],
        },
    ]

    if os.getenv("PYTEST_CURRENT_TEST"):
        steps = [step for step in steps if step["name"] != "tests"]

    results: list[dict[str, Any]] = []

    for step in steps:
        result = run_command(step["command"])
        result["name"] = step["name"]
        results.append(result)

        if not result["passed"]:
            break

    report_files = collect_report_files()
    manifests = [hash_file(path) for path in report_files]

    passed = all(result["passed"] for result in results)

    return {
        "generated_at": now_iso(),
        "project": "ZORTEX SCORE 7T Analysis Platform",
        "version": "1.0.0",
        "mode": "read-only",
        "pipeline_passed": passed,
        "steps": results,
        "artifacts": manifests,
        "artifact_count": len(manifests),
        "deployment_authorized": False,
        "decision": BLOCK_MESSAGE,
    }


def save_pipeline_report(report: dict[str, Any]) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    path = ARTIFACT_DIR / "pipeline-report.json"
    path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    return path
