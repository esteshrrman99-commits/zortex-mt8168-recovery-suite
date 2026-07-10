"""Read-only comparison engine for Android ROM profiles."""

from __future__ import annotations

from zortex.rom_knowledge.models import ComparisonResult, DeviceProfile


BLOCK_MESSAGE = (
    "BLOCKED: comparison evidence does not authorize firmware deployment."
)


def compare_profiles(
    reference: DeviceProfile,
    target: DeviceProfile,
) -> ComparisonResult:
    reference_map = {item.package: item for item in reference.packages}
    target_map = {item.package: item for item in target.packages}

    matching = sorted(reference_map.keys() & target_map.keys())
    missing = sorted(reference_map.keys() - target_map.keys())
    extra = sorted(target_map.keys() - reference_map.keys())

    conflicts: list[dict[str, str]] = []
    for package in matching:
        left = reference_map[package]
        right = target_map[package]

        if left.classification != right.classification:
            conflicts.append(
                {
                    "package": package,
                    "reference": left.classification,
                    "target": right.classification,
                }
            )

    platform_mismatches: list[str] = []
    comparisons = {
        "board": (reference.board, target.board),
        "soc": (reference.soc, target.soc),
        "architecture": (reference.architecture, target.architecture),
        "android_version": (
            reference.android_version,
            target.android_version,
        ),
        "api_level": (reference.api_level, target.api_level),
        "kernel": (reference.kernel, target.kernel),
        "treble": (reference.treble, target.treble),
        "vndk": (reference.vndk, target.vndk),
    }

    for field, values in comparisons.items():
        left, right = values
        if left is not None and right is not None and left != right:
            platform_mismatches.append(
                f"{field}: reference={left!r}, target={right!r}"
            )

    return ComparisonResult(
        reference_profile=reference.profile_id,
        target_profile=target.profile_id,
        matching_packages=matching,
        missing_from_target=missing,
        extra_on_target=extra,
        classification_conflicts=conflicts,
        platform_mismatches=platform_mismatches,
        deployment_authorized=False,
        decision=BLOCK_MESSAGE,
    )
