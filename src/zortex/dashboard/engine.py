"""ZORTEX v0.9 read-only dashboard engine."""

from __future__ import annotations

import html
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from zortex.reference_stack.catalog import audit as reference_audit
from zortex.rom_knowledge.catalog import (
    locked_target_profile,
    reference_profile,
    scan_public_sources,
)
from zortex.rom_knowledge.compare import compare_profiles


ROOT = Path.cwd()
REPORT_DIR = ROOT / "dashboard" / "reports"
BLOCK_MESSAGE = (
    "BLOCKED: dashboard analysis does not authorize firmware deployment."
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_dashboard_data() -> dict[str, Any]:
    reference = reference_profile()
    target = locked_target_profile()
    comparison = compare_profiles(reference, target)
    source_report = scan_public_sources()
    ref_audit = reference_audit()

    classifications = Counter(
        package.classification for package in reference.packages
    )

    privileged_packages = sorted(
        package.package
        for package in reference.packages
        if package.privileged
    )

    normal_apps = sorted(
        package.package
        for package in reference.packages
        if package.classification == "user_app"
    )

    dependency_edges: list[dict[str, str]] = []

    for package in reference.packages:
        if package.requires_matching_rom:
            dependency_edges.append(
                {
                    "component": package.package,
                    "depends_on": "matching_rom_framework",
                }
            )

        if package.privileged:
            dependency_edges.append(
                {
                    "component": package.package,
                    "depends_on": "privileged_system_permissions",
                }
            )

    return {
        "generated_at": now_iso(),
        "project": "ZORTEX SCORE 7T ROM Analysis Dashboard",
        "mode": "read-only",
        "reference_profile": reference.model_dump(),
        "target_profile": target.model_dump(),
        "comparison": comparison.model_dump(),
        "reference_audit": ref_audit,
        "source_inventory": source_report,
        "statistics": {
            "reference_packages": len(reference.packages),
            "target_packages_verified": len(target.packages),
            "missing_from_target": len(comparison.missing_from_target),
            "matching_packages": len(comparison.matching_packages),
            "source_repositories": source_report["repository_count"],
            "classifications": dict(classifications),
        },
        "normal_user_apps": normal_apps,
        "privileged_or_rom_packages": privileged_packages,
        "dependency_edges": dependency_edges,
        "deployment_authorized": False,
        "decision": BLOCK_MESSAGE,
    }


def save_json(data: dict[str, Any]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "dashboard.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def _list_items(values: list[str]) -> str:
    if not values:
        return "<li>None recorded</li>"

    return "".join(f"<li><code>{html.escape(value)}</code></li>" for value in values)


def save_html(data: dict[str, Any]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    statistics = data["statistics"]
    comparison = data["comparison"]

    classification_rows = "".join(
        (
            "<tr>"
            f"<td>{html.escape(name)}</td>"
            f"<td>{count}</td>"
            "</tr>"
        )
        for name, count in sorted(statistics["classifications"].items())
    )

    mismatch_rows = _list_items(comparison["platform_mismatches"])
    missing_rows = _list_items(comparison["missing_from_target"])
    user_app_rows = _list_items(data["normal_user_apps"])
    privileged_rows = _list_items(data["privileged_or_rom_packages"])

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZORTEX ROM Dashboard</title>
<style>
body {{
  font-family: system-ui, sans-serif;
  max-width: 1100px;
  margin: auto;
  padding: 24px;
  background: #111827;
  color: #f9fafb;
}}
h1, h2 {{ color: #67e8f9; }}
.card {{
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 12px;
  padding: 18px;
  margin: 16px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(180px,1fr));
  gap: 12px;
}}
.metric {{
  background: #0f172a;
  border-radius: 10px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  font-size: 1.8rem;
}}
table {{
  width: 100%;
  border-collapse: collapse;
}}
th, td {{
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid #374151;
}}
code {{
  color: #a7f3d0;
  overflow-wrap: anywhere;
}}
.blocked {{
  background: #451a1a;
  border: 1px solid #ef4444;
  color: #fecaca;
}}
small {{ color: #9ca3af; }}
</style>
</head>
<body>
<h1>ZORTEX SCORE 7T ROM Analysis Dashboard</h1>
<p><small>Generated: {html.escape(data["generated_at"])}</small></p>

<div class="card blocked">
<strong>{html.escape(data["decision"])}</strong>
</div>

<div class="grid">
  <div class="metric">
    <strong>{statistics["reference_packages"]}</strong>
    Reference components
  </div>
  <div class="metric">
    <strong>{statistics["target_packages_verified"]}</strong>
    Verified target components
  </div>
  <div class="metric">
    <strong>{statistics["missing_from_target"]}</strong>
    Missing or unverified
  </div>
  <div class="metric">
    <strong>{statistics["source_repositories"]}</strong>
    Public source repositories
  </div>
</div>

<div class="card">
<h2>Component classifications</h2>
<table>
<thead><tr><th>Classification</th><th>Count</th></tr></thead>
<tbody>{classification_rows}</tbody>
</table>
</div>

<div class="card">
<h2>Ordinary user-installable applications</h2>
<ul>{user_app_rows}</ul>
</div>

<div class="card">
<h2>ROM, privileged, framework or boot components</h2>
<ul>{privileged_rows}</ul>
</div>

<div class="card">
<h2>Missing or unverified on target</h2>
<ul>{missing_rows}</ul>
</div>

<div class="card">
<h2>Platform mismatches</h2>
<ul>{mismatch_rows}</ul>
<p>Unknown fields are not treated as proven matches.</p>
</div>

<div class="card">
<h2>Engineering interpretation</h2>
<p>
The working reference tablet contains a combined Android system-image stack.
Installing visible APK names alone cannot reproduce the same environment.
ROM-level components require a matching framework, vendor implementation,
kernel, device tree, partition layout and authorized installation path.
</p>
</div>
</body>
</html>
"""

    path = REPORT_DIR / "index.html"
    path.write_text(document, encoding="utf-8")
    return path


def save_markdown(data: dict[str, Any]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    statistics = data["statistics"]
    comparison = data["comparison"]

    lines = [
        "# ZORTEX SCORE 7T ROM Dashboard",
        "",
        f"Generated: `{data['generated_at']}`",
        "",
        "## Decision",
        "",
        data["decision"],
        "",
        "## Metrics",
        "",
        f"- Reference components: {statistics['reference_packages']}",
        f"- Verified target components: {statistics['target_packages_verified']}",
        f"- Missing or unverified: {statistics['missing_from_target']}",
        f"- Public source repositories: {statistics['source_repositories']}",
        "",
        "## User-installable applications",
        "",
    ]

    lines.extend(
        [f"- `{item}`" for item in data["normal_user_apps"]]
        or ["- None recorded"]
    )

    lines.extend(
        [
            "",
            "## Privileged, framework, vendor or boot components",
            "",
        ]
    )

    lines.extend(
        [f"- `{item}`" for item in data["privileged_or_rom_packages"]]
        or ["- None recorded"]
    )

    lines.extend(["", "## Missing or unverified on target", ""])

    lines.extend(
        [f"- `{item}`" for item in comparison["missing_from_target"]]
        or ["- None"]
    )

    lines.extend(["", "## Platform mismatches", ""])

    lines.extend(
        [f"- {item}" for item in comparison["platform_mismatches"]]
        or ["- No confirmed mismatch; unresolved fields remain."]
    )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Package names alone do not recreate a ROM.",
            "System components require matching framework, vendor, kernel,",
            "device-tree, partition and verified-boot architecture.",
            "",
        ]
    )

    path = REPORT_DIR / "dashboard.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_all_reports() -> tuple[Path, Path, Path]:
    data = build_dashboard_data()
    return save_json(data), save_html(data), save_markdown(data)
