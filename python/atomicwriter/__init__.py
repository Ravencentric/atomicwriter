# type: ignore
"""Cross-platform atomic file writer for all-or-nothing operations."""

from . import _impl

__all__ = ("AtomicWriter",)


class AtomicWriter:
    __slots__ = ("_impl",)

    def __init__(self, destination, *, overwrite=False):
        """
        Create and manage a file for atomic writes.

        Changes are staged in a temporary file within the destination file's directory,
        then atomically moved to the destination file on commit.

        Parameters
        ----------
        destination : StrPath
            The path to the destination file.
        overwrite : bool, optional
            Whether to overwrite the destination file if it already exists.

        Raises
        ------
        OSError
            If any OS-level error occurs during temporary file creation.

        """
        self._impl = _impl.AtomicWriter(destination, overwrite=overwrite)

    @property
    def destination(self):
        """The absolute path to the destination file."""
        return self._impl.destination

    @property
    def overwrite(self):
        """Whether to overwrite the destination file if it already exists."""
        return self._impl.overwrite

    def write_bytes(self, data, /):
        """
        Write bytes to the temporary file.

        Parameters
        ----------
        data : bytes
            The bytes to write.

        Raises
        ------
        ValueError
            If attempting to write to a file that has already been committed and closed.
        OSError
            If an OS-level error occurs during write.

        """
        self._impl.write_bytes(data)

    def write_text(self, data, /):
        """
        Write text to the temporary file.

        Parameters
        ----------
        data : str
            The text to write.

        Raises
        ------
        ValueError
            If attempting to write to a file that has already been committed and closed.
        OSError
            If an OS-level error occurs during write.

        """
        self._impl.write_text(data)

    def commit(self):
        """
        Commit the contents of the temporary file to the destination file.

        This method atomically moves the temporary file to the destination file.

        Raises
        ------
        FileExistsError
            If `overwrite` is `False` and the destination file already exists.
        ValueError
            If attempting to commit a file that has already been committed and closed.
        OSError
            If an OS-level error occurs during file persistence or sync.

        """
        self._impl.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self._impl.commit()

    def __repr__(self):
        return f"AtomicWriter(destination='{self.destination}', overwrite={self.overwrite})"
