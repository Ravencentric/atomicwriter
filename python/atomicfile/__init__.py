from pathlib import Path

from . import _rust_atomicfile

__all__ = _rust_atomicfile.__all__


def write_bytes(data, dest, *, overwrite=False):
    return Path(_rust_atomicfile.write_bytes(data, dest, overwrite=overwrite))


def write_text(data, dest, *, overwrite=False):
    return Path(_rust_atomicfile.write_text(data, dest, overwrite=overwrite))
