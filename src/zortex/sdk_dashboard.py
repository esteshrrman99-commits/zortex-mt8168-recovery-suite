from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from abc import ABC, abstractmethod
import html, json, sys, shutil, importlib.util
from typing import Any

@dataclass(frozen=True)
class DeviceProfile:
    profile_id: str
    manufacturer: str
    model: str
    chipset: str
    architecture: str
    android_version: str
    board_id: str = "unknown"
    partition_layout: str = "unknown"
    notes: str = ""
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

class DeviceProfileRegistry:
    def __init__(self, path: str | Path = "knowledge/device_profiles.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def load(self) -> list[DeviceProfile]:
        if not self.path.exists():
            return []
        return [DeviceProfile(**x) for x in json.loads(self.path.read_text())]
    def save(self, profiles: list[DeviceProfile]) -> None:
        self.path.write_text(json.dumps([p.to_dict() for p in profiles], indent=2) + "\n")
    def upsert(self, profile: DeviceProfile) -> list[DeviceProfile]:
        profiles = [p for p in self.load() if p.profile_id != profile.profile_id] + [profile]
        self.save(profiles)
        return profiles
    def get(self, profile_id: str) -> DeviceProfile | None:
        return next((p for p in self.load() if p.profile_id == profile_id), None)

class EvidenceTimeline:
    def __init__(self, path: str | Path = "artifacts/evidence_timeline.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def append(self, event_type: str, summary: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        event = {"timestamp": datetime.now(timezone.utc).isoformat(),
                 "event_type": event_type, "summary": summary, "data": data or {}}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")
        return event
    def read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(x) for x in self.path.read_text().splitlines() if x.strip()]

class KnowledgeBase:
    def __init__(self, root: str | Path = "knowledge/entries") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
    def add(self, title: str, category: str, content: str, tags: list[str] | None = None) -> dict[str, Any]:
        record = {"title": title, "category": category, "content": content, "tags": tags or []}
        record["entry_id"] = sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:16]
        (self.root / f"{record['entry_id']}.json").write_text(json.dumps(record, indent=2) + "\n")
        return record
    def list(self) -> list[dict[str, Any]]:
        return [json.loads(p.read_text()) for p in sorted(self.root.glob("*.json"))]
    def search(self, query: str) -> list[dict[str, Any]]:
        q = query.lower()
        return [x for x in self.list() if q in json.dumps(x).lower()]

@dataclass
class ZortexContext:
    device_id: str
    session_id: str
    evidence: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None

class ZortexSDKPlugin(ABC):
    name = "unnamed"
    version = "0.0.0"
    api_version = "1.0"
    @abstractmethod
    def run(self, context: ZortexContext) -> dict[str, Any]:
        raise NotImplementedError

class ZortexSDKRuntime:
    def __init__(self) -> None:
        self.plugins: dict[str, ZortexSDKPlugin] = {}
    def register(self, plugin: ZortexSDKPlugin) -> None:
        if plugin.name in self.plugins:
            raise ValueError(f"Plugin already registered: {plugin.name}")
        self.plugins[plugin.name] = plugin
    def execute(self, context: ZortexContext) -> dict[str, Any]:
        return {n: {"version": p.version, "api_version": p.api_version, "result": p.run(context)}
                for n, p in self.plugins.items()}

class DashboardBuilder:
    def build(self, inventory, profiles, timeline, reports, output="dashboard/index.html") -> str:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        def section(title, data):
            return f"<section><h2>{html.escape(title)}</h2><pre>{html.escape(json.dumps(data, indent=2))}</pre></section>"
        body = "".join([section("Device Inventory", inventory), section("Device Profiles", profiles),
                        section("Evidence Timeline", timeline), section("Reports", reports)])
        doc = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZORTEX Command Dashboard</title>
<style>body{{font-family:system-ui;margin:0;background:#0b1020;color:#e9eefc}}
header{{padding:20px;background:#111936}}main{{padding:16px;display:grid;gap:16px}}
section{{background:#151f3f;border:1px solid #2d3b72;border-radius:12px;padding:16px}}
pre{{white-space:pre-wrap;word-break:break-word;background:#0d1530;padding:12px;border-radius:8px}}</style>
</head><body><header><h1>ZORTEX Command Dashboard</h1>
<small>Generated {datetime.now(timezone.utc).isoformat()}</small></header><main>{body}</main></body></html>"""
        out.write_text(doc)
        return str(out)

class HealthChecker:
    def run(self) -> dict[str, Any]:
        return {"python": sys.version.split()[0], "git_available": shutil.which("git") is not None,
                "pytest_available": importlib.util.find_spec("pytest") is not None,
                "src_exists": Path("src/zortex").exists(), "tests_exists": Path("tests").exists()}
