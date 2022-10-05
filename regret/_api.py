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
            return Regretted.for_callable(thing).with_parameter(
                name=name,
                emit=self._emit_deprecation,
            )

        return deprecate

    def optional_parameter(self, version, name, default):
        """
        Deprecate a parameter that was optional and will become required.

        Arguments:

            version:

                the first version in which the parameter was to warn
                when unprovided

            name:

                the name of the parameter as specified in the callable's
                signature.

                Requiring an optional parameter that was previously
                accepted only via arbitrary keyword arguments
                ("``kwargs``") is also supported and should be specified
                using the name of the parameter as retrieved from the
                keyword arguments.

            default:

                whilst the parameter remains optional, the value that
                should be used when it is unprovided by a caller.

                It will be passed through to the wrapped callable,
                which can therefore assume the argument will always be
                present.
        """

        def deprecate(thing):
            return Regretted.for_callable(thing).with_optional_parameter(
                name=name,
                emit=self._emit_deprecation,
                default=default,
            )

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


@attr.s
class Regretted:
    """
    A partially regretted callable.
    """

    callable = attr.ib()
    signature = attr.ib()

    @classmethod
    def for_callable(cls, callable, **kwargs):
        regretted = getattr(callable, "__regretted__", None)
        if regretted is not None:
            return regretted
        return cls(
            callable=callable,
            signature=_inspect.SignatureWithRegret.for_callable(callable),
            **kwargs,
        )

    def with_parameter(self, emit, name):
        self.signature = self.signature.with_parameter(name)
        return self.wrapper(emit=emit)

    def with_optional_parameter(self, emit, name, default):
        self.signature = self.signature.with_optional_parameter(
            name=name,
            default=default,
        )
        return self.wrapper(emit=emit)

    def wrapper(self, emit):
        @wraps(self.callable)
        def wrapper(*args, **kwargs):
            bound = self.signature.bind(*args, **kwargs)
            for each, optional in self.signature.misused(
                bound_arguments=bound,
                callable=wrapper,
            ):
                if optional:
                    default = self.signature.set_default(bound, parameter=each)
                    kind = emitted.OptionalParameter(
                        callable=wrapper,
                        parameter=each,
                        default=default,
                    )
                else:
                    kind = emitted.Parameter(callable=wrapper, parameter=each)
                emit(kind=kind)
            return self.callable(*bound.args, **bound.kwargs)

        wrapper.__regretted__ = self
        return wrapper


_DEPRECATOR = Deprecator()
