# Amplifier Rust LSP Bundle

**Rust code intelligence via rust-analyzer Language Server**

The Rust LSP Bundle provides pre-configured Rust language support for Amplifier's LSP capabilities, enabling semantic code navigation, type information, trait resolution, macro expansion, and intelligent code exploration for Rust projects.

## What Is This Bundle?

This bundle extends the core LSP bundle with Rust-specific configuration, allowing AI agents to:

- **Navigate Rust code** - Jump to definitions, find references, locate trait implementations
- **Understand types** - Get type information, hover documentation, inlay hints, and call hierarchies
- **Explore traits** - Navigate trait hierarchies with supertypes and subtypes
- **Expand macros** - See what declarative and procedural macros expand to
- **Refactor safely** - Rename symbols, apply code actions, extract functions
- **Check correctness** - Get compiler diagnostics and clippy lints
- **Use rust-analyzer** - Pre-configured with clippy, all features, proc macros, and build scripts

## Components

This bundle provides:

1. **rust-lsp** - Behavior configuring rust-analyzer as the Rust language server
2. **rust-code-intel** - Agent specialized for Rust code exploration
3. **rust-lsp** - Context providing Rust-specific LSP usage guidance

The bundle includes the core `lsp` bundle, which provides the `tool-lsp` module and general LSP capabilities.

## Prerequisites

rust-analyzer must be installed in your environment:

```bash
# Using rustup (recommended)
rustup component add rust-analyzer

# Verify installation
rust-analyzer --version
```

## Installation

### Using the Bundle

Load the bundle directly with Amplifier:

```bash
# Load from git URL
amplifier bundle use git+https://github.com/microsoft/amplifier-bundle-lsp-rust@main
```

### Including in Another Bundle

Add to your bundle's `includes:` section:

```yaml
includes:
  - bundle: lsp-rust
```

## Quick Start

### Basic Usage

```bash
# Start a session with Rust LSP capabilities
amplifier run --bundle lsp-rust

# Navigate Rust code
> Find all implementations of the Handler trait
> Go to the definition of process_request
> What type does this function return?
> Show me the call hierarchy for the execute method
```

### Example Queries

```bash
# Type information
> What type does get_connection() return?

# Trait implementations
> What types implement the Serialize trait in this project?

# References
> Where is the Config struct used in this workspace?

# Call hierarchy
> What functions call emit_event?
> What does the handle function call?

# Macro expansion
> What does this derive macro expand to?

# Diagnostics
> Check this file for errors and clippy warnings
```

## Configuration

The bundle comes pre-configured for Rust with rust-analyzer. The default configuration:

```yaml
tools:
  - module: tool-lsp
    config:
      languages:
        rust:
          extensions: [".rs"]
          server:
            command: ["rust-analyzer"]
          initialization_options:
            checkOnSave:
              command: clippy
            cargo:
              allFeatures: true
              buildScripts:
                enable: true
              allTargets: true
            procMacro:
              enable: true
```

### Customizing

Override the configuration in your behavior:

```yaml
tools:
  - module: tool-lsp
    config:
      languages:
        rust:
          initialization_options:
            checkOnSave:
              command: check  # Use cargo check instead of clippy
            cargo:
              allFeatures: false  # Only default features
```

## Available Operations

### Standard LSP Operations

| Operation | Description |
|-----------|-------------|
| `goToDefinition` | Find where a symbol is defined |
| `findReferences` | Find all references to a symbol |
| `hover` | Get documentation and type info |
| `documentSymbol` | List all symbols in a file |
| `workspaceSymbol` | Search for symbols across the workspace |
| `goToImplementation` | Find implementations of traits |
| `prepareCallHierarchy` | Get call hierarchy at a position |
| `incomingCalls` | Find callers of a function |
| `outgoingCalls` | Find functions called by a function |
| `supertypes` | Navigate type hierarchy upward |
| `subtypes` | Navigate type hierarchy downward |
| `diagnostics` | Get compiler errors and clippy warnings |
| `rename` | Safely rename a symbol across all references |
| `codeAction` | Get suggested fixes and refactorings |
| `inlayHints` | See inferred types, lifetimes, parameter names |

### rust-analyzer Extensions (via customRequest)

| Method | Description |
|--------|-------------|
| `rust-analyzer/expandMacro` | Expand a macro at cursor position |
| `rust-analyzer/relatedTests` | Find tests related to a function/struct |
| `experimental/externalDocs` | Get docs.rs or std library doc links |
| `experimental/runnables` | Find runnable targets (tests, bins, examples) |
| `rust-analyzer/fetchDependencyList` | List all crate dependencies |
| `experimental/ssr` | Structural search and replace |
| `rust-analyzer/viewRecursiveMemoryLayout` | Inspect memory layout of a type |

## Agent: rust-code-intel

The `rust-code-intel` agent is a Rust-specialized code intelligence specialist. **Delegate to it for**:

- Complex multi-step navigation (tracing trait implementations across crates)
- Type system questions (generic bounds, lifetime constraints)
- Macro expansion and proc macro debugging
- Module dependency mapping across a workspace
- When deep Rust expertise is needed alongside LSP operations

For simple single-operation lookups (quick hover, single goToDefinition), use tool-lsp directly.

## Multi-Language Composition

Combine with other language bundles for polyglot projects:

```yaml
# Your bundle.yaml
bundle:
  name: my-project
  version: 0.1.0

includes:
  - bundle: lsp-rust    # Rust support
  - bundle: lsp-python  # Python support
```

Both language configs deep-merge into the same tool-lsp instance, producing:
```yaml
languages:
  rust: { ... }    # From lsp-rust
  python: { ... }  # From lsp-python
```

## Bundle Structure

```
amplifier-bundle-lsp-rust/
  bundle.yaml           # Bundle definition, includes lsp
  behaviors/
    rust-lsp.yaml       # rust-analyzer configuration
  agents/
    rust-code-intel.md  # Rust-specialized agent
  context/
    rust-lsp.md         # Rust LSP usage guidance
```

## Troubleshooting

### "rust-analyzer not found"
```bash
rustup component add rust-analyzer
# Ensure ~/.cargo/bin is in your PATH
```

### Slow or Missing Results
rust-analyzer may still be indexing a large workspace. Wait for indexing to complete, or run `cargo check` to warm up.

### Proc Macro Errors
Run `cargo build` to compile proc macro crates. Check that the `target/` directory exists.

### Missing Cross-Crate References
Ensure the root `Cargo.toml` lists all workspace members and run `cargo check` to build the dependency graph.

## Philosophy

The Rust LSP Bundle follows Amplifier's core principles:

- **Composable** - Extends the core LSP bundle with Rust specifics
- **Pre-configured** - Works out of the box with rust-analyzer
- **Observable** - All operations emit events for logging and debugging
- **Minimal** - Adds only Rust-specific configuration

## Project Status

**EXPERIMENTAL EXPLORATION**

This is experimental software shared openly but without support infrastructure. See [SUPPORT.md](SUPPORT.md) for details.

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
