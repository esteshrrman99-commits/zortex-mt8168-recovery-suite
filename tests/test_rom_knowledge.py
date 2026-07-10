from zortex.rom_knowledge.catalog import (
    locked_target_profile,
    reference_profile,
)
from zortex.rom_knowledge.compare import compare_profiles


def test_reference_profile_contains_packages() -> None:
    profile = reference_profile()
    assert len(profile.packages) >= 10


def test_target_profile_starts_without_inferred_packages() -> None:
    profile = locked_target_profile()
    assert profile.packages == []


def test_comparison_is_read_only_and_blocked() -> None:
    result = compare_profiles(
        reference_profile(),
        locked_target_profile(),
    )
    assert result.deployment_authorized is False
    assert result.decision.startswith("BLOCKED:")
    assert "com.android.systemui" in result.missing_from_target
