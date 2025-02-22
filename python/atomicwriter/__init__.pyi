"""Cross-platform atomic file writer for all-or-nothing operations."""

from pathlib import Path
from types import TracebackType
from typing import final

from _typeshed import StrPath
from typing_extensions import Self

__all__ = ("AtomicWriter",)

@final
class AtomicWriter:
    __slots__ = ("_impl",)

    def __init__(self, destination: StrPath, *, overwrite: bool = False) -> None:
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

    @property
    def destination(self) -> Path:
        """The absolute path to the destination file."""
    @property
    def overwrite(self) -> bool:
        """Whether to overwrite the destination file if it already exists."""

    def write_bytes(self, data: bytes) -> None:
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

    def write_text(self, data: str) -> None:
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

    def commit(self) -> None:
        """
        Commit the contents of the temporary file to the destination file.

        This method atomically moves the temporary file to the destination file.
        It's also idempotent and can be called multiple times without error.

        Raises
        ------
        FileExistsError
            If `overwrite` is `False` and the destination file already exists.
        OSError
            If an OS-level error occurs during file persistence or sync.

        """

    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
