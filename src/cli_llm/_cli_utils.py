import typing as t
from functools import cache
from importlib import util
from pathlib import Path
from types import ModuleType

import click

from cli_llm import ClmConfig, errors
from cli_llm._logging import ClmLogger
from cli_llm.types import RT, P

log = ClmLogger()


def common_options(fn: t.Callable[P, RT]) -> t.Callable[P, RT]:
    """Common options for commands."""
    return click.option("-v", "--verbose", count=True)(click.option("-q", "--quiet", is_flag=True, default=False)(fn))


@cache
def load_tool_script(filepath: Path) -> ModuleType:
    """Load the given filepath as a tool script."""
    module_name = filepath.stem
    tools_dir = filepath.parent

    log.info("Loading tool from: %s", filepath)

    spec = util.spec_from_file_location("test", filepath)
    if spec is None or spec.loader is None:  # pragma: no cover # Not sure how to trigger this scenario
        raise errors.InvalidModuleError(module_name, tools_dir)
    module = util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError as e:
        raise errors.InvalidModuleError(module_name, tools_dir) from e

    return module


class ToolGatherer(click.MultiCommand):
    """Click command for gathering all valid tools."""

    def list_commands(self, ctx: click.Context) -> list[str]:
        """Dynamically get the list of tool commands."""
        final_config: ClmConfig = ctx.obj
        rv = []
        for name, filepath in final_config.tool_files.items():
            try:
                module = load_tool_script(filepath)
            except Exception as e:  # noqa: BLE001
                log.warning("Failed to get the tool script from `%s` due to: %s", name, e)
                continue
            if not hasattr(module, "tool"):
                log.warning("The module `%s` does not have an attribute `tool`", name)
                continue
            if module.tool is None:
                log.debug("Skipping module `%s`", name)
                continue
            if not isinstance(module.tool, click.Command):
                log.warning("The attribute `tool` in the module `%s` is not of type `click.Command`", name)
                continue
            rv.append(name)
        rv.sort()

        return rv

    def get_command(self, ctx: click.Context, name: str) -> click.Command:
        """Dynamically get the named tool command."""
        final_config: ClmConfig = ctx.obj
        try:
            filepath = final_config.tool_files[name]
        except KeyError:
            msg = f"Unrecognized tool command `{name}`"
            raise click.UsageError(msg) from None
        module = load_tool_script(filepath)
        if not isinstance(module.tool, click.Command):  # pragma: no cover # Should be filtered out in list_commands
            msg = f"The attribute `tool` in the module :{module.__name__} is not of type `click.Command`"
            raise errors.InvalidToolCommandError(msg)
        return module.tool
