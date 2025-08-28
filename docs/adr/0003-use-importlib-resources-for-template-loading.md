# Use importlib.resources for Template Loading

## Context and Problem Statement

The ADR agent MCP server needed to load template files from the package resources. The initial implementation used relative path navigation with `Path("../../resources/MADR_MINIMAL_TEMPLATE.md")` which was fragile and dependent on the current working directory. This approach failed when the working directory changed and created maintenance issues with hardcoded relative paths.

## Considered Options

* Use relative paths with `Path(__file__).parent.parent.parent`
* Use `importlib.resources` for package resource access
* Define a constant at module level for the project root
* Search for project root by looking for marker files

## Decision Outcome

Chosen option: "Use importlib.resources for package resource access", because it's the most pythonic approach for accessing package resources, is independent of working directory, and provides a clean API specifically designed for this use case.

### Consequences

* Good, because it eliminates dependency on current working directory
* Good, because it follows Python packaging best practices
* Good, because it's more maintainable than hardcoded relative paths
* Good, because it works correctly when the package is installed via pip
* Bad, because it requires the resources to be properly packaged as part of the Python package
