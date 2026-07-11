#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from zortex.sdk_dashboard import *

p = argparse.ArgumentParser(description="ZORTEX SDK Dashboard")
s = p.add_subparsers(dest="cmd", required=True)
a = s.add_parser("profile-add")
a.add_argument("--id", required=True); a.add_argument("--manufacturer", required=True)
a.add_argument("--model", required=True); a.add_argument("--chipset", required=True)
a.add_argument("--architecture", default="arm64-v8a"); a.add_argument("--android", default="unknown")
a.add_argument("--board", default="unknown"); a.add_argument("--partition-layout", default="unknown")
s.add_parser("profile-list")
t = s.add_parser("timeline-add"); t.add_argument("--type", required=True); t.add_argument("--summary", required=True)
k = s.add_parser("kb-add"); k.add_argument("--title", required=True); k.add_argument("--category", required=True)
k.add_argument("--content", required=True); k.add_argument("--tags", default="")
q = s.add_parser("kb-search"); q.add_argument("query")
s.add_parser("dashboard-build"); s.add_parser("health")
x = p.parse_args()

if x.cmd == "profile-add":
    r = DeviceProfile(x.id,x.manufacturer,x.model,x.chipset,x.architecture,x.android,x.board,x.partition_layout)
    print(json.dumps([p.to_dict() for p in DeviceProfileRegistry().upsert(r)], indent=2))
elif x.cmd == "profile-list":
    print(json.dumps([p.to_dict() for p in DeviceProfileRegistry().load()], indent=2))
elif x.cmd == "timeline-add":
    print(json.dumps(EvidenceTimeline().append(x.type,x.summary), indent=2))
elif x.cmd == "kb-add":
    print(json.dumps(KnowledgeBase().add(x.title,x.category,x.content,[i.strip() for i in x.tags.split(",") if i.strip()]), indent=2))
elif x.cmd == "kb-search":
    print(json.dumps(KnowledgeBase().search(x.query), indent=2))
elif x.cmd == "dashboard-build":
    invp = Path("artifacts/device_inventory.json")
    inventory = json.loads(invp.read_text()) if invp.exists() else []
    reports = []
    if Path("reports").exists():
        for pth in sorted(Path("reports").rglob("*.json")):
            try: reports.append(json.loads(pth.read_text()))
            except Exception: pass
    out = DashboardBuilder().build(inventory,[p.to_dict() for p in DeviceProfileRegistry().load()],
                                   EvidenceTimeline().read(),reports)
    print(json.dumps({"dashboard":out}, indent=2))
else:
    print(json.dumps(HealthChecker().run(), indent=2))
