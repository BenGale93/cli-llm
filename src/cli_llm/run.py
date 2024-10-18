"""Module for running LLM tools."""

import typing as t
from abc import ABC, abstractmethod
from importlib import util

import jinja2
import llm

from cli_llm.config import ClmConfig
from cli_llm.errors import InvalidModuleError, InvalidToolClassError
from cli_llm.logging import get_logger, print
from cli_llm.response import Response

StringDict = dict[str, t.Any]

log = get_logger()


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
    def gather_data(self, cli_kwargs: StringDict) -> StringDict:
        """Gathers the data needed for the prompt."""

    def render(self, prompt_data: StringDict) -> str:
        """Renders the data to a jinja2 template."""
        return jinja2.Template(self.prompt).render(**prompt_data)

    @abstractmethod
    def process(self, ai_response: Response, data: StringDict) -> None:
        """Processes the response from the LLM."""

    def run(self, **kwargs: t.Any) -> None:
        """Runs the tool."""
        log.info("Running the gather_data method.")
        try:
            prompt_data = self.gather_data(cli_kwargs=kwargs)
        except Exception:
            log.exception("Error in your tool's gather_data method")
            raise SystemExit(1) from None

        log.info("Running the render method.")
        prompt = self.render(prompt_data)

        print(f"Prompting {self.model}\n")
        ai_response = Response(self.model.prompt(prompt))

        log.info("Running the process method.")
        try:
            self.process(ai_response, prompt_data)
        except Exception:
            log.exception("Error in your tool's process method")
            raise SystemExit(1) from None


def get_tool(name: str, settings: ClmConfig | None = None) -> type[ToolRunnerInterface]:
    """Get the tool with the given name."""
    settings = settings or ClmConfig()
    module_name, class_name = name.split(":")

    module_file = f"{module_name}.py"

    log.info("Looking for the tool in: %s", settings.tools_dir)
    full_module_file = settings.tools_dir / module_file

    spec = util.spec_from_file_location("test", full_module_file)
    if spec is None or spec.loader is None:  # pragma: no cover # Not sure how to trigger this scenario
        raise InvalidModuleError(name, settings.tools_dir)
    module = util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError as e:
        raise InvalidModuleError(name, settings.tools_dir) from e
    try:
        class_ = getattr(module, class_name)
    except AttributeError:
        msg = f"Could not find the class: `{class_name}` in the module: `{module_name}`"
        raise InvalidToolClassError(msg) from None

    if not issubclass(class_, ToolRunnerInterface):
        msg = f"The class `{class_name}` does not inherit from the `ToolRunnerInterface`."
        raise InvalidToolClassError(msg)
    return class_  # type: ignore [no-any-return]


def run_tool(name: str, cli_kwargs: StringDict, settings: ClmConfig | None = None) -> None:
    """Run the given tool with the desired settings and kwargs."""
    settings = settings or ClmConfig()
    log.debug("Using tool: %s", name)
    try:
        tool_class = get_tool(name, settings)
    except Exception:
        log.exception("Error trying to find the tool you specified.")
        raise SystemExit(1) from None

    log.debug("Getting LL model: %s", settings.ll_model)
    model = llm.get_model(settings.ll_model)
    tool = tool_class(model)
    tool.run(**cli_kwargs)
