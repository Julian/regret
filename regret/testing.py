"""
Helpers for testing your regret.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import contextlib

from attrs import field, frozen

from regret.emitted import Deprecation

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any

    from regret.typing import Deprecatable


class ExpectedDifferentDeprecations(AssertionError):
    """
    Different deprecation(s) were seen than the ones which were expected.
    """


@frozen
class Recorder:
    """
    Recorders keep track of deprecations as they are emitted.

    They provide helper methods for asserting about the deprecations
    afterwards.
    """

    _saw: list[Deprecatable] = field(factory=list, alias="saw")

    def emit(self, deprecation: Deprecatable, extra_stacklevel: int) -> None:
        """
        "Emit" a deprecation by simply storing it.

        An emitter suitable for passing to `regret.Deprecator` instances.
        """
        self._saw.append(deprecation)

    def expect(self, **kwargs: Any) -> contextlib.AbstractContextManager[None]:
        """
        Expect a given set of deprecations to be emitted.
        """
        return self.expect_deprecations(Deprecation(**kwargs))

    @contextlib.contextmanager
    def expect_deprecations(
        self,
        *deprecations: Deprecation,
    ) -> Iterator[None]:
        """
        Expect a given set of deprecations to be emitted.
        """
        expected = self._saw + list(deprecations)
        yield
        if self._saw != expected:
            raise ExpectedDifferentDeprecations((self._saw, expected))

    def expect_clean(self) -> contextlib.AbstractContextManager[None]:
        """
        Expect no deprecations to be emitted.
        """
        return self.expect_deprecations()
