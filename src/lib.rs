use pyo3::exceptions::{PyFileExistsError, PyOSError, PyValueError};
use pyo3::prelude::*;
use std::fs;
use std::{
    io::Write,
    path::{Path, PathBuf},
};

/// Returns the canonicalized parent directory of a given path,
/// creating it and any necessary ancestors if they don't exist.
fn get_parent_directory(path: impl AsRef<Path>) -> PyResult<PathBuf> {
    let dir = match path.as_ref().parent() {
        Some(parent) if parent == Path::new("") => Path::new("."),
        Some(parent) => parent,
        None => Path::new("."),
    }
    .to_path_buf();

    // Create the directories if they don't exist.
    fs::create_dir_all(&dir).map_err(|e| PyOSError::new_err(e.to_string()))?;

    Ok(dir)
}

/// A class for writing to a file atomically.
#[pyclass(module = "atomicwriter")]
struct AtomicWriter {
    #[pyo3(get)]
    dest: PathBuf,
    #[pyo3(get)]
    overwrite: bool,
    // Use Option<T> so that we can take ownership
    // of the NamedTempFile in self.commit()
    // Ref: https://github.com/PyO3/pyo3/issues/2225#issuecomment-1073705548
    tempfile: Option<tempfile::NamedTempFile>,
}

#[pymethods]
impl AtomicWriter {
    #[new]
    #[pyo3(signature = (dest, *, overwrite=false))]
    fn new(dest: PathBuf, overwrite: bool) -> PyResult<Self> {
        let dir = get_parent_directory(dest.as_path())?;

        let tempfile = tempfile::Builder::new()
            .append(true)
            .tempfile_in(dir.as_path())
            .map_err(|e| PyOSError::new_err(e.to_string()))?;
        Ok(Self {
            dest,
            overwrite,
            tempfile: Some(tempfile),
        })
    }

    fn write_bytes(&mut self, data: &[u8]) -> PyResult<()> {
        self.tempfile
            .as_mut()
            .ok_or_else(|| PyValueError::new_err("I/O operation on closed file."))?
            .write_all(data)
            .map_err(|e| PyOSError::new_err(e.to_string()))?;
        Ok(())
    }

    fn write_text(&mut self, data: &str) -> PyResult<()> {
        self.write_bytes(data.as_bytes())
    }

    /// Commit the contents of the temporary file to the destination file.
    fn commit(&mut self) -> PyResult<()> {
        // Error if overwrite is false and the destination already exists.
        if !self.overwrite && self.dest.exists() {
            return Err(PyFileExistsError::new_err(self.dest.clone()));
        }

        // Scope for managing the persisted file.
        {
            // Persist the temporary file.
            let file = self
                .tempfile
                .take()
                .ok_or_else(|| PyValueError::new_err("I/O operation on closed file."))?
                .persist(self.dest.as_path())
                .map_err(|e| PyOSError::new_err(e.to_string()))?;
            let synced = file.sync_all();

            // Clean up if the sync failed.
            if let Err(err) = synced {
                fs::remove_file(self.dest.as_path()).map_err(|e| PyOSError::new_err(e.to_string()))?;
                return Err(PyOSError::new_err(err.to_string()));
            }
        }

        Ok(())
    }
}

// Quick convenience wrapper method
#[pyfunction]
#[pyo3(signature = (data, dest, *, overwrite=false))]
fn write_bytes(data: &[u8], dest: PathBuf, overwrite: bool) -> PyResult<PathBuf> {
    {
        let mut file = AtomicWriter::new(dest.clone(), overwrite)?;
        file.write_bytes(data)?;
        file.commit()?;
    }
    Ok(dest)
}

// Quick convenience wrapper method
#[pyfunction]
#[pyo3(signature = (data, dest, *, overwrite=false))]
fn write_text(data: &str, dest: PathBuf, overwrite: bool) -> PyResult<PathBuf> {
    write_bytes(data.as_bytes(), dest, overwrite)
}

#[pymodule(gil_used = false)]
fn _rust_atomicwriter(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AtomicWriter>()?;
    m.add_function(wrap_pyfunction!(write_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(write_text, m)?)?;
    Ok(())
}
