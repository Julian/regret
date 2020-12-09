======================
Contributing to Regret
======================

Contributions to ``regret`` are most welcome! Below are some tips for setting
up a development environment and submitting a pull request.


Development Environment
-----------------------

*You likely will want to create a virtual environment for any
installations below.*

``regret`` uses `pre-commit <https://pre-commit.com/>`_ for some
of its linters, ensuring that they run before a commit is even
finished in ``git``.  After installing ``pre-commit`` (via e.g. ``pip
install pre-commit``, or your OS's package manager), you can set up
``pre-commit``'s hooks to run on commit with ``pre-commit install``,
after which each time you run ``git commit`` a small number of checks
will run. If you instead prefer, ``pre-commit`` can also be run via
``tox`` as described below.

``regret`` uses `tox <https://tox.readthedocs.io>`_ to define test
environments (the same ones which will run in CI via GitHub Actions).

After installing ``tox`` (via e.g. ``pip install tox`` or your OS's package
manager), running ``tox`` with no arguments will run all of ``regret``'s
testing environments. Doing so can be slow, and requires a number of different
Python versions to be installed (all the ones ``regret`` claims to support).
You may instead prefer to run something like ``tox -p auto`` to run them in
parallel, or to select a subset of environments such as ``tox -e
py39-tests,style`` to run only the test suite and style checkers.

Generally, I (Julian) personally only run ``tox``, even as above, right
before pushing a set of commits. During incremental development, I run
a test runner directly on ``regret`` without using ``tox`` via e.g.
``virtue regret``.

``regret``'s test suite is written simply with ``unittest``, so any
test runner that knows how to execute ``unittest`` test suites should
work; feel free to use your favorite (``virtue`` above is mine, but
``py.test`` or ``trial`` or ``green`` or etc. should work).


Documentation
-------------

``regret``'s documentation is written with `Sphinx in ReStructuredText
<https://www.sphinx-doc.org>`_, using `Google-style Napoleon
<https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_.

A number of documentation related test environments run in CI (to ensure
links function, spelling is correct, etc.). For documentation changes,
you may want to run them locally, via e.g. ``tox -e docs-spelling``.


Submitting Changes
------------------

Small, single-purpose changes are infinitely easier to review than large
ones.  Whenever possible, it's appreciated if changes do precisely one
thing, and aren't longer than around 200 lines.

If such a thing seems difficult, you're certainly welcome to ask for
help splitting the changes up, or to submit it for review regardless and
we'll try to make it work.
