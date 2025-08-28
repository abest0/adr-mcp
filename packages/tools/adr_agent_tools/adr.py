import re
from importlib import resources
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field


class AdrData(BaseModel):
    number_prefix: Annotated[
        str, Field(description="The number prefix for the ADR document (e.g., '0001')")
    ]
    adr_directory: Annotated[str, Field(description="location where the adrs should be stored")]
    template: Annotated[
        str, Field(description="The ADR template content to be used for generating the document")
    ]


def setup_adr_directory(start_path: Path | str = ".") -> Path:
    """Find workspace root and ensure docs/adr directory exists."""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            adr_path = current / "docs" / "adr"
            adr_path.mkdir(parents=True, exist_ok=True)
            return adr_path
        current = current.parent
    raise FileNotFoundError("Git repository root not found")


def calculate_next_adr_number(adr_directory: Path) -> str:
    """Calculate the next ADR number based on existing files."""
    pattern = re.compile(r"^(\d{4})-.*\.md$")
    numbers = []

    for file_path in adr_directory.glob("*.md"):
        match = pattern.match(file_path.name)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers, default=0) + 1
    return f"{next_number:04d}"


def read_adr_template() -> str:
    return resources.read_text("adr_agent_tools.resources", "MADR_MINIMAL_TEMPLATE.md")
