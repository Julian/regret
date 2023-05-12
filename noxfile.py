from pathlib import Path

import nox

ROOT = Path(__file__).parent
PYPROJECT = ROOT / "pyproject.toml"
DOCS = ROOT / "docs"
PACKAGE = ROOT / "regret"


nox.options.sessions = []


def session(default=True, **kwargs):
    def _session(fn):
        if default:
            nox.options.sessions.append(kwargs.get("name", fn.__name__))
        return nox.session(**kwargs)(fn)

    return _session


@session(python=["3.8", "3.9", "3.10", "3.11", "pypy3"])
def tests(session):
    session.install(ROOT, "virtue", "-r", ROOT / "test-requirements.txt")
    if session.posargs == ["coverage"]:
        session.install("coverage[toml]")
        session.run("coverage", "run", "-m", "virtue", PACKAGE)
        session.run("coverage", "report")
    else:
        session.run("python", "-m", "virtue", *session.posargs, "regret")


@session()
def pytest_tests(session):
    session.install(ROOT, "pytest", "-r", ROOT / "test-requirements.txt")
    session.run("pytest", *session.posargs, PACKAGE)


@session()
def audit(session):
    session.install("pip_audit", ROOT)
    session.run("python", "-m", "pip_audit")


@session(tags=["build"])
def build(session):
    session.install("build")
    tmpdir = session.create_tmp()
    session.run("python", "-m", "build", ROOT, "--outdir", tmpdir)


@session(tags=["style"])
def readme(session):
    session.install("build", "docutils", "twine")
    tmpdir = session.create_tmp()
    session.run("python", "-m", "build", ROOT, "--outdir", tmpdir)
    session.run("python", "-m", "twine", "check", tmpdir + "/*")

    CONTRIBUTING = ROOT / "CONTRIBUTING.rst"
    session.run("rst2html5.py", "--halt=warning", CONTRIBUTING, "/dev/null")


@session(tags=["style"])
def style(session):
    session.install("ruff")
    session.run("ruff", "check", ROOT)


@session()
def typing(session):
    session.install("pyright", ROOT)
    session.run("pyright", PACKAGE)


@session(tags=["docs"])
@nox.parametrize(
    "builder",
    [
        nox.param(name, id=name)
        for name in [
            "dirhtml",
            "doctest",
            "linkcheck",
            "man",
            "spelling",
        ]
    ],
)
def docs(session, builder):
    session.install("-r", DOCS / "requirements.txt")
    tmpdir = Path(session.create_tmp())
    argv = ["-n", "-T", "-W"]
    if builder != "spelling":
        argv += ["-q"]
    session.run(
        "python",
        "-m",
        "sphinx",
        "-b",
        builder,
        DOCS,
        tmpdir / builder,
        *argv,
    )


@session(tags=["docs", "style"], name="docs(style)")
def docs_style(session):
    session.install(
        "doc8",
        "pygments",
        "pygments-github-lexers",
    )
    session.run("python", "-m", "doc8", "--config", PYPROJECT, DOCS)


@session(default=False)
def requirements(session):
    session.install("pip-tools")
    for each in [DOCS / "requirements.in", ROOT / "test-requirements.in"]:
        session.run(
            "pip-compile",
            "--resolver",
            "backtracking",
            "-U",
            each.relative_to(ROOT),
        )
