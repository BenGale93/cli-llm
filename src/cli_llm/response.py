"""Module for encapsulating the llm.Response class."""

import typing as t
from pathlib import Path

import llm

from cli_llm._logging import console, spinner


class Response:
    """Response from the LLM."""

    def __init__(self, response: llm.Response) -> None:
        """Initialise with the "underlying llm Response object."""
        self._response = response

    @property
    def response(self) -> llm.Response:
        """Returns the underlying llm Response object."""
        return self._response

    def __repr__(self) -> str:
        """String representation of this class instance."""
        return repr(self._response)

    @spinner("Fetching response from LLM...")
    def text(self) -> str:
        """Returns the full text response from the LLM."""
        return str(self._response.text())

    def __iter__(self) -> t.Iterator[str]:
        """Iterate over this class instance's underlying llm Response object's iterator."""
        return iter(self._response)

    def stream(self) -> None:
        """Stream the AI response to the terminal."""
        for chunk in self:
            console.print(chunk, end="")

    @spinner("Fetching JSON response from LLM...")
    def json(self) -> t.Any:
        """Return LLM response as a JSON, if applicable."""
        return self._response.json()

    def write_to_file(self, filepath: str | Path) -> None:
        """Writes the full text response from the LLM to a given file path."""
        import os

        contents = self.text()
        if not contents.endswith(os.linesep):
            contents += os.linesep
        Path(filepath).write_text(contents)
