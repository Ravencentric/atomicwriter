from __future__ import annotations

import contextlib
import os
import re
import sys
import typing
from pathlib import Path

import atomicfile
import pytest

StrPath: typing.TypeAlias = typing.Union[str, os.PathLike[str]]


class MyPathLike(os.PathLike[str]):
    def __init__(self, p: str) -> None:
        self.p = p

    def __fspath__(self) -> str:
        return self.p

    def __repr__(self) -> str:
        return f"MyPathLike('{self.p}')"


def generate_pathlikes(*args: str) -> tuple[StrPath, ...]:
    pathlikes: list[StrPath] = []

    for arg in args:
        pathlikes.extend((arg, Path(arg), MyPathLike(arg)))

    return tuple(pathlikes)


@pytest.mark.parametrize("file", generate_pathlikes("dest.txt"), ids=repr)
def test_write_text(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False
    dest2 = atomicfile.write_text("hello world", dest)
    assert dest2 == Path(dest).resolve()
    assert dest2.is_file()
    assert dest2.read_text() == "hello world"


@pytest.mark.parametrize("file", generate_pathlikes("dest.bin"), ids=repr)
def test_write_bytes(file: StrPath, tmp_path: Path) -> None:
    dest = tmp_path / file
    assert dest.exists() is False
    dest2 = atomicfile.write_bytes(b"hello world", dest)
    assert dest2 == Path(dest).resolve()
    assert dest2.is_file()
    assert dest2.read_bytes() == b"hello world"


@pytest.mark.parametrize("file", generate_pathlikes("dest.txt"), ids=repr)
def test_overwrite(file: StrPath, tmp_path: Path) -> None:
    # Pretend we have an existing file.
    dest = tmp_path / file
    dest.write_text("bye world")
    assert dest.is_file() is True

    # Failed write.
    with pytest.raises(FileExistsError, match=re.escape(str(dest.resolve()))):
        atomicfile.write_text("hello world", dest)

    # Must be unaltered because the write failed.
    assert dest.read_text() == "bye world"

    dest2 = atomicfile.write_text("hello world", dest, overwrite=True)
    assert dest2.is_file()
    assert dest2.read_text() == "hello world"


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires contextlib.chdir (3.11+)")
@pytest.mark.parametrize("file", generate_pathlikes("dest.txt", "./dest.txt", r".\dest.txt"), ids=repr)
def test_cwd(file: StrPath, tmp_path: Path) -> None:
    with contextlib.chdir(tmp_path):
        dest = atomicfile.write_text("hello", file)
        assert dest.read_text() == "hello"
        assert dest == Path(file).resolve()
