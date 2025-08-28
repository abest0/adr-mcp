"""Hello unit test module."""

from adr_agent_tools.hello import hello


def test_hello():
    """Test the hello function."""
    assert hello() == "Hello adr_agent.tools"
