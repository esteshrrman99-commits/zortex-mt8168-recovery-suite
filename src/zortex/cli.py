"""ZORTEX command-line interface."""

import json

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from zortex.intelligence import (
    firmware_report,
    identify_device,
    save_report,
    usb_report,
)

console = Console()


def print_dictionary(title: str, data: dict) -> None:
    table = Table(title=title, show_header=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value")

    for key, value in data.items():
        if isinstance(value, list):
            value = "\n".join(f"• {item}" for item in value)
        elif isinstance(value, dict):
            value = json.dumps(value, indent=2)

        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@click.group()
@click.version_option(version="0.2.0")
def main() -> None:
    """ZORTEX MT8168 Recovery Suite."""


@main.command()
def doctor() -> None:
    """Display development environment status."""
    console.print(
        Panel.fit(
            "[bold green]ZORTEX MT8168 Recovery Suite[/bold green]\n"
            "Status: Development environment initialized.\n"
            "Mission: Backup first • Inspect second • Modify last"
        )
    )


@main.command()
def identify() -> None:
    """Display the known Score 711 device profile."""
    print_dictionary("Score 711 Device Identification", identify_device())


@main.command()
def firmware() -> None:
    """Analyze the known stock firmware profile."""
    print_dictionary("Firmware Intelligence", firmware_report())


@main.command()
def usb() -> None:
    """Inspect available USB and Android command-line tools."""
    print_dictionary("USB Host Inspection", usb_report())


@main.command()
def report() -> None:
    """Generate JSON and HTML diagnostic reports."""
    json_path, html_path = save_report()

    console.print("[bold green]Diagnostic reports generated.[/bold green]")
    console.print(f"JSON: {json_path}")
    console.print(f"HTML: {html_path}")


if __name__ == "__main__":
    main()
