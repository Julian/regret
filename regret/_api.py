from functools import wraps

from qualname import qualname
import attr

from regret import _sphinx, _warnings


@attr.s(eq=True, frozen=True)
class Deprecator(object):
    """
    Deprecators help manifest regret.

    Arguments:

        emit:

            a callable which will be called with one argument, an
            `EmittedDeprecation` instance, whenever a deprecated object
            has been used. If unprovided, by default, a warning will be
            shown using the standard library `warnings` module.

        name_of:

            a callable which given any Python object should
            return a suitable name for the object. If unprovided,
            `qualname.qualname` will be used, and therefore an object's
            (non-fully-)qualified name will appear in messages.

        new_docstring:

            a callable which should produce a docstring for newly
            deprecated objects. It will be called with three *keyword*
            arguments:

                * ``object``, the object that is being depreated

                * ``name_of``, the callable described above for use in
                  calculating object names

                * ``version``, the version that deprecates the provided object

            and it should return a single string which will become the new
            docstring for a deprecated object. If unprovided, deprecation
            docstrings will be constructed using syntax suitable for `Sphinx`,
            via the `deprecated` directive.
    """

    _emit = attr.ib(default=_warnings.emit)
    _name_of = attr.ib(default=qualname)
    _new_docstring = attr.ib(default=_sphinx.doc_with_deprecated_directive)

    def emit_deprecation(self, **kwargs):
        self._emit(EmittedDeprecation(name_of=self._name_of, **kwargs))

    # -- Deprecatable objects --

    def callable(
        self,
        version,
        replacement=None,
        removal_date=None,
        addendum=None,
    ):
        """
        Deprecate a callable as of the given version.

        Arguments:

            version:

                the first version in which the deprecated object was considered
                deprecated

            replacement:

                optionally, an object that is the (direct or indirect)
                replacement for the functionality previously performed
                by the deprecated callable

            removal_date (date):

                optionally, a date when the object is expected to be
                removed entirely

            addendum (str):

                an optional additional message to include at the end of
                warnings emitted for this deprecation
        """

        def deprecate(thing):
            @wraps(thing)
            def call_deprecated(*args, **kwargs):
                self.emit_deprecation(
                    object=thing,
                    replacement=replacement,
                    removal_date=removal_date,
                    addendum=addendum,
                )
                return thing(*args, **kwargs)

            __doc__ = thing.__doc__
            if __doc__ is not None:
                call_deprecated.__doc__ = self._new_docstring(
                    object=thing,
                    name_of=self._name_of,
                    replacement=replacement,
                    removal_date=removal_date,
                    version=version,
                )

            return call_deprecated
        return deprecate


@attr.s(eq=True, frozen=True, hash=True)
class EmittedDeprecation(object):

    _object = attr.ib()
    _name_of = attr.ib(default=qualname)
    _replacement = attr.ib(default=None)
    _removal_date = attr.ib(default=None)
    _addendum = attr.ib(default=None)

    def message(self):
        parts = ["{} is deprecated.".format(self._name_of(self._object))]
        if self._removal_date is not None:
            parts.append(
                "It will be removed on or after {}.".format(self._removal_date)
            )
        if self._replacement is not None:
            parts.append(
                "Please use {} instead.".format(
                    self._name_of(self._replacement),
                ),
            )
        if self._addendum is not None:
            parts.append(self._addendum)
        return " ".join(parts)


_DEPRECATOR = Deprecator()
