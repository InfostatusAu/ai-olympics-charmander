
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_research_prospect_contract():
    server_params = StdioServerParameters(command="non_existent_command")
    async with stdio_client(server_params) as session:
        result = await session.call_tool("research_prospect", {"company": "TestCorp"})
        assert "error" not in result
        assert "prospect_id" in result
