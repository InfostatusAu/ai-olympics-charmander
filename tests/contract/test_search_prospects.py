
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_search_prospects_contract():
    server_params = StdioServerParameters(command="non_existent_command")
    async with stdio_client(server_params) as session:
        result = await session.call_tool("search_prospects", {"query": "some query"})
        assert "error" not in result
        assert "prospects" in result
