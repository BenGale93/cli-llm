from pathlib import Path

import llm
import pytest
from logot import Logot, logged

from cli_llm import errors
from cli_llm.config import ClmConfig
from cli_llm.run import get_tool, run_tool
from tests import example


def test_mock_model(mock_model):
    mock_model.enqueue(["hello world"])
    mock_model.enqueue(["second"])
    model = llm.get_model("mock")
    response = model.prompt(prompt="hello")
    assert response.text() == "hello world"
    assert str(response) == "hello world"
    assert model.history[0][0].prompt == "hello"
    response2 = model.prompt(prompt="hello again")
    assert response2.text() == "second"


def test_example_run(capsys, mock_model):
    mock_model.enqueue(["helloworld"])
    tool = example.Summarise(llm.get_model("mock"))

    tool.run()

    captured = capsys.readouterr()

    assert "helloworld" in captured.out


def test_render_prompt():
    tool = example.Summarise(llm.get_model("mock"))

    prompt = tool.render({"test": "hello"})

    assert prompt == "\n- This is a test prompt\n\nhello"


def test_invalid_module_error():
    with pytest.raises(errors.InvalidModuleError, match="fake"):
        get_tool("tests/fake:FakeTool")


def test_not_an_instance_of_toolrunnerinterface():
    with pytest.raises(TypeError, match="The class MockModel does not inherit from the ToolRunnerInterface."):
        get_tool("conftest:MockModel", ClmConfig(ll_model="mock", tools_dir=Path("tests")))


def test_failure_in_gather_data(logot: Logot):
    tool = example.BadGatherData(llm.get_model("mock"))

    with pytest.raises(SystemExit):
        tool.run()

    logot.assert_logged(logged.error("Error in your tool's gather_data method"))


def test_failure_in_process(logot: Logot):
    tool = example.BadProcess(llm.get_model("mock"))

    with pytest.raises(SystemExit):
        tool.run()

    logot.assert_logged(logged.error("Error in your tool's process method"))


def test_run_tool_cant_find(logot: Logot):
    with pytest.raises(SystemExit):
        run_tool("fake:FakeTool", {})

    logot.assert_logged(logged.error("Error trying to find the tool you specified."))
