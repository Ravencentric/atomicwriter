import contextlib
import re
import sys
from pathlib import Path

import atomicfile
import pytest


def test_write_text(tmp_path: Path) -> None:
    dest = tmp_path / "dest.txt"
    assert dest.exists() is False
    atomicfile.write_text("hello world", dest)
    assert dest.is_file()
    assert dest.read_text() == "hello world"


def test_write_bytes(tmp_path: Path) -> None:
    dest = tmp_path / "dest.bin"
    assert dest.exists() is False
    atomicfile.write_bytes(b"hello world", dest)
    assert dest.is_file()
    assert dest.read_bytes() == b"hello world"


def test_overwrite(tmp_path: Path) -> None:
    dest = tmp_path / "dest.txt"
    dest.write_text("bye world")
    assert dest.is_file() is True

    with pytest.raises(FileExistsError, match=re.escape(str(dest.resolve()))):
        atomicfile.write_text("hello world", dest)

    atomicfile.write_text("hello world", dest, overwrite=True)
    assert dest.is_file()
    assert dest.read_text() == "hello world"


@pytest.mark.skipif(sys.version_info <= (3, 10), reason="requires contextlib.chdir")
@pytest.mark.parametrize("file", ["dest.txt", "./dest.txt", r".\dest.txt"])
def test_cwd(file: str, tmp_path: Path) -> None:
    with contextlib.chdir(tmp_path):
        atomicfile.write_text("hello", file)
        output = tmp_path / file
        assert output.read_text() == "hello"
        assert output == Path(file).resolve()
