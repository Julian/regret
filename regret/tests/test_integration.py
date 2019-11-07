import warnings

from qualname import qualname
from twisted.trial.unittest import SynchronousTestCase

import regret


class Calculator(object):
    @regret.callable(version="1.2.3")
    def __call__(self):
        return 12

    @regret.callable(version="1.2.3")
    def calculate(self):
        return 12


@regret.callable(version="1.2.3")
def calculate():
    return 12


@regret.callable(version="1.2.3")
def add(x, y):
    return x + y


@regret.callable(version="1.2.3", replacement=Calculator)
def calculator_fn():
    return 9


def divide():
    return 7


class TestRegret(SynchronousTestCase):
    def assertDeprecated(self, message, filename, fn, args=(), kwargs={}):
        # Sigh... assertWarns takes positional args positionally, instead of as
        # a sequence.
        return self.assertWarns(
            DeprecationWarning,
            message,
            filename,
            fn,
            *args,
            **kwargs
        )

    def test_function(self):
        result = self.assertDeprecated(
            message="'calculate' is deprecated.",
            filename=__file__,
            fn=calculate,
        )
        self.assertEqual(result, 12)

    def test_function_with_args(self):
        result = self.assertDeprecated(
            message="'add' is deprecated.",
            filename=__file__,
            fn=add,
            args=(9,),
            kwargs=dict(y=3),
        )
        self.assertEqual(result, 12)

    def test_function_with_replacement(self):
        result = self.assertDeprecated(
            message=(
                "'calculator_fn' is deprecated. "
                "Please use 'Calculator' instead."
            ),
            filename=__file__,
            fn=calculator_fn,
        )
        self.assertEqual(result, 9)

    def test_method(self):
        calculator = Calculator()
        result = self.assertDeprecated(
            message="'Calculator.calculate' is deprecated.",
            filename=__file__,
            fn=calculator.calculate,
        )
        self.assertEqual(result, 12)

    def test_dunder_call(self):
        calculator = Calculator()
        result = self.assertDeprecated(
            message="'Calculator.__call__' is deprecated.",
            filename=__file__,
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

        result = self.assertDeprecated(
            message="'etaluclac' is deprecated.",
            filename=__file__,
            fn=calculate,
        )

    def test_custom_docstring_modifier(self):
        deprecate = regret.Deprecator(
            name_of=lambda object: "OBJECTNAME",
            new_docstring=lambda object, replacement, name_of, version: (
                object.__doc__
                + name_of(object)
                + " deprecated in "
                + version
                + " replaced by "
                + replacement.__doc__
            )
        )

        def replacement():
            "New hotness."

        @deprecate.callable(version="v1.2.3", replacement=replacement)
        def calculate():
            "Very important docstring for "

        self.assertEqual(
            calculate.__doc__, (
                "Very important docstring for "
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
                "'divide' is deprecated. "
                "Division is also terrible and we should all be friends."
            ),
            filename=__file__,
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
                "'divide' is deprecated. Please use 'Calculator' instead. "
                "Division is also terrible and we should all be friends."
            ),
            filename=__file__,
            fn=deprecated,
        )
