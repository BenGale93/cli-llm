"""Example tool."""

import click
import rich

from cli_llm import Response, StringDict, ToolRunnerInterface

PROMPT = """
- This is a test prompt

{{test}}
"""


class Summarise(ToolRunnerInterface):
    prompt = PROMPT
    ARGS = (click.Option(["--key1"]),)

    def gather_data(self, cli_kwargs: StringDict) -> StringDict:
        return cli_kwargs

    def process(self, ai_response: Response, data: StringDict) -> None:
        for chunk in ai_response:
            rich.print(chunk, end="")
        for key, value in data.items():
            rich.print(f"{key}: {value}")


class BadGatherData(Summarise):
    def gather_data(self, cli_kwargs: StringDict) -> StringDict:  # noqa: ARG002
        raise ZeroDivisionError


class BadProcess(Summarise):
    def process(self, ai_response: Response, data: StringDict) -> None:  # noqa: ARG002
        raise ZeroDivisionError
