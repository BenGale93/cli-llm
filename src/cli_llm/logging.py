"""Module defining the applications logging and other terminal feedback."""

import logging
import typing as t

import click
import rich
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="WARNING",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])],
)

NO_LOGGING = 60


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
            return
        self.verbose = self.VERBOSE_COUNT[verbose]
        self._log.setLevel(self.verbose)

    def print(
        self, *objects: t.Any, sep: str = " ", end: str = "\n", file: t.IO[str] | None = None, flush: bool = False
    ) -> None:
        """Print if not quiet."""
        if self.verbose < NO_LOGGING:
            rich.print(*objects, sep=sep, end=end, file=file, flush=flush)


_clm_logger = ClmLogger()

get_logger = _clm_logger.get_logger

set_verbosity = _clm_logger.set_verbosity

print = _clm_logger.print  # noqa: A001
