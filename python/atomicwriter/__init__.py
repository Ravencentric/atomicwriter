from pathlib import Path

from . import _rust_atomicwriter

__all__ = ("AtomicWriter", "write_bytes", "write_text")


class AtomicWriter:
    __slots__ = ("_writer",)

    def __init__(self, dest, *, overwrite=False):
        self._writer = _rust_atomicwriter.AtomicWriter(dest, overwrite=overwrite)

    @property
    def dest(self):
        return Path(self._writer.dest)

    @property
    def overwrite(self):
        return self._writer.overwrite

    def write_bytes(self, data):
        self._writer.write_bytes(data)

    def write_text(self, data):
        self._writer.write_text(data)

    def commit(self):
        self._writer.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.commit()

    def __repr__(self):
        return f"{self.__class__.__name__}(dest='{self.dest}', overwrite={self.overwrite})"


def write_bytes(data, dest, *, overwrite=False):
    return Path(_rust_atomicwriter.write_bytes(data, dest, overwrite=overwrite))


def write_text(data, dest, *, overwrite=False):
    return Path(_rust_atomicwriter.write_text(data, dest, overwrite=overwrite))
