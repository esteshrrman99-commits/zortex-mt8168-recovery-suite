from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path
from typing import Iterable

from .models import RunState, StepResult, utc_now
from .policy import enforce_command_policy

ROOT = Path.cwd()
STATE_DIR = ROOT / "artifacts" / "orchestrator"
REPORT_DIR = ROOT / "reports" / "orchestrator"


class Orchestrator:
    def __init__(self, root: Path = ROOT) -> None:
        self.root = root
        self.state_dir = root / "artifacts" / "orchestrator"
        self.report_dir = root / "reports" / "orchestrator"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def plan(self) -> list[tuple[str, list[str]]]:
        steps: list[tuple[str, list[str]]] = [
            ("discover", ["git", "status", "--short"]),
            ("syntax", [sys.executable, "-m", "compileall", "-q", "src"]),
            ("tests", [sys.executable, "-m", "pytest", "-q", "--maxfail=1"]),
        ]

        if shutil.which("ruff"):
            steps.append(("lint", ["ruff", "check", "."]))

        if shutil.which("mypy"):
            steps.append(("typecheck", ["mypy", "src"]))

        return steps

    def new_state(self, mode: str) -> RunState:
        return RunState(run_id=str(uuid.uuid4()), mode=mode)

    def save_state(self, state: RunState) -> Path:
        path = self.state_dir / "latest.json"
        path.write_text(json.dumps(state.to_dict(), indent=2) + "\n", encoding="utf-8")
        return path

    def execute(self, dry_run: bool = False) -> RunState:
        state = self.new_state("dry-run" if dry_run else "run")
        state.status = "running"
        self.save_state(state)

        for name, command in self.plan():
            state.current_step = name
            self.save_state(state)

            result = StepResult(name=name, status="planned", command=command)
            state.steps.append(result)

            if dry_run:
                result.status = "skipped"
                result.finished_at = utc_now()
                continue

            try:
                enforce_command_policy(command)
                completed = subprocess.run(
                    command,
                    cwd=self.root,
                    text=True,
                    capture_output=True,
                    check=False,
                    env={**os.environ, "ZORTEX_ORCHESTRATOR_ACTIVE": "1"},
                )
                result.returncode = completed.returncode
                result.stdout = completed.stdout[-12000:]
                result.stderr = completed.stderr[-12000:]
                result.finished_at = utc_now()
                result.status = "passed" if completed.returncode == 0 else "failed"

                if completed.returncode != 0:
                    state.status = "blocked"
                    state.blocked_reason = f"{name} failed with exit code {completed.returncode}"
                    break
            except Exception as exc:
                result.status = "blocked"
                result.stderr = str(exc)
                result.finished_at = utc_now()
                state.status = "blocked"
                state.blocked_reason = str(exc)
                break

        if state.status == "running":
            state.status = "passed"

        state.current_step = None
        state.finished_at = utc_now()
        self.save_state(state)
        self.write_report(state)
        return state

    def write_report(self, state: RunState) -> Path:
        payload = state.to_dict()
        path = self.report_dir / "acceptance.json"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def status(self) -> dict:
        path = self.state_dir / "latest.json"
        if not path.exists():
            return {"status": "not_started"}
        return json.loads(path.read_text(encoding="utf-8"))

    def hash_manifest(self, paths: Iterable[Path]) -> dict[str, dict[str, str]]:
        manifest: dict[str, dict[str, str]] = {}

        for path in paths:
            if not path.is_file():
                continue
            data = path.read_bytes()
            manifest[str(path.relative_to(self.root))] = {
                "sha256": hashlib.sha256(data).hexdigest(),
                "sha512": hashlib.sha512(data).hexdigest(),
            }

        output = self.state_dir / "hashes.json"
        output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return manifest

    def bundle(self) -> Path:
        candidates = [
            p for parent in (self.state_dir, self.report_dir)
            for p in parent.rglob("*") if p.is_file()
        ]
        self.hash_manifest(candidates)

        bundle = self.state_dir / "zortex-orchestrator-bundle.zip"
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in candidates + [self.state_dir / "hashes.json"]:
                if path.exists():
                    archive.write(path, path.relative_to(self.root))
        return bundle
