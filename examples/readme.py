"""README generation tool.

Example usage:

`clm run readme src/ --pattern "*.py"`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, helpers, run

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


@click.command()
@click.argument("path", type=Path)
@click.option("--pattern", type=str, default="*")
@click.pass_obj
def tool(config: ClmConfig, path: Path, pattern: str) -> None:
    """Correct the grammar of a given python file."""
    file_contents = helpers.gather_file_contents(search_path=path, pattern=pattern)
    data = {"files": file_contents}

    ai_response = run(config, PROMPT, data)

    ai_response.write_to_file("README.md")
