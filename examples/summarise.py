"""Summarisation tool.

Example usage:

`clm run summarise src/ -l python -p "*.py"`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, helpers, run

PROMPT = """
- Below are some {{lang}} files from a library.
- Each file will be listed with its name and then its content.
- Summarise the code and make some suggestions for new features.

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
@click.option("-o", "--output", type=Path | None, default=None)
@click.pass_obj
def tool(config: ClmConfig, path: Path, lang: str, pattern: str, output: Path | None) -> None:
    """Summarise a given set of files."""
    file_contents = helpers.gather_file_contents(search_path=path, pattern=pattern)
    data = {"files": file_contents, "lang": lang}

    ai_response = run(config, PROMPT, data)

    if output is not None:
        ai_response.write_to_file(output)
    else:
        ai_response.stream()
