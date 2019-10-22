from unittest import TestCase

from regret import EmittedDeprecation, Deprecator
from regret.testing import Recorder


def calculate():
    """
    Perform a super important calculation.
    """
    return 12


def add(x, y):
    return 12


class TestRegret(TestCase):
    def setUp(self):
        self.recorder = Recorder()
        self.regret = Deprecator(emit=self.recorder.emit)

    def test_function(self):
        self.assertEqual(
            (self.regret.callable()(calculate)(), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=calculate)]),
            ),
        )

    def test_function_with_args(self):
        self.assertEqual(
            (self.regret.callable()(add)(9, y=3), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=add)]),
            ),
        )

    def test_function_is_wrapped(self):
        deprecated = self.regret.callable()(calculate)
        self.assertEqual(
            (calculate.__name__, calculate.__doc__),
            (deprecated.__name__, deprecated.__doc__),
        )

    def test_method(self):
        class Calculator(object):
            def _calculate(self):
                return 12

            calculate = self.regret.callable()(_calculate)

        unbound = getattr(
            Calculator._calculate, "im_func", Calculator._calculate,
        )

        self.assertEqual(
            (Calculator().calculate(), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=unbound)]),
            ),
        )

    def test_method_is_wrapped(self):
        class Calculator(object):
            def _calculate(self):
                """
                Perform a super important calculation.
                """
                return 12

            calculate = self.regret.callable()(_calculate)

        self.assertEqual(
            (
                Calculator.calculate.__name__,
                Calculator.calculate.__doc__,
                Calculator().calculate.__name__,
                Calculator().calculate.__doc__,
            ),
            (
                Calculator._calculate.__name__,
                Calculator._calculate.__doc__,
                Calculator._calculate.__name__,
                Calculator._calculate.__doc__,
            ),
        )

    def test_dunder_call(self):
        class Calculator(object):
            def _calculate(self):
                return 12

            __call__ = self.regret.callable()(_calculate)

        unbound = getattr(
            Calculator._calculate, "im_func", Calculator._calculate,
        )

        self.assertEqual(
            (Calculator()(), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=unbound)]),
            ),
        )
