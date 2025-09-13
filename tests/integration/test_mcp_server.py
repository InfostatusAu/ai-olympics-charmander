
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_mcp_server_tool_discovery():
    server_params = StdioServerParameters(command="non_existent_command")
    async with stdio_client(server_params) as session:
        tools = await session.list_tools()
        tool_names = [tool.name for tool in tools]
        assert "research_prospect" in tool_names
        assert "create_profile" in tool_names
        assert "get_prospect_data" in tool_names
        assert "search_prospects" in tool_names
