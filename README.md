# amplifier-bundle-lsp-rust

> **DEPRECATED — This bundle has been consolidated into
> [amplifier-bundle-rust-dev](https://github.com/microsoft/amplifier-bundle-rust-dev).**

This repository is now a **forwarding stub**. It transparently loads `rust-dev`
so existing configurations continue to work. A deprecation warning will appear on
session start to guide you through migration.

## Migration

Update your bundle includes:

```diff
- - bundle: git+https://github.com/microsoft/amplifier-bundle-lsp-rust@main
+ - bundle: git+https://github.com/microsoft/amplifier-bundle-rust-dev@main
```

## What Changed?

The `lsp-rust` bundle provided LSP/rust-analyzer support only. The new `rust-dev`
bundle includes everything `lsp-rust` had, plus:

- **Code quality tools** — cargo fmt, clippy, and cargo check integration
- **Automatic checking** — hooks that run on file write/edit
- **Stub detection** — identifies generated/derived code
- **Expert agent** — `rust-dev` agent with full Rust development knowledge

## Timeline

This forwarding stub will remain active for 2–3 months to allow migration.
After that, this repository will be archived.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
