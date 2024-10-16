"""Module defining the applications logging and other terminal feedback."""

import logging
import typing as t
from functools import wraps

import click
from rich.console import Console
from rich.logging import RichHandler

from cli_llm.types import RT

console = Console(record=True, stderr=True)

FORMAT = "%(message)s"
logging.basicConfig(
    level="WARNING",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click], console=console)],
)

NO_LOGGING = logging.ERROR


def spinner(message: str) -> t.Callable[[t.Callable[..., RT]], t.Callable[..., RT]]:
    """Runs the decorated function with a rich spinner using the given message."""

    def decorator(func: t.Callable[..., RT]) -> t.Callable[..., RT]:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> RT:
            with console.status(message):
                return func(*args, **kwargs)

        return wrapper

    return decorator


class ClmLogger:
    """Application logger singleton."""

    VERBOSE_COUNT: t.ClassVar[dict[int, int]] = {
        0: 30,
        1: 20,
        2: 10,
    }

    def __init__(self) -> None:
        """Initialise with default verbosity."""
        self.verbose = 30
        self._log = logging.getLogger("cli-llm")

    def get_logger(self) -> logging.Logger:
        """Get the logger."""
        return self._log

    def set_verbosity(self, *, verbose: int, quiet: bool) -> None:
        """Set the verbosity of the logger."""
        if quiet:
            self.verbose = NO_LOGGING
        else:
            self.verbose = self.VERBOSE_COUNT[verbose]
        self._log.setLevel(self.verbose)

    def print(self, *objects: t.Any, sep: str = " ", end: str = "\n") -> None:
        """Print if not quiet."""
        if self.verbose < NO_LOGGING:
            console.print(*objects, sep=sep, end=end)


_clm_logger = ClmLogger()

get_logger = _clm_logger.get_logger

set_verbosity = _clm_logger.set_verbosity

print = _clm_logger.print  # noqa: A001
