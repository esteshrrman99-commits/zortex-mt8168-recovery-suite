"""Central ZORTEX restoration safety gate.

All potentially device-mutating actions remain blocked unless a separately
validated authorization process explicitly approves them.
"""

from __future__ import annotations

BLOCK_MESSAGE = "BLOCKED: authorized restoration gate has not been satisfied."

MUTATING_ACTIONS = frozenset(
    {
        "flash",
        "erase",
        "format",
        "write",
        "unlock",
        "patch",
        "restore",
        "repartition",
    }
)


def enforce_restoration_gate(
    *,
    action: str,
    authorized: bool = False,
) -> None:
    """Enforce the restoration safety boundary.

    Args:
        action: Requested operation, such as ``flash`` or ``erase``.
        authorized: Whether a separately validated authorization gate passed.

    Raises:
        ValueError: When no valid action name is supplied.
        RuntimeError: When authorization has not been established.
    """
    normalized_action = action.strip().lower()

    if not normalized_action:
        raise ValueError("A restoration action is required.")

    if not authorized:
        raise RuntimeError(BLOCK_MESSAGE)

    # Authorization alone does not perform the operation. This function only
    # validates the gate; no flashing or device-writing adapter exists here.
    return None
