"""Improve the writing of a given file.

Example usage:

`clm run improve FILE.txt`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, run

IMPROVE_PROMPT = """
- The user will provide you with the content of a file.
- You will improve the writing style to be more grammatically correct and engaging.
- Do not respond with anything than the modified file.
- Make sure that lines are no longer than 100 characters.

```
{{file.read_text()}}
```
"""

CORRECT_PYTHON_PROMPT = """
- The user will provide you with the content of a Python programming file.
- You will correct the English in the comments, but leave everything else unchanged.
- Only modify comments if there is a spelling or grammar mistake.
- Make sure not to change the code, except for typos within strings.
- Do not change the code itself, only comments.
- Do not respond with anything than the modified code.
- Do not include any backtick fenced code blocks.

```python
{{file.read_text()}}
```
"""

prompt_map = {
    "improve": IMPROVE_PROMPT,
    "correct-python": CORRECT_PYTHON_PROMPT,
}


@click.command()
@click.argument("path", type=Path)
@click.option("--prompt", default="improve", type=click.Choice(list(prompt_map)))
@click.pass_obj
def tool(config: ClmConfig, path: Path, prompt: str) -> None:
    """Correct the grammar and writing style of a given file."""
    data = {"file": path}
    selected_prompt = prompt_map[prompt]

    ai_response = run(config, selected_prompt, data)

    ai_response.write_to_file(data["file"])
