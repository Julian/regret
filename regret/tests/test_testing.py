"""
Integration tests for the testing helper(s).
"""
from unittest import TestCase

from regret import Deprecator, emitted, testing


def calculate():
    return 12


class TestRecorder(TestCase):
    def test_it_can_expect_a_deprecation(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with recorder.expect(kind=emitted.Callable(object=deprecated)):
            deprecated()

    def test_it_errors_when_not_seeing_an_expected_deprecation(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with self.assertRaises(testing.ExpectedDifferentDeprecations):
            with recorder.expect(kind=emitted.Callable(object=deprecated)):
                pass

    def test_it_errors_when_seeing_extra_deprecations(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with self.assertRaises(testing.ExpectedDifferentDeprecations):
            with recorder.expect(kind=emitted.Callable(object=deprecated)):
                deprecated()
                deprecated()

    def test_it_sees_emitted_deprecations(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with recorder.expect_deprecations(
            emitted.Deprecation(kind=emitted.Callable(object=deprecated)),
            emitted.Deprecation(kind=emitted.Callable(object=deprecated)),
        ):
            deprecated()
            deprecated()

    def test_it_errors_for_missing_deprecations(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with self.assertRaises(testing.ExpectedDifferentDeprecations):
            with recorder.expect_deprecations(
                emitted.Deprecation(kind=emitted.Callable(object=deprecated)),
                emitted.Deprecation(kind=emitted.Callable(object=deprecated)),
            ):
                deprecated()

    def test_it_errors_for_extra_deprecations(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with self.assertRaises(testing.ExpectedDifferentDeprecations):
            with recorder.expect_deprecations(
                emitted.Deprecation(kind=emitted.Callable(object=deprecated)),
                emitted.Deprecation(kind=emitted.Callable(object=deprecated)),
            ):
                deprecated()
                deprecated()
                deprecated()

    def test_it_errors_for_non_matching_deprecations(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with self.assertRaises(testing.ExpectedDifferentDeprecations):
            with recorder.expect_deprecations(
                emitted.Deprecation(kind=emitted.Callable(object=int)),
            ):
                deprecated()

    def test_it_can_expect_no_deprecations(self):
        recorder = testing.Recorder()
        with recorder.expect_clean():
            pass

    def test_it_fails_for_unexpected_deprecations(self):
        recorder = testing.Recorder()
        regret = Deprecator(emit=recorder.emit)

        deprecated = regret.callable(version="1.2.3")(calculate)

        with self.assertRaises(testing.ExpectedDifferentDeprecations):
            with recorder.expect_clean():
                deprecated()
