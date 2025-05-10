from __future__ import annotations

import contextlib
import re
import sys
import textwrap
from pathlib import Path

import pytest
from atomicwriter import AtomicWriter

from .utils import StrPath, generate_pathlikes


@pytest.mark.parametrize("file", generate_pathlikes("dest.txt"), ids=repr)
def test_properties(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    atfile = AtomicWriter(dest)
    atfile.destination == dest
    atfile.overwrite is False

    atfile.write_text("hello world")
    assert dest.exists() is False  # Still doesn't exist

    atfile.commit()
    assert dest.is_file()  # Now it does exist
    assert dest.read_text() == "hello world"


@pytest.mark.parametrize("file", generate_pathlikes("dest.txt"), ids=repr)
def test_write_text(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    atfile = AtomicWriter(dest)
    atfile.write_text("hello world")
    assert dest.exists() is False  # Still doesn't exist

    atfile.commit()
    assert dest.is_file()  # Now it does exist
    assert dest.read_text() == "hello world"


@pytest.mark.parametrize("file", generate_pathlikes("dest.bin"), ids=repr)
def test_write_bytes(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    atfile = AtomicWriter(dest)
    atfile.write_bytes(b"hello world")
    assert dest.exists() is False  # Still doesn't exist

    atfile.commit()
    assert dest.is_file()  # Now it does exist
    assert dest.read_bytes() == b"hello world"


@pytest.mark.parametrize("file", generate_pathlikes("dest.txt"), ids=repr)
def test_overwrite(file: StrPath, tmp_path: Path) -> None:
    # Pretend we have an existing file.
    dest = tmp_path / file
    dest.write_text("bye world")
    assert dest.is_file() is True

    # Failed write.
    with pytest.raises(FileExistsError, match=re.escape(str(dest))):
        atfile = AtomicWriter(dest)
        atfile.write_text("hello world")
        atfile.commit()

    # Must be unaltered because the write failed.
    assert dest.read_text() == "bye world"

    atfile2 = AtomicWriter(dest, overwrite=True)
    atfile2.write_text("hello world")
    atfile2.commit()
    assert dest.is_file()
    assert dest.read_text() == "hello world"


@pytest.mark.parametrize("file", generate_pathlikes("dest.txt"), ids=repr)
def test_commit_idempotence(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    atfile = AtomicWriter(dest)
    atfile.write_text("hello world")
    assert dest.exists() is False  # Still doesn't exist

    atfile.commit()
    assert dest.is_file()  # Now it does exist
    assert dest.read_text() == "hello world"

    # Nothing happens
    atfile.commit()
    assert dest.is_file()
    assert dest.read_text() == "hello world"

    # Nothing happens
    atfile.commit()
    assert dest.is_file()
    assert dest.read_text() == "hello world"


@pytest.mark.parametrize("file", generate_pathlikes("Alpha Trion.txt"), ids=repr)
def test_multiple_write_text_calls(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    with AtomicWriter(dest) as atfile:
        atfile.write_text("What defines a Transformer is not the cog in his chest, ")
        atfile.write_text("but the Spark that resides in their core.\n")
        assert dest.exists() is False  # Still doesn't exist
        atfile.write_text("A Spark that gives you the will to make your world better.\n")
        atfile.write_text("My fellow Primes had that spark, and I see their strength in you.")

    assert dest.is_file()  # Now it does exist
    assert (
        dest.read_text()
        == textwrap.dedent("""
    What defines a Transformer is not the cog in his chest, but the Spark that resides in their core.
    A Spark that gives you the will to make your world better.
    My fellow Primes had that spark, and I see their strength in you.
    """).strip()
    )


@pytest.mark.parametrize("file", generate_pathlikes("Alpha Trion.txt"), ids=repr)
def test_multiple_write_text_call_fails(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    try:
        with AtomicWriter(dest) as atfile:
            atfile.write_text("What defines a Transformer is not the cog in his chest, ")
            atfile.write_text("but the Spark that resides in their core.\n")
            raise Exception  # failed mid write
            atfile.write_text("A Spark that gives you the will to make your world better.\n")
            atfile.write_text("My fellow Primes had that spark, and I see their strength in you.")
    except Exception:
        pass

    assert dest.exists() is False  # Must not exist


@pytest.mark.parametrize("file", generate_pathlikes("Alpha Trion.txt"), ids=repr)
def test_multiple_write_byte_calls(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    with AtomicWriter(dest) as atfile:
        atfile.write_bytes(b"What defines a Transformer is not the cog in his chest, ")
        atfile.write_bytes(b"but the Spark that resides in their core.\n")
        assert dest.exists() is False  # Still doesn't exist
        atfile.write_bytes(b"A Spark that gives you the will to make your world better.\n")
        atfile.write_bytes(b"My fellow Primes had that spark, and I see their strength in you.")

    assert dest.is_file()  # Now it does exist
    assert (
        dest.read_bytes()
        == textwrap.dedent("""
    What defines a Transformer is not the cog in his chest, but the Spark that resides in their core.
    A Spark that gives you the will to make your world better.
    My fellow Primes had that spark, and I see their strength in you.
    """)
        .strip()
        .encode()
    )


@pytest.mark.parametrize("file", generate_pathlikes("Alpha Trion.txt"), ids=repr)
def test_multiple_write_bytes_call_fails(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False  # Doesn't exist

    try:
        with AtomicWriter(dest) as atfile:
            atfile.write_bytes(b"What defines a Transformer is not the cog in his chest, ")
            atfile.write_bytes(b"but the Spark that resides in their core.\n")
            raise Exception  # failed mid write
            atfile.write_bytes(b"A Spark that gives you the will to make your world better.\n")
            atfile.write_bytes(b"My fellow Primes had that spark, and I see their strength in you.")
    except Exception:
        pass

    assert dest.exists() is False  # Must not exist


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires contextlib.chdir (3.11+)")
@pytest.mark.parametrize("file", generate_pathlikes("dest.txt", "./dest.txt", r".\dest.txt"), ids=repr)
def test_cwd(file: StrPath, tmp_path: Path) -> None:
    with contextlib.chdir(tmp_path):
        atfile = AtomicWriter(file)
        atfile.write_text("hello")
        atfile.commit()
        assert atfile.destination == Path(file).absolute()

        with open(file) as dest:
            assert dest.read() == "hello"
