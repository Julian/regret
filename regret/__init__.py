"""
You made a thing, but now you wish it'd go away... Deprecations, a love story.
"""
from regret._api import (  # type: ignore[reportPrivateUsage]  # noqa: E501
    _DEPRECATOR,
    Deprecator,
)

callable = _DEPRECATOR.callable
inheritance = _DEPRECATOR.inheritance
parameter = _DEPRECATOR.parameter
optional_parameter = _DEPRECATOR.optional_parameter

__all__ = [
    "Deprecator",
    "callable",
    "inheritance",
    "optional_parameter",
    "parameter",
]
