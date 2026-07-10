from click.testing import CliRunner

from zortex.cli import main


def test_cli_exposes_score_7t_commands() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["doctor"])
    assert result.exit_code == 0

    result = runner.invoke(main, ["ready"])
    assert result.exit_code == 0

    result = runner.invoke(main, ["dry-run"])
    assert result.exit_code == 0
