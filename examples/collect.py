"""README generation tool.

Example usage:

`clm run collect src/ --pattern "*.py" --prompt readme`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, helpers, run

PROMPT = """
- Below are some python files from a library.
- Each file will be listed with its name and then its content.
{{ sub_prompt }}

{% for f, contents in files %}
Filename: {{f}}

```python
{{contents}}
```
{% endfor %}
"""

SUBPROMPT_MAP = {
    "readme": "- Write a README in markdown format that explains how to use the python library.",
    "summarise": "- Summarise the code and make some suggestions for new features.",
}


@click.command()
@click.argument("path", type=Path)
@click.option("--pattern", type=str, default="*")
@click.option("--prompt", type=str, default="summarise")
@click.pass_obj
def tool(config: ClmConfig, path: Path, pattern: str, prompt: str) -> None:
    """Correct the grammar of a given python file."""
    file_contents = helpers.gather_file_contents(search_path=path, pattern=pattern)
    data = {"files": file_contents, "sub_prompt": SUBPROMPT_MAP[prompt]}

    ai_response = run(config, PROMPT, data)

    if prompt == "readme":
        ai_response.write_to_file("README.md")
    else:
        ai_response.stream()
