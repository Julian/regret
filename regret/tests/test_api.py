from unittest import TestCase

from regret import EmittedDeprecation, Deprecator
from regret.testing import Recorder


class TestRegret(TestCase):
    def setUp(self):
        self.recorder = Recorder()
        self.regret = Deprecator(emit=self.recorder.emit)

    def test_function(self):
        def calculate():
            return 12

        self.assertEqual(
            (self.regret.callable()(calculate)(), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=calculate)]),
            ),
        )

    def test_function_with_args(self):
        def add(x, y):
            return 12

        self.assertEqual(
            (self.regret.callable()(add)(9, y=3), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation(object=add)]),
            ),
        )
