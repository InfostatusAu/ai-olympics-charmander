
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_complete_workflow():
    server_params = StdioServerParameters(command="non_existent_command")
    async with stdio_client(server_params) as session:
        # Step 1: Research a prospect
        research_result = await session.call_tool("research_prospect", {"company": "TestCorp"})
        assert "error" not in research_result
        prospect_id = research_result["prospect_id"]

        # Step 2: Create a profile
        profile_result = await session.call_tool("create_profile", {"prospect_id": prospect_id})
        assert "error" not in profile_result
        assert "profile_markdown" in profile_result
