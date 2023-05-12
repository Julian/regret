"""
Signature helpers for deprecated (or partially-deprecated) callables.
"""
from __future__ import annotations

from typing import Any, Callable, Iterable
import inspect

from attrs import evolve, field, frozen


class AlreadyDeprecated(Exception):
    """
    An attempt was made to deprecate an already-deprecated parameter.
    """


class NoSuchParameter(Exception):
    """
    An attempt was made to deprecate a parameter that does not exist.
    """


@frozen
class SignatureWithRegret:
    """
    An `inspect.Signature`, along with its regretted subparts.
    """

    _signature: inspect.Signature = field(alias="signature")
    _deprecated: list[str] = field(factory=list, alias="deprecated")
    _defaults_for_optional_parameters: dict[str, Any] = field(
        factory=dict,
        alias="defaults_for_optional_parameters",
    )
    kwargs_parameter_name: str | None = field(init=False)
    _order: dict[str | None, int] = field(init=False)

    def __attrs_post_init__(self) -> None:
        object.__setattr__(
            self,
            "kwargs_parameter_name",
            next(
                (
                    name
                    for name, parameter in reversed(
                        self._signature.parameters.items(),
                    )
                    if parameter.kind == inspect.Parameter.VAR_KEYWORD
                ),
                None,
            ),
        )

        object.__setattr__(
            self,
            "_order",
            {
                parameter: index
                for index, parameter in enumerate(self._signature.parameters)
            },
        )

    @classmethod
    def for_callable(
        cls,
        callable: Callable[..., Any],
        **kwargs: Any,
    ) -> SignatureWithRegret:
        return cls(
            signature=inspect.signature(callable, follow_wrapped=False),
            **kwargs,
        )

    def would_accept(self, name: str):
        """
        Does this signature know about a parameter with the given name?
        """  # noqa: D401
        return (
            name in self._signature.parameters
            or self.kwargs_parameter_name is not None
        )

    def with_parameter(self, name: str, **kwargs: Any) -> SignatureWithRegret:
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
        return evolve(self, deprecated=deprecated, **kwargs)

    def with_optional_parameter(self, name: str, default: Any):
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

    def misused(
        self,
        bound_arguments: inspect.BoundArguments,
        callable: Callable[..., Any],
    ) -> Iterable[tuple[inspect.Parameter, bool]]:
        """
        Collect the arguments (optional or required) that are misused.
        """
        arguments = bound_arguments.arguments
        kwargs = bound_arguments.arguments.get(self.kwargs_parameter_name, ())  # type: ignore[reportGeneralTypeIssues]  # noqa: E501

        for name in self._deprecated:
            is_optional = name in self._defaults_for_optional_parameters
            if is_optional:
                if name in arguments or name in kwargs:
                    continue

                parameter = self._signature.parameters.get(name)
                if parameter is None:
                    if self.kwargs_parameter_name is None:
                        continue
                    else:
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

    def bind(self, *args: Any, **kwargs: Any) -> inspect.BoundArguments:
        return self._signature.bind_partial(*args, **kwargs)

    def set_default(
        self,
        bound_arguments: inspect.BoundArguments,
        parameter: inspect.Parameter,
    ) -> Any:
        """
        Set the default for the given parameter within some bound arguments.
        """
        name = parameter.name
        default = self._defaults_for_optional_parameters[name]
        if name in self._signature.parameters:
            bound_arguments.arguments[name] = default
        elif self.kwargs_parameter_name is None:
            raise TypeError(
                f"No parameter {name} and no kwargs accepted.",
            )
        else:
            kwargs: dict[str, Any] = bound_arguments.arguments.setdefault(
                self.kwargs_parameter_name,
                {},
            )
            kwargs[name] = default
        return default
