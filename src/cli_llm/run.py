"""Module for running LLM tools."""

import typing as t
from functools import cache
from importlib import util
from pathlib import Path
from types import ModuleType

import jinja2

from cli_llm.config import ClmConfig
from cli_llm.errors import InvalidModuleError
from cli_llm.logging import get_logger, print
from cli_llm.response import Response

StringDict = dict[str, t.Any]

log = get_logger()


def render(prompt: str, prompt_data: StringDict) -> str:
    """Render the prompt with the given data."""
    log.info("Rendering the prompt.")
    rendered_prompt = jinja2.Template(prompt).render(**prompt_data)
    log.debug("Prompt: %s", rendered_prompt)
    return rendered_prompt


def run(config: ClmConfig, prompt: str, prompt_data: StringDict) -> Response:
    """Run the LLM.

    Args:
        config: The LLM configuration object.
        prompt: The prompt to render with the given data.
        prompt_data: The data to render the prompt with.

    Returns:
        The response from the LLM.
    """
    rendered_prompt = render(prompt, prompt_data)

    log.info("Getting the model: %s", config.ll_model)
    model = config.model()

    print(f"Prompting {model}\n")
    return Response(model.prompt(rendered_prompt))


@cache
def load_tool_script(module_name: str, tools_dir: Path) -> ModuleType:
    """Load module_name from tools_dir."""
    module_file = f"{module_name}.py"

    log.info("Looking for the tool in: %s", tools_dir)
    full_module_file = tools_dir / module_file

    spec = util.spec_from_file_location("test", full_module_file)
    if spec is None or spec.loader is None:  # pragma: no cover # Not sure how to trigger this scenario
        raise InvalidModuleError(module_name, tools_dir)
    module = util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError as e:
        raise InvalidModuleError(module_name, tools_dir) from e

    return module
