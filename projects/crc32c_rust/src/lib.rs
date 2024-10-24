use pyo3::prelude::*;
use std::fs::File;
use std::io::{BufReader, Read};

use std::hash::Hasher;

#[pyfunction]
fn calculate_crc32c(path: &str) -> PyResult<u64> {
    let file = File::open(path)?;
    let mut reader = BufReader::with_capacity(1024 * 1024, file); // 1MB buffer
                                                                  // let mut hasher = crc32c::Crc32c::new();
    let mut hasher = crc32c::Crc32cHasher::default();
    let mut buffer = [0; 1024 * 1024];

    loop {
        match reader.read(&mut buffer) {
            Ok(0) => break, // EOF
            Ok(n) => hasher.write(&buffer[..n]),
            Err(e) => return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string())),
        }
    }

    Ok(hasher.finish())
}

#[pymodule]
fn crc32c_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_crc32c, m)?)?;
    Ok(())
}
