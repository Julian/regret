"""
Integration with the standard library's `warnings` module.
"""
import warnings

from regret.emitted import Deprecation

_STACKLEVELS_UNTIL_EMIT_IS_CALLED = 4


def emit(deprecation: Deprecation, extra_stacklevel: int):
    warnings.warn(
        deprecation.message(),
        DeprecationWarning,
        stacklevel=_STACKLEVELS_UNTIL_EMIT_IS_CALLED + extra_stacklevel,
    )
