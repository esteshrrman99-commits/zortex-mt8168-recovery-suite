from __future__ import annotations

BLOCK_MESSAGE = "BLOCKED: authorized restoration gate has not been satisfied."

MUTATING_TERMS = {
    "flash",
    "erase",
    "format",
    "unlock",
    "repartition",
    "patch-device",
    "write-device",
    "force-push",
    "reset-hard",
}


def enforce_command_policy(command: list[str]) -> None:
    normalized = " ".join(command).lower()

    if any(term in normalized for term in MUTATING_TERMS):
        raise RuntimeError(BLOCK_MESSAGE)

    if "git push --force" in normalized or "git reset --hard" in normalized:
        raise RuntimeError("BLOCKED: destructive Git operation is not permitted.")
