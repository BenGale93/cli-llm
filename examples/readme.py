"""README generation tool.

Example usage:

`clm run readme:Readme -p path=src/ -p "pattern=*.py"`
"""

from pathlib import Path

from cli_llm import Response, StringDict, ToolRunnerInterface, helpers

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

    def gather_data(self, cli_kwargs: StringDict) -> StringDict:
        """Gather the source tree."""
        search_path = cli_kwargs.get("path", Path.cwd())
        pattern = cli_kwargs.get("pattern", "*")
        file_contents = helpers.gather_file_contents(search_path=search_path, pattern=pattern)
        return {"files": file_contents}

    def process(self, ai_response: Response, _data: StringDict) -> None:
        """Save the new README."""
        ai_response.write_to_file("README.md")
