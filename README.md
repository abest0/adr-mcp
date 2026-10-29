# adr-mcp

A lightweight Python Model Context Protocol (MCP) server and Agent Skill ([`SKILL.md`](SKILL.md)) that generates and manages **Architecture Decision Records (ADRs)** in the [MADR 3.0+](https://adr.github.io/madr/) format under `docs/adr/`.

## Features

- **Deterministic Scaffolding (`adr` MCP tool)**: Walks up from `cwd` to locate the `.git` repository root, ensures `docs/adr/` and `docs/adr/README.md` exist, calculates the next zero-padded 4-digit ADR number (`0001`, `0002`, ...), and returns the MADR 3.0+ template and authoring guidelines.
- **Enhanced MADR 3.0+ Template**: Includes metadata (`Status`, `Date`, `Deciders`), `Decision Drivers`, `Considered Options` with explicit rejection rationale, `Confirmation & Verification Strategy`, optional Mermaid `Architecture Diagram`, and `Consequences` (`Positive`, `Negative`, `Risks & Mitigations`).
- **Dual Mode (MCP Server + Agent Skill)**: Can be connected as an MCP server (`stdio` or `streamable-http`) or loaded directly as an Agent Skill via [`SKILL.md`](SKILL.md).

## Project Structure

```text
adr-mcp/
├── pyproject.toml                  # Single-package uv configuration
├── SKILL.md                        # Agent Skill instructions & workflow
├── adr_agent_tools/
│   ├── adr.py                      # Directory setup, numbering, index init, & template loader
│   ├── mcp_server/
│   │   ├── server.py               # FastMCP server & `adr` tool definition
│   │   ├── stdio.py                # Stdio transport entrypoint
│   │   └── http.py                 # Streamable HTTP transport entrypoint
│   └── resources/
│       └── MADR_MINIMAL_TEMPLATE.md
├── docs/adr/                       # Repository ADRs & README.md index table
└── tests/
    └── test_adr.py                 # Unit tests
```

## Quick Start

### Install & Sync Dependencies

```bash
uv sync
```

### Run the MCP Server

```bash
# Stdio transport
uv run adr-mcp-stdio
# or: uv run -m adr_agent_tools.mcp_server.stdio

# Streamable HTTP transport
uv run adr-mcp-http
# or: uv run -m adr_agent_tools.mcp_server.http
```

### Use as an Agent Skill

Symlink the repository into your agent skills directory:

```bash
ln -s /path/to/adr-mcp ~/.gemini/config/skills/adr-mcp
```

## Development

```bash
# Run tests with coverage
uv run pytest

# Lint and format check
uv run ruff check .
uv run ruff format --check .
```
