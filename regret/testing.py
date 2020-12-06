"""
Helpers for testing your regret.
"""
from contextlib import contextmanager
import sys
import warnings

import attr

from regret.emitted import Deprecation


class ExpectedDifferentDeprecations(AssertionError):
    pass


@attr.s(eq=True)
class Recorder:

    _saw = attr.ib(factory=list)

    def emit(self, deprecation, extra_stacklevel):
        """
        An emitter suitable for passing to `Deprecator` instances.
        """
        self._saw.append(deprecation)

    def expect(self, **kwargs):
        """
        Expect a given set of deprecations to be emitted.
        """
        return self.expect_deprecations(Deprecation(**kwargs))

    @contextmanager
    def expect_deprecations(self, *deprecations):
        """
        Expect a given set of deprecations to be emitted.
        """
        expected = self._saw + list(deprecations)
        yield
        if self._saw != expected:
            raise ExpectedDifferentDeprecations((self._saw, expected))

    def expect_clean(self):
        """
        Expect no deprecations to be emitted.
        """
        return self.expect_deprecations()


class _Warning:
    """
    It represents one warning emitted through the standard Python
    warning system.

    @ivar message: The string which was passed as the message parameter to
        L{warnings.warn}.

    @ivar category: The L{Warning} subclass which was passed as the category
        parameter to L{warnings.warn}.

    @ivar filename: The name of the file containing the definition of the code
        object which was C{stacklevel} frames above the call to
        L{warnings.warn}, where C{stacklevel} is the value of the C{stacklevel}
        parameter passed to L{warnings.warn}.

    @ivar lineno: The source line associated with the active instruction of the
        code object object which was C{stacklevel} frames above the call to
        L{warnings.warn}, where C{stacklevel} is the value of the C{stacklevel}
        parameter passed to L{warnings.warn}.
    """

    def __init__(self, message, category, filename, lineno):
        self.message = message
        self.category = category
        self.filename = filename
        self.lineno = lineno

    def __repr__(self):
        """
        Test failure reporting friendly representation of the captured warning.
        """
        return (
            f'{self.category}"{self.message}"\n'
            f'{self.filename}:{self.lineno}\n'
            )


def _reset_warnings():
    """
    Disable the per-module cache for every module otherwise if the warning
    which the caller is expecting us to collect was already emitted it won't
    be re-emitted by the call to f which happens below.
    """
    for v in list(sys.modules.values()):
        if v is not None:
            try:
                v.__warningregistry__ = None
            except BaseException:
                # Don't specify a particular exception type to handle in case
                # some wacky object raises some wacky exception in response to
                # the setattr attempt.
                pass


class WarningsCollector:
    """
    Helper for catching and verifying emitted warnings inside the testing
    context manager.

    For now, usage is supported only as a context manager.
    In the future it can provide explicit `start` and `stop` methods to
    help usage outside of a context.
    """
    def __init__(self):
        self._queue = []

    def _append(self, warning):
        """
        Private method used together with the context manager.
        """
        self._queue.append(warning)

    def expect_regret(self, target, replacement=None, source=None, lineno=None):
        """
        Expect that a regret warning was emitted.
        """
        message = f'{target} is deprecated.'
        if replacement:
            message += f' Please use {replacement} instead.'

        self.expect(
            message,
            category=DeprecationWarning,
            source=source,
            lineno=lineno,
            )

    def expect(
        self, message, category=DeprecationWarning, source=None, lineno=None,
            ):
        """
        Check the first warnings that was emitted and then remove it from the
        expectation list.

        `message` is the expected message contained by the emitted warning.

        `category` is the class of the emitted deprecation. Defaults to
        `DeprecationWarning`.

        `source` is the name of the Python module from which the warning is
        emitted.
        Don't include the full path or the `.py` extension.
        It is designed to make it easy to write tests on Unix and Windows.

        `lineno` is the line number from where the warning was emitted.

        It will accept any `source` or `lineno` when no expected values are
        provided for them.
        """
        actual = self._queue.pop(0)

        if message != actual.message:
            raise AssertionError(
                f'Expecting warning with message "{message}". '
                f'Got "{actual.message}".')

        if actual.category != category:
            raise AssertionError(
                f'Expecting warning as "{category}". Got "{actual.category}".')

        if source:
            if not actual.filename.endswith(f'{source}.py'):
                raise AssertionError(
                    f'Expecting warning from path ending with "{source}.py". '
                    f'Got "{actual.filename}".')

        if lineno:
            if actual.lineno != lineno:
                raise AssertionError(
                    f'Expecting warning at line "{lineno}". '
                    f'Got "{actual.lineno}".')

    def expect_clean(self):
        """
        Expect no warning were left unverified.
        """
        if self._queue:
            raise AssertionError(
                'Warnings queue was not completely checked.\n'
                + repr(self._queue))


@contextmanager
def collect_warnings():
    """
    Catches the warnings emitted inside the context.

    Returns a `WarningsCollector` that is used inside a context to check the
    emitted warnings.

    All warnings must the checked  before the end of the context.
    """
    collector = WarningsCollector()

    def catch_warning(
            warning, category, filename, lineno, file=None, line=None):
        """
        Injected into Python to allow catching all warnings.
        """
        assert isinstance(warning, Warning)
        collector._append(_Warning(str(warning), category, filename, lineno))

    _reset_warnings()

    origFilters = warnings.filters[:]
    origShow = warnings.showwarning
    warnings.simplefilter("always")
    try:
        warnings.showwarning = catch_warning
        yield collector
    finally:
        warnings.filters[:] = origFilters
        warnings.showwarning = origShow
        collector.expect_clean()

