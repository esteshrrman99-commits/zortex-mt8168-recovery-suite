"""Read-only reference-stack catalog for the SCORE 7T laboratory."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MANIFEST = Path("reference-stack/manifests/components.json")
BLOCK_MESSAGE = (
    "BLOCKED: reference-stack analysis does not authorize device deployment."
)


@dataclass(frozen=True)
class Component:
    id: str
    display_name: str
    package: str
    classification: str
    source: str
    installable_as_normal_apk: bool | str
    requires_matching_rom: bool
    notes: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Component":
        return cls(
            id=str(value["id"]),
            display_name=str(value["display_name"]),
            package=str(value["package"]),
            classification=str(value["classification"]),
            source=str(value["source"]),
            installable_as_normal_apk=value["installable_as_normal_apk"],
            requires_matching_rom=bool(value["requires_matching_rom"]),
            notes=str(value["notes"]),
        )


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def components() -> list[Component]:
    return [Component.from_dict(item) for item in load_manifest()["components"]]


def audit() -> dict[str, Any]:
    items = components()
    user_apps = [item.id for item in items if item.classification == "user_app"]
    rom_components = [
        item.id
        for item in items
        if item.classification
        in {
            "privileged_system_app",
            "framework_component",
            "boot_component",
            "vendor_dependent_component",
        }
    ]

    raw = MANIFEST.read_bytes()
    return {
        "component_count": len(items),
        "normal_user_apps": user_apps,
        "rom_or_privileged_components": rom_components,
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "deployment_authorized": False,
        "deployment_decision": BLOCK_MESSAGE,
    }
