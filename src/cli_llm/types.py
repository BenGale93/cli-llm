"""Module containing type definitions used across the application."""

import typing as t

RT = t.TypeVar("RT")
P = t.ParamSpec("P")

StringDict = dict[str, t.Any]
