"""
Objects emitted whilst a deprecated object is being used.
"""
from datetime import date
from typing import Any, Callable, Optional, Type
import inspect

try:  # pragma: no cover
    from typing import Protocol
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol

import attr


class Kind(Protocol):
    """
    A type of deprecated thing that has been (mis)-used.

    Will be emitted within `Deprecation` objects.
    """

    def message(self, name_of) -> str:
        """
        A suitable message (within a warning or otherwise) for this kind.
        """


def _qualname(obj: Any) -> str:
    """
    Return the (non-fully-)qualified name of the given object.
    """
    return obj.__qualname__


@attr.define(kw_only=True)
class Deprecation:
    """
    A single emitted deprecation.
    """

    _kind: Kind
    _name_of: Callable[[Any], str] = attr.field(default=_qualname, repr=False)
    _replacement: Optional[Any] = attr.field(default=None, repr=False)
    _removal_date: Optional[date] = attr.field(default=None, repr=False)
    _addendum: Optional[str] = attr.field(default=None, repr=False)

    def message(self):
        parts = [self._kind.message(name_of=self._name_of)]
        if self._removal_date is not None:
            parts.append(
                f"It will be removed on or after {self._removal_date}.",
            )
        if self._replacement is not None:
            parts.append(
                f"Please use {self._name_of(self._replacement)} instead.",
            ),
        if self._addendum is not None:
            parts.append(self._addendum)
        return " ".join(parts)


# --* Implementations of deprecated Kinds *--

@attr.define()
class Callable:
    """
    A parameter for a particular callable.
    """

    _object: Any

    def message(self, name_of):
        return f"{name_of(self._object)} is deprecated."


@attr.define()
class Inheritance:
    """
    The subclassing of a given parent type.
    """

    _type: Type

    def message(self, name_of):
        return f"Subclassing from {name_of(self._type)} is deprecated."


@attr.define()
class Parameter(object):
    """
    A parameter for a particular callable.
    """

    _callable: Callable
    _parameter: inspect.Parameter

    def message(self, name_of):
        return f"The {self._parameter.name!r} parameter is deprecated."
