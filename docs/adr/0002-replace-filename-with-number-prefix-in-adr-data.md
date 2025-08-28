# Replace file_name with number_prefix in AdrData class

## Context and Problem Statement

The ADR generation tool was returning a static filename "some-file.md" which didn't provide useful information about the ADR numbering sequence. Users needed a way to automatically calculate the next ADR number based on existing ADR files in the directory, following the standard NNNN-title.md naming convention.

## Considered Options

* Keep the existing file_name property and manually manage ADR numbering
* Replace file_name with a calculated number_prefix that automatically determines the next ADR number
* Add both file_name and number_prefix properties to maintain backward compatibility

## Decision Outcome

Chosen option: "Replace file_name with a calculated number_prefix", because it provides automatic ADR numbering, eliminates manual tracking of ADR sequences, and ensures consistent four-digit zero-padded numbering format.

### Consequences

* Good, because ADR numbering is now automated and consistent
* Good, because it prevents duplicate ADR numbers
* Good, because it follows the standard NNNN-title.md naming convention
* Bad, because it breaks backward compatibility with existing code that expects file_name property
