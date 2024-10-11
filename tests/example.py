"""Example tool."""

from typing import Any

import llm
import rich

from cli_llm.run import ToolRunnerInterface

PROMPT = """
- This is a test prompt

{{test}}
"""


class Summarise(ToolRunnerInterface):
    prompt = PROMPT

    def gather_data(self, **kwargs: Any) -> dict[str, Any]:
        return kwargs

    def process(self, ai_response: llm.Response, data: dict[str, Any]) -> None:
        for chunk in ai_response:
            rich.print(chunk, end="")
        for key, value in data.items():
            rich.print(f"{key}: {value}")
