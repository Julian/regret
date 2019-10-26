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

.. |CI| image:: https://travis-ci.com/Julian/regret.svg?branch=master
  :alt: Build status
  :target: https://travis-ci.com/Julian/regret

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


Design Goals
------------

``Regret`` is meant to cover all of the deprecations an author may encounter.

It is intended to:

    * be versioning system agnostic (i.e. `SemVer
      <https://semver.org/>`_, `CalVer <https://calver.org/>`_, `HipsTer
      <https://en.wikipedia.org/wiki/Hipster_(contemporary_subculture)>`_,
      etc.)

    * be itself fully tested

    * minimize the amount of deprecation-related code required for authors

In particular, as a lofty first milestone, it is intended to cover all
of the specific deprecations required for these `jsonschema issues
<https://github.com/Julian/jsonschema/issues?utf8=%E2%9C%93&q=label%3A%22Pending+Deprecation%22>`_,
and with luck, to subsume all the functionality present in
`twisted.python.deprecate <https://twistedmatrix.com/documents/current/api/twisted.python.deprecate.html>`_.
