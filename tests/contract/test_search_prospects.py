
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_search_prospects_contract():
    """Test the search_prospects MCP tool contract."""
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
            assert "search_prospects" in tool_names
            
            # First create a prospect to have some data to search
            research_result = await session.call_tool("research_prospect", {"company": "TestCorp"})
            assert research_result is not None
            
            # Test search functionality
            result = await session.call_tool("search_prospects", {"query": "TestCorp"})
            assert result is not None
            assert len(result.content) > 0
            
            # Should return search results with Found count
            content_text = result.content[0].text
            assert "Found" in content_text or "search" in content_text.lower()
            
            # Test empty search
            empty_result = await session.call_tool("search_prospects", {"query": "NonExistentCompany123"})
            assert empty_result is not None
            assert len(empty_result.content) > 0
