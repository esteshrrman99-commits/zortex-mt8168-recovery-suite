#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from zortex.compatibility import CompatibilityEngine
from zortex.inventory import DeviceInventory,DeviceRecord
from zortex.provenance import ProvenanceGraph
from zortex.attestation import AttestationEngine
from zortex.reports import ReportBuilder
p=argparse.ArgumentParser(description='ZORTEX Elite Diagnostics')
s=p.add_subparsers(dest='cmd',required=True)
a=s.add_parser('inventory-add'); a.add_argument('--id',required=True); a.add_argument('--manufacturer',default='unknown'); a.add_argument('--model',default='unknown'); a.add_argument('--chipset',default='unknown'); a.add_argument('--android',default='unknown')
s.add_parser('inventory-list'); s.add_parser('compatibility-demo'); s.add_parser('provenance-demo'); s.add_parser('report-demo')
x=p.parse_args()
if x.cmd=='inventory-add':
    r=DeviceRecord(x.id,x.manufacturer,x.model,x.chipset,x.android)
    print(json.dumps([i.to_dict() for i in DeviceInventory().upsert(r)],indent=2))
elif x.cmd=='inventory-list':
    print(json.dumps([i.to_dict() for i in DeviceInventory().load()],indent=2))
elif x.cmd=='compatibility-demo':
    print(json.dumps(CompatibilityEngine().score({'board_match':True,'chipset_match':True,'architecture_match':True,'partition_fit':False,'firmware_provenance':False,'vendor_compatible':True}),indent=2))
elif x.cmd=='provenance-demo':
    g=ProvenanceGraph(); d=g.add_node('device',{'model':'SCORE7T','chipset':'MT8168'}); e=g.add_node('evidence',{'type':'usb_probe','status':'no_enumeration'}); g.link(d,'produced',e); print(json.dumps(g.export('artifacts/provenance_graph.json'),indent=2))
else:
    sections={'inventory':[i.to_dict() for i in DeviceInventory().load()],'compatibility':CompatibilityEngine().score({}),'attestation':AttestationEngine().attest({'milestone':'elite'},'local-demo-key')}
    print(json.dumps(ReportBuilder().build('ZORTEX Elite Diagnostic Report',sections),indent=2))
