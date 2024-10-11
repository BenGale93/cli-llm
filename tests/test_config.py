import os
from pathlib import Path

from click.testing import CliRunner

from cli_llm.cli import cli

EXAMPLE = Path("tests/example.py").read_text()


def test_config_from_pyproject(temp_fs_factory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen(
        {
            "pyproject.toml": {"tool": {"cli-llm": {"ll_model": "mock"}}},
            "example.py": EXAMPLE,
        }
    )

    with temp_fs.chdir():
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1"])

    assert result.exit_code == 0
    assert result.output == "key1: value1\n"


def test_config_from_cli_overrides_pyproject(temp_fs_factory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen(
        {
            "pyproject.toml": {"tool": {"cli-llm": {"ll_model": "fake"}}},
            "example.py": Path("tests/example.py").read_text(),
        }
    )

    with temp_fs.chdir():
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1", "-m", "mock"])

    assert result.exit_code == 0
    assert result.output == "key1: value1\n"


def test_config_from_env(temp_fs_factory, func_name):
    temp_fs = temp_fs_factory.mktemp(func_name)

    temp_fs.gen(
        {
            "example.py": Path("tests/example.py").read_text(),
        }
    )

    with temp_fs.chdir():
        os.environ["LL_MODEL"] = "mock"
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1"])

    assert result.exit_code == 0
    assert result.output == "key1: value1\n"
