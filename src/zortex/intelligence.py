"""Device, firmware, USB, and reporting intelligence."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from zortex.device_profile import SCORE_711


def run_command(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return (result.stdout or result.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"Unavailable: {exc}"


def identify_device() -> dict:
    return SCORE_711.copy()


def firmware_report() -> dict:
    profile = identify_device()

    return {
        "model": profile["model"],
        "platform": profile["platform"],
        "android_version": profile["android_version"],
        "firmware": profile["firmware"],
        "firmware_type": profile["firmware_type"],
        "google_play_store": profile["google_play_store"],
        "google_mobile_services": profile["google_mobile_services"],
        "assessment": (
            "The available evidence is consistent with a minimal MediaTek "
            "AOSP stock build rather than corrupted Google Play installation."
        ),
    }


def usb_report() -> dict:
    tools = {
        "adb": shutil.which("adb"),
        "fastboot": shutil.which("fastboot"),
        "lsusb": shutil.which("lsusb"),
    }

    report = {
        "host_platform": platform.platform(),
        "codespaces_notice": (
            "GitHub Codespaces cannot directly access a tablet physically "
            "connected to the user's phone."
        ),
        "tools": tools,
        "usb_devices": "Not inspected",
        "adb_devices": "Not inspected",
    }

    if tools["lsusb"]:
        report["usb_devices"] = run_command(["lsusb"])

    if tools["adb"]:
        report["adb_devices"] = run_command(["adb", "devices", "-l"])

    return report


def complete_report() -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "ZORTEX MT8168 Recovery Suite",
        "policy": "Backup first. Inspect second. Modify last.",
        "device": identify_device(),
        "firmware": firmware_report(),
        "usb": usb_report(),
    }


def save_report(output_directory: str = "reports") -> tuple[Path, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    data = complete_report()
    serialized = json.dumps(data, indent=2)

    json_path = output / "score-711-report.json"
    html_path = output / "score-711-report.html"

    json_path.write_text(serialized + "\n", encoding="utf-8")

    html_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZORTEX Score 711 Report</title>
<style>
body {{
    font-family: system-ui, sans-serif;
    max-width: 1000px;
    margin: auto;
    padding: 24px;
}}
pre {{
    background: #111;
    color: #eee;
    padding: 18px;
    border-radius: 10px;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}}
</style>
</head>
<body>
<h1>ZORTEX Score 711 Diagnostic Report</h1>
<p>Backup first. Inspect second. Modify last.</p>
<pre>{serialized}</pre>
</body>
</html>
""",
        encoding="utf-8",
    )

    return json_path, html_path
