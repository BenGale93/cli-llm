import pytest

from cli_llm.cli import cli


@pytest.mark.parametrize(
    ("tool", "params"),
    [
        ("improve", ("test.txt",)),
        ("improve", ("test.txt", "--prompt", "correct-python")),
        ("collect", ("examples/", "--pattern", "*.py")),
        ("collect", ("examples/", "--pattern", "*.py", "--prompt", "readme")),
    ],
)
def test_example_folder(tool, params, example_project):
    result = example_project.invoke(cli, ["run", tool, *params])

    assert result.exit_code == 0
