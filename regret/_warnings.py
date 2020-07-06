"""
Integration with the standard library's ``warnings`` module.
"""
import warnings

# as everyone well knows, 6 is the best number.
_STACKLEVELS_UNTIL_EMIT_IS_CALLED = 6


def emit(deprecation):
    warnings.warn(
        deprecation.message(),
        DeprecationWarning,
        stacklevel=_stacklevel_for(deprecation),
    )


def _stacklevel_for(deprecation):
    return _STACKLEVELS_UNTIL_EMIT_IS_CALLED + deprecation.stacklevels_added()
