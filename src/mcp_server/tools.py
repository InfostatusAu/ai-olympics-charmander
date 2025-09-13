from mcp import mcp_tool
from src.database import operations as db_operations
from src.file_manager import storage as fm_storage
from src.prospect_research import research as pr_research
from src.prospect_research import profile as pr_profile
import uuid
import os

@mcp_tool("research_prospect")
async def research_prospect(company: str) -> str:
    """
    Researches a prospect company and generates a research markdown file.
    """
    try:
        # First, create a prospect entry in the database
        prospect = await db_operations.create_prospect(company_name=company, domain=f"{company.lower().replace(' ', '')}.com")
        
        # Then, perform the research and save the report
        research_result = await pr_research.research_prospect(str(prospect.id)) # Pass prospect_id as company_identifier
        
        # Update prospect status in DB
        await db_operations.update_prospect_status(prospect.id, db_operations.ProspectStatus.RESEARCHED)
        
        return f"Research for {company} completed. Prospect ID: {prospect.id}, Report: {research_result['report_filename']}"
    except Exception as e:
        return f"Error during research_prospect for {company}: {e}"

@mcp_tool("create_profile")
async def create_profile(prospect_id: str) -> str:
    """
    Creates a detailed prospect profile and conversation strategy based on research.
    """
    try:
        prospect_uuid = uuid.UUID(prospect_id)
        research_report_filename = f"{prospect_id}_research.md"
        profile_result = await pr_profile.create_profile(prospect_id, research_report_filename)
        
        # Update prospect status in DB
        await db_operations.update_prospect_status(prospect_uuid, db_operations.ProspectStatus.PROFILED)
        
        return f"Profile creation for {prospect_id} completed. Profile: {profile_result['profile_filename']}"
    except Exception as e:
        return f"Error during create_profile for {prospect_id}: {e}"

@mcp_tool("get_prospect_data")
async def get_prospect_data(prospect_id: str) -> str:
    """
    Retrieves complete prospect context, including research and profile.
    """
    try:
        prospect_uuid = uuid.UUID(prospect_id)
        prospect = await db_operations.get_prospect(prospect_uuid)
        if not prospect:
            return f"Prospect with ID {prospect_id} not found."

        research_filename = f"{prospect_id}_research.md"
        profile_filename = f"{prospect_id}_profile.md"

        research_content = ""
        profile_content = ""

        research_path = await fm_storage.get_prospect_report_path(prospect_id, research_filename)
        if os.path.exists(research_path):
            research_content = await fm_storage.read_markdown_file(research_path)

        profile_path = await fm_storage.get_prospect_report_path(prospect_id, profile_filename)
        if os.path.exists(profile_path):
            profile_content = await fm_storage.read_markdown_file(profile_path)

        return f"Prospect Data for {prospect_id}:\n\n" \
               f"Company Name: {prospect.company_name}\n" \
               f"Domain: {prospect.domain}\n" \
               f"Status: {prospect.status.name}\n\n" \
               f"--- Research Report ({research_filename}) ---\n{research_content}\n\n" \
               f"--- Profile Report ({profile_filename}) ---\n{profile_content}"
    except Exception as e:
        return f"Error during get_prospect_data for {prospect_id}: {e}"

@mcp_tool("search_prospects")
async def search_prospects(query: str) -> str:
    """
    Queries prospects with content search.
    """
    try:
        all_prospects = await db_operations.list_prospects()
        matching_prospects = []

        for prospect in all_prospects:
            prospect_id = str(prospect.id)
            research_filename = f"{prospect_id}_research.md"
            profile_filename = f"{prospect_id}_profile.md"

            research_content = ""
            profile_content = ""

            research_path = await fm_storage.get_prospect_report_path(prospect_id, research_filename)
            if os.path.exists(research_path):
                research_content = await fm_storage.read_markdown_file(research_path)

            profile_path = await fm_storage.get_prospect_report_path(prospect_id, profile_filename)
            if os.path.exists(profile_path):
                profile_content = await fm_storage.read_markdown_file(profile_path)

            if query.lower() in prospect.company_name.lower() or \
               query.lower() in prospect.domain.lower() or \
               query.lower() in research_content.lower() or \
               query.lower() in profile_content.lower():
                matching_prospects.append(f"- {prospect.company_name} (ID: {prospect_id}, Status: {prospect.status.name})")
        
        if matching_prospects:
            return "Found matching prospects:\n" + "\n".join(matching_prospects)
        else:
            return "No matching prospects found."
    except Exception as e:
        return f"Error during search_prospects for query '{query}': {e}"