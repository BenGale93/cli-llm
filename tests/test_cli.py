from click.testing import CliRunner
from logot import Logot, logged

from cli_llm.cli import cli


def test_run_tool_with_parameters_and_quiet():
    runner = CliRunner(mix_stderr=False)

    result = runner.invoke(cli, ["run", "tests/example:Summarise", "--parameter", "key1=value1", "-m", "mock", "-q"])

    assert result.exit_code == 0
    assert result.output == "key1: value1\n"


def test_run_tool_with_printing():
    runner = CliRunner(mix_stderr=False)

    result = runner.invoke(cli, ["run", "tests/example:Summarise", "--parameter", "key1=value1", "-m", "mock"])

    assert result.exit_code == 0
    assert result.output == "Prompting MockModel: mock\n\nkey1: value1\n"


def test_run_tool_with_info(logot: Logot):
    runner = CliRunner(mix_stderr=False)

    runner.invoke(cli, ["run", "tests/example:Summarise", "--parameter", "key1=value1", "-m", "mock", "-v"])

    logot.assert_logged(
        logged.info("Running the gather_data method.")
        >> logged.info("Running the render method.")
        >> logged.info("Running the process method.")
    )


def test_run_tool_with_debug(logot: Logot):
    runner = CliRunner(mix_stderr=False)

    runner.invoke(cli, ["run", "tests/example:Summarise", "--parameter", "key1=value1", "-m", "mock", "-vv"])

    logot.assert_logged(logged.debug("Using tool: tests/example:Summarise") >> logged.debug("Getting LL model: mock"))
