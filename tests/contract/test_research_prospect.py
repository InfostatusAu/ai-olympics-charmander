
import pytest
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from src.data_sources.linkedin_source import LinkedInSource
from src.data_sources.job_boards_source import JobBoardsSource

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

@pytest.mark.asyncio
async def test_linkedin_source_enhanced():
    """Test enhanced LinkedIn source functionality."""
    # Test without credentials (should use fallback)
    linkedin_source = LinkedInSource()
    
    result = await linkedin_source.research_company("TestCorp")
    
    assert result is not None
    assert result["company"] == "TestCorp"
    assert result["source"] == "linkedin"
    assert "status" in result
    
    # Clean up
    await linkedin_source.close()

@pytest.mark.asyncio
async def test_linkedin_source_with_firecrawl():
    """Test LinkedIn source with Firecrawl API key."""
    # Test with fake API key (should get authentication error)
    linkedin_source = LinkedInSource(firecrawl_api_key="fake_key")
    
    result = await linkedin_source.research_company("TestCorp")
    
    assert result is not None
    assert result["company"] == "TestCorp"
    assert result["source"] == "linkedin"
    
    # Clean up
    await linkedin_source.close()

@pytest.mark.asyncio 
async def test_linkedin_people_search():
    """Test LinkedIn people search functionality."""
    linkedin_source = LinkedInSource()
    
    result = await linkedin_source.search_people("TestCorp", ["Engineer", "Manager"])
    
    assert result is not None
    assert result["company"] == "TestCorp"
    assert result["source"] == "linkedin_people_search"
    assert "people" in result
    assert "search_metadata" in result
    
    # Clean up
    await linkedin_source.close()

@pytest.mark.asyncio
async def test_job_boards_source_basic():
    """Test basic job boards source functionality."""
    job_boards = JobBoardsSource()
    
    result = await job_boards.research_jobs("TestCorp")
    
    assert result is not None
    assert result["company"] == "TestCorp"
    assert result["source"] == "job_boards"
    assert "platform_results" in result
    assert "jobs" in result
    
    # Clean up
    await job_boards.close()

@pytest.mark.asyncio
async def test_job_boards_with_filters():
    """Test job boards search with title and platform filters."""
    job_boards = JobBoardsSource()
    
    result = await job_boards.research_jobs(
        "TestCorp", 
        job_titles=["Engineer", "Developer"],
        platforms=["indeed", "glassdoor"]
    )
    
    assert result is not None
    assert result["company"] == "TestCorp"
    assert result["search_criteria"]["job_titles"] == ["Engineer", "Developer"]
    assert len(result["search_criteria"]["platforms_searched"]) == 2
    
    # Clean up
    await job_boards.close()

@pytest.mark.asyncio
async def test_job_boards_culture_data():
    """Test company culture data collection."""
    job_boards = JobBoardsSource()
    
    result = await job_boards.get_company_culture_data("TestCorp")
    
    assert result is not None
    assert result["company"] == "TestCorp"
    assert result["source"] == "job_boards_culture" 
    assert "glassdoor_data" in result
    assert "indeed_data" in result
    
    # Clean up
    await job_boards.close()
