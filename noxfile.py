import os
import shutil

import nox

nox.needs_version = ">=2024.10.9"
nox.options.default_venv_backend = "uv"

PYTHON_VERSIONS = ("3.9", "3.10", "3.11", "3.12", "3.13", "pypy3.9", "pypy3.10")


def cargo(session: nox.Session, *args: str) -> None:
    session.run("cargo", *args, external=True)


def install(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--only-group",
        "dev",
        "--locked",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("maturin", "develop", "--uv")


@nox.session(venv_backend=None, default=False)
def clean(session: nox.Session) -> None:
    cargo(session, "clean")

    paths = (
        "./.mypy_cache",
        "./.pytest_cache",
        "./.ruff_cache",
        "./dist",
        "./tests/__pycache__",
        "./__pycache__",
        "./.nox",
    )

    for p in paths:
        try:
            shutil.rmtree(p)
        except FileNotFoundError:
            pass


@nox.session
def lint(session: nox.Session) -> None:
    install(session)

    if os.getenv("CI"):
        # Do not modify files in CI, simply fail.
        cargo(session, "fmt", "--check")
        cargo(session, "clippy")
        session.run("ruff", "check", ".")
        session.run("ruff", "format", ".", "--check")
    else:
        # Fix any fixable errors if running locally.
        cargo(session, "fmt")
        cargo(session, "clippy", "--fix", "--lib", "-p", "atomicfile", "--allow-dirty")
        session.run("ruff", "check", ".", "--fix")
        session.run("ruff", "format", ".")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    install(session)
    session.run("pytest", "-vv", *session.posargs)
