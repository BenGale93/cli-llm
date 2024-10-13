"""CLI module for the application."""

import typing as t

import click

from cli_llm.config import ClmConfig
from cli_llm.logging import set_verbosity
from cli_llm.run import run_tool
from cli_llm.types import RT


@click.group()
def cli() -> None:
    """Welcome to the CLI-llm tool!"""


def process_cli_kwargs(parameters: tuple[str, t.Any]) -> dict[str, t.Any]:
    """Processes the CLI kwargs into a dictionary.

    A helper function for click.
    """
    parameter_list = [tuple(p.split("=", maxsplit=1)) for p in parameters]
    return dict(parameter_list)


def common_options(fn: t.Callable[..., RT]) -> t.Callable[..., RT]:
    """Common options for commands."""
    return click.option("-v", "--verbose", count=True)(click.option("-q", "--quiet", is_flag=True, default=False)(fn))


@cli.command()
@click.argument("name", required=True, type=str)
@click.option("-m", "--ll-model", default=None, help="The LLM to use.")
@click.option("-p", "--parameter", multiple=True, help="Parameters to forward to the selected tool.")
@common_options
def run(*, name: str, ll_model: str | None, parameter: tuple[str, t.Any], verbose: int, quiet: bool) -> None:
    """Run the specified LLM tool."""
    set_verbosity(verbose=verbose, quiet=quiet)

    cli_settings = {}
    if ll_model:
        cli_settings["ll_model"] = ll_model

    final_config = ClmConfig(**cli_settings)

    parameters = process_cli_kwargs(parameter)
    run_tool(name, final_config, parameters)
