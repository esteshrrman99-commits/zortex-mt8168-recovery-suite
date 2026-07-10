"""ZORTEX v0.6 read-only environment and restoration-readiness engine."""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BLOCK_MESSAGE = "BLOCKED: authorized restoration gate has not been satisfied."


def run_read_only(command: list[str], timeout: int = 20) -> dict[str, Any]:
    """Run a read-only host command and capture structured evidence."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "command": command,
            "return_code": None,
            "stdout": "",
            "stderr": str(exc),
        }


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def tool_version(executable: str, arguments: list[str]) -> dict[str, Any]:
    path = shutil.which(executable)

    if not path:
        return {
            "installed": False,
            "path": None,
            "version": None,
        }

    result = run_read_only([path, *arguments])

    return {
        "installed": True,
        "path": path,
        "version": result["stdout"] or result["stderr"],
    }


def doctor_report() -> dict[str, Any]:
    return {
        "generated_at": timestamp(),
        "mode": "read-only",
        "host": {
            "platform": platform.platform(),
            "system": platform.system(),
            "architecture": platform.machine(),
            "python": platform.python_version(),
        },
        "tools": {
            "git": tool_version("git", ["--version"]),
            "python": tool_version("python", ["--version"]),
            "adb": tool_version("adb", ["version"]),
            "fastboot": tool_version("fastboot", ["--version"]),
            "lsusb": tool_version("lsusb", ["--version"]),
            "mtk": tool_version("mtk", ["--help"]),
        },
        "codespaces_usb_notice": (
            "GitHub Codespaces cannot directly access a USB device attached "
            "to the user's Motorola phone."
        ),
    }


def usb_probe_report() -> dict[str, Any]:
    report: dict[str, Any] = {
        "generated_at": timestamp(),
        "mode": "read-only",
        "usb_enumeration": "Unavailable",
        "adb_devices": "Unavailable",
        "recognized_mode": "No physical USB evidence",
    }

    if shutil.which("lsusb"):
        result = run_read_only(["lsusb"])
        report["usb_enumeration"] = result
        report["usb_output_sha256"] = sha256_text(
            result["stdout"] + result["stderr"]
        )

    if shutil.which("adb"):
        result = run_read_only(["adb", "devices", "-l"])
        report["adb_devices"] = result

    return report


def mtk_inspection_report() -> dict[str, Any]:
    installed = bool(shutil.which("mtk"))

    return {
        "generated_at": timestamp(),
        "mode": "read-only",
        "mtkclient_installed": installed,
        "allowed_operations": [
            "host dependency inspection",
            "USB mode classification",
            "chip identification",
            "partition-table acquisition after authorization",
            "read-only backup planning",
        ],
        "blocked_operations": [
            "write",
            "erase",
            "format",
            "unlock",
            "payload execution",
            "security configuration modification",
        ],
        "physical_device_observed": False,
        "status": (
            "READY FOR READ-ONLY PROBING"
            if installed
            else "MTKCLIENT NOT INSTALLED"
        ),
    }


def hardware_profile() -> dict[str, Any]:
    return {
        "generated_at": timestamp(),
        "evidence_status": "User-observed; requires software verification",
        "device": {
            "brand": "SCORE",
            "model": "7T",
            "board": "P73A0-7T",
            "reported_soc_family": "MediaTek MT8168",
            "ram": "2 GB DDR",
            "storage": "32 GB eMMC",
            "android": "10",
            "build_family": "vnd_tb8168p1",
            "usb": "USB-C",
            "fcc_id": "2A3XN-SCORE7T",
        },
        "unknown_components": [
            "exact display panel",
            "touchscreen controller",
            "Wi-Fi chipset firmware",
            "audio codec",
            "kernel version",
            "DTB and DTBO",
            "partition geometry",
            "AVB topology",
            "trusted key fingerprint",
            "rollback indexes",
            "bootloader state",
        ],
    }


def readiness_report() -> dict[str, Any]:
    gates = {
        "gate_01_device_identity": False,
        "gate_02_usb_mode_identified": False,
        "gate_03_partition_table_verified": False,
        "gate_04_dual_backup_verified": False,
        "gate_05_artifact_hashes_verified": False,
        "gate_06_boot_image_parsed": False,
        "gate_07_dtb_dtbo_verified": False,
        "gate_08_hardware_matrix_complete": False,
        "gate_09_avb_chain_documented": False,
        "gate_10_rollback_indexes_recorded": False,
        "gate_11_firmware_provenance_verified": False,
        "gate_12_partition_fit_verified": False,
        "gate_13_vendor_compatibility_verified": False,
        "gate_14_authorized_trust_path_verified": False,
        "gate_15_dry_run_verified": False,
        "gate_16_human_approval_recorded": False,
    }

    passed = sum(gates.values())
    total = len(gates)

    return {
        "generated_at": timestamp(),
        "status": "BLOCKED",
        "passed_gates": passed,
        "total_gates": total,
        "readiness_percent": round((passed / total) * 100, 2),
        "gates": gates,
        "decision": BLOCK_MESSAGE,
        "next_required_evidence": [
            "Enumerate an authorized physical USB interface",
            "Acquire exact partition table read-only",
            "Create two independently verified backups",
            "Inspect boot, recovery, DTBO and vbmeta",
            "Document AVB keys and rollback indexes",
            "Identify an official or authorized trust path",
        ],
    }


def save_report(name: str, data: dict[str, Any]) -> Path:
    directory = Path("reports/v06")
    directory.mkdir(parents=True, exist_ok=True)

    path = directory / f"{name}.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
