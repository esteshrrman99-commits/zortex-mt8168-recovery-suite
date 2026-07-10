from zortex.dashboard.engine import (
    BLOCK_MESSAGE,
    build_dashboard_data,
)


def test_dashboard_is_read_only() -> None:
    data = build_dashboard_data()
    assert data["mode"] == "read-only"
    assert data["deployment_authorized"] is False
    assert data["decision"] == BLOCK_MESSAGE


def test_dashboard_has_reference_components() -> None:
    data = build_dashboard_data()
    assert data["statistics"]["reference_packages"] >= 10


def test_dashboard_separates_user_and_system_components() -> None:
    data = build_dashboard_data()
    assert "app.lawnchair" in data["normal_user_apps"]
    assert "com.android.systemui" in data["privileged_or_rom_packages"]
