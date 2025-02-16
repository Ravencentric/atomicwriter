from __future__ import annotations

import os
import typing
from pathlib import Path

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
