import warnings

from twisted.trial.unittest import SynchronousTestCase

import regret


@regret.callable()
def calculate():
    return 12


@regret.callable()
def add(x, y):
    return x + y


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
            message="'regret.tests.test_integration.calculate' is deprecated.",
            filename=__file__,
            fn=calculate,
        )
        self.assertEqual(result, 12)

    def test_function_with_args(self):
        result = self.assertDeprecated(
            message="'regret.tests.test_integration.add' is deprecated.",
            filename=__file__,
            fn=add,
            args=(9,),
            kwargs=dict(y=3),
        )
        self.assertEqual(result, 12)
