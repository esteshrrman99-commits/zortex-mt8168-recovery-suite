import pytest

from zortex.restoration import enforce_restoration_gate


def test_restoration_gate_blocks_mutating_attempts() -> None:
    with pytest.raises(RuntimeError, match="BLOCKED: authorized restoration gate has not been satisfied"):
        enforce_restoration_gate(action="flash", authorized=False)

    with pytest.raises(RuntimeError, match="BLOCKED: authorized restoration gate has not been satisfied"):
        enforce_restoration_gate(action="erase", authorized=False)
