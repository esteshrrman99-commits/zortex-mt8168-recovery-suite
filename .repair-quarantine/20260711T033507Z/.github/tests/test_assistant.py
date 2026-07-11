from pathlib import Path

from zortex.assistant import AssistantEngine
from zortex.assistant.policy import BLOCK_MESSAGE, validate_command


def test_search(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Knowledge graph ready.\n", encoding="utf-8")
    response = AssistantEngine(tmp_path).ask("knowledge graph")
    assert response.evidence
    assert response.evidence[0].path == "README.md"


def test_explain_missing_file(tmp_path: Path) -> None:
    response = AssistantEngine(tmp_path).explain("FileNotFoundError: no such file")
    assert response.inference
    assert any("pwd" in item.lower() for item in response.recommendations)


def test_plan_requires_approval(tmp_path: Path) -> None:
    plan = AssistantEngine(tmp_path).plan("check repository health")
    assert plan
    assert all(item.requires_approval for item in plan if item.command)


def test_mutating_command_blocked() -> None:
    ok, message = validate_command(["fastboot", "flashing", "unlock"])
    assert ok is False
    assert message == BLOCK_MESSAGE


def test_status_mock_mode(tmp_path: Path) -> None:
    status = AssistantEngine(tmp_path).status()
    assert status["provider"] == "mock"
    assert status["automatic_shell_execution"] is False
