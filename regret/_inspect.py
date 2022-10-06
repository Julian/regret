"""
Signature helpers for deprecated (or partially-deprecated) callables.
"""

import inspect

import attr


class AlreadyDeprecated(Exception):
    """
    An attempt was made to deprecate an already-deprecated parameter.
    """


class NoSuchParameter(Exception):
    """
    An attempt was made to deprecate a parameter that does not exist.
    """


@attr.s
class SignatureWithRegret:
    """
    An `inspect.Signature`, along with its regretted subparts.
    """

    _signature = attr.ib()
    _deprecated = attr.ib(factory=list)
    _defaults_for_optional_parameters = attr.ib(factory=dict)

    def __attrs_post_init__(self):
        self.kwargs_parameter_name = next(
            (
                name
                for name, parameter in reversed(
                    self._signature.parameters.items(),
                )
                if parameter.kind == inspect.Parameter.VAR_KEYWORD
            ),
            None,
        )

        self._order = {
            parameter: index
            for index, parameter in enumerate(self._signature.parameters)
        }

    @classmethod
    def for_callable(cls, callable, **kwargs):
        return cls(
            signature=inspect.signature(callable, follow_wrapped=False),
            **kwargs,
        )

    def would_accept(self, name):
        """
        Does this signature know about a parameter with the given name?
        """
        return (
            name in self._signature.parameters
            or self.kwargs_parameter_name is not None
        )

    def with_parameter(self, name, **kwargs):
        """
        Evolve this signature to add a deprecated parameter.
        """
        if not self.would_accept(name):
            raise NoSuchParameter(name)
        elif name in self._deprecated:
            raise AlreadyDeprecated(name)

        deprecated = sorted(
            self._deprecated + [name],
            key=lambda each: (
                self._order.get(
                    each,
                    self._order.get(self.kwargs_parameter_name, -1),
                ),
                each,
            ),
        )
        return attr.evolve(self, deprecated=deprecated, **kwargs)

    def with_optional_parameter(self, name, default):
        """
        Evolve this signature to add a deprecated optional parameter.
        """
        return self.with_parameter(
            name,
            defaults_for_optional_parameters={
                name: default,
                **self._defaults_for_optional_parameters,
            },
        )

    def misused(self, bound_arguments, callable):
        """
        Collect the arguments (optional or required) that are misused.
        """
        arguments = bound_arguments.arguments
        kwargs = bound_arguments.arguments.get(self.kwargs_parameter_name, ())

        for name in self._deprecated:
            is_optional = name in self._defaults_for_optional_parameters
            if is_optional:
                if name in arguments or name in kwargs:
                    continue

                parameter = self._signature.parameters.get(name)
                if parameter is None is not self.kwargs_parameter_name:
                    parameter = inspect.Parameter(
                        name=name,
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    )
                yield parameter, is_optional
            else:
                if name in arguments:
                    yield self._signature.parameters[name], is_optional
                elif name in kwargs:
                    yield inspect.Parameter(
                        name=name,
                        kind=inspect.Parameter.KEYWORD_ONLY,
                    ), is_optional

    def bind(self, *args, **kwargs):
        return self._signature.bind_partial(*args, **kwargs)

    def set_default(self, bound_arguments, parameter):
        """
        Set the default for the given parameter within some bound arguments.
        """

        name = parameter.name
        default = self._defaults_for_optional_parameters[name]
        if name in self._signature.parameters:
            bound_arguments.arguments[name] = default
        else:
            kwargs = bound_arguments.arguments.setdefault(
                self.kwargs_parameter_name,
                {},
            )
            kwargs[name] = default
        return default
