"""ZORTEX v0.6 CLI extension preserving the existing command group."""

from __future__ import annotations

import json

import click
from rich.console import Console
from rich.panel import Panel

from zortex.cli import main
from zortex.v06_engine import (
    doctor_report,
    hardware_profile,
    mtk_inspection_report,
    readiness_report,
    save_report,
    usb_probe_report,
)

console = Console()


def display_and_save(title: str, filename: str, data: dict) -> None:
    path = save_report(filename, data)
    console.print(Panel.fit(title, style="bold cyan"))
    console.print_json(json.dumps(data))
    console.print(f"\n[green]Saved:[/green] {path}")


@main.command("doctor-v06")
def doctor_v06() -> None:
    """Inspect the host environment and installed restoration tools."""
    display_and_save(
        "ZORTEX v0.6 Environment Doctor",
        "doctor",
        doctor_report(),
    )


@main.command("usb-probe")
def usb_probe() -> None:
    """Collect available read-only USB evidence."""
    display_and_save(
        "ZORTEX Read-Only USB Probe",
        "usb-probe",
        usb_probe_report(),
    )


@main.command("mtk-inspect")
def mtk_inspect() -> None:
    """Inspect MTKClient availability without touching a device."""
    display_and_save(
        "ZORTEX MTKClient Inspection",
        "mtk-inspect",
        mtk_inspection_report(),
    )


@main.command("hardware-profile")
def hardware_profile_command() -> None:
    """Generate the current SCORE 7T hardware profile."""
    display_and_save(
        "SCORE 7T Hardware Profile",
        "hardware-profile",
        hardware_profile(),
    )


@main.command()
def readiness() -> None:
    """Evaluate the sixteen authorized restoration gates."""
    display_and_save(
        "ZORTEX Restoration Readiness",
        "readiness",
        readiness_report(),
    )


@main.command("write-test")
def write_test() -> None:
    """Prove that mutating operations remain blocked."""
    raise click.ClickException(
        "BLOCKED: authorized restoration gate has not been satisfied."
    )
