from logot import Logot, logged

from cli_llm.cli import cli


def test_run_tool_with_parameters_and_quiet(fake_project):
    result = fake_project.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1", "-q"])

    assert result.exit_code == 0
    assert result.output == "key1: value1\n"


def test_run_tool_with_printing(fake_project):
    result = fake_project.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1"])

    assert result.exit_code == 0
    assert result.stdout == "key1: value1\n"
    assert result.stderr == "Prompting MockModel: mock\n\n"


def test_run_tool_with_info(fake_project, logot: Logot):
    fake_project.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1", "-v"])

    logot.assert_logged(
        logged.info("Running the gather_data method.")
        >> logged.info("Running the render method.")
        >> logged.info("Running the process method.")
    )


def test_run_tool_with_debug(fake_project, logot: Logot):
    fake_project.invoke(cli, ["run", "example:Summarise", "--parameter", "key1=value1", "-vv"])

    logot.assert_logged(logged.debug("Using tool: example:Summarise") >> logged.debug("Getting LL model: mock"))
