import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_mcp_server_tool_discovery():
    server_params = StdioServerParameters(command="non_existent_command")
    async with stdio_client(server_params) as session:
        tools = await session.list_tools()
        tool_names = {tool.name for tool in tools}

        expected_tools = {
            "research_prospect",
            "create_profile",
            "get_prospect_data",
            "search_prospects",
        }

        assert expected_tools.issubset(tool_names)