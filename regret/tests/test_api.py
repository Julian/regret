from textwrap import dedent
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
            (
                self.regret.callable(version="1.2.3")(calculate)(),
                self.recorder,
            ), (
                12,
                Recorder(saw=[EmittedDeprecation(object=calculate)]),
            ),
        )

    def test_function_with_args(self):
        self.assertEqual(
            (
                self.regret.callable(version="1.2.3")(add)(9, y=3),
                self.recorder,
            ), (
                12,
                Recorder(saw=[EmittedDeprecation(object=add)]),
            ),
        )

    def test_function_gets_deprecation_notice_in_docstring(self):
        deprecated = self.regret.callable(version="v2.3.4")(calculate)
        self.assertEqual(
            deprecated.__doc__, dedent(
                """
                Perform a super important calculation.

                .. deprecated:: v2.3.4
                """,
            )
        )

    def test_function_with_no_docstring_does_not_get_deprecation_notice(self):
        """
        If you're too lazy to add docstrings I ain't helping you.
        """
        def calculate():
            return 12
        deprecated = self.regret.callable(version="v2.3.4")(calculate)
        self.assertIsNone(deprecated.__doc__)

    def test_function_with_replacement(self):
        self.assertEqual(
            (
                self.regret.callable(
                    version="1.2.3",
                    replacement=add,
                )(calculate)(),
                self.recorder,
            ), (
                12,
                Recorder(
                    saw=[
                        EmittedDeprecation(object=calculate, replacement=add),
                    ],
                ),
            ),
        )

    def test_function_is_wrapped(self):
        deprecated = self.regret.callable(version="1.2.3")(calculate)
        self.assertEqual(calculate.__name__, deprecated.__name__)

    def test_original_functions_are_not_mutated(self):
        """
        Deprecating a function in one spot does not mutate the original.

        Any existing references are unchanged.
        """

        def original():
            "Original function docstring."

        original.something = 12
        self.assertEqual(
            (
                original.__name__,
                original.__doc__,
                getattr(original, "__dict__", {}),
            ), (
                "original",
                "Original function docstring.",
                {"something": 12},
            ),
        )

        self.regret.callable(version="1.2.3")(original)

        self.assertEqual(
            (
                original.__name__,
                original.__doc__,
                getattr(original, "__dict__", {}),
            ), (
                "original",
                "Original function docstring.",
                {"something": 12},
            ),
        )

    def test_method(self):
        class Calculator(object):
            def _calculate(self):
                return 12

            calculate = self.regret.callable(version="1.2.3")(_calculate)

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

            calculate = self.regret.callable(version="1.2.3")(_calculate)

        self.assertEqual(
            (
                Calculator.calculate.__name__,
                Calculator().calculate.__name__,
            ),
            (
                Calculator._calculate.__name__,
                Calculator._calculate.__name__,
            ),
        )

    def test_method_gets_deprecation_notice_in_docstring(self):
        class Calculator(object):
            def _calculate(self):
                """
                Perform a super important calculation.
                """
                return 12

            calculate = self.regret.callable(version="4.5.6")(_calculate)

        expected = """
        Perform a super important calculation.

        .. deprecated:: 4.5.6
        """

        self.assertEqual(
            (
                Calculator.calculate.__doc__,
                Calculator().calculate.__doc__,
            ),
            (
                dedent(expected),
                dedent(expected),
            ),
        )

    def test_original_methods_are_not_mutated(self):
        """
        Deprecating a method in one spot does not mutate the original.

        Any existing references are unchanged.
        """

        class Class(object):
            def method(self):
                "Original method docstring."

            method.something = 12

            deprecated = self.regret.callable(version="4.5.6")(method)

        self.assertEqual(
            (
                Class.method.__name__,
                Class.method.__doc__,
                getattr(Class.method, "__dict__", {}),
            ), (
                "method",
                "Original method docstring.",
                {"something": 12},
            ),
        )

    def test_dunder_call(self):
        class Calculator(object):
            def _calculate(self):
                return 12

            __call__ = self.regret.callable(version="1.2.3")(_calculate)

        unbound = getattr(
            Calculator._calculate, "im_func", Calculator._calculate,
        )

        self.assertEqual(
            (Calculator()(), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=unbound)]),
            ),
        )
