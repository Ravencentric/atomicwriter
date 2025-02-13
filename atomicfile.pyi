from _typeshed import StrPath

__all__ = ["write_bytes", "write_text"]

def write_bytes(data: bytes, dest: StrPath, *, overwrite: bool = False) -> None:
    """
    Write bytes to a file atomically.

    Parameters
    ----------
    data : bytes
        Bytes to write.
    dest : StrPath
        Destination file path.
    overwrite : bool, optional
        Whether to overwrite the destination file if it already exists.

    Raises
    ------
    FileExistsError
        If `overwrite` is False and `dest` exists.
    OSError
        If any other error occurs.

    """

def write_text(data: str, dest: StrPath, *, overwrite: bool = False) -> None:
    """
    Write string to a file atomically.

    Parameters
    ----------
    data : str
        String to write.
    dest : StrPath
        Destination file path.
    overwrite : bool, optional
        Whether to overwrite the destination file if it already exists.

    Raises
    ------
    FileExistsError
        If `overwrite` is False and `dest` exists.
    OSError
        If any other error occurs.

    """
