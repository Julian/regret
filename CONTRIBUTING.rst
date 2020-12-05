API docstring are written using Sphinx / ReStructredText format.

Before a commit run all the tests with `tox -e test`.
To run a single test use::

    $ python -m virtue regret.tests.test_api.TestModuleDeprecation.test_deprecated_module_reference
