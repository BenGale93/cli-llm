"""Errors used in the package."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class CliLlmError(Exception):
    """Base exception for all exceptions raised by this package."""


class InvalidModuleError(CliLlmError):
    """Raised when an invalid module is specified."""

    def __init__(self, module_name: str, tools_dir: "Path") -> None:
        """Initialise the exception with the invalid module name.

        Args:
            module_name: The invalid module name passed by the user.
            tools_dir: Where the tool was searched for.
        """
        super().__init__(
            f"Invalid module name: {module_name}." f" Searched in the following directory: {tools_dir.resolve()}"
        )
