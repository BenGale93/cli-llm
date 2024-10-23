"""Module for creating new tools more easily."""

from pathlib import Path

import jinja2

TOOL_TEMPLATE = Path(__file__).parent / "_template.py.jinja"


def new_tool(dest: Path, *, name: str) -> None:
    """Creates a new tool script at the given destination."""
    new_tool = jinja2.Template(TOOL_TEMPLATE.read_text()).render(name=name)

    new_tool_file = dest / f"{name}.py"

    new_tool_file.write_text(new_tool)
