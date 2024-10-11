"""README generation tool."""

import contextlib
from pathlib import Path
from typing import Any

import llm

from cli_llm.run import ToolRunnerInterface

TEST_PROMPT = """
- Below are some python files from a library.
- Each file will be listed with its name and then its content.
- Write a README in markdown format that explains how to use the python library.

{% for f, contents in files %}
Filename: {{file}}

```python
{{contents}}
```
{% endfor %}
"""


class Readme(ToolRunnerInterface):
    """Generate a README for the library."""

    prompt = TEST_PROMPT

    def gather_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gather the source tree."""
        search_path = kwargs.get("path", Path.cwd())
        pattern = kwargs.get("pattern", "*")
        files = list(Path(search_path).rglob(pattern))
        file_contents = []
        for f in files:
            if not f.is_file():
                continue
            with contextlib.suppress(UnicodeDecodeError):
                contents = f.read_text()
                file_contents.append((f, contents))
        return {"files": file_contents}

    def process(self, ai_response: llm.Response, _data: dict[str, Any]) -> None:
        """Save the new README."""
        Path("README.md").write_text(ai_response.text())
