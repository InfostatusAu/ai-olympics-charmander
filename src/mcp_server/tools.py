"""
MCP Tools Implementation for Prospect Research.
Implements the 4 core MCP tools as standalone async functions.
"""

from src.database import operations as db_operations
from src.database.models import ProspectStatus
from src.file_manager import storage as fm_storage
from src.prospect_research import research as pr_research
from src.prospect_research import profile as pr_profile
import uuid
import os

async def research_prospect(company: str) -> str:
    """
    Researches a prospect company and generates a research markdown file.
    Integrates with enhanced research logic that uses real data sources.
    """
    try:
        # Generate a unique prospect ID
        prospect_id = str(uuid.uuid4())
        
        # First, create a prospect entry in the database using the default session functions
        prospect = await db_operations.create_prospect_default(
            prospect_id=prospect_id,
            company_name=company, 
            domain=f"{company.lower().replace(' ', '').replace('&', 'and')}.com"
        )
        
        # Perform the research using the company name (not prospect ID)
        # The research function will generate its own prospect ID for file naming
        research_result = await pr_research.research_prospect(company)
        
        # Update prospect status in DB
        await db_operations.update_prospect_status_default(prospect.id, ProspectStatus.RESEARCHED)
        
        # Return detailed result with data sources used
        data_sources = research_result.get('data_sources_used', [])
        return f"✅ Research completed for {company}\n" \
               f"📊 Prospect ID: {prospect.id}\n" \
               f"📄 Report: {research_result['report_filename']}\n" \
               f"🔍 Data sources: {', '.join(data_sources)}\n" \
               f"💼 Database Status: RESEARCHED"
        
    except Exception as e:
        return f"❌ Error during research_prospect for {company}: {str(e)}"

async def create_profile(prospect_id: str) -> str:
    """
    Creates a detailed prospect profile and conversation strategy based on research.
    Transforms the research markdown into structured profile with outreach strategy.
    """
    try:
        # Try UUID validation first, but allow both UUID and timestamp-based IDs
        is_uuid = False
        try:
            prospect_uuid = uuid.UUID(prospect_id)
            is_uuid = True
        except ValueError:
            # Not a UUID, might be a timestamp-based ID - allow it
            pass
        
        if is_uuid:
            # Verify prospect exists in database
            prospect = await db_operations.get_prospect_default(prospect_id)
            if not prospect:
                return f"❌ Prospect with ID {prospect_id} not found in database"
            
            # Check if research has been completed
            if prospect.status != ProspectStatus.RESEARCHED:
                return f"❌ Prospect {prospect_id} must be researched first. Current status: {prospect.status.name}"
            
            # Find matching research file for this prospect
            import glob
            import os
            
            research_files = glob.glob(f"data/prospects/prospect_*/prospect_*_research.md")
            if not research_files:
                return f"❌ No research files found. Please run research_prospect first."
            
            # Find the most recent research file by modification time
            research_files.sort(key=os.path.getmtime, reverse=True)
            research_file_path = research_files[0]
            research_filename = os.path.basename(research_file_path)
            
            # Extract the research prospect_id from the filename for profile creation
            research_prospect_id = research_filename.replace("_research.md", "")
            
            # Create the profile using the research prospect ID and research filename
            profile_result = await pr_profile.create_profile(research_prospect_id, research_filename)
            
            # Update prospect status in DB
            await db_operations.update_prospect_status_default(prospect_id, ProspectStatus.PROFILED)
            
            return f"✅ Profile created for {prospect.company_name}\n" \
                   f"📊 Prospect ID: {prospect_id}\n" \
                   f"📄 Profile: {profile_result['profile_filename']}\n" \
                   f"🎯 Strategy: {profile_result.get('strategy_summary', 'Conversation strategy included')}\n" \
                   f"💼 Database Status: PROFILED"
        else:
            # Handle timestamp-based prospect ID directly (from research_prospect tool output)
            research_filename = f"{prospect_id}_research.md"
            
            # Check if research file exists
            import os
            research_file_path = f"data/prospects/{prospect_id}/{research_filename}"
            if not os.path.exists(research_file_path):
                return f"❌ Research file not found at {research_file_path}. Please run research_prospect first."
            
            # Create the profile using the research prospect ID and research filename
            profile_result = await pr_profile.create_profile(prospect_id, research_filename)
            
            return f"✅ Profile created for {prospect_id}\n" \
                   f"📄 Profile: {profile_result['profile_filename']}\n" \
                   f"🎯 Strategy: {profile_result.get('strategy_summary', 'Conversation strategy included')}\n" \
                   f"💡 Use this prospect_id: {prospect_id} for future operations"
               
    except Exception as e:
        return f"❌ Error during create_profile for {prospect_id}: {str(e)}"

async def get_prospect_data(prospect_id: str) -> str:
    """
    Retrieves complete prospect context, including research and profile.
    Returns comprehensive prospect intelligence in markdown format.
    """
    try:
        # Try UUID validation first, but allow both UUID and timestamp-based IDs
        is_uuid = False
        try:
            prospect_uuid = uuid.UUID(prospect_id)
            is_uuid = True
        except ValueError:
            # Not a UUID, might be a timestamp-based ID - allow it
            pass
        
        if is_uuid:
            # Handle database prospect with UUID
            prospect = await db_operations.get_prospect_default(prospect_id)
            if not prospect:
                return f"❌ Prospect with ID {prospect_id} not found."

            # Build comprehensive prospect data response
            result_parts = [
                f"# 📊 Prospect Data Summary",
                f"",
                f"**Prospect ID**: {prospect_id}",
                f"**Company Name**: {prospect.company_name}",
                f"**Domain**: {prospect.domain}",
                f"**Status**: {prospect.status.name}",
                f"**Created**: {prospect.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"**Updated**: {prospect.updated_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f""
            ]

            # Find and include research content (use latest research file)
            import glob
            research_files = glob.glob(f"data/prospects/prospect_*_research.md")
            
        else:
            # Handle timestamp-based prospect ID directly
            result_parts = [
                f"# 📊 Prospect Data Summary",
                f"",
                f"**Prospect ID**: {prospect_id}",
                f"**Type**: Research-generated prospect",
                f"**Data Location**: data/prospects/{prospect_id}/",
                f""
            ]

            # Find research and profile files for this timestamp-based ID
            import glob
            research_files = glob.glob(f"data/prospects/{prospect_id}/{prospect_id}_research.md")
        
        # Find and include research content
        if research_files:
            research_files.sort(key=os.path.getmtime, reverse=True)
            research_path = research_files[0]
            research_filename = os.path.basename(research_path)
            
            try:
                research_content = await fm_storage.read_markdown_file(research_path)
                result_parts.extend([
                    f"## 🔍 Research Report",
                    f"**File**: {research_filename}",
                    f"",
                    research_content,
                    f""
                ])
            except Exception as e:
                result_parts.extend([
                    f"## 🔍 Research Report",
                    f"**File**: {research_filename}",
                    f"❌ Error reading research file: {str(e)}",
                    f""
                ])
        else:
            result_parts.extend([
                f"## 🔍 Research Report",
                f"❌ No research file found for prospect {prospect_id}",
                f""
            ])

        # Find and include profile content
        if is_uuid:
            profile_files = glob.glob(f"data/prospects/prospect_*_profile.md")
        else:
            profile_files = glob.glob(f"data/prospects/{prospect_id}/{prospect_id}_profile.md")
            
        if profile_files:
            profile_files.sort(key=os.path.getmtime, reverse=True)
            profile_path = profile_files[0]
            profile_filename = os.path.basename(profile_path)
            
            try:
                profile_content = await fm_storage.read_markdown_file(profile_path)
                result_parts.extend([
                    f"## 🎯 Prospect Profile",
                    f"**File**: {profile_filename}",
                    f"",
                    profile_content,
                    f""
                ])
            except Exception as e:
                result_parts.extend([
                    f"## 🎯 Prospect Profile", 
                    f"**File**: {profile_filename}",
                    f"❌ Error reading profile file: {str(e)}",
                    f""
                ])
        else:
            result_parts.extend([
                f"## 🎯 Prospect Profile", 
                f"⏳ Profile not yet created. Run create_profile to generate.",
                f""
            ])

        return "\n".join(result_parts)
        
    except Exception as e:
        return f"❌ Error during get_prospect_data for {prospect_id}: {str(e)}"

async def search_prospects(query: str) -> str:
    """
    Queries prospects with content search across research and profile files.
    Searches company names, domains, and markdown file content.
    """
    try:
        if not query or len(query.strip()) < 2:
            return "❌ Search query must be at least 2 characters long"
        
        query_lower = query.lower()
        all_prospects = await db_operations.list_prospects_default()
        matching_prospects = []

        for prospect in all_prospects:
            prospect_id = str(prospect.id)
            match_details = []
            
            # Check company name and domain
            if query_lower in prospect.company_name.lower():
                match_details.append("Company Name")
            if query_lower in prospect.domain.lower():
                match_details.append("Domain")

            # Search research content
            import glob
            research_files = glob.glob(f"data/prospects/*{prospect_id}*research.md")
            if not research_files:
                research_files = glob.glob(f"data/prospects/prospect_*_research.md")
            
            if research_files:
                research_files.sort(key=os.path.getmtime, reverse=True)
                try:
                    research_content = await fm_storage.read_markdown_file(research_files[0])
                    if query_lower in research_content.lower():
                        match_details.append("Research Content")
                except Exception:
                    pass

            # Search profile content
            profile_files = glob.glob(f"data/prospects/*{prospect_id}*profile.md")
            if profile_files:
                profile_files.sort(key=os.path.getmtime, reverse=True)
                try:
                    profile_content = await fm_storage.read_markdown_file(profile_files[0])
                    if query_lower in profile_content.lower():
                        match_details.append("Profile Content")
                except Exception:
                    pass

            # If any matches found, add to results
            if match_details:
                match_summary = f"**{prospect.company_name}**"
                match_summary += f"\n  📊 ID: {prospect_id}"
                match_summary += f"\n  🌐 Domain: {prospect.domain}"  
                match_summary += f"\n  📈 Status: {prospect.status.name}"
                match_summary += f"\n  🎯 Matches: {', '.join(match_details)}"
                match_summary += f"\n  📅 Updated: {prospect.updated_at.strftime('%Y-%m-%d')}"
                matching_prospects.append(match_summary)
        
        if matching_prospects:
            result = f"# 🔍 Search Results for '{query}'\n\n"
            result += f"Found **{len(matching_prospects)}** matching prospects:\n\n"
            result += "\n\n".join(matching_prospects)
            return result
        else:
            return f"# 🔍 Search Results for '{query}'\n\n" \
                   f"❌ No matching prospects found.\n\n" \
                   f"**Search Tips:**\n" \
                   f"- Try broader terms (e.g., 'tech' instead of 'technology')\n" \
                   f"- Search company names, domains, or keywords from research\n" \
                   f"- Use partial matches (e.g., 'micro' for 'Microsoft')"
                   
    except Exception as e:
        return f"❌ Error during search_prospects for query '{query}': {str(e)}"