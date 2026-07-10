"""Known device profiles for ZORTEX."""

SCORE_711 = {
    "manufacturer": "Score",
    "model": "711",
    "platform": "MediaTek MT8168",
    "android_version": "10",
    "firmware": "vnd_tb8168p1_dsp1779111601",
    "firmware_type": "MediaTek AOSP stock firmware",
    "google_play_store": False,
    "google_mobile_services": False,
    "developer_options": "Not currently available",
    "usb_debugging": "Not currently available",
    "package_installer": "Unknown",
    "recommended_strategy": [
        "Preserve stock firmware",
        "Test ordinary APK sideloading",
        "Inspect USB interfaces from Android host phone",
        "Create backups before firmware operations",
    ],
}
