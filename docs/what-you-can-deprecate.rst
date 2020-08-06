==============================
What You Can Deprecate and How
==============================

*Most things should be easy to deprecate and everything should be
possible.*

This page attempts to demonstrate a variety of practical deprecations
that library authors face, alongside how to perform the deprecation
using :ref:`regret`.

The `API documentation <api>` also contains a full list for reference.

.. testsetup::

    import sys
    import warnings
    import regret

    def _redirected(message, category, filename, lineno, file=None, line=None):
        showwarning(message, category, filename, lineno, sys.stdout, line)
    showwarning, warnings.showwarning = warnings.showwarning, _redirected

.. testcleanup::

    warnings.showwarning = showwarning


Functions & Callables
---------------------

Deprecating a single function or callable in its entirety is one of the
simplest and most common deprecations to perform.

Consider as an example a greeting function which we wish to deprecate:

.. testcode::

    def greeting(first_name, last_name):
        return f"Hello {first_name} {last_name}!"

Doing so can be done via the `regret.callable` decorator by simply
specifying the version in which the function has been deprecated:

.. testcode::

    @regret.callable(version="v2020-07-08")
    def greeting(first_name, last_name):
        return f"Hello {first_name} {last_name}!"

at which point any code which uses the function will receive a suitable
deprecation warning:

.. testcode::

    print(greeting("Joe", "Smith"))

.. testoutput::

    ...: DeprecationWarning: greeting is deprecated.
      print(greeting("Joe", "Smith"))
    Hello Joe Smith!

.. note::

    Class objects are themselves simply callables, and as such,
    deprecating an entire class can be done in the same manner.

    However, if you have an API that primarily encouraged
    subclassing of the class to be deprecated, the object returned by
    `regret.Deprecator.callable` is *not* guaranteed to be a type (i.e.
    a class), and therefore may not support being subclassed as the
    original object did.

    .. todo::

        Link to ``regret.Deprecator.Class`` once it exists.


Subclassability
---------------

A deprecation library isn't necessarily the place to opine on `the pros
and cons of inheritance <https://www.youtube.com/watch?v=3MNVP9-hglc>`_.

For library authors however who have released public APIs that heavily
depend on or require users to inherit from provided superclasses,
:ref:`regret` provides a mechanism for deprecating the inheritability of
classes.

Consider for example:

.. testcode::

    class Contact:
        name: str
        phone: str
        address: str

which downstream users of the class extend via e.g.:

.. testcode::

    class EMailContact(Contact):
        email: str

We can deprecate the downstream use of the contact class in inheritance
hierarchies via:

.. testcode::

    @regret.inheritance(version="v1.2.3")
    class Contact:
        name: str
        phone: str
        address: str

at which point, the act itself of subclassing will produce:

.. testcode::

    class EMailContact(Contact):
        email: str

.. testoutput::

    ...: DeprecationWarning: Subclassing from Contact is deprecated.
      class EMailContact(Contact):
