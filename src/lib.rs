use pyo3::exceptions::{PyFileExistsError, PyOSError};
use pyo3::prelude::*;
use std::fs;
use std::{
    io::Write,
    path::{Path, PathBuf},
};
use tempfile::NamedTempFile;

/// Returns the canonicalized parent directory of a given path,
/// creating it and any necessary ancestors if they don't exist.
fn get_parent_directory(path: impl AsRef<Path>) -> PyResult<PathBuf> {
    let dir = match path.as_ref().parent() {
        Some(parent) if parent == Path::new("") => Path::new("."),
        Some(parent) => parent,
        None => Path::new("."),
    };

    let dir = dunce::canonicalize(dir).map_err(|e| PyOSError::new_err(e.to_string()))?;

    // Create the directories if they don't exist.
    fs::create_dir_all(dir.as_path()).map_err(|e| PyOSError::new_err(e.to_string()))?;

    Ok(dir)
}

#[pyfunction]
#[pyo3(signature = (data, dest, *, overwrite=false))]
fn write_bytes(data: &[u8], dest: PathBuf, overwrite: bool) -> PyResult<PathBuf> {
    // Get the destination's parent directory
    // Assumes current working directory if parent cannot be determined.
    // This directory is where we'll make the temporary file.

    let dir = get_parent_directory(dest.as_path())?;

    {
        // Make a temporary file and write to it.
        let mut tmpfile = NamedTempFile::new_in(dir).map_err(|e| PyOSError::new_err(e.to_string()))?;
        tmpfile.write_all(data).map_err(|e| PyOSError::new_err(e.to_string()))?;

        // Error if overwrite is false and the destination already exists.
        if !overwrite && dest.exists() {
            return Err(PyFileExistsError::new_err(dest));
        }

        // Persist the temporary file.
        let file = tmpfile
            .persist(dest.as_path())
            .map_err(|e| PyOSError::new_err(e.to_string()))?;
        let synced = file.sync_all();

        // Clean up if the sync failed.
        if let Err(err) = synced {
            fs::remove_file(dest.as_path()).map_err(|e| PyOSError::new_err(e.to_string()))?;
            return Err(PyOSError::new_err(err.to_string()));
        }
    }

    dunce::canonicalize(dest).map_err(|e| PyOSError::new_err(e.to_string()))
}

#[pyfunction]
#[pyo3(signature = (data, dest, *, overwrite=false))]
fn write_text(data: &str, dest: PathBuf, overwrite: bool) -> PyResult<PathBuf> {
    write_bytes(data.as_bytes(), dest, overwrite)
}

#[pymodule(gil_used = false)]
fn _rust_atomicfile(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(write_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(write_text, m)?)?;
    m.add("__all__", vec!["write_bytes", "write_text"])?;
    Ok(())
}
