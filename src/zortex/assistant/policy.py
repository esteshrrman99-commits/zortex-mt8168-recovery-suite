from __future__ import annotations

BLOCK_MESSAGE = "BLOCKED: authorized restoration gate has not been satisfied."

SAFE_PREFIXES = {
    ("git", "status"),
    ("pytest",),
    ("python", "-m", "pytest"),
    ("python", "scripts/zortex_graph.py"),
    ("python", "scripts/zortex_assistant.py"),
}

DENIED_TERMS = {
    "flash", "erase", "format", "unlock", "repartition",
    "force-push", "reset --hard", "rm -rf", "adb root",
    "fastboot flashing", "disable-verity", "vbmeta patch",
}


def validate_command(command: list[str]) -> tuple[bool, str]:
    normalized = " ".join(command).strip().lower()
    if any(term in normalized for term in DENIED_TERMS):
        return False, BLOCK_MESSAGE

    for prefix in SAFE_PREFIXES:
        if tuple(command[: len(prefix)]) == prefix:
            return True, "approved-for-human-review"

    return False, "BLOCKED: command is not on the assistant allowlist."
