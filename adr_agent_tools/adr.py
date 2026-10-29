import re
from importlib import resources
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field

ADR_INDEX_HEADER = """# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
"""

ADR_AUTHORING_GUIDELINES = [
    (
        "1. Pre-Research: Check existing ADRs in docs/adr/ to ensure consistency and avoid "
        "conflicts."
    ),
    (
        "2. Format: Place '# NNNN: [Short Title]' on line 1. Include at least 2 viable options "
        "with balanced 'Good, because...' / 'Bad, because...' and 'Why Rejected' rationale."
    ),
    (
        "3. Verification: Populate the 'Confirmation & Verification Strategy' section with "
        "concrete tests, lint rules, or module boundary checks."
    ),
    (
        "4. Human Confirmation: Present the draft ADR summary and target file path to the user "
        "for confirmation before writing (unless prior consent was given)."
    ),
    (
        "5. Index Update: Write 'docs/adr/{number_prefix}-<slug>.md' and append a row "
        "'| [{number_prefix}]({number_prefix}-<slug>.md) | <Title> | <Status> | YYYY-MM-DD |' "
        "to 'docs/adr/README.md'."
    ),
]


class AdrData(BaseModel):
    number_prefix: Annotated[
        str, Field(description="The number prefix for the ADR document (e.g., '0001')")
    ]
    adr_directory: Annotated[
        str, Field(description="Directory path where the ADR files are stored (docs/adr)")
    ]
    index_file: Annotated[
        str,
        Field(description="Path to the ADR index file (docs/adr/README.md) to update in lockstep"),
    ]
    template: Annotated[
        str,
        Field(description="The MADR 3.0+ template content to use for generating the document"),
    ]
    guidelines: Annotated[
        list[str],
        Field(
            default_factory=lambda: list(ADR_AUTHORING_GUIDELINES),
            description=(
                "Workflow steps for researching, drafting, confirming, and indexing the ADR"
            ),
        ),
    ]


def setup_adr_directory(start_path: Path | str = ".") -> Path:
    """Find workspace git root and ensure docs/adr directory and README.md index exist."""
    current = Path(start_path).resolve()
    while True:
        if (current / ".git").exists():
            adr_path = current / "docs" / "adr"
            adr_path.mkdir(parents=True, exist_ok=True)
            index_path = adr_path / "README.md"
            if not index_path.exists():
                index_path.write_text(ADR_INDEX_HEADER, encoding="utf-8")
            return adr_path
        if current == current.parent:
            break
        current = current.parent
    raise FileNotFoundError("Git repository root not found")


def calculate_next_adr_number(adr_directory: Path) -> str:
    """Calculate the next zero-padded 4-digit ADR number based on existing files."""
    pattern = re.compile(r"^(\d{4})-.*\.md$")
    numbers = []

    for file_path in adr_directory.glob("*.md"):
        match = pattern.match(file_path.name)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers, default=0) + 1
    return f"{next_number:04d}"


def read_adr_template() -> str:
    """Read the bundled MADR 3.0+ template from package resources."""
    return (
        resources.files("adr_agent_tools.resources")
        .joinpath("MADR_MINIMAL_TEMPLATE.md")
        .read_text(encoding="utf-8")
    )
