import warnings

from twisted.trial.unittest import SynchronousTestCase

import regret


@regret.callable()
def calculate():
    return 12


class TestRegret(SynchronousTestCase):
    def test_function(self):
        result = self.assertWarns(
            message="'regret.tests.test_integration.calculate' is deprecated.",
            category=DeprecationWarning,
            filename=__file__,
            f=calculate,
        )
        self.assertEqual(result, 12)
