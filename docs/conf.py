import importlib.metadata
import re

project = "regret"
author = "Julian Berman"
copyright = f"2019, {author}"

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


# See sphinx-doc/sphinx#10785
_TYPE_ALIASES = dict(
    _Callable=("class", "Callable"),
    name_of=("data", "name_of"),
)


def _resolve_broken_refs(app, env, node, contnode):
    kind, target = _TYPE_ALIASES.get(node["reftarget"], (None, None))
    if kind is not None:
        return app.env.get_domain("py").resolve_xref(
            env,
            node["refdoc"],
            app.builder,
            kind,
            target,
            node,
            contnode,
        )


def setup(app):
    app.connect("missing-reference", _resolve_broken_refs)


def entire_domain(host):
    return r"http.?://" + re.escape(host) + r"($|/.*)"


linkcheck_ignore = [
    entire_domain("img.shields.io"),
    "https://epydoc.sourceforge.net/",
    "https://github.com/Julian/regret/actions",
    "https://github.com/Julian/regret/workflows/CI/badge.svg",
]


autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
}

# -- autosectionlabel ----------------------------------

autosectionlabel_prefix_document = True

# -- intersphinx ---------------------------------------

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

# -- sphinxcontrib-spelling --

spelling_word_list_filename = "spelling-wordlist.txt"
spelling_show_suggestions = True
