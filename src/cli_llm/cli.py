"""CLI module for the application."""

import typing as t
from pathlib import Path

import click

from cli_llm import ClmConfig
from cli_llm._cli_utils import ToolGatherer, common_options
from cli_llm._logging import ClmLogger

log = ClmLogger()


@click.group()
@click.option("-m", "--ll-model", default=None, help="The LLM to use.")
@common_options
@click.pass_context
def cli(ctx: click.Context, *, ll_model: str, verbose: int, quiet: bool) -> None:
    """Welcome to the CLI-llm tool!"""
    log.set_verbosity(verbose=verbose, quiet=quiet)
    cli_settings: dict[str, t.Any] = {}
    if ll_model:
        cli_settings["ll_model"] = ll_model

    final_config = ClmConfig(**cli_settings)

    ctx.obj = final_config


@cli.command(cls=ToolGatherer)
def run() -> None:
    """Runs the specified CLI-llm tool."""


@cli.command()
@click.argument("name")
@click.option("-d", "--dest", type=click.Path(path_type=Path), default=Path.cwd())
def new(*, name: str, dest: Path) -> None:
    """Creates a new CLI-llm tool template file at the given destination."""
    from cli_llm.new import new_tool

    new_tool(dest, name=name)
