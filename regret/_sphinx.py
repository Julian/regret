from textwrap import dedent


def doc_with_deprecated_directive(object, replacement, name_of, version):
    """
    Add a `deprecated` directive to the provided object's docstring.

    Suitable for use with `regret.Deprecator`.
    """

    parts = [
        dedent(object.__doc__),
        "\n.. deprecated:: {}\n".format(version),
    ]
    if replacement is not None:
        parts.append(
            "\n    Please use `{}` instead.\n".format(name_of(replacement)),
        )
    return "".join(parts)
