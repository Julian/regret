==============================
What You Can Deprecate and How
==============================

*Most things should be easy to deprecate and everything should be
possible.*

This page attempts to demonstrate a variety of practical deprecations
that library authors face, alongside how to perform the deprecation
using `regret`.

The `API documentation <api>` also contains a full list for reference.


Deprecating a Function or Arbitrary Callable
--------------------------------------------

Deprecating a single function or callable in its entirety is one of the
simplest and most common deprecations to perform.

Consider as an example a greeting function which we wish to deprecate:

.. testsetup::

    from functools import partial
    import sys
    import warnings
    def _redirected(message, category, filename, lineno, file=None, line=None):
        showwarning(message, category, filename, lineno, sys.stdout, line)
    showwarning, warnings.showwarning = warnings.showwarning, _redirected

.. testcleanup::

    warnings.showwarning = showwarning

.. testcode::

    def greeting(first_name, last_name):
        return f"Hello {first_name} {last_name}!"

Doing so can be done via the `regret.callable` decorator by simply
specifying the version in which the function has been deprecated:

.. testsetup::

   import regret

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

   Class objects are themselves simply callables, and as such, deprecating an
   entire class can be done in the same manner.

   However, if you have an API that primarily encouraged subclassing
   of the class to be deprecated, the object returned by
   `regret.Deprecator.callable` is *not* guaranteed to be a type (i.e.
   a class), and therefore may not support being subclassed as the
   original object did.

   .. todo::

        Link to ``regret.Deprecator.Class`` once it exists.
