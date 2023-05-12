"""
Typing related helpers for regret.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable, Protocol


class Deprecatable(Protocol):
    """
    A single kind of deprecatable behavior.
    """

    def message(self, name_of: name_of) -> str:
        """
        Return a message summarizing this deprecation.
        """
        ...


class Emitter(Protocol):
    """
    A callable which reports when deprecated things are used.
    """

    def __call__(
        self,
        extra_stacklevel: int = ...,
        **kwargs: Any,
    ) -> None:
        """
        Somehow emit that something deprecated has been used.
        """
        ...


name_of = Callable[[Any], str]


class new_docstring(Protocol):
    """
    A callable which transforms docstrings to include deprecation info.
    """

    def __call__(
        self,
        object: Any,
        name_of: name_of,
        replacement: Any | None,
        removal_date: date | None,
        version: str,
    ) -> str:
        """
        Transform the docstring, producing a new one.
        """
        ...
