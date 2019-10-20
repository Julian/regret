from unittest import TestCase

from regret import EmittedDeprecation, Deprecator
from regret.testing import Recorder


class TestRegret(TestCase):
    def setUp(self):
        self.recorder = Recorder()
        self.regret = Deprecator(emit=self.recorder.emit)

    def test_function(self):
        @self.regret.callable()
        def calculate():
            return 12

        self.assertEqual(
            (calculate(), self.recorder), (
                12,
                Recorder(saw=[EmittedDeprecation()]),
            ),
        )
