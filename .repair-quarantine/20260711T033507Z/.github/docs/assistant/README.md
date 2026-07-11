# ZORTEX v1.3 AI Assistant Console

Local-first, repository-scoped, deterministic in mock mode, and unable to run
shell commands automatically.

## Commands

```bash
python scripts/zortex_assistant.py status
python scripts/zortex_assistant.py ask "knowledge graph orchestrator"
python scripts/zortex_assistant.py explain "FileNotFoundError"
python scripts/zortex_assistant.py plan "check repository health"
```

Audit records are written to `artifacts/assistant/`.

Every proposed command requires human approval. Device mutation and destructive
Git operations remain blocked.
