# Rust LSP Context

You have access to Rust code intelligence via the LSP tool with rust-analyzer.

## Quick Start - Most Useful Operations

| Want to... | Use this |
|------------|----------|
| See type of a variable | `hover` on the variable |
| Find all usages of a symbol | `findReferences` on the symbol |
| Jump to a definition | `goToDefinition` on a call site or use statement |
| Find trait implementors | `goToImplementation` on a trait name |
| See what calls a function | `incomingCalls` on the function |
| See what a function calls | `outgoingCalls` on the function |
| Navigate trait hierarchy up | `supertypes` on a trait or type |
| Navigate trait hierarchy down | `subtypes` on a trait or type |
| List symbols in a file | `documentSymbol` on the file |
| Search symbols across workspace | `workspaceSymbol` with a query |
| Check for errors | `diagnostics` on a file |
| Rename a symbol safely | `rename` on the symbol |
| Get suggested fixes | `codeAction` at a diagnostic location |
| See inferred types in bulk | `inlayHints` on a range |
| Expand a macro | `customRequest` with `rust-analyzer/expandMacro` |
| Find related tests | `customRequest` with `rust-analyzer/relatedTests` |

**Tip**: `hover` and `goToImplementation` are the most powerful starting points for Rust. Start with these.

## Rust-Specific Capabilities

- **Trait Resolution**: Navigate trait hierarchies with `goToImplementation`, `supertypes`, and `subtypes`
- **Macro Expansion**: See what macros expand to via `customRequest` with `rust-analyzer/expandMacro`
- **Cargo Workspace**: Understands multi-crate workspaces, cross-crate references
- **Clippy Integration**: Diagnostics include clippy lints alongside compiler errors
- **Lifetime/Borrow Info**: Inlay hints show lifetime annotations and borrow information
- **Proc Macro Support**: Analyzes proc macro expansions when crates are compiled

## When to Use LSP vs grep

| Task | Use LSP | Use grep |
|------|---------|----------|
| Find where a function is defined | `goToDefinition` (precise) | May match comments/strings |
| Find all callers of a function | `incomingCalls` (semantic) | Matches text, not calls |
| Get type of a variable | `hover` (inferred types) | Cannot do this |
| Find trait implementors | `goToImplementation` (precise) | Unreliable with generics |
| Search for text pattern | Too specific | `grep` (fast, broad) |
| Find files by name | Not applicable | `glob` (fast) |
| Rename a symbol safely | `rename` (all references) | May miss or over-match |
| Check for compiler errors | `diagnostics` (real errors) | Cannot do this |
| Expand a macro | `customRequest` | Cannot do this |

**Rule**: Use LSP for semantic code understanding (types, references, call chains, implementations). Use grep for text pattern matching.

## When to Delegate to rust-code-intel

For simple single-operation lookups, use tool-lsp directly. **Delegate to `rust-code-intel` for**:
- Complex multi-step navigation ("trace all implementations of this trait across crates")
- Type system questions ("what trait bounds constrain this generic?")
- Macro debugging ("what does this derive macro generate?")
- Module dependency mapping across a workspace
- When deep Rust expertise is needed alongside LSP operations

## customRequest Quick Reference (rust-analyzer Extensions)

| Method | Description |
|--------|-------------|
| `rust-analyzer/expandMacro` | Expand a macro at cursor position |
| `rust-analyzer/relatedTests` | Find tests related to a function/struct |
| `experimental/externalDocs` | Get docs.rs or std library doc links |
| `experimental/runnables` | Find runnable targets (tests, bins, examples) |
| `rust-analyzer/fetchDependencyList` | List all crate dependencies |
| `experimental/ssr` | Structural search and replace |
| `rust-analyzer/viewRecursiveMemoryLayout` | Inspect memory layout of a type |

## Workspace Detection

The Rust LSP detects workspace root by looking for:
- Cargo.toml (preferred)
- Cargo.lock
- .git directory

Ensure your project has a `Cargo.toml` at the root for accurate analysis. For Cargo workspaces, rust-analyzer reads the workspace `Cargo.toml` and understands all member crates.

## Installation

rust-analyzer is installed via rustup:

```bash
rustup component add rust-analyzer
```

Verify installation:
```bash
rust-analyzer --version
```

## Known Limitations

### workspaceSymbol May Return Empty Initially
Large Cargo workspaces need time for rust-analyzer to index:
- **Workaround**: Run `documentSymbol` on relevant files first, wait 2-3 seconds, then retry `workspaceSymbol`.

### Proc Macro Expansion Requires Build
Proc macro crates must be compiled before rust-analyzer can expand them:
- **Workaround**: Run `cargo build` or `cargo check` to compile proc macro crates. Check that `target/` exists.

### Slow Initial Indexing on Large Workspaces
Very large Cargo workspaces may take time for initial indexing:
- **Workaround**: Wait for rust-analyzer to finish loading. First operations may be slow; subsequent ones will be fast.

### Build Script Output
Code generated by `build.rs` requires the `target/` directory:
- **Workaround**: Run `cargo check` to generate build script output before using LSP on generated types.

## Troubleshooting

### "rust-analyzer not found"
1. **Check**: `rust-analyzer --version`
2. **Install**: `rustup component add rust-analyzer`
3. **Verify**: Ensure `~/.cargo/bin` is in your PATH

### Slow or Missing Results
1. **Check**: rust-analyzer may still be indexing (check `diagnostics` output)
2. **Fix**: Wait for indexing to complete, or run `cargo check` to warm up
3. **Verify**: `documentSymbol` returns results on known files

### Proc Macro Errors
1. **Check**: `cargo build` succeeds for proc macro crates
2. **Fix**: Ensure `target/` directory exists and is current
3. **Verify**: `hover` on derived items shows expanded types

### Missing Cross-Crate References
1. **Check**: Root `Cargo.toml` lists all workspace members
2. **Fix**: Ensure all crates are part of the workspace
3. **Verify**: `goToDefinition` navigates across crate boundaries
