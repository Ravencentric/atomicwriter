# rnzb

[![Tests](https://img.shields.io/github/actions/workflow/status/Ravencentric/rnzb/tests.yml?label=tests)](https://github.com/Ravencentric/rnzb/actions/workflows/tests.yml)
[![Build](https://img.shields.io/github/actions/workflow/status/Ravencentric/rnzb/release.yml?label=build)](https://github.com/Ravencentric/rnzb/actions/workflows/release.yml)
![PyPI - Types](https://img.shields.io/pypi/types/rnzb)
![License](https://img.shields.io/pypi/l/rnzb?color=success)

[![PyPI - Latest Version](https://img.shields.io/pypi/v/rnzb?color=blue)](https://pypi.org/project/rnzb)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rnzb)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/rnzb)

Python bindings to the [nzb-rs](https://crates.io/crates/nzb-rs) library - a [spec](https://sabnzbd.org/wiki/extra/nzb-spec) compliant parser for [NZB](https://en.wikipedia.org/wiki/NZB) files, written in Rust.

## Table Of Contents

- [About](#about)
- [Installation](#installation)
- [Related projects](#related-projects)
- [Performance](#performance)
- [Supported platforms](#supported-platforms)
- [Building from source](#building-from-source)
- [License](#license)
- [Contributing](#contributing)

## About

`rnzb.Nzb` is a drop-in replacement for [`nzb.Nzb`](https://nzb.ravencentric.cc/api-reference/parser/#nzb.Nzb).

For documentation and usage examples, refer to the [`nzb`](https://pypi.org/project/nzb) library's resources:

- [Tutorial](https://nzb.ravencentric.cc/tutorial/)
- [API Reference](https://nzb.ravencentric.cc/api-reference/parser/)

### Error handling

- `rnzb` uses the same error type (`rnzb.InvalidNzbError`) as `nzb` but it's not a drop-in replacement.
- Error messages will be largely similar to `nzb`'s, though not guaranteed to be identical in every case.
- `rnzb.InvalidNzbError` is a simpler exception (See [PyO3/pyo3#295](https://github.com/PyO3/pyo3/issues/295) for why). Its implementation is effectively:
  
  ```python
  class InvalidNzbError(Exception): pass
  ```
  
  This means that it's lacking custom attributes like `.message` found in `nzb`'s version. Code relying on such attributes on `nzb.InvalidNzbError` will require adjustment. Consider using the standard exception message (`str(e)`) to achieve the same result.

- `rnzb` will *only ever* raise explicitly documented errors for each function. Undocumented errors should be reported as bugs.

## Installation

`rnzb` is available on [PyPI](https://pypi.org/project/rnzb/), so you can simply use pip to install it.

```bash
pip install rnzb
```

## Related projects

Considering this is the fourth library for parsing a file format that almost nobody cares about and lacks a formal specification, here's an overview to help you decide:

| Project                                                  | Description                 | Parser | Meta Editor |
| -------------------------------------------------------- | --------------------------- | ------ | ----------- |
| [`nzb`](https://pypi.org/project/nzb)                    | Original Python Library     | ✅     | ✅          |
| [`nzb-rs`](https://crates.io/crates/nzb-rs)              | Rust port of `nzb`          | ✅     | ❌          |
| [`rnzb`](https://pypi.org/project/nzb)                   | Python bindings to `nzb-rs` | ✅     | ❌          |
| [`nzb-parser`](https://www.npmjs.com/package/nzb-parser) | Javascript port of `nzb`    | ✅     | ❌          |

## Performance

Although [`nzb`](https://pypi.org/project/nzb) is already quite fast due to its use of C-based [expat](https://docs.python.org/3/library/pyexpat.html) parser from Python's standard library, `rnzb` offers even better performance, being approximately 5 times faster than `nzb`.

```console
$ hyperfine --warmup 1 "python test_nzb.py" "python test_rnzb.py"
Benchmark 1: python test_nzb.py
  Time (mean ± σ):      3.848 s ±  0.023 s    [User: 3.561 s, System: 0.248 s]
  Range (min … max):    3.816 s …  3.885 s    10 runs

Benchmark 2: python test_rnzb.py
  Time (mean ± σ):     756.4 ms ±   3.5 ms    [User: 595.3 ms, System: 149.7 ms]
  Range (min … max):   749.0 ms … 761.8 ms    10 runs

Summary
  python test_rnzb.py ran
    5.09 ± 0.04 times faster than python test_nzb.py
```

The above benchmark was performed by looping over 10 random NZB files I had lying around, with the following code:

```console
$ cat test_nzb.py
from pathlib import Path
from nzb import Nzb

for p in Path.cwd().glob("*.nzb"):
    Nzb.from_file(p)

$ cat test_rnzb.py
from pathlib import Path
from rnzb import Nzb

for p in Path.cwd().glob("*.nzb"):
    Nzb.from_file(p)
```

This benchmark isn't super scientific, but it gives a pretty good idea of the performance difference.

## Supported platforms

Refer to the following table for the platforms and Python versions for which `rnzb` publishes prebuilt wheels:

| Platform                            | CPython 3.9-3.13 | CPython 3.13 (t) | PyPy 3.9-3.10 |
| ----------------------------------- | ---------------- | ---------------- | ------------- |
| 🐧 Linux (`x86_64`, `glibc>=2.28`)  | ✅               | ✅               | ✅            |
| 🐧 Linux (`x86_64`, `musl>=1.2`)    | ✅               | ✅               | ✅            |
| 🐧 Linux (`aarch64`, `glibc>=2.28`) | ✅               | ✅               | ✅            |
| 🐧 Linux (`aarch64`, `musl>=1.2`)   | ✅               | ✅               | ✅            |
| 🪟 Windows (`x86_64`)               | ✅               | ✅               | ✅            |
| 🍏 macOS (`x86_64`)                 | ✅               | ✅               | ✅            |
| 🍏 macOS (`arm64`)                  | ✅               | ✅               | ✅            |

The library itself is not inherently tied to any specific platform or Python version. The available wheels are based on what can be (reasonably) built using GitHub Actions.

## Building from source

Building from source requires the [Rust toolchain](https://rustup.rs/) and [Python 3.9+](https://www.python.org/downloads/).

- With [`uv`](https://docs.astral.sh/uv/):

  ```bash
  git clone https://github.com/Ravencentric/rnzb
  cd rnzb
  uv build
  ```

- With [`pypa/build`](https://github.com/pypa/build):

  ```bash
  git clone https://github.com/Ravencentric/rnzb
  cd rnzb
  python -m build
  ```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](https://github.com/Ravencentric/rnzb/blob/main/LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](https://github.com/Ravencentric/rnzb/blob/main/LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

## Contributing

Contributions are welcome! Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.
