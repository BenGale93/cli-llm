import typing as t
from functools import cache
from importlib import util
from pathlib import Path
from types import ModuleType

import click

from cli_llm import ClmConfig, errors
from cli_llm._logging import get_logger
from cli_llm.types import RT

log = get_logger()


def common_options(fn: t.Callable[..., RT]) -> t.Callable[..., RT]:
    """Common options for commands."""
    return click.option("-v", "--verbose", count=True)(click.option("-q", "--quiet", is_flag=True, default=False)(fn))


@cache
def load_tool_script(module_name: str, tools_dir: Path) -> ModuleType:
    """Load module_name from tools_dir."""
    module_file = f"{module_name}.py"

    log.info("Looking for the tool in: %s", tools_dir)
    full_module_file = tools_dir / module_file

    spec = util.spec_from_file_location("test", full_module_file)
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
