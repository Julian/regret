"""
Integration with the standard library's ``warnings`` module.
"""
import warnings


def emit(deprecation):
    warnings.warn(
        deprecation.message(),
        DeprecationWarning,
        stacklevel=6,  # as everyone well knows, 6 is the best number.
    )
