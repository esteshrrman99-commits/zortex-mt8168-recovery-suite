# ZORTEX v2.0 Orchestrator

The orchestrator controls repository analysis and software-quality workflows only.

## Commands

```bash
python scripts/zortex_orchestrator.py plan
python scripts/zortex_orchestrator.py dry-run
python scripts/zortex_orchestrator.py run
python scripts/zortex_orchestrator.py status
python scripts/zortex_orchestrator.py report
python scripts/zortex_orchestrator.py bundle
```

## Safety

- no device-writing adapters;
- no destructive Git;
- no force push;
- no automatic merge or tagging;
- fail-closed policy enforcement;
- mock/dry-run support;
- JSON execution state and acceptance reporting.

Any device-mutating operation must terminate with:

```text
BLOCKED: authorized restoration gate has not been satisfied.
```
