from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EvidenceItem:
    path: str
    line: int | None
    excerpt: str
    kind: str = "verified_evidence"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlanItem:
    order: int
    action: str
    command: list[str] = field(default_factory=list)
    requires_approval: bool = True
    status: str = "proposed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AssistantResponse:
    query: str
    answer: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    inference: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    blocked_operations: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "answer": self.answer,
            "evidence": [x.to_dict() for x in self.evidence],
            "inference": self.inference,
            "missing_evidence": self.missing_evidence,
            "blocked_operations": self.blocked_operations,
            "recommendations": self.recommendations,
            "generated_at": self.generated_at,
        }
