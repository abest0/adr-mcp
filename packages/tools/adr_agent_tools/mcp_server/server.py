import re
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(
    name="Adr",
    host="0.0.0.0",
    stateless_http=True,
)


TEMPLATE = """
# {short title, representative of solved problem and found solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story. You may want to articulate the problem in form of a question and add links to collaboration boards or issue management systems.}

## Considered Options

* {title of option 1}
* {title of option 2}
* {title of option 3}
* … <!-- numbers of options can vary -->

## Decision Outcome

Chosen option: "{title of option 1}", because {justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

<!-- This is an optional element. Feel free to remove. -->
### Consequences

* Good, because {positive consequence, e.g., improvement of one or more desired qualities, …}
* Bad, because {negative consequence, e.g., compromising one or more desired qualities, …}
* … <!-- numbers of consequences can vary -->
"""  # noqa: E501


def setup_adr_directory(start_path: Path | str = "."):
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


class AdrData(BaseModel):
    number_prefix: str = Field(
        description="The number prefix for the ADR document (e.g., '0001')"
    )
    template: str = Field(
        description="The ADR template content to be used for generating the document"
    )


@mcp.tool(description="Generates an ADR based on the context of the conversation",)
async def adr(cwd: str, ctx: Context) -> AdrData:
    """Generate an ADR

    Args:
        cwd: Current working directory to start searching for git repository root

    Returns:
        AdrData: A package with instructions for the ADR that should be generated
    """

    await ctx.info('Oh snap my neezy, we really in here')
    print ('HEEEEEEEEEEEEEERRRRRRRRRRRRRE')
    ctx.s



    adr_directory = setup_adr_directory(cwd)
    number_prefix = calculate_next_adr_number(adr_directory)
    res = AdrData(number_prefix=number_prefix, template=TEMPLATE)
    return res
