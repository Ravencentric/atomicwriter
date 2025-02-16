from pathlib import Path
from types import TracebackType
from typing import final

from _typeshed import StrPath
from typing_extensions import Self

__all__ = ("AtomicWriter", "write_bytes", "write_text")

@final
class AtomicWriter:
    """
    Create and manage a file for atomic writes.

    This class provides a context manager for writing to a file atomically.
    It uses a temporary file to stage changes, and then moves
    the temporary file to the destination file on commit.
    """

    __slots__ = ("_writer",)

    def __init__(self, dest: StrPath, *, overwrite: bool = False) -> None:
        """
        Initialize AtomicWriter.

        Parameters
        ----------
        dest : PathLike
            The path to the destination file.
        overwrite : bool, optional
            Whether to overwrite the destination file if it already exists.

        Raises
        ------
        OSError
            If any OS-level error occurs during temporary file creation.

        """

    @property
    def dest(self) -> Path:
        """The path to the destination file."""
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
            If the file is closed.
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
            If the file is closed.
        OSError
            If an OS-level error occurs during write.

        """

    def commit(self) -> None:
        """
        Commit the contents of the temporary file to the destination file.

        This operation atomically moves the temporary file to the destination file.

        Raises
        ------
        FileExistsError
            If ``overwrite`` is `False` and the destination file already exists.
        ValueError
            If the file is closed.
        OSError
            If an OS-level error occurs during file persistence or sync.

        """

    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

def write_bytes(data: bytes, dest: StrPath, *, overwrite: bool = False) -> Path:
    """
    Write bytes to a file atomically.

    Parameters
    ----------
    data : bytes
        Bytes to write.
    dest : StrPath
        The path to the destination file.
    overwrite : bool, optional
        Whether to overwrite the destination file if it already exists.

    Returns
    -------
    Path
        `Path` object representing the destination file.

    Raises
    ------
    FileExistsError
        If ``overwrite`` is `False` and the destination file already exists.
    OSError
        If any OS-level error occurs during the process.

    """

def write_text(data: str, dest: StrPath, *, overwrite: bool = False) -> Path:
    """
    Write text to a file atomically.

    Parameters
    ----------
    data : str
        Text to write.
    dest : StrPath
        The path to the destination file.
    overwrite : bool, optional
        Whether to overwrite the destination file if it already exists.

    Returns
    -------
    Path
        `Path` object representing the destination file.

    Raises
    ------
    FileExistsError
        If ``overwrite`` is `False` and the destination file already exists.
    OSError
        If any OS-level error occurs during the process.

    """
