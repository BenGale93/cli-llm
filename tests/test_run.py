from pathlib import Path
from typing import TYPE_CHECKING

import llm
import pytest

from cli_llm import errors
from cli_llm.config import ClmConfig
from cli_llm.run import load_tool_script, render, run

if TYPE_CHECKING:
    from conftest import MockModel


def test_mock_model(mock_model):
    mock_model.enqueue(["hello world"])
    mock_model.enqueue(["second"])
    model: MockModel = llm.get_model("mock")
    response = model.prompt(prompt="hello")
    assert response.text() == "hello world"
    assert str(response) == "hello world"
    assert model.history[0][0].prompt == "hello"
    response2 = model.prompt(prompt="hello again")
    assert response2.text() == "second"


@pytest.fixture
def mock_config() -> ClmConfig:
    return ClmConfig(ll_model="mock")


def test_example_run(mock_model, mock_config):
    mock_model.enqueue(["helloworld"])
    response = run(mock_config, "test", {})

    assert response.text() == "helloworld"


def test_render_prompt():
    prompt = render("{{test}}", {"test": "hello"})

    assert prompt == "hello"


def test_invalid_module_error():
    with pytest.raises(errors.InvalidModuleError, match="fake"):
        load_tool_script("fake", Path("tests"))
