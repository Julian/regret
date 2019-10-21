from qualname import qualname
import attr

from regret import _warnings


@attr.s(eq=True, frozen=True)
class Deprecator(object):

    _emit = attr.ib(default=_warnings.emit)

    def emit_deprecation(self, **kwargs):
        self._emit(EmittedDeprecation(**kwargs))

    # -- Deprecatable objects --

    def callable(self):
        def deprecate(thing):
            def call_deprecated(*args, **kwargs):
                self.emit_deprecation(object=thing)
                return thing(*args, **kwargs)
            return call_deprecated
        return deprecate


@attr.s(eq=True, frozen=True, hash=True)
class EmittedDeprecation(object):

    _object = attr.ib()

    def message(self):
        return "{!r} is deprecated.".format(qualname(self._object))


_DEPRECATOR = Deprecator()
