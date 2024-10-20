"""Improve the writing of a given file.

Example usage:

`clm run improve FILE.txt`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, run

PROMPT = """
- The user will provide you with the content of a file.
- You will improve the writing style to be more grammatically correct and engaging.
- Do not respond with anything than the modified file.

```
{{file.read_text()}}
```
"""


@click.command()
@click.argument("path", type=Path)
@click.pass_obj
def tool(config: ClmConfig, path: Path) -> None:
    """Correct the grammar and writing style of a given file."""
    data = {"file": path}

    ai_response = run(config, PROMPT, data)

    ai_response.write_to_file(data["file"])
