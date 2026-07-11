from __future__ import annotations

import json
import re
from pathlib import Path

from .models import AssistantResponse, EvidenceItem, PlanItem, utc_now
from .policy import validate_command
from .providers import load_provider


class AssistantEngine:
    def __init__(self, root: Path, provider_name: str = "mock") -> None:
        self.root = root.resolve()
        self.provider = load_provider(provider_name)
        self.audit_dir = self.root / "artifacts" / "assistant"
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def ask(self, query: str) -> AssistantResponse:
        evidence = self.search(query)
        context = "\n".join(
            f"{item.path}:{item.line or 0}: {item.excerpt}"
            for item in evidence[:20]
        )
        response = AssistantResponse(
            query=query,
            answer=self.provider.summarize(query, context),
            evidence=evidence,
            missing_evidence=[] if evidence else [
                "No matching repository evidence was found."
            ],
            recommendations=[
                "Review cited files before editing.",
                "Run the smallest relevant test, then the full suite.",
            ],
        )
        self._audit("ask", response.to_dict())
        return response

    def explain(self, text: str) -> AssistantResponse:
        lowered = text.lower()
        inference: list[str] = []
        recommendations: list[str] = []

        if "modulenotfounderror" in lowered:
            inference.append("The package or import path may be incomplete.")
            recommendations += [
                "Confirm the module file exists.",
                "Run python -m pip install -e .",
                "Run the smallest failing test.",
            ]
        elif "filenotfounderror" in lowered or "no such file" in lowered:
            inference.append("The path or filename likely does not match the current location.")
            recommendations += [
                "Run pwd.",
                "Run find . -maxdepth 4 -iname '*keyword*'.",
                "Use the exact returned path.",
            ]
        else:
            inference.append("No specialized deterministic rule matched.")
            recommendations.append("Inspect the first traceback and repository evidence.")

        response = AssistantResponse(
            query=text,
            answer="Deterministic local explanation.",
            evidence=self.search(text),
            inference=inference,
            recommendations=recommendations,
        )
        self._audit("explain", response.to_dict())
        return response

    def plan(self, goal: str) -> list[PlanItem]:
        steps = [
            PlanItem(1, "Inspect repository status", ["git", "status", "--short"]),
            PlanItem(2, "Review knowledge graph", ["python", "scripts/zortex_graph.py", "summary"]),
            PlanItem(3, "Run tests", ["python", "-m", "pytest", "-q"]),
        ]
        if any(x in goal.lower() for x in {"flash", "erase", "unlock", "format", "repartition"}):
            steps.append(PlanItem(4, "Reject device-mutating request", [], False, "blocked"))

        result: list[PlanItem] = []
        for step in steps:
            if not step.command:
                result.append(step)
                continue
            ok, message = validate_command(step.command)
            result.append(PlanItem(
                step.order,
                f"{step.action}: {message}",
                step.command,
                True,
                "proposed" if ok else "blocked",
            ))

        self._audit("plan", {
            "goal": goal,
            "items": [x.to_dict() for x in result],
            "generated_at": utc_now(),
        })
        return result

    def status(self) -> dict[str, object]:
        records = sorted(self.audit_dir.glob("*.json"))
        return {
            "provider": self.provider.name,
            "mode": "local-first",
            "automatic_shell_execution": False,
            "human_approval_required": True,
            "audit_record_count": len(records),
            "latest_audit": records[-1].name if records else None,
        }

    def search(self, query: str, limit: int = 20) -> list[EvidenceItem]:
        tokens = [x.lower() for x in re.findall(r"[A-Za-z0-9_./-]+", query) if len(x) >= 3]
        if not tokens:
            return []

        ignored = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
        allowed = {".py", ".md", ".txt", ".json", ".toml", ".yml", ".yaml"}
        found: list[EvidenceItem] = []

        for path in sorted(self.root.rglob("*")):
            if len(found) >= limit:
                break
            if not path.is_file() or any(part in ignored for part in path.parts):
                continue
            if path.suffix.lower() not in allowed:
                continue

            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue

            relative = path.relative_to(self.root).as_posix()
            for number, line in enumerate(lines, 1):
                haystack = f"{relative} {line}".lower()
                if any(token in haystack for token in tokens):
                    found.append(EvidenceItem(relative, number, line.strip()[:300]))
                    if len(found) >= limit:
                        break
        return found

    def _audit(self, action: str, payload: dict[str, object]) -> Path:
        index = len(list(self.audit_dir.glob("*.json"))) + 1
        path = self.audit_dir / f"{index:04d}-{action}.json"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path
