# ZORTEX v0.9 ROM Analysis Dashboard

The dashboard converts ZORTEX reference, source and comparison data into:

- JSON
- HTML
- Markdown
- component statistics
- ordinary-app lists
- privileged/system-component lists
- unresolved target differences
- platform compatibility warnings

## Build reports

```bash
python scripts/zortex_dashboard.py summary
python scripts/zortex_dashboard.py build
