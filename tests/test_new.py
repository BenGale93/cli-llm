from pathlib import Path

from click.testing import CliRunner

from cli_llm.cli import cli
from cli_llm.new import new_tool


def test_tool_runs_without_any_errors(named_temp_fs) -> None:
    named_temp_fs.gen(
        {
            "pyproject.toml": {"tool": {"cli-llm": {"ll_model": "mock", "tools_dir": "."}}},
        }
    )

    with named_temp_fs.chdir():
        new_tool(Path.cwd(), name="fake")
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(cli, ["-q", "run", "fake"])

    assert result.exit_code == 0
