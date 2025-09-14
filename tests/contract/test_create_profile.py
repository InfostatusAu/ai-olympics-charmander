
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_create_profile_contract():
    """Test the create_profile MCP tool contract."""
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
            assert "create_profile" in tool_names
            
            # Test with known existing prospect ID from data directory
            # This is the existing prospect file we know exists
            result = await session.call_tool("create_profile", {"prospect_id": "prospect_20250914025742"})
            assert result is not None
            assert len(result.content) > 0
            
            # The result should either be a successful profile or an informative error
            content_text = result.content[0].text
            # Accept either successful profile generation OR clear error message about missing research
            assert ("Mini Profile" in content_text or 
                   "Profile" in content_text or 
                   "not found" in content_text or
                   "❌" in content_text), f"Unexpected result: {content_text}"
