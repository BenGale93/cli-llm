"""Correct the grammar of a given python file.

Example usage:

`clm run correct FILE.txt`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, run

PROMPT = """
- The user will provide you with the content of a Python programming file.
- You will correct the English in the comments, but leave everything else unchanged.
- Only modify comments if there is a spelling or grammar mistake.
- Make sure not to change the code, except for typos within strings.
- Do not change the code itself, only comments.
- Do not respond with anything than the modified code

```python
{{file.read_text()}}
```
"""


@click.command()
@click.argument("path", type=Path)
@click.pass_obj
def tool(config: ClmConfig, path: Path) -> None:
    """Correct the grammar of a given python file."""
    data = {"file": path}

    ai_response = run(config, PROMPT, data)

    ai_response.write_to_file(data["file"])
