from pathlib import Path

from logot import Logot, logged

from cli_llm.cli import cli


def test_run_tool_with_parameters_and_quiet(fake_project):
    result = fake_project.invoke(cli, ["-q", "run", "example", "summarise", "--test", "value1"])

    assert result.exit_code == 0
    assert result.output == "test: value1\n"


def test_run_tool_with_printing(fake_project):
    result = fake_project.invoke(cli, ["run", "example", "summarise", "--test", "value1"])

    assert result.exit_code == 0
    assert result.stdout == "test: value1\n"
    assert result.stderr == "Prompting MockModel: mock\n\n"


def test_run_tool_with_info(fake_project, logot: Logot):
    fake_project.invoke(cli, ["-v", "run", "example", "summarise", "--test", "value1"])

    logot.assert_logged(logged.info("Rendering the prompt.") >> logged.info("Getting the model: mock"))


def test_run_tool_with_debug(fake_project, logot: Logot):
    fake_project.invoke(cli, ["-vv", "run", "example", "summarise", "--test", "value1"])

    logot.assert_logged(logged.debug("Prompt: %s"))


def test_run_tool_with_help(fake_project):
    result = fake_project.invoke(cli, ["run", "example", "--help"])

    assert result.exit_code == 0
    assert "summarise" in result.output


def test_tool_search_logging(fake_project, logot):
    result = fake_project.invoke(cli, ["-vv", "run", "--help"])
    assert result.exit_code == 0
    assert "example" in result.output
    logot.assert_logged(
        logged.warning("Failed to get the tool script from `bad_module` due to: division by zero")
        >> logged.warning("The attribute `tool` in the module `bad_type` is not of type `click.Command`")
        >> logged.warning("The module `no_attr` does not have an attribute `tool`")
        >> logged.debug("Skipping module `skip`")
    )


def test_new_tool(fake_project):
    result = fake_project.invoke(cli, ["new", "fake", "--dest", "tools/"])

    assert result.exit_code == 0
    assert (Path.cwd() / "tools/fake.py").exists()
