use pyo3::exceptions::{PyFileExistsError, PyOSError, PyValueError};
use pyo3::prelude::*;
use std::io;
use std::{
    io::{BufWriter, Write},
    path::{self, PathBuf},
};

/// ValueError because that's what Python raises.
///
/// ```python
/// >>> f = open("foo.txt", "w")
/// >>> f.close()
/// >>> f.write("oops")
/// Traceback (most recent call last):
/// File "<python-input-2>", line 1, in <module>
///     f.write("oops")
///     ~~~~~~~^^^^^^^^
/// ValueError: I/O operation on closed file.
/// ```
fn closed_file_error() -> PyErr {
    PyValueError::new_err("I/O operation on closed file.")
}

fn os_error(e: impl ToString) -> PyErr {
    PyOSError::new_err(e.to_string())
}

/// A class for writing to a file atomically.
#[pyclass]
struct AtomicWriter {
    #[pyo3(get)]
    destination: PathBuf,
    #[pyo3(get)]
    overwrite: bool,
    // Use Option<T> so that we can take ownership
    // of T in self.commit()
    // Ref: https://github.com/PyO3/pyo3/issues/2225#issuecomment-1073705548
    inner: Option<BufWriter<tempfile::NamedTempFile>>,
}

#[pymethods]
impl AtomicWriter {
    #[new]
    #[pyo3(signature = (destination, *, overwrite=false))]
    fn new(destination: PathBuf, overwrite: bool) -> PyResult<Self> {
        let destination = path::absolute(destination).map_err(os_error)?;
        let parent = destination
            .parent()
            .ok_or_else(|| PyValueError::new_err("destination must have a parent directory"))?;

        let tmpfile = tempfile::Builder::new()
            .append(true)
            .tempfile_in(parent)
            .map_err(os_error)?;

        let writer = BufWriter::new(tmpfile);

        Ok(Self {
            destination,
            overwrite,
            inner: Some(writer),
        })
    }

    #[pyo3(signature = (data, /))]
    fn write_bytes(&mut self, data: &[u8]) -> PyResult<()> {
        self.inner
            .as_mut()
            .ok_or_else(closed_file_error)?
            .write_all(data)
            .map_err(os_error)?;
        Ok(())
    }

    #[pyo3(signature = (data, /))]
    fn write_text(&mut self, data: &str) -> PyResult<()> {
        self.write_bytes(data.as_bytes())
    }

    /// Commit the contents of the temporary file to the destination file.
    fn commit(&mut self) -> PyResult<()> {
        let tempfile = {
            // Take ownership of the underlying writer.
            let mut bufwriter = self.inner.take().ok_or_else(closed_file_error)?;
            // As per docs: "It is critical to call flush before BufWriter<W> is dropped."
            bufwriter.flush().map_err(os_error)?;
            bufwriter.into_inner().map_err(os_error)?
        };

        // Sync before persisting the temporary file.
        tempfile.as_file().sync_all().map_err(os_error)?;

        let persisted = match self.overwrite {
            true => tempfile.persist(&self.destination),
            false => tempfile.persist_noclobber(&self.destination),
        };

        match persisted {
            Ok(_) => Ok(()),
            Err(e) if e.error.kind() == io::ErrorKind::AlreadyExists => {
                Err(PyFileExistsError::new_err(self.destination.clone()))
            }
            Err(e) => Err(os_error(e)),
        }
    }
}

#[pymodule(gil_used = false)]
fn _impl(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AtomicWriter>()?;
    Ok(())
}
