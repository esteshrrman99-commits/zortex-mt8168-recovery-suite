"""JSON and Markdown report generation."""

from __future__ import annotations

import json
from pathlib import Path

from zortex.rom_knowledge.models import ComparisonResult


REPORT_DIR = Path("rom-analysis/reports")


def save_comparison(result: ComparisonResult) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIR / "score7t-comparison.json"
    md_path = REPORT_DIR / "score7t-comparison.md"

    json_path.write_text(
        result.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )

    markdown = [
        "# ZORTEX SCORE 7T ROM Comparison",
        "",
        f"- Reference profile: `{result.reference_profile}`",
        f"- Target profile: `{result.target_profile}`",
        f"- Deployment authorized: `{result.deployment_authorized}`",
        "",
        "## Decision",
        "",
        result.decision,
        "",
        "## Matching packages",
        "",
    ]

    markdown.extend(
        [f"- `{item}`" for item in result.matching_packages]
        or ["- None recorded"]
    )

    markdown.extend(["", "## Missing from target", ""])
    markdown.extend(
        [f"- `{item}`" for item in result.missing_from_target]
        or ["- None"]
    )

    markdown.extend(["", "## Extra on target", ""])
    markdown.extend(
        [f"- `{item}`" for item in result.extra_on_target]
        or ["- None"]
    )

    markdown.extend(["", "## Platform mismatches", ""])
    markdown.extend(
        [f"- {item}" for item in result.platform_mismatches]
        or ["- No confirmed mismatch; unresolved fields may remain."]
    )

    markdown.extend(
        [
            "",
            "## Interpretation",
            "",
            "Missing ROM-level packages cannot be reproduced by copying APKs.",
            "They require a compatible system image, framework, vendor layer,",
            "kernel, partition layout, and authorized installation route.",
            "",
        ]
    )

    md_path.write_text("\n".join(markdown), encoding="utf-8")
    return json_path, md_path
