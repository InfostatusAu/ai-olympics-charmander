
import pytest
import asyncio
import os
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

@pytest.mark.asyncio
async def test_markdown_file_generation():
    server_params = StdioServerParameters(command="non_existent_command")
    async with stdio_client(server_params) as session:
        # Step 1: Research a prospect
        research_result = await session.call_tool("research_prospect", {"company": "TestCorp"})
        assert "error" not in research_result
        prospect_id = research_result["prospect_id"]

        # Step 2: Check for the markdown file
        file_path = f"data/prospects/{prospect_id}_research.md"
        assert os.path.exists(file_path)
