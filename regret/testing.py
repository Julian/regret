"""
Helpers for testing your regret.
"""
import attr


@attr.s(eq=True)
class Recorder(object):

    saw = attr.ib(factory=list)

    def emit(self, deprecation):
        self.saw.append(deprecation)
