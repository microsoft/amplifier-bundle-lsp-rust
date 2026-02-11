"""Validate rust-lsp bundle composition."""

import yaml
from pathlib import Path


def deep_merge(base, overlay):
    result = base.copy()
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def test_rust_config_merges():
    """Rust language config merges into lsp-core's empty languages slot."""
    behavior = yaml.safe_load(
        (Path(__file__).parent.parent / "behaviors" / "rust-lsp.yaml").read_text()
    )
    rust_config = next(
        t["config"] for t in behavior["tools"] if t["module"] == "tool-lsp"
    )
    core_config = {"languages": {}, "timeout_seconds": 30}
    merged = deep_merge(core_config, rust_config)
    assert "rust" in merged["languages"]
    assert merged["languages"]["rust"]["extensions"] == [".rs"]
    assert merged["languages"]["rust"]["server"]["command"] == ["rust-analyzer"]
    assert merged["timeout_seconds"] == 30


def test_rust_server_config_complete():
    """Rust server config has all required fields."""
    behavior = yaml.safe_load(
        (Path(__file__).parent.parent / "behaviors" / "rust-lsp.yaml").read_text()
    )
    rust = next(t["config"] for t in behavior["tools"] if t["module"] == "tool-lsp")[
        "languages"
    ]["rust"]
    assert "extensions" in rust
    assert "workspace_markers" in rust
    assert "server" in rust
    assert "command" in rust["server"]
    assert "install_check" in rust["server"]
    assert "install_hint" in rust["server"]


def test_rust_capabilities_declared():
    """Rust bundle declares supported capabilities."""
    behavior = yaml.safe_load(
        (Path(__file__).parent.parent / "behaviors" / "rust-lsp.yaml").read_text()
    )
    caps = next(t["config"] for t in behavior["tools"] if t["module"] == "tool-lsp")[
        "languages"
    ]["rust"]["capabilities"]
    # typeHierarchy removed: rust-analyzer does not support prepareTypeHierarchy
    assert "typeHierarchy" not in caps
    assert caps.get("diagnostics") is True
    assert caps.get("rename") is True
    assert caps.get("codeAction") is True
    assert caps.get("inlayHints") is True
    assert caps.get("customRequest") is True


def test_bundle_metadata():
    """Root bundle has required metadata."""
    bundle = yaml.safe_load((Path(__file__).parent.parent / "bundle.yaml").read_text())
    assert bundle["bundle"]["name"] == "lsp-rust"
    assert "version" in bundle["bundle"]
    assert "description" in bundle["bundle"]


def test_agent_frontmatter():
    """Agent file has proper meta frontmatter."""
    content = (
        Path(__file__).parent.parent / "agents" / "rust-code-intel.md"
    ).read_text()
    parts = content.split("---", 2)
    assert len(parts) >= 3, "Agent must have YAML frontmatter between --- markers"
    meta = yaml.safe_load(parts[1])
    assert meta["meta"]["name"] == "rust-code-intel"
    assert "description" in meta["meta"]
    # Agent must declare tools for sub-session independence
    assert "tools" in meta
    assert any(t["module"] == "tool-lsp" for t in meta["tools"])


def test_all_yaml_valid():
    """All YAML files parse without error."""
    root = Path(__file__).parent.parent
    for yaml_file in root.rglob("*.yaml"):
        content = yaml.safe_load(yaml_file.read_text())
        assert content is not None, f"{yaml_file} is empty or invalid"


def test_agent_has_prerequisite_validation():
    """Agent includes prerequisite validation section before strategies."""
    content = (
        Path(__file__).parent.parent / "agents" / "rust-code-intel.md"
    ).read_text()

    # Section must exist
    assert "## Prerequisite Validation" in content, (
        "Agent must have a '## Prerequisite Validation' section"
    )

    # Must appear before the strategy sections
    prereq_pos = content.index("## Prerequisite Validation")
    strategies_pos = content.index("## Rust-Specific Strategies")
    assert prereq_pos < strategies_pos, (
        "Prerequisite Validation must appear before Rust-Specific Strategies"
    )

    # Must mention key validation steps
    assert (
        "rust-analyzer --version" in content
        or "rust-analyzer is not installed" in content
    ), "Must provide installation guidance"
    assert "expandMacro" in content, "Must mention custom extension checking"


def test_agent_description_mentions_validation():
    """Agent frontmatter description mentions prerequisite validation."""
    content = (
        Path(__file__).parent.parent / "agents" / "rust-code-intel.md"
    ).read_text()
    parts = content.split("---", 2)
    meta = yaml.safe_load(parts[1])
    description = meta["meta"]["description"]
    assert (
        "rust-analyzer" in description.lower() or "validates" in description.lower()
    ), "Description should mention rust-analyzer validation"
    assert "installation" in description.lower() or "install" in description.lower(), (
        "Description should mention installation guidance"
    )


def test_context_has_preflight_check():
    """Rust LSP context includes preflight check section."""
    content = (Path(__file__).parent.parent / "context" / "rust-lsp.md").read_text()

    assert "## Preflight Check" in content, (
        "Context must have a '## Preflight Check' section"
    )

    # Must appear early — after quick start table but before detailed sections
    preflight_pos = content.index("## Preflight Check")
    capabilities_pos = content.index("## Rust-Specific Capabilities")
    assert preflight_pos < capabilities_pos, (
        "Preflight Check must appear before Rust-Specific Capabilities"
    )

    assert "rust-analyzer --version" in content, (
        "Preflight section must include version check command"
    )
