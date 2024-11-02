import llm
import pytest
from rich.console import Console

from cli_llm import _logging
from cli_llm.response import Response


@pytest.fixture
def patched_console():
    old_console = _logging.console
    _logging.console = Console(record=True, stderr=True, force_terminal=True)
    try:
        yield _logging.console
    finally:
        _logging.console = old_console


def test_text(mock_model, patched_console):
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    response = Response(model.prompt(""))
    with patched_console.capture() as capture:
        result = response.text()

    assert "Fetching response from LLM..." in capture.get()
    assert result == "helloworld"


def test_json(mock_model, patched_console):
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    response = Response(model.prompt(""))
    with patched_console.capture() as capture:
        result = response.json()

    assert "Fetching JSON response from LLM..." in capture.get()
    assert result is None


def test_response_interface(mock_model):
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    core_response = model.prompt("")
    response = Response(core_response)

    assert response.response == core_response
    assert repr(response) == repr(core_response)


def test_stream(mock_model, capsys):
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    response = Response(model.prompt(""))
    response.stream()

    assert "helloworld" in capsys.readouterr()


def test_write_to_file(mock_model, named_temp_fs):
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    response = Response(model.prompt(""))

    test_file = named_temp_fs / "test.txt"
    response.write_to_file(test_file)

    assert test_file.read_text() == "helloworld\n"


def test_write_to_file_has_newline(mock_model, named_temp_fs):
    mock_model.enqueue(["helloworld\n"])
    model = llm.get_model("mock")

    response = Response(model.prompt(""))

    test_file = named_temp_fs / "test.txt"
    response.write_to_file(test_file)

    assert test_file.read_text() == "helloworld\n"
