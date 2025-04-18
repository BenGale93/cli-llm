"""Module for running LLM tools."""

from typing import TYPE_CHECKING

import jinja2

from cli_llm._logging import ClmLogger
from cli_llm.response import Response

if TYPE_CHECKING:
    from cli_llm.config import ClmConfig
    from cli_llm.types import StringDict

log = ClmLogger()


def _render(prompt: str, prompt_data: "StringDict") -> str:
    """Render the prompt with the given data."""
    log.info("Rendering the prompt.")
    rendered_prompt = jinja2.Template(prompt).render(**prompt_data)
    log.debug("Prompt: %s", rendered_prompt)
    return rendered_prompt


def run(config: "ClmConfig", prompt: str, prompt_data: "StringDict") -> Response:
    """Run the LLM.

    Args:
        config: The LLM configuration object.
        prompt: The prompt to render with the given data.
        prompt_data: The data to render the prompt with.

    Returns:
        The response from the LLM.
    """
    rendered_prompt = _render(prompt, prompt_data)

    log.info("Getting the model: %s", config.ll_model)
    model = config.model()

    log.print(f"Prompting {model}\n")
    return Response(model.prompt(rendered_prompt))
