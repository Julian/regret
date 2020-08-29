from functools import wraps

import attr

from regret import _inspect, _sphinx, _warnings, emitted


@attr.s(eq=True, frozen=True)
class Deprecator:
    """
    Deprecators help manifest regret.

    Arguments:

        emit:

            a callable which will be called with one argument, a
            `regret.emitted.Deprecation` instance, whenever a deprecated
            object has been used. If unprovided, by default, a warning
            will be shown using the standard library `warnings` module.

        name_of:

            a callable which given any Python object should return
            a suitable name for the object. If unprovided, the
            `__qualname__ <definition.__qualname__>` will be used, and
            therefore an object's (non-fully-)qualified name will appear
            in messages.

        new_docstring:

            a callable which should produce a docstring for newly
            deprecated objects. It will be called with three *keyword*
            arguments:

                * ``object``, the object that is being deprecated

                * ``name_of``, the callable described above for use in
                  calculating object names

                * ``version``, the version that deprecates the provided object

            and it should return a single string which will become
            the new docstring for a deprecated object. If unprovided,
            deprecation docstrings will be constructed using syntax
            suitable for `Sphinx <sphinx:index>`, via the `deprecated`
            directive.
    """

    _emit = attr.ib(default=_warnings.emit)
    _name_of = attr.ib(default=emitted._qualname)
    _new_docstring = attr.ib(default=_sphinx.doc_with_deprecated_directive)

    def _emit_deprecation(self, extra_stacklevel=0, **kwargs):
        self._emit(
            deprecation=emitted.Deprecation(name_of=self._name_of, **kwargs),
            extra_stacklevel=extra_stacklevel,
        )

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

                the first version in which the deprecated object was
                considered deprecated

            replacement:

                optionally, an object that is the (direct or indirect)
                replacement for the functionality previously performed
                by the deprecated callable

            removal_date (datetime.date):

                optionally, a date when the object is expected to be
                removed entirely

            addendum (str):

                an optional additional message to include at the end of
                warnings emitted for this deprecation
        """

        def deprecate(thing):
            @wraps(thing)
            def call_deprecated(*args, **kwargs):
                self._emit_deprecation(
                    kind=emitted.Callable(object=call_deprecated),
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

    def parameter(self, version, name):
        """
        Deprecate a parameter that was previously required and will be removed.

        Arguments:

            version:

                the first version in which the deprecated parameter was
                considered deprecated

            name:

                the name of the parameter as specified in the callable's
                signature.

                Deprecating a parameter that was previously accepted
                only via arbitrary keyword arguments ("``kwargs``") is
                also supported and should be specified using the name of
                the parameter as retrieved from the keyword arguments.
        """
        def deprecate(thing):
            if hasattr(thing, "__regret_parameter__"):
                return thing.__regret_parameter__(name)
            return PartiallyDeprecated(
                emit=self._emit_deprecation,
                callable=thing,
            ).__regret_parameter__(name)
        return deprecate

    def inheritance(self, version):
        """
        Deprecate allowing a class to be subclassed.

        Arguments:

            version:

                the first version in which the deprecated object was
                considered deprecated
        """

        def deprecate(cls):
            @wraps(cls, updated=())
            class DeprecatedForSubclassing(cls):
                def __init_subclass__(Subclass, **kwargs):
                    self._emit_deprecation(
                        kind=emitted.Inheritance(
                            type=DeprecatedForSubclassing,
                        ),
                    )
                    super().__init_subclass__(**kwargs)
            return DeprecatedForSubclassing

        return deprecate


class PartiallyDeprecated:
    """
    A partially deprecated callable.
    """

    def __init__(self, emit, callable, deprecated_parameters=()):
        wraps(callable)(self)

        signature = _inspect.SignatureWithRegret.for_callable(
            callable, deprecated=deprecated_parameters,
        )

        def _maybe_emit_deprecation(*args, **kwargs):
            for each in signature.deprecated_parameters_used(*args, **kwargs):
                emit(
                    kind=emitted.Parameter(callable=self, parameter=each),
                    extra_stacklevel=1,
                )
            return callable(*args, **kwargs)

        def _regret_additional_parameter(name):
            return PartiallyDeprecated(
                emit=emit,
                callable=callable,
                deprecated_parameters=signature.deprecated_insorted(name),
            )

        self.__regret_maybe_emit_deprecation__ = _maybe_emit_deprecation
        self.__regret_parameter__ = _regret_additional_parameter

    def __call__(self, *args, **kwargs):
        return self.__regret_maybe_emit_deprecation__(*args, **kwargs)


_DEPRECATOR = Deprecator()
