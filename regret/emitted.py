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
class Deprecation(object):
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
                "It will be removed on or after {}.".format(self._removal_date)
            )
        if self._replacement is not None:
            parts.append(
                "Please use {} instead.".format(
                    self._name_of(self._replacement),
                ),
            )
        if self._addendum is not None:
            parts.append(self._addendum)
        return " ".join(parts)


# --* Representations of deprecated things *--

@attr.s(eq=True, frozen=True, hash=True)
class Callable(object):
    """
    A parameter for a particular callable.
    """

    _object = attr.ib()

    def message(self, name_of):
        return "{} is deprecated.".format(name_of(self._object))


@attr.s(eq=True, frozen=True, hash=True)
class Inheritance(object):
    """
    The subclassing of a given parent type.
    """

    _type = attr.ib()

    def message(self, name_of):
        return "Subclassing from {} is deprecated.".format(
            name_of(self._type),
        )
