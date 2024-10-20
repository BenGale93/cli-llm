"""CLI module for the application."""

import typing as t

import click

from cli_llm import ClmConfig, errors
from cli_llm.logging import get_logger, set_verbosity
from cli_llm.run import load_tool_script
from cli_llm.types import RT

log = get_logger()


def common_options(fn: t.Callable[..., RT]) -> t.Callable[..., RT]:
    """Common options for commands."""
    return click.option("-v", "--verbose", count=True)(click.option("-q", "--quiet", is_flag=True, default=False)(fn))


class ToolGatherer(click.MultiCommand):
    """Click command for gathering all valid tools."""

    def list_commands(self, ctx: click.Context) -> list[str]:
        """Dynamically get the list of tool commands."""
        final_config: ClmConfig = ctx.obj
        rv = []
        for filepath in final_config.tool_files():
            try:
                module = load_tool_script(filepath.stem, final_config.tools_dir)
            except Exception as e:  # noqa: BLE001
                log.warning("Failed to get the tool script from `%s` due to: %s", filepath.stem, e)
                continue
            if not hasattr(module, "tool"):
                log.warning("The module `%s` does not have an attribute `tool`", filepath.stem)
                continue
            if module.tool is None:
                log.debug("Skipping module `%s`", filepath.stem)
                continue
            if not isinstance(module.tool, click.Command):
                log.warning("The attribute `tool` in the module `%s` is not of type `click.Command`", filepath.stem)
                continue
            rv.append(filepath.stem)
        rv.sort()

        return rv

    def get_command(self, ctx: click.Context, name: str) -> click.Command:
        """Dynamically get the named tool command."""
        final_config: ClmConfig = ctx.obj
        module = load_tool_script(name, final_config.tools_dir)
        if not isinstance(module.tool, click.Command):  # pragma: no cover # Should be filtered out in list_commands
            msg = f"The attribute `tool` in the module :{module.__name__} is not of type `click.Command`"
            raise errors.InvalidToolCommandError(msg)
        return module.tool


@click.group()
@click.option("-m", "--ll-model", default=None, help="The LLM to use.")
@common_options
@click.pass_context
def cli(ctx: click.Context, *, ll_model: str, verbose: int, quiet: bool) -> None:
    """Welcome to the CLI-llm tool!"""
    set_verbosity(verbose=verbose, quiet=quiet)
    cli_settings: dict[str, t.Any] = {}
    if ll_model:
        cli_settings["ll_model"] = ll_model

    final_config = ClmConfig(**cli_settings)

    ctx.obj = final_config


@cli.command(cls=ToolGatherer)
def run() -> None:
    """Runs the specified CLI-llm tool."""
