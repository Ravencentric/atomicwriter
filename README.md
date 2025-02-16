# atomicwriter

Write files atomically.

```py
import atomicwriter

atomicwriter.write_text("hello world", "hello.txt")
```


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
