==============================
What You Can Deprecate and How
==============================

*Most things should be easy to deprecate and everything should be
possible.*

This page attempts to demonstrate a variety of practical deprecations
that library authors face, alongside how to perform the deprecation
using :ref:`regret`.

The `API Reference <api/modules>` also contains a full list for completeness.

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


Replacements
============

It is often the case when deprecating an object that a newer replacement
API subsumes its functionality, and is meant to be used instead.

`regret.callable` accommodates this common use case by allowing you to
specify which object is the replacement while deprecating:

.. testcode::

    def better_greeting(first_name, last_name):
        return f"Hello {first_name} {last_name}! You are amazing!"

    @regret.callable(version="1.0.0", replacement=better_greeting)
    def greeting(first_name, last_name):
        return f"Hello {first_name} {last_name}!"

which will then show the replacement object in warnings emitted:

.. testcode::

    print(greeting("Joe", "Smith"))

.. testoutput::

    ...: DeprecationWarning: greeting is deprecated. Please use better_greeting instead.
      print(greeting("Joe", "Smith"))
    Hello Joe Smith!


Parameters
----------

There are various scenarios in which a callable's signature may require
deprecation.


Removing a Required Parameter
=============================

:ref:`regret` can help deprecate a parameter (argument) which previously
was required and which now is to be removed.

Consider again our ``greeting`` function, but where we have decided to
replace the separate specification of first and last names with a single
``name`` parameter\ `, <https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/>`_
and therefore wish to deprecate providing the name in separate parameters:

.. testcode::

    @regret.parameter(version="v1.2.3", name="first_name")
    @regret.parameter(version="v1.2.3", name="last_name")
    def greeting(first_name=None, last_name=None, *, name=None):
        if first_name is not None:
            name = first_name
            if last_name is not None:
                name += f" {last_name}"
        return f"Hello {name}!"

After the above, using the function with the previous parameters will
show a deprecation warning:

.. testcode::

    print(greeting("Joe", "Smith"))

.. testoutput::

    ...: DeprecationWarning: The 'first_name' parameter is deprecated.
      print(greeting("Joe", "Smith"))
    ...: DeprecationWarning: The 'last_name' parameter is deprecated.
      print(greeting("Joe", "Smith"))
    Hello Joe Smith!

but via the new parameter, will not:

.. testcode::

    print(greeting(name="Joe Smith"))

.. testoutput::

    Hello Joe Smith!


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
