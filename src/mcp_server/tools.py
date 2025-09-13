from mcp import mcp_tool
from src.database import operations as db_operations
from src.file_manager import storage as fm_storage
from src.prospect_research import research as pr_research
from src.prospect_research import profile as pr_profile

@mcp_tool("research_prospect")
async def research_prospect(company: str) -> str:
    """
    Researches a prospect company and generates a research markdown file.
    """
    # This will be implemented in detail later, for now, a placeholder.
    # It will likely call pr_research.perform_research and fm_storage.save_markdown
    return f"Research for {company} initiated."

@mcp_tool("create_profile")
async def create_profile(prospect_id: str) -> str:
    """
    Creates a detailed prospect profile and conversation strategy based on research.
    """
    # This will be implemented in detail later, for now, a placeholder.
    # It will likely call pr_profile.generate_profile and fm_storage.save_markdown
    return f"Profile creation for {prospect_id} initiated."

@mcp_tool("get_prospect_data")
async def get_prospect_data(prospect_id: str) -> str:
    """
    Retrieves complete prospect context, including research and profile.
    """
    # This will be implemented in detail later, for now, a placeholder.
    # It will likely call db_operations.get_prospect and fm_storage.load_markdown
    return f"Retrieving data for {prospect_id}."

@mcp_tool("search_prospects")
async def search_prospects(query: str) -> str:
    """
    Queries prospects with content search.
    """
    # This will be implemented in detail later, for now, a placeholder.
    # It will likely call db_operations.search_prospects and fm_storage.search_markdown
    return f"Searching prospects for query: {query}."
