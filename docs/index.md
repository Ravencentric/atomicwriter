# atomicwriter

[![Tests](https://img.shields.io/github/actions/workflow/status/Ravencentric/atomicwriter/tests.yml?label=tests)](https://github.com/Ravencentric/atomicwriter/actions/workflows/tests.yml)
[![Build](https://img.shields.io/github/actions/workflow/status/Ravencentric/atomicwriter/release.yml?label=build)](https://github.com/Ravencentric/atomicwriter/actions/workflows/release.yml)
![PyPI - Types](https://img.shields.io/pypi/types/atomicwriter)
![License](https://img.shields.io/pypi/l/atomicwriter?color=success)

[![PyPI - Latest Version](https://img.shields.io/pypi/v/atomicwriter?color=blue)](https://pypi.org/project/atomicwriter)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/atomicwriter)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/atomicwriter)

`atomicwriter` provides the `AtomicWriter` class, which performs cross-platform atomic file writes to ensure "all-or-nothing" operations—if a write fails, the target file is left unchanged.

## Usage

```python
from pathlib import Path
from atomicwriter import AtomicWriter

destination = Path("alpha_trion.txt")  # or str

with AtomicWriter(destination) as writer:
    writer.write_text("What defines a Transformer is not the cog in his chest, ")
    writer.write_text("but the Spark that resides in their core.\n")
    assert destination.is_file() is False

assert destination.is_file()
```

## Installation

`atomicwriter` is available on [PyPI](https://pypi.org/project/atomicwriter/), so you can simply use pip to install it.

```console
pip install atomicwriter
```

## Building from source

Building from source requires the [Rust toolchain](https://rustup.rs/) and [Python 3.9+](https://www.python.org/downloads/).

- With [`uv`](https://docs.astral.sh/uv/):

  ```console
  git clone https://github.com/Ravencentric/atomicwriter
  cd atomicwriter
  uv build
  ```

- With [`pypa/build`](https://github.com/pypa/build):

  ```console
  git clone https://github.com/Ravencentric/atomicwriter
  cd atomicwriter
  python -m build
  ```

## Acknowledgements

This project is essentially a thin wrapper around the excellent [`tempfile`](https://crates.io/crates/tempfile) crate, which handles all the heavy lifting for atomic file operations.

It is also heavily inspired by the now-archived [`atomicwrites`](https://pypi.org/project/atomicwrites/) project and uses a similar API.

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](https://github.com/Ravencentric/atomicwriter/blob/main/LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](https://github.com/Ravencentric/atomicwriter/blob/main/LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

## Contributing

Contributions are welcome! Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.
