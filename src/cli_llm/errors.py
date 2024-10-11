"""Errors used in the package."""


class CliLlmError(Exception):
    """Base exception for all exceptions raised by this package."""


class InvalidModuleError(CliLlmError):
    """Raised when an invalid module is specified."""

    def __init__(self, module_name: str) -> None:
        """Initialise the exception with the invalid module name.

        Args:
            module_name: The invalid module name passed by the user.
        """
        super().__init__(
            f"Invalid module name: {module_name}." " It is usually the name of the python file you are trying to use."
        )
