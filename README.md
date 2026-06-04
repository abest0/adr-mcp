# ADR MCP Server

This repo contains a Python MCP server that helps agents create Architecture
Decision Records in MADR format.

The server exposes one MCP tool: `adr`. Given a working directory, it finds the
git repository root, ensures `docs/adr/` exists, calculates the next four-digit
ADR number, and returns the MADR template content.

It does not write the final ADR markdown file. The calling agent uses the
returned metadata to create something like `docs/adr/0004-use-postgres.md`.

## Requirements

- `uv`
- Python 3.12 or newer
- This repo available at a stable path, for example:

```sh
/home/dev/code/adr-mcp
```

The examples below assume that path. If you clone the repo somewhere else,
replace `/home/dev/code/adr-mcp` in the config snippets.

## Run Locally

The stdio MCP server is launched with:

```sh
uv run --directory /home/dev/code/adr-mcp -m adr_agent_tools.mcp_server.stdio
```

For direct development, the Nx target does the same thing:

```sh
pnpm exec nx run adr_agent.tools:mcp-server-serve-stdio
```

## Claude Code Setup

Claude Code can load this as a user-level MCP server from
`~/.claude/.mcp.json`.

```json
{
  "mcpServers": {
    "adr": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/dev/code/adr-mcp",
        "-m",
        "adr_agent_tools.mcp_server.stdio"
      ]
    }
  }
}
```

Restart Claude Code after changing the file. In Claude, run `/mcp` and confirm
the `adr` server is connected.

## Codex Setup

Codex loads MCP servers from `~/.codex/config.toml`.

```toml
[mcp_servers.adr]
command = "uv"
args = ["run", "--directory", "/home/dev/code/adr-mcp", "-m", "adr_agent_tools.mcp_server.stdio"]
```

Verify Codex sees the server:

```sh
codex mcp list
```

Expected result: an `adr` entry with `Status` set to `enabled`.

## Validate The Tool

Create a disposable git repo:

```sh
mkdir -p /home/dev/code/adr-mcp-validation
git -C /home/dev/code/adr-mcp-validation init
```

Ask Claude or Codex to use the ADR tool from that repo. The tool should return:

- `number_prefix`: `0001`
- `adr_directory`: `/home/dev/code/adr-mcp-validation/docs/adr`
- `template`: the MADR markdown template

It should also create the directory:

```sh
/home/dev/code/adr-mcp-validation/docs/adr
```

The tool will not create `0001-*.md` by itself. The agent should write that file
using the returned number, directory, and template.

## Development

Package source lives in:

```sh
packages/tools/adr_agent_tools
```

Useful commands:

```sh
pnpm exec nx run adr_agent.tools:test
pnpm exec nx run adr_agent.tools:lint
pnpm exec nx run adr_agent.tools:format
pnpm exec nx run adr_agent.tools:build
```

The MCP entrypoints are:

```sh
python -m adr_agent_tools.mcp_server.stdio
python -m adr_agent_tools.mcp_server.http
```
