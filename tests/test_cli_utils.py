from pathlib import Path

import pytest

from cli_llm import errors
from cli_llm._cli_utils import load_tool_script


def test_module_loads_correctly():
    module = load_tool_script(Path("src/cli_llm/_logging.py"))

    assert module is not None


def test_file_not_found():
    with pytest.raises(errors.InvalidModuleError, match="fake"):
        load_tool_script(Path("tests") / "fake.py")
