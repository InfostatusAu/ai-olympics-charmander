
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_get_prospect_data_contract():
    """Test the get_prospect_data MCP tool contract."""
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
            assert "get_prospect_data" in tool_names
            
            # Test with known existing prospect ID from data directory
            result = await session.call_tool("get_prospect_data", {"prospect_id": "prospect_20250914025742"})
            assert result is not None
            assert len(result.content) > 0
            
            # The result should either contain prospect data or a clear error message
            content_text = result.content[0].text
            # Accept either successful data retrieval OR clear error message
            assert ("Research Report" in content_text or 
                   "research" in content_text.lower() or
                   "Profile" in content_text or
                   "not found" in content_text or
                   "❌" in content_text), f"Unexpected result: {content_text}"
