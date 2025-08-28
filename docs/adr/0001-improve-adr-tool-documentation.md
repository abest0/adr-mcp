# Improve ADR Tool Documentation with Field Descriptions and Clear Parameter Documentation

## Context and Problem Statement

The ADR tool in the MCP server lacked clear documentation about its parameters and return types. The `cwd` parameter purpose was unclear, and the `AdrData` model fields had no descriptions, making it difficult for users to understand what the tool does and how to use it effectively.

## Considered Options

* Leave documentation as minimal docstrings only
* Add comprehensive Field descriptions and parameter documentation
* Create external documentation files instead of inline documentation

## Decision Outcome

Chosen option: "Add comprehensive Field descriptions and parameter documentation", because it provides immediate clarity for developers using the tool, follows Python best practices with pydantic Field descriptions, and keeps documentation close to the code for maintainability.

### Consequences

* Good, because developers can immediately understand the purpose of each parameter and return field
* Good, because pydantic Field descriptions provide automatic API documentation
* Good, because the documentation is maintainable alongside the code
* Bad, because it adds slight verbosity to the codebase
