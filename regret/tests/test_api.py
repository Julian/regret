from datetime import date
from textwrap import dedent
from unittest import TestCase
import inspect

from regret.emitted import Callable, Deprecation, Inheritance, Parameter
from regret.testing import Recorder
import regret


class Adder:
    """
    Add things.
    """

    def __init__(self, x=12, y=0):
        self.value = x + y

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):  # pragma: no cover
        return f"<Adder {self.value}>"


def calculate():
    """
    Perform a super important calculation.
    """
    return 12


def add(x, y):
    return 12


class Calculator:
    def better(self):  # pragma: no cover
        return 13

    @regret.callable(version="4.5.6", replacement=better)
    def calculate(self):  # pragma: no cover
        """
        12. Just 12.
        """
        return 12


class TestDeprecator(TestCase):
    def setUp(self):
        self.recorder = Recorder()
        self.regret = regret.Deprecator(emit=self.recorder.emit)

    def test_function(self):
        deprecated = self.regret.callable(version="1.2.3")(calculate)
        with self.recorder.expect(
            Deprecation(kind=Callable(object=calculate)),
        ):
            self.assertEqual(deprecated(), 12)

    def test_method(self):
        class Calculator:
            def _calculate(self):
                return 12

            calculate = self.regret.callable(version="1.2.3")(_calculate)

        with self.recorder.expect(
            Deprecation(kind=Callable(object=Calculator._calculate)),
        ):
            self.assertEqual(Calculator().calculate(), 12)

    def test_class_via_callable(self):
        Deprecated = self.regret.callable(version="1.2.3")(Adder)
        with self.recorder.expect(Deprecation(kind=Callable(object=Adder))):
            self.assertEqual(Deprecated(), Adder())

    def test_function_with_args(self):
        deprecated = self.regret.callable(version="1.2.3")(add)
        with self.recorder.expect(Deprecation(kind=Callable(object=add))):
            self.assertEqual(deprecated(9, y=3), 12)

    def test_class_with_args_via_callable(self):
        Deprecated = self.regret.callable(version="1.2.3")(Adder)
        with self.recorder.expect(Deprecation(kind=Callable(object=Adder))):
            self.assertEqual(Deprecated(9, y=2), Adder(11))

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

    def test_method_gets_deprecation_notice_in_docstring(self):
        class Calculator:
            def _calculate(self):  # pragma: no cover
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

    def test_class_via_callable_gets_deprecation_notice_in_docstring(self):
        Deprecated = self.regret.callable(version="v2.3.4")(Adder)
        self.assertEqual(
            Deprecated.__doc__, dedent(
                """
                Add things.

                .. deprecated:: v2.3.4
                """,
            )
        )

    def test_function_with_no_docstring_does_not_get_deprecation_notice(self):
        """
        If you're too lazy to add docstrings I ain't helping you.
        """
        def calculate():  # pragma: no cover
            return 12
        deprecated = self.regret.callable(version="v2.3.4")(calculate)
        self.assertIsNone(deprecated.__doc__)

    def test_method_with_no_docstring_does_not_get_notice(self):
        """
        If you're too lazy to add docstrings I ain't helping you.
        """
        class Lazy:
            @self.regret.callable(version="v2.3.4")
            def method():  # pragma: no cover
                pass
        self.assertIsNone(Lazy.method.__doc__)

    def test_class_via_callable_with_no_docstring_does_not_get_notice(self):
        """
        If you're too lazy to add docstrings I ain't helping you.
        """
        @self.regret.callable(version="v2.3.4")
        class Lazy:
            pass
        self.assertIsNone(Lazy.__doc__)

    def test_function_with_removal_date(self):
        removal_date = date(year=2012, month=12, day=12)
        deprecated = self.regret.callable(
            version="1.2.3",
            removal_date=removal_date,
        )(calculate)

        with self.recorder.expect(
            Deprecation(
                kind=Callable(object=calculate),
                removal_date=removal_date,
            ),
        ):
            self.assertEqual(deprecated(), 12)

    def test_method_with_removal_date(self):
        removal_date = date(year=2012, month=12, day=12)

        class Class:
            def _method(self):  # pragma: no cover
                return 12

            method = self.regret.callable(
                version="v2.3.4",
                removal_date=removal_date,
            )(_method)

        with self.recorder.expect(
            Deprecation(
                kind=Callable(object=Class._method),
                removal_date=removal_date,
            ),
        ):
            self.assertEqual(Class().method(), 12)

    def test_function_with_removal_date_deprecation_notice_in_docstring(self):
        removal_date = date(year=2012, month=12, day=12)
        deprecated = self.regret.callable(
            version="1.2.3",
            removal_date=removal_date,
        )(calculate)
        self.assertEqual(
            deprecated.__doc__, dedent(
                """
                Perform a super important calculation.

                .. deprecated:: 1.2.3

                    It will be removed on or after 2012-12-12.
                """,
            ),
        )

    def test_function_with_replacement(self):
        deprecated = self.regret.callable(
            version="1.2.3",
            replacement=add,
        )(calculate)

        with self.recorder.expect(
            Deprecation(
                kind=Callable(object=calculate),
                replacement=add,
            ),
        ):
            self.assertEqual(deprecated(), 12)

    def test_class_via_callable_with_replacement(self):
        class Subtractor:
            pass

        Deprecated = self.regret.callable(
            version="1.2.3",
            replacement=Subtractor,
        )(Adder)

        with self.recorder.expect(
            Deprecation(kind=Callable(object=Adder), replacement=Subtractor),
        ):
            self.assertEqual(Deprecated(), Adder())

    def test_function_with_replacement_deprecation_notice_in_docstring(self):
        deprecated = self.regret.callable(
            version="1.2.3",
            replacement=add,
        )(calculate)
        self.assertEqual(
            deprecated.__doc__, dedent(
                """
                Perform a super important calculation.

                .. deprecated:: 1.2.3

                    Please use `add` instead.
                """,
            ),
        )

    def test_method_with_replacement_deprecation_notice_in_docstring(self):
        expected = """
        12. Just 12.

        .. deprecated:: 4.5.6

            Please use `Calculator.better` instead.
        """
        self.assertEqual(Calculator.calculate.__doc__, dedent(expected))

    def test_class_via_callable_with_replacement_deprecation_docstring(self):
        Deprecated = self.regret.callable(
            version="v2.3.4",
            replacement=Calculator,
        )(Adder)
        self.assertEqual(
            Deprecated.__doc__, dedent(
                """
                Add things.

                .. deprecated:: v2.3.4

                    Please use `Calculator` instead.
                """,
            )
        )

    def test_function_with_removal_date_and_replacement_docstring(self):
        removal_date = date(year=2012, month=12, day=12)
        deprecated = self.regret.callable(
            version="1.2.3",
            replacement=add,
            removal_date=removal_date,
        )(calculate)
        self.assertEqual(
            deprecated.__doc__, dedent(
                """
                Perform a super important calculation.

                .. deprecated:: 1.2.3

                    Please use `add` instead.

                    It will be removed on or after 2012-12-12.
                """,
            ),
        )

    def test_function_is_wrapped(self):
        deprecated = self.regret.callable(version="1.2.3")(calculate)
        self.assertEqual(calculate.__name__, deprecated.__name__)

    def test_method_is_wrapped(self):
        class Calculator:
            def _calculate(self):  # pragma: no cover
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

    def test_class_via_callable_is_wrapped(self):
        Deprecated = self.regret.callable(version="1.2.3")(Adder)
        self.assertEqual(Deprecated.__name__, Adder.__name__)

    def test_original_functions_are_not_mutated(self):
        """
        Deprecating a function in one spot does not mutate the original.

        Any existing references are unchanged.
        """

        def original():
            """Original function docstring."""

        original.something = 12
        self.assertEqual(
            (
                original.__name__,
                original.__doc__,
                vars(original),
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
                vars(original),
            ), (
                "original",
                "Original function docstring.",
                {"something": 12},
            ),
        )

    def test_original_methods_are_not_mutated(self):
        """
        Deprecating a method in one spot does not mutate the original.

        Any existing references are unchanged.
        """

        class Class:
            def method(self):
                """Original method docstring."""

            method.something = 12

            deprecated = self.regret.callable(version="4.5.6")(method)

        self.assertEqual(
            (
                Class.method.__name__,
                Class.method.__doc__,
                vars(Class.method),
            ), (
                "method",
                "Original method docstring.",
                {"something": 12},
            ),
        )

    def test_original_classes_are_not_mutated_via_callable(self):
        """
        Deprecating a class in one spot does not mutate the original.

        Any existing references are unchanged.
        """

        class Original:
            """Original class docstring."""

        Original.something = 12
        self.assertEqual(
            (
                Original.__name__,
                Original.__doc__,
                getattr(Original, "something", None),
            ), (
                "Original",
                "Original class docstring.",
                12,
            ),
        )

        self.regret.callable(version="1.2.3")(Original)

        self.assertEqual(
            (
                Original.__name__,
                Original.__doc__,
                getattr(Original, "something", None),
            ), (
                "Original",
                "Original class docstring.",
                12,
            ),
        )

    def test_dunder_call(self):
        class Calculator:
            def _calculate(self):
                return 12

            __call__ = self.regret.callable(version="1.2.3")(_calculate)

        with self.recorder.expect(
            Deprecation(kind=Callable(object=Calculator._calculate)),
        ):
            self.assertEqual(Calculator()(), 12)

    def test_function_parameter(self):
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y, z):
            return x + y + z

        with self.recorder.expect(
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="z",
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                ),
            ),
        ):
            self.assertEqual(add3(1, 2, z=3), 6)

    def test_function_parameter_positionally(self):
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y, z):
            return x + y + z

        with self.recorder.expect(
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="z",
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                ),
            ),
        ):
            self.assertEqual(add3(1, 2, 3), 6)

    def test_function_parameter_keyword_only(self):
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y, *, z):
            return x + y + z

        with self.recorder.expect(
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="z",
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    ),
                ),
            ),
        ):
            self.assertEqual(add3(1, 2, z=3), 6)

    def test_function_parameter_unprovided_does_not_warn(self):
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y, z=0):
            return x + y + z

        with self.recorder.expect_clean():
            self.assertEqual(add3(1, 2), 3)

    def test_function_with_deprecated_parameter_is_wrapped(self):
        deprecated = self.regret.parameter(version="1.2.3", name="y")(add)
        self.assertEqual(add.__name__, deprecated.__name__)

    def test_function_with_deprecated_parameter_does_not_mutate_original(self):
        """
        Deprecating a function parameter does not mutate the original function.
        """

        def original(x):
            """Original function docstring."""

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

        self.regret.parameter(version="1.2.3", name="x")(original)

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

    def test_multiple_function_parameters(self):
        @self.regret.parameter(version="1.2.3", name="y")
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y, z):
            return x + y + z

        with self.recorder.expect(
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="y",
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                ),
            ),
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="z",
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                ),
            ),
        ):
            self.assertEqual(add3(1, 2, z=3), 6)

    def test_multiple_function_parameters_positionally(self):
        @self.regret.parameter(version="1.2.3", name="y")
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y, z):
            return x + y + z

        with self.recorder.expect(
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="y",
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                ),
            ),
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="z",
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                ),
            ),
        ):
            self.assertEqual(add3(1, 2, 3), 6)

    def test_multiple_function_parameters_keyword_only(self):
        @self.regret.parameter(version="1.2.3", name="y")
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, *, y, z):
            return x + y + z

        with self.recorder.expect(
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="y",
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    ),
                ),
            ),
            Deprecation(
                kind=Parameter(
                    callable=add3,
                    parameter=inspect.Parameter(
                        name="z",
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    ),
                ),
            ),
        ):
            self.assertEqual(add3(1, y=2, z=3), 6)

    def test_multiple_function_parameters_warn_in_definition_order(self):
        """
        No matter what order parameters are deprecated in, warnings are emitted
        in the definition order that parameters were originally defined in.
        """

        @self.regret.parameter(version="1.2.3", name="z")
        @self.regret.parameter(version="1.2.3", name="v")
        @self.regret.parameter(version="1.2.3", name="x")
        @self.regret.parameter(version="1.2.3", name="y")
        def add5(v, w, x, y, z):
            return v + w + x + y + z

        with self.recorder.expect(
            *[
                Deprecation(
                    kind=Parameter(
                        callable=add5,
                        parameter=inspect.Parameter(
                            name=each,
                            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        ),
                    ),
                ) for each in "vxyz"
            ],
        ):
            self.assertEqual(add5(1, 2, 3, 4, 5), 15)

    def test_multiple_function_parameters_unprovided_does_not_warn(self):
        @self.regret.parameter(version="1.2.3", name="y")
        @self.regret.parameter(version="1.2.3", name="z")
        def add3(x, y=0, z=0):
            return x + y + z

        with self.recorder.expect_clean():
            self.assertEqual(add3(1), 1)

    def test_function_with_multiple_deprecated_parameters_is_wrapped(self):
        deprecated = self.regret.parameter(
            version="1.2.3",
            name="x",
        )(
            self.regret.parameter(
                version="1.2.3",
                name="y",
            )(add)
        )
        self.assertEqual(add.__name__, deprecated.__name__)

    def test_inheritance(self):
        class Inheritable:
            pass

        with self.recorder.expect_clean():
            class SubclassOfInheritable(Inheritable):
                pass

        Uninheritable = self.regret.inheritance(version="2.3.4")(Inheritable)

        with self.recorder.expect(
            Deprecation(kind=Inheritance(type=Uninheritable)),
        ):
            class SubclassOfUninheritable(Uninheritable):
                pass

    def test_inheritance_has_init_subclass(self):
        class Inheritable:
            def __init_subclass__(Subclass, **kwargs):
                Subclass.init = kwargs

        class SubclassOfInheritable(Inheritable, foo="bar"):
            pass

        self.assertEqual(SubclassOfInheritable.init, dict(foo="bar"))

        Uninheritable = self.regret.inheritance(version="2.3.4")(Inheritable)

        with self.recorder.expect(
            Deprecation(kind=Inheritance(type=Uninheritable)),
        ):
            class SubclassOfUninheritable(Uninheritable, baz="quux"):
                pass

        self.assertEqual(SubclassOfUninheritable.init, dict(baz="quux"))

    def test_inheritance_nonclass(self):
        def not_a_class():  # pragma: no cover
            pass

        with self.assertRaises(Exception) as e:
            class Subclass(not_a_class):
                pass

        with self.assertRaises(e.exception.__class__):
            self.regret.inheritance(version="2.3.4")(not_a_class)

    def test_class_with_deprecated_inheritance_is_wrapped(self):
        Uninheritable = self.regret.inheritance(version="1.2.3")(Adder)
        self.assertEqual(
            (
                Uninheritable.__name__,
                Uninheritable.__doc__,
                public_members(Uninheritable),
            ), (
                Adder.__name__,
                Adder.__doc__,
                public_members(Adder),
            ),
        )

    def test_original_classes_are_not_mutated_via_inheritance(self):
        """
        Deprecating inheritance in one spot does not mutate the original class.

        Any existing references are unchanged.
        """

        class Original:
            """Original class docstring."""

        Original.something = 12
        self.assertEqual(
            (
                Original.__name__,
                Original.__doc__,
                getattr(Original, "something", None),
            ), (
                "Original",
                "Original class docstring.",
                12,
            ),
        )

        self.regret.inheritance(version="1.2.3")(Original)

        self.assertEqual(
            (
                Original.__name__,
                Original.__doc__,
                getattr(Original, "something", None),
            ), (
                "Original",
                "Original class docstring.",
                12,
            ),
        )


def public_members(thing):
    return {
        name for name, _ in inspect.getmembers(thing)
        if not name.startswith("_")
    }


class TestRegretDefaultDeprecator(TestCase):
    def test_it_exposes_deprecator_methods_in_default_configuration(self):
        self.assertGreaterEqual(
            public_members(regret),
            public_members(regret.Deprecator),
        )
