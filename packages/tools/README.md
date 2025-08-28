# ADR Agent Tools

A Python MCP (Model Context Protocol) server that automatically generates Architecture Decision Records (ADRs) in MADR format from conversation context.

## Features

- **Automated ADR Generation**: Creates structured decision records from conversation context
- **MADR Template Support**: Uses Markdown Architecture Decision Records format
- **Automatic Numbering**: Sequential ADR numbering with zero-padded prefixes
- **Multiple Transport Protocols**: HTTP, stdio, and WebSocket support
- **Template-based**: Built-in MADR minimal template for consistent formatting

## Installation

```bash
# Install dependencies
nx run adr_agent.tools:install

# Sync dependencies
nx run adr_agent.tools:sync
```

## Development Commands

### Core Targets

```bash
# Build the project (runs lint, compile, and test)
nx run adr_agent.tools:build

# Run tests with coverage
nx run adr_agent.tools:test

# Lint code with ruff
nx run adr_agent.tools:lint

# Compile/build the package
nx run adr_agent.tools:compile

# Format code
nx run adr_agent.tools:format
```

### MCP Server Targets

```bash
# Start MCP server with stdio transport
nx run adr_agent.tools:mcp-server-serve-stdio

# Start MCP server with HTTP transport
nx run adr_agent.tools:mcp-server-serve-http

# Inspect MCP server capabilities
nx run adr_agent.tools:mcp-server-inspect
```

### Additional Commands

```bash
# Add new dependencies
nx run adr_agent.tools:add

# Remove dependencies
nx run adr_agent.tools:remove

# Update dependencies
nx run adr_agent.tools:update

# Lock dependencies
nx run adr_agent.tools:lock
```

## Usage

The ADR agent tool provides a single `adr` function that generates architecture decision records based on conversation context. It automatically:

1. Determines the next ADR number by scanning existing ADR files
2. Creates the appropriate directory structure (`docs/adr/`)
3. Loads the MADR template
4. Returns structured data for ADR generation

## Project Structure

```
adr_agent_tools/
├── __init__.py
├── adr.py                 # Core ADR generation logic
├── mcp_server/           # MCP server implementations
│   ├── __init__.py
│   ├── server.py         # Base server functionality
│   ├── stdio.py          # Stdio transport
│   └── http.py           # HTTP transport
└── resources/            # Template files
    └── MADR_MINIMAL_TEMPLATE.md
```

## Testing

Tests are located in the `tests/` directory and use pytest with coverage reporting:

```bash
# Run tests
nx run adr_agent.tools:test
```

Coverage reports are generated in `../../coverage/packages/tools/` and test reports in `../../reports/packages/tools/`.
