Here are some notes for developing `regret`.

API docstring are written using Sphinx / ReStructredText format.

Before a commit, stage all files and run all the tests with::

    tox -e tests,style

To run a single test use::

    $ python -m virtue regret.tests.test_api.TestModuleDeprecation.test_deprecated_module_reference
