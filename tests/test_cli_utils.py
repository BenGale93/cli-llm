from pathlib import Path

import pytest

from cli_llm import errors
from cli_llm._cli_utils import load_tool_script


def test_invalid_module_error():
    with pytest.raises(errors.InvalidModuleError, match="fake"):
        load_tool_script("fake", Path("tests"))
