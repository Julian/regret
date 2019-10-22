from functools import wraps

from qualname import qualname
import attr

from regret import _warnings


@attr.s(eq=True, frozen=True)
class Deprecator(object):

    _emit = attr.ib(default=_warnings.emit)

    def emit_deprecation(self, **kwargs):
        self._emit(EmittedDeprecation(**kwargs))

    # -- Deprecatable objects --

    def callable(self, replacement=None):
        def deprecate(thing):
            @wraps(thing)
            def call_deprecated(*args, **kwargs):
                self.emit_deprecation(object=thing, replacement=replacement)
                return thing(*args, **kwargs)
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
