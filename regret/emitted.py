"""
Objects emitted whilst a deprecated object is being used.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable as _Callable
import inspect

from attrs import field, frozen

from regret.typing import Deprecatable, name_of


def _qualname(obj: Any) -> str:
    """
    Return the (non-fully-)qualified name of the given object.
    """
    return obj.__qualname__


@frozen
class Deprecation:
    """
    A single emitted deprecation.
    """

    _kind: Deprecatable = field(alias="kind")
    _name_of: name_of = field(
        default=_qualname,
        repr=False,
        alias="name_of",
    )
    _replacement: Any = field(default=None, repr=False, alias="replacement")
    _removal_date: date | None = field(
        default=None,
        repr=False,
        alias="removal_date",
    )
    _addendum: str | None = field(default=None, repr=False, alias="addendum")

    def message(self) -> str:
        """
        Express this deprecation as a comprehensible message.
        """
        parts: list[str] = [self._kind.message(name_of=self._name_of)]
        if self._removal_date is not None:
            parts.append(
                f"It will be removed on or after {self._removal_date}.",
            )
        if self._replacement is not None:
            parts.append(
                f"Please use {self._name_of(self._replacement)} instead.",
            )
        if self._addendum is not None:
            parts.append(self._addendum)
        return " ".join(parts)


# --* Representations of deprecated things *--


@frozen
class Callable:
    """
    A parameter for a particular callable.
    """

    _object: Any = field(alias="object")

    def message(self, name_of: name_of) -> str:
        """
        Express this deprecation as a comprehensible message.
        """
        return f"{name_of(self._object)} is deprecated."


@frozen
class Inheritance:
    """
    The subclassing of a given parent type.
    """

    _type: type = field(alias="type")

    def message(self, name_of: name_of) -> str:
        """
        Express this deprecation as a comprehensible message.
        """
        return f"Subclassing from {name_of(self._type)} is deprecated."


@frozen
class Parameter:
    """
    A parameter for a particular callable which should no longer be used.
    """

    _callable: _Callable[..., Any] = field(alias="callable")
    _parameter: inspect.Parameter = field(alias="parameter")

    def message(self, name_of: name_of) -> str:
        """
        Express this deprecation as a comprehensible message.
        """
        return f"The {self._parameter.name!r} parameter is deprecated."


@frozen
class OptionalParameter:
    """
    A parameter for a particular callable which will become mandatory.
    """

    _callable: _Callable[..., Any] = field(alias="callable")
    _parameter: inspect.Parameter = field(alias="parameter")
    _default: Any = field(alias="default")

    def message(self, name_of: name_of) -> str:
        """
        Express this deprecation as a comprehensible message.
        """
        return (
            f"Calling {name_of(self._callable)} without providing the "
            f"{self._parameter.name!r} parameter is deprecated. Using "
            f"{self._default!r} as a default."
        )
