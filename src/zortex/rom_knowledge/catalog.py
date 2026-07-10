"""ROM catalog loading, inventory generation, and source inspection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from zortex.reference_stack.catalog import components as reference_components
from zortex.rom_knowledge.models import DeviceProfile, PackageRecord


ROOT = Path.cwd()
INVENTORY_DIR = ROOT / "rom-analysis" / "inventories"
SOURCE_DIR = ROOT / "reference-stack" / "sources"


def reference_profile() -> DeviceProfile:
    records: list[PackageRecord] = []

    for component in reference_components():
        records.append(
            PackageRecord(
                package=component.package,
                display_name=component.display_name,
                classification=component.classification,
                source=component.source,
                privileged=component.classification
                in {
                    "privileged_system_app",
                    "framework_component",
                    "boot_component",
                    "vendor_dependent_component",
                },
                requires_matching_rom=component.requires_matching_rom,
                notes=component.notes,
            )
        )

    return DeviceProfile(
        profile_id="score7t-working-reference",
        device_name="SCORE 7T Working Reference",
        board="P73A0-7T",
        soc="MediaTek MT8168",
        architecture="unknown",
        android_version="10",
        api_level=29,
        kernel=None,
        treble=True,
        vndk="28/29 observed",
        ram="2 GB",
        storage="32 GB",
        packages=records,
    )


def locked_target_profile() -> DeviceProfile:
    return DeviceProfile(
        profile_id="score7t-locked-target",
        device_name="SCORE 7T Locked Target",
        board="P73A0-7T",
        soc="MediaTek MT8168",
        architecture="unknown",
        android_version="10",
        api_level=29,
        kernel=None,
        treble=None,
        vndk=None,
        ram="2 GB",
        storage="32 GB",
        packages=[],
    )


def save_profile(profile: DeviceProfile) -> Path:
    INVENTORY_DIR.mkdir(parents=True, exist_ok=True)
    path = INVENTORY_DIR / f"{profile.profile_id}.json"
    path.write_text(
        profile.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def load_profile(path: Path) -> DeviceProfile:
    return DeviceProfile.model_validate_json(path.read_text(encoding="utf-8"))


def scan_public_sources() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []

    if SOURCE_DIR.exists():
        for directory in sorted(SOURCE_DIR.iterdir()):
            if not directory.is_dir():
                continue

            git_dir = directory / ".git"
            entries.append(
                {
                    "name": directory.name,
                    "path": str(directory),
                    "git_repository": git_dir.exists(),
                    "has_android_manifest": bool(
                        list(directory.rglob("AndroidManifest.xml"))
                    ),
                    "has_gradle": (
                        (directory / "build.gradle").exists()
                        or (directory / "build.gradle.kts").exists()
                        or bool(list(directory.glob("*.gradle")))
                    ),
                }
            )

    return {
        "source_root": str(SOURCE_DIR),
        "repository_count": len(entries),
        "repositories": entries,
    }


def save_source_report() -> Path:
    report = scan_public_sources()
    output = ROOT / "rom-analysis" / "reports" / "source-inventory.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return output
