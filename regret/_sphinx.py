from textwrap import dedent


def doc_with_deprecated_directive(object, name_of, version):
    """
    Add a `deprecated` directive to the provided object's docstring.

    Suitable for use with `regret.Deprecator`.
    """

    return dedent(object.__doc__) + "\n.. deprecated:: {}\n".format(version)
