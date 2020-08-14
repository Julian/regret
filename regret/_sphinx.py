from textwrap import dedent


def doc_with_deprecated_directive(
    object,
    replacement,
    removal_date,
    name_of,
    version,
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
