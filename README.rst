======
regret
======

|PyPI| |Pythons| |CI| |Codecov| |ReadTheDocs|

.. |PyPI| image:: https://img.shields.io/pypi/v/regret.svg
  :alt: PyPI version
  :target: https://pypi.org/project/regret/

.. |Pythons| image:: https://img.shields.io/pypi/pyversions/regret.svg
  :alt: Supported Python versions
  :target: https://pypi.org/project/regret/

.. |CI| image:: https://github.com/Julian/regret/workflows/CI/badge.svg
  :alt: Build status
  :target: https://github.com/Julian/regret/actions?query=workflow%3ACI

.. |Codecov| image:: https://codecov.io/gh/Julian/regret/branch/master/graph/badge.svg
  :alt: Codecov Code coverage
  :target: https://codecov.io/gh/Julian/regret

.. |ReadTheDocs| image:: https://readthedocs.org/projects/regret/badge/?version=stable&style=flat
  :alt: ReadTheDocs status
  :target: https://regret.readthedocs.io/en/stable/

``Regret`` is a library for deprecating functionality in Python
libraries and applications.

Its documentation lives on `Read the Docs
<https://regret.readthedocs.io/en/stable/>`_.


Deprecations
------------

``Regret`` can deprecate:

    - [x] callables
        - [x] functions
        - [x] classes
            - [ ] subclassable classes
            - [ ] old-style classes
    - [ ] attributes
        - [ ] of modules
        - [ ] of classes
            - [ ] of old-style classes
        - [ ] of instances
    - [ ] descriptors
        - [ ] classmethod
    - [ ] modules
    - [ ] arguments to callables
        - [ ] required arguments that will be removed
        - [ ] optional arguments that are now required
        - [ ] mutual exclusion
    - [ ] ``zope.interface``\s


Design Goals
------------

``Regret`` is meant to cover all of the deprecations an author may encounter.

It is intended to:

    * be versioning system agnostic (i.e. `SemVer
      <https://semver.org/>`_, `CalVer <https://calver.org/>`_, `HipsTer
      <https://en.wikipedia.org/wiki/Hipster_(contemporary_subculture)>`_,
      etc.)

    * be documentation system agnostic, though potentially documentation
      system aware (i.e. `Sphinx <https://www.sphinx-doc.org>`_,
      `epydoc <https://en.wikipedia.org/wiki/Epydoc>`_, `Plaintext
      <https://lmgtfy.com/?q=use+sphinx>`_, etc.)

    * be itself fully tested

    * support removal date indication, and likely "policies" which automate
      choosing default removal dates

    * minimize the amount of deprecation-related code required for authors

In particular, as a lofty first milestone, it is intended to cover all
of the specific deprecations required for these `jsonschema issues
<https://github.com/Julian/jsonschema/issues?utf8=%E2%9C%93&q=label%3A%22Pending+Deprecation%22>`_,
and with luck, to subsume all the functionality present in
`twisted.python.deprecate <https://twistedmatrix.com/documents/current/api/twisted.python.deprecate.html>`_.
