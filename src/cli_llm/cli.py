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


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("name", required=True, type=str)
@click.option("-m", "--ll-model", default=None, help="The LLM to use.")
@click.argument("unprocessed_args", nargs=-1, type=click.UNPROCESSED)
@common_options
def run(*, name: str, ll_model: str | None, unprocessed_args: tuple[str, ...], verbose: int, quiet: bool) -> None:
    """Run the specified LLM tool."""
    set_verbosity(verbose=verbose, quiet=quiet)

    cli_settings: dict[str, t.Any] = {}
    if ll_model:
        cli_settings["ll_model"] = ll_model

    final_config = ClmConfig(**cli_settings)

    run_tool(name, unprocessed_args, final_config)
