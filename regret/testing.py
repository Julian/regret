"""
Helpers for testing your regret.
"""
from contextlib import contextmanager

import attr

from regret.emitted import Deprecation


class ExpectedDifferentDeprecations(AssertionError):
    pass


@attr.s(eq=True)
class Recorder:

    _saw = attr.ib(factory=list)

    def emit(self, deprecation, extra_stacklevel):
        """
        An emitter suitable for passing to `Deprecator` instances.
        """
        self._saw.append(deprecation)

    def expect(self, **kwargs):
        """
        Expect a given set of deprecations to be emitted.
        """
        return self.expect_deprecations(Deprecation(**kwargs))

    @contextmanager
    def expect_deprecations(self, *deprecations):
        """
        Expect a given set of deprecations to be emitted.
        """
        expected = self._saw + list(deprecations)
        yield
        if self._saw != expected:
            raise ExpectedDifferentDeprecations((self._saw, expected))

    def expect_clean(self):
        """
        Expect no deprecations to be emitted.
        """
        return self.expect_deprecations()
