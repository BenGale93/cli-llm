from click.testing import CliRunner

from cli_llm.cli import cli


def test_run_tool_with_parameters():
    runner = CliRunner(mix_stderr=False)

    result = runner.invoke(cli, ["run", "tests/example:Summarise", "--parameter", "key1=value1", "-m", "mock"])

    assert result.exit_code == 0
    assert result.output == "key1: value1\n"
