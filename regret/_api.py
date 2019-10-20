import attr

from regret import _warnings


@attr.s(eq=True, frozen=True)
class Deprecator(object):

    _emit = attr.ib(default=_warnings.emit)

    def emit(self, **kwargs):
        self._emit(EmittedDeprecation(**kwargs))

    def callable(self):
        def deprecate(thing):
            def call_deprecated():
                self.emit()
                return thing()
            return call_deprecated
        return deprecate


@attr.s(eq=True, frozen=True, hash=True)
class EmittedDeprecation(object):
    pass


_DEPRECATOR = Deprecator()
