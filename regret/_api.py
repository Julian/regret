from functools import wraps
from textwrap import dedent

from qualname import qualname
import attr

from regret import _warnings


@attr.s(eq=True, frozen=True)
class Deprecator(object):

    _emit = attr.ib(default=_warnings.emit)

    def emit_deprecation(self, **kwargs):
        self._emit(EmittedDeprecation(**kwargs))

    # -- Deprecatable objects --

    def callable(self, version, replacement=None):
        """
        Deprecate a callable as of the given version.

        Arguments:

            version:

                the first version in which the deprecated object was considered
                deprecated

            replacement:

                optionally, an object that is the (direct or indirect)
                replacement for the functionality previously performed
                by the deprecated callable
        """

        def deprecate(thing):
            @wraps(thing)
            def call_deprecated(*args, **kwargs):
                self.emit_deprecation(object=thing, replacement=replacement)
                return thing(*args, **kwargs)

            __doc__ = thing.__doc__
            if __doc__ is not None:
                call_deprecated.__doc__ = dedent(__doc__) + dedent(
                    """
                    .. deprecated:: {version}
                    """.format(version=version),
                )

            return call_deprecated
        return deprecate


@attr.s(eq=True, frozen=True, hash=True)
class EmittedDeprecation(object):

    _object = attr.ib()
    _replacement = attr.ib(default=None)

    def message(self):
        if self._replacement is None:
            replacement_info = ""
        else:
            replacement_info = " Please use {!r} instead.".format(
                qualname(self._replacement),
            )
        return "{qualname!r} is deprecated.{replacement_info}".format(
            qualname=qualname(self._object),
            replacement_info=replacement_info,
        )


_DEPRECATOR = Deprecator()
