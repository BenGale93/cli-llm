"""CLI module for the application."""

import typing as t

import click
import llm

from cli_llm.config import ClmConfig
from cli_llm.run import get_tool


@click.group()
def cli() -> None:
    """Welcome to the CLI-llm tool!"""


def process_cli_kwargs(parameters: tuple[str, t.Any]) -> dict[str, t.Any]:
    """Processes the CLI kwargs into a dictionary.

    A helper function for click.
    """
    parameter_list = [tuple(p.split("=", maxsplit=1)) for p in parameters]
    return dict(parameter_list)


@cli.command()
@click.argument("name", required=True, type=str)
@click.option("-m", "--ll-model", default=None, help="The LLM to use.")
@click.option("-p", "--parameter", multiple=True, help="Parameters to forward to the selected tool.")
def run(name: str, ll_model: str | None, parameter: tuple[str, t.Any]) -> None:
    """Run the specified LLM tool."""
    parameters = process_cli_kwargs(parameter)

    cli_settings = {}
    if ll_model:
        cli_settings["ll_model"] = ll_model

    final_config = ClmConfig(**cli_settings)

    tool = get_tool(name)

    model = llm.get_model(final_config.ll_model)
    tool(model).run(**parameters)
