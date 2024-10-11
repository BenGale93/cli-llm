"""Module containing useful helper functions."""

import contextlib
from pathlib import Path


def gather_file_contents(*, search_path: Path, pattern: str) -> list[tuple[Path, str]]:
    """Gather the contents of all files matching a pattern under the search path.

    Args:
        search_path: The search path to use when searching for the file contents.
        pattern: The pattern to use when searching for the file contents.

    Returns:
        A list of tuples containing the file path and its content as a string.
    """
    files = [p for p in Path(search_path).rglob(pattern) if p.is_file()]
    file_contents = []
    for f in files:
        with contextlib.suppress(UnicodeDecodeError):
            contents = f.read_text()
            file_contents.append((f, contents))

    return file_contents
