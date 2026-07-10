"""Typed models for the ZORTEX ROM knowledge engine."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ComponentClass = Literal[
    "user_app",
    "privileged_system_app",
    "framework_component",
    "boot_component",
    "vendor_dependent_component",
    "optional_reference_only",
    "unknown",
]


class PackageRecord(BaseModel):
    package: str
    display_name: str
    classification: ComponentClass
    version: str | None = None
    source: str | None = None
    partition: str | None = None
    privileged: bool = False
    requires_matching_rom: bool = False
    permissions: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    notes: str = ""


class DeviceProfile(BaseModel):
    profile_id: str
    device_name: str
    board: str | None = None
    soc: str | None = None
    architecture: str | None = None
    android_version: str | None = None
    api_level: int | None = None
    kernel: str | None = None
    treble: bool | None = None
    vndk: str | None = None
    ram: str | None = None
    storage: str | None = None
    packages: list[PackageRecord] = Field(default_factory=list)


class ComparisonResult(BaseModel):
    reference_profile: str
    target_profile: str
    matching_packages: list[str]
    missing_from_target: list[str]
    extra_on_target: list[str]
    classification_conflicts: list[dict[str, str]]
    platform_mismatches: list[str]
    deployment_authorized: bool = False
    decision: str
