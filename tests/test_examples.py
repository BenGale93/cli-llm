import pytest

from cli_llm.cli import cli


@pytest.mark.parametrize(
    ("tool", "params"),
    [
        ("correct", ("test.txt",)),
        ("improve", ("test.txt",)),
        ("readme", ("examples/", "--pattern", "*.py")),
        ("summarise", ("examples/", "--pattern", "*.py")),
    ],
)
def test_example_folder(tool, params, example_project):
    result = example_project.invoke(cli, ["run", tool, *params])

    assert result.exit_code == 0
