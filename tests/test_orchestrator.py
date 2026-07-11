from pathlib import Path

from zortex.orchestrator import Orchestrator
from zortex.orchestrator.policy import BLOCK_MESSAGE, enforce_command_policy


def test_plan_contains_core_quality_gates(tmp_path: Path) -> None:
    engine = Orchestrator(tmp_path)
    names = [name for name, _ in engine.plan()]
    assert "discover" in names
    assert "syntax" in names
    assert "tests" in names


def test_dry_run_is_non_mutating(tmp_path: Path) -> None:
    engine = Orchestrator(tmp_path)
    state = engine.execute(dry_run=True)
    assert state.status == "passed"
    assert all(step.status == "skipped" for step in state.steps)


def test_policy_blocks_device_mutation() -> None:
    try:
        enforce_command_policy(["flash", "boot.img"])
    except RuntimeError as exc:
        assert str(exc) == BLOCK_MESSAGE
    else:
        raise AssertionError("mutating command was not blocked")
