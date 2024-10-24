"""Example of a sub tool.

This is purely an example and would be better structured as a single tool that
took an argument that specified the poem type to use.

To list the sub-tools:

`clm run subtools --help`
"""

from pathlib import Path

import click

import cli_llm


@click.group()
def tool() -> None:
    """Example of a sub tool."""


LIMERICK_PROMPT = """
- The user will provide you with the content of a file.
- You will write a limerick that describes the content of the given file.

```
{{file.read_text()}}
```
"""


@tool.command()
@click.argument("path", type=Path)
@click.pass_obj
def limerick(config: cli_llm.ClmConfig, path: Path) -> None:
    """Writes a limerick about the provided file."""
    data = {"file": path}
    ai_response = cli_llm.run(config, LIMERICK_PROMPT, data)

    ai_response.stream()


HAIKU_PROMPT = """
- The user will provide you with the content of a file.
- You will write a haiku that describes the content of the given file.

```
{{file.read_text()}}
```
"""


@tool.command()
@click.argument("path", type=Path)
@click.pass_obj
def haiku(config: cli_llm.ClmConfig, path: Path) -> None:
    """Writes a haiku about the provided file."""
    data = {"file": path}
    ai_response = cli_llm.run(config, HAIKU_PROMPT, data)

    ai_response.stream()
