from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import date
    from typing import Any


def doc_with_deprecated_directive(
    object: Any,
    replacement: Any | None,
    removal_date: date | None,
    name_of: Callable[..., str],
    version: str,
):
    """
    Add a `deprecated` directive to the provided object's docstring.

    Suitable for use with `regret.Deprecator`.
    """
    parts = [
        dedent(object.__doc__),
        f"\n.. deprecated:: {version}\n",
    ]
    if replacement is not None:
        parts.append(
            f"\n    Please use `{name_of(replacement)}` instead.\n",
        )
    if removal_date is not None:
        parts.append(
            f"\n    It will be removed on or after {removal_date}.\n",
        )
    return "".join(parts)
