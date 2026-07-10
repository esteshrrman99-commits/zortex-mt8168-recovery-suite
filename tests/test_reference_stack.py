from zortex.reference_stack.catalog import BLOCK_MESSAGE, audit, components


def test_manifest_has_components() -> None:
    assert len(components()) >= 10


def test_deployment_is_blocked() -> None:
    report = audit()
    assert report["deployment_authorized"] is False
    assert report["deployment_decision"] == BLOCK_MESSAGE


def test_user_apps_are_separated_from_rom_components() -> None:
    report = audit()
    assert "lawnchair" in report["normal_user_apps"]
    assert "activity-launcher" in report["normal_user_apps"]
    assert "systemui" in report["rom_or_privileged_components"]
    assert "magisk" in report["rom_or_privileged_components"]
