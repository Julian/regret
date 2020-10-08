==================================
:ref:`regret`'s Deprecation Policy
==================================

This document is :ref:`regret`'s own deprecation policy.

It attempts to define, with as much forethought as is known, how
backwards-incompatible changes to the library will be performed.


Public API
----------

:ref:`regret`'s public API broadly follows what is often intuitively or
culturally understood in the Python ecosystem. Here though is a more
precise (though potentially still incomplete) description of things
*not* considered part of its public API:

    * any object whose name follows Python's "private" convention
      (starting with an underscore)

    * the entire contents of any *module* named in the above way (with a
      leading underscore)

    * the contents of the ``regret.tests`` package, i.e. the test suite,
      even if objects "appear" to be named publicly

    * the exact wording or contents of any exception message emitted

    * the exact structure or contents of any object `repr`\ s

    * the subclassability (i.e. ability of a class to be a superclass of
      another) of *any* object not explicitly marked as subclassable

    * any "transitive" imported objects -- meaning, if a module
      ``regret.foo`` imports an object ``regret.bar.Baz``, the presence of
      ``Baz`` is not public within ``foo``, only within ``bar``


Versioning
----------

With the above public API in mind, :ref:`regret` attempts to follow
the `Semantic Versioning specification <https://semver.org/>`_ as an
(imperfect) communication mechanism. Specifically, major version numbers
will be bumped for each backwards incompatible change, including changes
which have been through the deprecation period discussed `below
<regret-deprecation-period>`.


Backwards Incompatible Changes
------------------------------

In accordance with the semantic `Versioning <compatibility:Versioning>`
scheme mentioned in this document, :ref:`regret`'s public API may change
more drastically until it reaches version 1.0.0 (it's "official" public
release).

.. _regret-deprecation-period:

In the event that an API requires a backwards incompatible change, a
deprecation period of *six months* or *two releases* will preserve the
original behavior unchanged, whilst emitting a `DeprecationWarning`, and
introducing any replacement APIs.


Python Version Support
----------------------

In general, :ref:`regret`'s support for particular versions of
Python will end at *latest* on or around the `end of life dates
<cpython-devguide:devcycle>` for each respective version, but more
typically once they constitute a meaningful maintenance burden and
constitute a smaller proportion of installations. Exceptions may be made
in some circumstances where versions see continued use, but should not
be relied upon. Support contracts are available for situations which
require them.

Unless otherwise noted, only the *latest* patch version of each CPython
release is officially supported.

Attempts will always be made to have :ref:`regret`'s supported Python
versions reflected in its built distributions (i.e. via `python_requires
<packaging:python_requires>`), such that installation tools do
not install versions unless they are compatible with the running
interpreter.


Further Notes
-------------

:ref:`regret`'s `continuous integration and test suite
<https://github.com/Julian/regret/actions?query=workflow%3ACI>`_ should
be referenced as a representation of execution "environments" it
supports.

This includes both operating system support, as well as broader concerns
– as a hypothetical example, if a new way of installing or running
:ref:`regret` is used which is not already being tested in the automated
suite, its support or continuing function is *not* guaranteed.

Pull requests are welcome to add additional supported environments,
though some discretion may still be applied if there is likelihood of
ongoing maintenance burden.
