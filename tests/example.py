"""Example tool."""

import click
import rich

from cli_llm import ClmConfig, run

PROMPT = """
- This is a test prompt

{{test}}
"""


@click.group()
def tool():
    """The sub root of this example command."""


@tool.command()
@click.option("--test")
@click.pass_obj
def summarise(config: ClmConfig, test: str | None) -> None:
    data = {"test": test}

    ai_response = run(config, PROMPT, data)

    for chunk in ai_response:
        rich.print(chunk, end="")
    for key, value in data.items():
        rich.print(f"{key}: {value}")
