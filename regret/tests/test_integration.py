from datetime import date
import collections
import sys

from twisted.trial.unittest import SynchronousTestCase

import regret


class Calculator:
    @regret.callable(version="1.2.3")
    def __call__(self):
        return 12

    @regret.callable(version="1.2.3")
    def calculate(self):
        return 12


CalculatorWithDeprecatedInheritance = regret.inheritance(version="1.2.3")(
    Calculator,
)


@regret.callable(version="1.2.3")
def calculate():
    return 12


@regret.callable(version="1.2.3")
def add(x, y):
    return x + y


@regret.parameter(version="1.2.3", name="z")
def add3(x, y, z):
    return x + y + z


@regret.optional_parameter(version="1.2.3", name="z", default=0)
def add4(w, x, y, z):
    return w + x + y + z


@regret.parameter(version="1.2.3", name="y")
@regret.optional_parameter(version="1.2.3", name="z", default=0)
def add5(v, w, x, y, z):
    return v + w + x + y + z


@regret.callable(version="1.2.3", replacement=Calculator)
def calculator_fn():
    return 9


def divide():
    return 7


class TestRegret(SynchronousTestCase):
    def assertDeprecated(
        self,
        message,
        fn,
        *,
        filename=None,
        args=(),
        kwargs={},  # noqa: B006
    ):
        if filename is None:
            # sigh, see https://twistedmatrix.com/trac/ticket/9363
            filename = sys.modules[self.assertWarns.__module__].__file__

        # Sigh... assertWarns takes positional args positionally,
        # instead of as a sequence.
        return self.assertWarns(
            DeprecationWarning,
            message,
            filename,
            fn,
            *args,
            **kwargs,
        )

    def test_function(self):
        result = self.assertDeprecated(
            message="calculate is deprecated.",
            fn=calculate,
        )
        self.assertEqual(result, 12)

    def test_function_with_args(self):
        result = self.assertDeprecated(
            message="add is deprecated.",
            fn=add,
            args=(9,),
            kwargs=dict(y=3),
        )
        self.assertEqual(result, 12)

    def test_function_with_replacement(self):
        result = self.assertDeprecated(
            message=(
                "calculator_fn is deprecated. "
                "Please use Calculator instead."
            ),
            fn=calculator_fn,
        )
        self.assertEqual(result, 9)

    def test_function_with_builtin_replacement(self):
        """
        This will never happen. Right?
        """
        deprecated = regret.callable(
            version="1.2.3",
            replacement=str,
        )(collections.UserString)
        result = self.assertDeprecated(
            message=("UserString is deprecated. " "Please use str instead."),
            fn=deprecated,
            args=("foo",),
        )
        self.assertEqual(result, "foo")

    def test_method(self):
        calculator = Calculator()
        result = self.assertDeprecated(
            message="Calculator.calculate is deprecated.",
            fn=calculator.calculate,
        )
        self.assertEqual(result, 12)

    def test_dunder_call(self):
        calculator = Calculator()
        result = self.assertDeprecated(
            message="Calculator.__call__ is deprecated.",
            fn=calculator,
        )
        self.assertEqual(result, 12)

    def test_custom_qualname(self):
        etacerped = regret.Deprecator(
            name_of=lambda object: object.__name__[::-1],
        )

        @etacerped.callable(version="v1.2.3")
        def calculate():
            return 12

        self.assertDeprecated(
            message="etaluclac is deprecated.",
            fn=calculate,
        )

    def test_custom_docstring_modifier(self):
        def new_docstring(
            object,
            replacement,
            removal_date,
            name_of,
            version,
        ):
            return (
                object.__doc__
                + name_of(object)
                + " deprecated in "
                + version
                + " replaced by "
                + replacement.__doc__
            )

        deprecate = regret.Deprecator(
            name_of=lambda object: "OBJECTNAME",
            new_docstring=new_docstring,
        )

        def replacement():
            """New hotness."""

        @deprecate.callable(version="v1.2.3", replacement=replacement)
        def calculate():
            """Very important docstring for..."""

        self.assertEqual(
            calculate.__doc__,
            (
                "Very important docstring for..."
                "OBJECTNAME deprecated in v1.2.3 "
                "replaced by New hotness."
            ),
        )

    def test_addendum(self):
        deprecated = regret.callable(
            version="1.2.3",
            addendum="Division is also terrible and we should all be friends.",
        )(divide)

        self.assertDeprecated(
            message=(
                "divide is deprecated. "
                "Division is also terrible and we should all be friends."
            ),
            fn=deprecated,
        )

    def test_addendum_with_replacement(self):
        deprecated = regret.callable(
            version="1.2.3",
            replacement=Calculator,
            addendum="Division is also terrible and we should all be friends.",
        )(divide)

        self.assertDeprecated(
            message=(
                "divide is deprecated. Please use Calculator instead. "
                "Division is also terrible and we should all be friends."
            ),
            fn=deprecated,
        )

    def test_removal_date(self):
        deprecated = regret.callable(
            version="1.2.3",
            removal_date=date(year=2012, month=12, day=12),
        )(divide)

        self.assertDeprecated(
            message=(
                "divide is deprecated. "
                "It will be removed on or after 2012-12-12."
            ),
            fn=deprecated,
        )

    def test_removal_date_with_replacement(self):
        deprecated = regret.callable(
            version="1.2.3",
            removal_date=date(year=2012, month=12, day=12),
            replacement=Calculator,
        )(divide)

        self.assertDeprecated(
            message=(
                "divide is deprecated. "
                "It will be removed on or after 2012-12-12. "
                "Please use Calculator instead."
            ),
            fn=deprecated,
        )

    def test_removal_date_with_addendum(self):
        deprecated = regret.callable(
            version="1.2.3",
            removal_date=date(year=2012, month=12, day=12),
            addendum="Division is also terrible and we should all be friends.",
        )(divide)

        self.assertDeprecated(
            message=(
                "divide is deprecated. "
                "It will be removed on or after 2012-12-12. "
                "Division is also terrible and we should all be friends."
            ),
            fn=deprecated,
        )

    def test_removal_date_with_replacement_and_addendum(self):
        deprecated = regret.callable(
            version="1.2.3",
            removal_date=date(year=2012, month=12, day=12),
            replacement=Calculator,
            addendum="Division is also terrible and we should all be friends.",
        )(divide)

        self.assertDeprecated(
            message=(
                "divide is deprecated. "
                "It will be removed on or after 2012-12-12. "
                "Please use Calculator instead. "
                "Division is also terrible and we should all be friends."
            ),
            fn=deprecated,
        )

    def test_function_parameter(self):
        self.assertDeprecated(
            message="The 'z' parameter is deprecated.",
            fn=add3,
            kwargs=dict(x=1, y=2, z=3),
        )

    def test_optional_function_parameter(self):
        self.assertDeprecated(
            message=(
                "Calling add4 without providing the 'z' parameter "
                "is deprecated. Using 0 as a default."
            ),
            fn=add4,
            kwargs=dict(w=0, x=1, y=2),
        )

    def test_mixed_function_parameters(self):
        add5(v=0, w=0, x=1, y=2)
        self.assertEqual(
            [each["message"] for each in self.flushWarnings()],
            [
                "The 'y' parameter is deprecated.",
                (
                    "Calling add5 without providing the 'z' parameter "
                    "is deprecated. Using 0 as a default."
                ),
            ],
        )

    def test_inheritance(self):
        def subclass():
            class Subclass(CalculatorWithDeprecatedInheritance):
                pass

        self.assertDeprecated(
            message="Subclassing from Calculator is deprecated.",
            filename=__file__,
            fn=subclass,
        )

    def test_nested_callable(self):
        """
        Ensure we do something sensible with things that are deprecated as
        nested callables inside some locals.

        This probably should never happen, but ensure it doesn't blow up,
        essentially.
        """

        @regret.callable(version="1.2.3")
        def nested_thing():
            return 12

        self.assertDeprecated(
            message=(
                "TestRegret.test_nested_callable.<locals>.nested_thing "
                "is deprecated."
            ),
            fn=nested_thing,
        )
