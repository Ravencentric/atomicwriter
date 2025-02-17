from pathlib import Path

from . import _impl

__all__ = ("AtomicWriter", "write_bytes", "write_text")


class AtomicWriter:
    __slots__ = ("_impl",)

    def __init__(self, destination, *, overwrite=False):
        self._impl = _impl.AtomicWriter(destination, overwrite=overwrite)

    @property
    def destination(self):
        return Path(self._impl.destination)

    @property
    def overwrite(self):
        return self._impl.overwrite

    def write_bytes(self, data):
        self._impl.write_bytes(data)

    def write_text(self, data):
        self._impl.write_text(data)

    def commit(self):
        return Path(self._impl.commit())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.commit()

    def __repr__(self):
        return f"{self.__class__.__name__}(destination='{self.destination}', overwrite={self.overwrite})"


def write_bytes(data, destination, *, overwrite=False):
    return Path(_impl.write_bytes(data, destination, overwrite=overwrite))


def write_text(data, destination, *, overwrite=False):
    return Path(_impl.write_text(data, destination, overwrite=overwrite))
