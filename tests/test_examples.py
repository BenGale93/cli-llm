import pytest

from cli_llm.cli import cli


@pytest.mark.parametrize(
    ("tool", "params"),
    [
        ("improve", ("test.txt",)),
        ("improve", ("test.txt", "--prompt", "correct-python")),
        ("readme", ("examples/", "--pattern", "*.py", "-l", "python")),
        ("summarise", ("examples/", "--pattern", "*.py", "-l", "python")),
    ],
)
def test_example_folder(tool, params, example_project):
    result = example_project.invoke(cli, ["run", tool, *params])

    assert result.exit_code == 0
