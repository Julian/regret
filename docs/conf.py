import importlib.metadata
import re

project = "regret"
author = "Julian Berman"
copyright = "2019, " + author

# version: The short X.Y version
# release: The full version, including alpha/beta/rc tags.
release = importlib.metadata.version("regret")
version = release.partition("-")[0]

language = "en"
default_role = "any"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinxcontrib.spelling",
    "sphinxext.opengraph",
]

pygments_style = "lovelace"
pygments_dark_style = "one-dark"

html_theme = "furo"

# -- Extension configuration -------------------------------------------------

# -- Options for autodoc extension -------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
}

# -- Options for autosectionlabel extension ----------------------------------

autosectionlabel_prefix_document = True

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    "attrs": ("https://attrs.org/en/stable/", None),
    "cpython-devguide": ("https://devguide.python.org/", None),
    "jsonschema": (
        "https://python-jsonschema.readthedocs.io/en/latest/",
        None,
    ),
    "packaging": ("https://packaging.python.org/en/latest/", None),
    "python": ("https://docs.python.org/3/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# -- Options for the linkcheck builder ------------------------------------


def entire_domain(host):
    return r"http.?://" + re.escape(host) + r"($|/.*)"


linkcheck_ignore = [
    entire_domain("codecov.io"),
    entire_domain("img.shields.io"),
    "https://github.com/Julian/regret/actions",
    "https://github.com/Julian/regret/workflows/CI/badge.svg",
]
