from logging import Logger

from mcp.server.fastmcp import Context, FastMCP
from pydantic import AnyUrl

from ..adr import (
    ADR_AUTHORING_GUIDELINES,
    AdrData,
    calculate_next_adr_number,
    read_adr_template,
    setup_adr_directory,
)

log = Logger(__name__)

mcp = FastMCP(
    name="Adr",
    host="0.0.0.0",
    stateless_http=True,
)


@mcp.tool(
    description=(
        "Prepares metadata, MADR 3.0+ template, and authoring guidelines for recording an "
        "Architecture Decision Record (ADR) in docs/adr/ based on the conversation context."
    ),
)
async def adr(cwd: str, ctx: Context) -> AdrData:
    """Generate metadata and template for creating an Architecture Decision Record (ADR).

    Args:
        cwd: Current working directory to start searching for the git repository root

    Returns:
        AdrData: Metadata including next 4-digit number_prefix, adr_directory, index_file,
            MADR 3.0+ template, and authoring guidelines.
    """
    template_content = await ctx.read_resource(AnyUrl("template://MADR_MINIMAL_TEMPLATE"))
    content = template_content[0]
    template = content.content if hasattr(content, "content") else str(content)

    adr_directory = setup_adr_directory(cwd)
    number_prefix = calculate_next_adr_number(adr_directory)
    index_file = adr_directory / "README.md"
    return AdrData(
        number_prefix=number_prefix,
        adr_directory=str(adr_directory),
        index_file=str(index_file),
        template=template,
        guidelines=list(ADR_AUTHORING_GUIDELINES),
    )


@mcp.resource("template://MADR_MINIMAL_TEMPLATE")
def read_template() -> str:
    return read_adr_template()


if __name__ == "__main__":
    mcp.run()
