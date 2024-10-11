"""README generation tool.

Example usage:

`clm run readme:Readme -p path=src/ -p "patten=*.py"`
"""

from pathlib import Path
from typing import Any

import llm

from cli_llm import ToolRunnerInterface, helpers

PROMPT = """
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

    prompt = PROMPT

    def gather_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gather the source tree."""
        search_path = kwargs.get("path", Path.cwd())
        pattern = kwargs.get("pattern", "*")
        file_contents = helpers.gather_file_contents(search_path=search_path, pattern=pattern)
        return {"files": file_contents}

    def process(self, ai_response: llm.Response, _data: dict[str, Any]) -> None:
        """Save the new README."""
        Path("README.md").write_text(ai_response.text())
