"""
Objects emitted whilst a deprecated object is being used.
"""
import attr


def _qualname(obj):
    """
    Return the (non-fully-)qualified name of the given object.
    """
    return obj.__qualname__


@attr.s(eq=True, frozen=True, hash=True)
class Deprecation:
    """
    A single emitted deprecation.
    """

    _kind = attr.ib()
    _name_of = attr.ib(default=_qualname, repr=False)
    _replacement = attr.ib(default=None, repr=False)
    _removal_date = attr.ib(default=None, repr=False)
    _addendum = attr.ib(default=None, repr=False)

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


# --* Representations of deprecated things *--

@attr.s(eq=True, frozen=True, hash=True)
class Callable:
    """
    A parameter for a particular callable.
    """

    _object = attr.ib()

    def message(self, name_of):
        return f"{name_of(self._object)} is deprecated."


@attr.s(eq=True, frozen=True, hash=True)
class Inheritance:
    """
    The subclassing of a given parent type.
    """

    _type = attr.ib()

    def message(self, name_of):
        return f"Subclassing from {name_of(self._type)} is deprecated."


@attr.s(eq=True, frozen=True, hash=True)
class Parameter(object):
    """
    A parameter for a particular callable.
    """

    _callable = attr.ib()
    _parameter = attr.ib()

    def message(self, name_of):
        return f"The {self._parameter.name!r} parameter is deprecated."
