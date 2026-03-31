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

## Contributing

> [!NOTE]
> This project is not currently accepting external contributions, but we're actively working toward opening this up. We value community input and look forward to collaborating in the future. For now, feel free to fork and experiment!

Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
