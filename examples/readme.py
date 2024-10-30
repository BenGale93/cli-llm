"""README generation tool.

Example usage:

`clm run readme src/ -l python -p "*.py" -o README.md`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, helpers, run

PROMPT = """
- Below are some {{lang}} files from a library.
- Each file will be listed with its name and then its content.
- Write a README in markdown format that explains how to use the {{lang}} library.

{% for f, contents in files %}
Filename: {{f}}

```{{lang}}
{{contents}}
```
{% endfor %}
"""


@click.command()
@click.argument("path", type=Path)
@click.option("-l", "--lang", type=str, default="")
@click.option("-p", "--pattern", type=str, default="*")
@click.option("-o", "--output", type=Path, default=Path("README.md"))
@click.pass_obj
def tool(config: ClmConfig, path: Path, lang: str, pattern: str, output: Path) -> None:
    """Write a README for a given library."""
    file_contents = helpers.gather_file_contents(search_path=path, pattern=pattern)
    data = {"files": file_contents, "lang": lang}

    ai_response = run(config, PROMPT, data)

    ai_response.write_to_file(output)
