"""Module for running LLM tools."""

import typing as t
from abc import ABC, abstractmethod
from importlib import util

import jinja2
import llm

from cli_llm.errors import InvalidModuleError


class ToolRunnerInterface(ABC):
    """Class defining the LLM tool runner interface.

    Using the template pattern, this class defines an interface that child classes can hook into.
    """

    def __init__(self, model: llm.Model) -> None:
        """Initialises the tool with a given model to run the prompt against."""
        self.model = model

    @property
    @abstractmethod
    def prompt(self) -> str:
        """The prompt for the tool."""

    @abstractmethod
    def gather_data(self, **kwargs: t.Any) -> dict[str, t.Any]:
        """Gathers the data needed for the prompt."""

    def render(self, prompt_data: dict[str, t.Any]) -> str:
        """Renders the data to a jinja2 template."""
        return jinja2.Template(self.prompt).render(**prompt_data)

    @abstractmethod
    def process(self, ai_response: llm.Response, data: dict[str, t.Any]) -> None:
        """Processes the response from the LLM."""

    def run(self, **kwargs: t.Any) -> None:
        """Runs the tool."""
        prompt_data = self.gather_data(**kwargs)
        prompt = self.render(prompt_data)
        ai_response = self.model.prompt(prompt)

        self.process(ai_response, prompt_data)


def get_tool(name: str) -> type[ToolRunnerInterface]:
    """Get the tool with the given name."""
    module_name, class_name = name.split(":")

    module_file = f"{module_name}.py"

    spec = util.spec_from_file_location("test", module_file)
    if spec is None or spec.loader is None:  # pragma: no cover # Not sure how to trigger this scenario
        raise InvalidModuleError(name)
    module = util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError as e:
        raise InvalidModuleError(name) from e
    class_ = getattr(module, class_name)

    if not issubclass(class_, ToolRunnerInterface):
        msg = "TODO"
        raise TypeError(msg)
    return class_  # type: ignore [no-any-return]
