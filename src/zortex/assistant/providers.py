from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Provider(Protocol):
    name: str

    def summarize(self, prompt: str, context: str) -> str:
        ...


@dataclass
class MockProvider:
    name: str = "mock"

    def summarize(self, prompt: str, context: str) -> str:
        if not context.strip():
            return "No verified repository context was available."
        return "Repository-grounded mock summary:\n" + context[:1600]


def load_provider(name: str | None) -> Provider:
    normalized = (name or "mock").strip().lower()
    if normalized != "mock":
        raise RuntimeError(
            "External providers are disabled until a reviewed adapter and "
            "environment-variable gate are configured."
        )
    return MockProvider()
