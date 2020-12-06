"""
Integration tests for the testing helper(s).
"""
import warnings

from unittest import TestCase

import regret
from regret import Deprecator, emitted, testing


def calculate():
    return 12

def replacement_calculate():
    return 11


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


class TestWarnigsCollector(TestCase):
    """
    Tests for `collect_warnings` helper.
    """

    def test_no_warnings(self):
        """
        No error is raised if no warning is raised inside the context
        manager.
        """
        with testing.collect_warnings():
            """
            No warning emitted here.
            """

    def test_fail_on_unchecked_warnings(self):
        """
        No error is raised if no warning is raised inside the context
        manager.
        """
        with self.assertRaises(AssertionError) as context:
            with testing.collect_warnings():
                warnings.warn("A warning that is not checked.")

        self.assertTrue(context.exception.args[0].startswith(
            'Warnings queue was not completely checked.'))

    def test_expect_warning(self):
        """
        The context manager returns a helper that can be used to
        assert the emitted warnings.
        """
        with testing.collect_warnings() as collector:
            warnings.warn("A warning that is checked.", UserWarning)

            collector.expect(
                'A warning that is checked.', category=UserWarning)

    def test_expect_warning_unchecked(self):
        """
        When an emitted warning is left unchecked, an AssertionError is
        raised when the context exists.
        """
        with self.assertRaises(AssertionError) as context:
            with testing.collect_warnings() as collector:
                warnings.warn("A warning that is checked.", UserWarning)
                warnings.warn("A warning that is checked.", UserWarning)

                collector.expect(
                    'A warning that is checked.', category=UserWarning)

        self.assertTrue(context.exception.args[0].startswith(
            'Warnings queue was not completely checked.'))

    def test_expect_regret(self):
        """
        It provide a helper to expect a warning raised by regret.
        """
        deprecated = regret.callable(version="1.2.0")(calculate)

        with testing.collect_warnings() as collector:
            deprecated()

            collector.expect_regret('calculate')

    def test_expect_regret_with_replacement(self):
        """
        It provide a helper to expect a warning raised by regret.
        """
        deprecated = regret.callable(
            version="1.2.0",
            replacement=replacement_calculate,
            )(calculate)

        with testing.collect_warnings() as collector:
            deprecated()

            collector.expect_regret(
                'calculate', replacement='replacement_calculate')

    def test_expect_regret_source(self):
        """
        It provide a helper to expect a warning raised by regret from
        a specific source file.
        """
        deprecated = regret.callable(version="1.2.0")(calculate)

        with testing.collect_warnings() as collector:
            deprecated()

            collector.expect_regret('calculate', source='test_testing')

    def test_expect_regret_source_mismatch(self):
        """
        It raised AssertionError when the expected source is different than
        the source associated with the regret.
        """
        deprecated = regret.callable(version="1.2.0")(calculate)

        with self.assertRaises(AssertionError) as context:
            with testing.collect_warnings() as collector:
                deprecated()

                collector.expect_regret('calculate', source='bad_source')

        self.assertTrue(context.exception.args[0].startswith(
            'Expecting warning from path ending with "bad_source.py". Got '))
