
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_research_prospect_contract():
    """Test the research_prospect MCP tool contract."""
    server_params = StdioServerParameters(
        command="python", 
        args=["-m", "src.mcp_server.server"]
    )
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            await session.initialize()
            
            # Test tool discovery
            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            assert "research_prospect" in tool_names
            
            # Test tool execution
            result = await session.call_tool("research_prospect", {"company": "TestCorp"})
            assert result is not None
            assert len(result.content) > 0
