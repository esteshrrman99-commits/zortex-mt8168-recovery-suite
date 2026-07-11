#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from zortex.capability_registry.models import Capability
from zortex.capability_registry.service import CapabilityRegistry
from zortex.simulations import SimulationEngine
from zortex.restoration_planner import RestorationPlanner
p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
s.add_parser("list"); x=s.add_parser("simulate"); x.add_argument("capability",choices=[c.value for c in Capability]); s.add_parser("plan")
a=p.parse_args()
if a.cmd=="list": print(json.dumps([r.to_dict() for r in CapabilityRegistry().list()],indent=2))
elif a.cmd=="simulate": print(json.dumps(SimulationEngine().run(Capability(a.capability)),indent=2))
else: print(json.dumps(RestorationPlanner().build({}),indent=2))
