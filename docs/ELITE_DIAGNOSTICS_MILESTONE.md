# ZORTEX Elite Diagnostics Milestone

Adds device inventory, evidence hashing, compatibility scoring, provenance knowledge graph,
local cryptographic attestations, plugin architecture, and JSON/Markdown reporting.

Elite feature: **Provenance + Attestation Fabric**. It links devices, evidence, firmware
observations, compatibility decisions, and reports into a traceable graph.

Commands:
```bash
python scripts/zortex_elite.py inventory-add --id score7t-001 --manufacturer Keefe --model 711 --chipset MT8168 --android 10
python scripts/zortex_elite.py inventory-list
python scripts/zortex_elite.py compatibility-demo
python scripts/zortex_elite.py provenance-demo
python scripts/zortex_elite.py report-demo
```
