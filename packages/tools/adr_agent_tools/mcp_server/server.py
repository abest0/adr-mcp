from logging import Logger

from mcp.server.fastmcp import Context, FastMCP
from pydantic import AnyUrl

from ..adr import AdrData, calculate_next_adr_number, read_adr_template, setup_adr_directory

log = Logger(__name__)

mcp = FastMCP(
    name="Adr",
    host="0.0.0.0",
    stateless_http=True,
)


@mcp.tool(
    description="Generates an ADR based on the context of the conversation",
)
async def adr(cwd: str, ctx: Context) -> AdrData:
    """Generate metadata for creating an ADR(Architectural Decision Record)

    Args:
        cwd: Current working directory to start searching for git repository root

    Returns:
        AdrData: A package with instructions for the ADR that should be generated
    """

    template_content = await ctx.read_resource(AnyUrl("template://MADR_MINIMAL_TEMPLATE"))
    content = template_content[0]  # noqa: E501
    template = content.content if hasattr(content, "content") else str(content)

    adr_directory = setup_adr_directory(cwd)
    number_prefix = calculate_next_adr_number(adr_directory)
    res = AdrData(number_prefix=number_prefix, adr_directory=str(adr_directory), template=template)
    return res


@mcp.resource("template://MADR_MINIMAL_TEMPLATE")
def read_template() -> str:
    return read_adr_template()


if __name__ == "__main__":
    mcp.run()
