"""
Helpers for testing your regret.
"""
import attr


@attr.s(eq=True)
class Recorder:

    saw = attr.ib(factory=list)

    def emit(self, deprecation, extra_stacklevel):
        self.saw.append(deprecation)
