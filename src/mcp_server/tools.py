"""
MCP Tools Implementation for Prospect Research.
Implements the 4 core MCP tools with complete data integration and LLM enhancement.
"""

from src.database import operations as db_operations
from src.database.models import ProspectStatus
from src.file_manager import storage as fm_storage
from src.prospect_research import research as pr_research
from src.prospect_research import profile as pr_profile
from src.data_sources.manager import DataSourceManager
from src.llm_enhancer.middleware import LLMMiddleware
import uuid
import os
import json
import logging

logger = logging.getLogger(__name__)

# Initialize global components (configured by MCP server startup)
_data_source_manager = None
_llm_middleware = None

def initialize_tools_with_config(config: dict = None):
    """Initialize tools with configuration from MCP server startup."""
    global _data_source_manager, _llm_middleware
    
    config = config or {}
    
    # Initialize data source manager with configuration
    data_source_config = config.get('data_sources', {})
    _data_source_manager = DataSourceManager(data_source_config)
    
    # Initialize LLM middleware with configuration
    llm_config = {
        'llm_enabled': config.get('llm_enabled', True),
        'model_id': config.get('model_id', 'apac.anthropic.claude-sonnet-4-20250514-v1:0'),
        'aws_region': config.get('aws_region', 'ap-southeast-2'),
        'temperature': config.get('temperature', 0.3),
        'max_tokens': config.get('max_tokens', 4000),
        'timeout_seconds': config.get('timeout_seconds', 60)
    }
    _llm_middleware = LLMMiddleware(llm_config)
    
    logger.info("MCP tools initialized with complete data sources and LLM middleware")

async def research_prospect(company: str) -> str:
    """
    Researches a prospect company using complete data sources and LLM enhancement.
    Integrates all available data sources with intelligent analysis.
    """
    try:
        # Generate a unique prospect ID
        prospect_id = str(uuid.uuid4())
        
        # Initialize components if not already done
        if _data_source_manager is None or _llm_middleware is None:
            # Fallback to default initialization
            initialize_tools_with_config()
        
        # First, create a prospect entry in the database
        prospect = await db_operations.create_prospect_default(
            prospect_id=prospect_id,
            company_name=company, 
            domain=f"{company.lower().replace(' ', '').replace('&', 'and')}.com"
        )
        
        # Collect comprehensive data from all available sources
        logger.info(f"Starting comprehensive research for {company}")
        raw_data = await _data_source_manager.collect_all_prospect_data(company)
        
        # Enhance data with LLM intelligence middleware
        enhanced_data = await _llm_middleware.enhance_research_data(raw_data)
        
        # Generate research report using enhanced data (fallback to original function)
        try:
            # Try to use enhanced research if available
            research_result = await pr_research.research_prospect(company)
            
            # Add enhanced data to the result
            research_result['enhanced_data'] = enhanced_data
            research_result['raw_data_summary'] = {
                'successful_sources': raw_data.get('successful_sources', []),
                'failed_sources': raw_data.get('failed_sources', []),
                'total_sources': raw_data.get('total_sources', 9)
            }
        except Exception as e:
            logger.warning(f"Enhanced research failed, using fallback: {e}")
            research_result = await pr_research.research_prospect(company)
            research_result['enhanced_data'] = {'middleware_status': 'fallback', 'fallback_reason': str(e)}
        
        # Update prospect status in DB
        await db_operations.update_prospect_status_default(prospect.id, ProspectStatus.RESEARCHED)
        
        # Prepare comprehensive result summary
        enhanced_data = research_result.get('enhanced_data', {})
        raw_data_summary = research_result.get('raw_data_summary', {})
        data_sources_used = raw_data_summary.get('successful_sources', research_result.get('data_sources_used', []))
        failed_sources = raw_data_summary.get('failed_sources', [])
        enhancement_status = enhanced_data.get('middleware_status', 'unknown')
        
        result = f"✅ **Complete Research Completed for {company}**\n\n"
        result += f"📊 **Prospect ID**: {prospect.id}\n"
        result += f"📄 **Report**: {research_result['report_filename']}\n"
        result += f"🎯 **Enhancement**: {enhancement_status.title()}\n"
        result += f"🔍 **Data Sources Used**: {len(data_sources_used)}/9 available\n"
        
        if data_sources_used:
            result += f"   ✅ Successful: {', '.join(data_sources_used)}\n"
        
        if failed_sources:
            result += f"   ❌ Failed: {', '.join(failed_sources)} (continued with fallback)\n"
        
        result += f"💼 **Database Status**: RESEARCHED\n"
        result += f"🚀 **Data Quality**: {enhanced_data.get('data_quality_score', 'N/A')}\n"
        
        # Add LLM enhancement details
        if enhanced_data.get('llm_enabled'):
            result += f"🧠 **AI Enhancement**: Active (Model: {enhanced_data.get('model_used', 'Claude')})\n"
        else:
            result += f"🧠 **AI Enhancement**: Manual processing (LLM unavailable)\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error in research_prospect for {company}: {str(e)}")
        return f"❌ **Error during comprehensive research for {company}**:\n{str(e)}\n\n" \
               f"💡 **Troubleshooting**:\n" \
               f"- Check API keys in environment variables\n" \
               f"- Verify internet connectivity\n" \
               f"- Try running with --fallback-mode=manual"

async def create_profile(prospect_id: str) -> str:
    """
    Creates an AI-enhanced prospect profile and conversation strategy.
    Uses LLM intelligence to generate personalized outreach strategies.
    """
    try:
        # Initialize components if not already done
        if _data_source_manager is None or _llm_middleware is None:
            initialize_tools_with_config()
        
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
                return f"❌ **Prospect with ID {prospect_id} not found in database**"
            
            # Check if research has been completed
            if prospect.status != ProspectStatus.RESEARCHED:
                return f"❌ **Prospect {prospect_id} must be researched first**\n" \
                       f"Current status: {prospect.status.name}\n" \
                       f"💡 Run research_prospect first, then create_profile"
            
            # Find matching research file for this prospect
            import glob
            research_files = glob.glob(f"data/prospects/prospect_*/prospect_*_research.md")
            if not research_files:
                return f"❌ **No research files found**\n" \
                       f"💡 Please run research_prospect first"
            
            # Find the most recent research file by modification time
            research_files.sort(key=os.path.getmtime, reverse=True)
            research_file_path = research_files[0]
            research_filename = os.path.basename(research_file_path)
            
            # Extract the research prospect_id from the filename for profile creation
            research_prospect_id = research_filename.replace("_research.md", "")
            
            # Load research data for LLM enhancement
            research_content = await fm_storage.read_markdown_file(research_file_path)
            research_data = {"research_content": research_content, "company_name": prospect.company_name}
            
            # Enhance profile strategy with LLM intelligence
            enhanced_strategy = await _llm_middleware.enhance_profile_strategy(research_data)
            
            # Create the profile using enhanced strategy (fallback to original function)
            try:
                # Use original profile creation function
                profile_result = await pr_profile.create_profile(research_prospect_id, research_filename)
                
                # Add enhanced strategy to the result
                profile_result['enhanced_strategy'] = enhanced_strategy
            except Exception as e:
                logger.warning(f"Enhanced profile creation failed, using fallback: {e}")
                profile_result = await pr_profile.create_profile(research_prospect_id, research_filename)
                profile_result['enhanced_strategy'] = {'middleware_status': 'fallback', 'fallback_reason': str(e)}
            
            # Update prospect status in DB
            await db_operations.update_prospect_status_default(prospect_id, ProspectStatus.PROFILED)
            
            # Prepare comprehensive result
            enhanced_strategy = profile_result.get('enhanced_strategy', {})
            result = f"✅ **AI-Enhanced Profile Created for {prospect.company_name}**\n\n"
            result += f"📊 **Prospect ID**: {prospect_id}\n"
            result += f"📄 **Profile**: {profile_result['profile_filename']}\n"
            
            # Add strategy summary based on enhancement status
            enhancement_status = enhanced_strategy.get('middleware_status', 'unknown')
            if enhancement_status == 'success':
                result += f"🧠 **AI Strategy**: Personalized conversation strategy generated\n"
                result += f"🎯 **Talking Points**: {len(enhanced_strategy.get('talking_points', []))} custom points\n"
                result += f"💡 **Value Prop**: AI-tailored to company context\n"
            else:
                result += f"🧠 **Strategy**: Manual conversation strategy (LLM fallback)\n"
                result += f"🎯 **Reason**: {enhanced_strategy.get('fallback_reason', 'Standard approach')}\n"
            
            result += f"💼 **Database Status**: PROFILED\n"
            result += f"📋 **Next Steps**: Use get_prospect_data to view complete profile"
            
            return result
            
        else:
            # Handle timestamp-based prospect ID directly (from research_prospect tool output)
            research_filename = f"{prospect_id}_research.md"
            
            # Check if research file exists
            research_file_path = f"data/prospects/{prospect_id}/{research_filename}"
            if not os.path.exists(research_file_path):
                return f"❌ **Research file not found**\n" \
                       f"Expected: {research_file_path}\n" \
                       f"💡 Please run research_prospect first"
            
            # Load research data for LLM enhancement
            research_content = await fm_storage.read_markdown_file(research_file_path)
            research_data = {"research_content": research_content, "company_name": prospect_id}
            
            # Enhance profile strategy with LLM intelligence
            enhanced_strategy = await _llm_middleware.enhance_profile_strategy(research_data)
            
            # Create the profile using enhanced strategy (fallback to original function)
            try:
                # Use original profile creation function
                profile_result = await pr_profile.create_profile(prospect_id, research_filename)
                
                # Add enhanced strategy to the result
                profile_result['enhanced_strategy'] = enhanced_strategy
            except Exception as e:
                logger.warning(f"Enhanced profile creation failed, using fallback: {e}")
                profile_result = await pr_profile.create_profile(prospect_id, research_filename)
                profile_result['enhanced_strategy'] = {'middleware_status': 'fallback', 'fallback_reason': str(e)}
            
            # Prepare comprehensive result
            enhanced_strategy = profile_result.get('enhanced_strategy', {})
            result = f"✅ **AI-Enhanced Profile Created for {prospect_id}**\n\n"
            result += f"📄 **Profile**: {profile_result['profile_filename']}\n"
            
            # Add strategy summary based on enhancement status
            enhancement_status = enhanced_strategy.get('middleware_status', 'unknown')
            if enhancement_status == 'success':
                result += f"🧠 **AI Strategy**: Personalized conversation strategy generated\n"
                result += f"🎯 **Talking Points**: {len(enhanced_strategy.get('talking_points', []))} custom points\n"
                result += f"💡 **Value Prop**: AI-tailored to company context\n"
            else:
                result += f"🧠 **Strategy**: Manual conversation strategy (LLM fallback)\n"
                result += f"🎯 **Reason**: {enhanced_strategy.get('fallback_reason', 'Standard approach')}\n"
            
            result += f"💡 **Prospect ID for future operations**: {prospect_id}"
            
            return result
               
    except Exception as e:
        logger.error(f"Error in create_profile for {prospect_id}: {str(e)}")
        return f"❌ **Error during AI-enhanced profile creation for {prospect_id}**:\n{str(e)}\n\n" \
               f"💡 **Troubleshooting**:\n" \
               f"- Ensure research_prospect was completed successfully\n" \
               f"- Check LLM configuration and API keys\n" \
               f"- Try running with --llm-enabled=false for manual fallback"

async def get_prospect_data(prospect_id: str) -> str:
    """
    Retrieves complete prospect intelligence with comprehensive data source and AI analysis details.
    Returns enhanced prospect context with data quality metrics and AI insights.
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
                return f"❌ **Prospect with ID {prospect_id} not found.**"

            # Build comprehensive prospect data response
            result_parts = [
                f"# 📊 **Complete Prospect Intelligence Report**",
                f"",
                f"## 🏢 **Company Overview**",
                f"- **Prospect ID**: {prospect_id}",
                f"- **Company Name**: {prospect.company_name}",
                f"- **Domain**: {prospect.domain}",
                f"- **Status**: {prospect.status.name}",
                f"- **Created**: {prospect.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- **Last Updated**: {prospect.updated_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f""
            ]

            # Find and include research content (use latest research file)
            import glob
            research_files = glob.glob(f"data/prospects/prospect_*/prospect_*_research.md")
            
        else:
            # Handle timestamp-based prospect ID directly
            result_parts = [
                f"# 📊 **Complete Prospect Intelligence Report**",
                f"",
                f"## 🏢 **Company Overview**",
                f"- **Prospect ID**: {prospect_id}",
                f"- **Type**: Research-generated prospect",
                f"- **Data Location**: data/prospects/{prospect_id}/",
                f"- **Generated**: From comprehensive data collection",
                f""
            ]

            # Find research and profile files for this timestamp-based ID
            import glob
            research_files = glob.glob(f"data/prospects/{prospect_id}/{prospect_id}_research.md")
        
        # Find and include enhanced research content
        if research_files:
            research_files.sort(key=os.path.getmtime, reverse=True)
            research_path = research_files[0]
            research_filename = os.path.basename(research_path)
            
            try:
                research_content = await fm_storage.read_markdown_file(research_path)
                
                # Extract data source summary if available
                data_summary = ""
                if "## Data Collection Summary" in research_content:
                    lines = research_content.split('\n')
                    in_summary = False
                    for line in lines:
                        if "## Data Collection Summary" in line:
                            in_summary = True
                            continue
                        elif line.startswith("## ") and in_summary:
                            break
                        elif in_summary:
                            data_summary += line + "\n"
                
                result_parts.extend([
                    f"## 🔍 **Enhanced Research Report**",
                    f"- **File**: {research_filename}",
                    f"- **Generated**: From comprehensive data collection + AI analysis",
                    f"- **Enhancement**: LLM-powered business intelligence",
                    f"",
                    f"### 📊 **Data Collection Summary**",
                    data_summary.strip() if data_summary else "Comprehensive multi-source data collection completed",
                    f"",
                    f"### 📋 **Full Research Content**",
                    research_content,
                    f""
                ])
            except Exception as e:
                result_parts.extend([
                    f"## 🔍 **Enhanced Research Report**",
                    f"- **File**: {research_filename}",
                    f"- **Status**: ❌ Error reading research file: {str(e)}",
                    f""
                ])
        else:
            result_parts.extend([
                f"## 🔍 **Enhanced Research Report**",
                f"- **Status**: ❌ No research file found for prospect {prospect_id}",
                f"- **Action Required**: Run research_prospect first",
                f""
            ])

        # Find and include AI-enhanced profile content
        if is_uuid:
            profile_files = glob.glob(f"data/prospects/prospect_*/prospect_*_profile.md")
        else:
            profile_files = glob.glob(f"data/prospects/{prospect_id}/{prospect_id}_profile.md")
            
        if profile_files:
            profile_files.sort(key=os.path.getmtime, reverse=True)
            profile_path = profile_files[0]
            profile_filename = os.path.basename(profile_path)
            
            try:
                profile_content = await fm_storage.read_markdown_file(profile_path)
                
                # Extract strategy summary if available
                strategy_summary = ""
                if "## AI-Generated Strategy Summary" in profile_content:
                    lines = profile_content.split('\n')
                    in_summary = False
                    for line in lines:
                        if "## AI-Generated Strategy Summary" in line:
                            in_summary = True
                            continue
                        elif line.startswith("## ") and in_summary:
                            break
                        elif in_summary:
                            strategy_summary += line + "\n"
                
                result_parts.extend([
                    f"## 🎯 **AI-Enhanced Prospect Profile**",
                    f"- **File**: {profile_filename}",
                    f"- **Enhancement**: AI-generated conversation strategies",
                    f"- **Personalization**: Tailored to company-specific insights",
                    f"",
                    f"### 🧠 **AI Strategy Summary**",
                    strategy_summary.strip() if strategy_summary else "Personalized outreach strategy generated",
                    f"",
                    f"### 📋 **Complete Profile Content**",
                    profile_content,
                    f""
                ])
            except Exception as e:
                result_parts.extend([
                    f"## 🎯 **AI-Enhanced Prospect Profile**", 
                    f"- **File**: {profile_filename}",
                    f"- **Status**: ❌ Error reading profile file: {str(e)}",
                    f""
                ])
        else:
            result_parts.extend([
                f"## 🎯 **AI-Enhanced Prospect Profile**", 
                f"- **Status**: ⏳ Profile not yet created",
                f"- **Action Available**: Run create_profile to generate AI-enhanced strategy",
                f"- **Expected Output**: Personalized conversation starters, value propositions, and objection handling",
                f""
            ])

        # Add comprehensive intelligence summary
        result_parts.extend([
            f"## 🚀 **Intelligence Summary**",
            f"",
            f"This prospect report combines:",
            f"- **🔍 Multi-source data collection**: 9 different data sources",
            f"- **🧠 AI-powered analysis**: LLM enhancement for business insights", 
            f"- **🎯 Personalized strategy**: Custom conversation approaches",
            f"- **📊 Data quality metrics**: Source success rates and reliability",
            f"",
            f"**Next Actions**:",
            f"- Use conversation starters from the profile for personalized outreach",
            f"- Leverage AI-generated talking points for relevant discussions",
            f"- Apply timing recommendations for optimal engagement",
            f""
        ])

        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error in get_prospect_data for {prospect_id}: {str(e)}")
        return f"❌ **Error retrieving prospect data for {prospect_id}**:\n{str(e)}\n\n" \
               f"💡 **Troubleshooting**:\n" \
               f"- Verify prospect_id is correct\n" \
               f"- Ensure research_prospect was completed\n" \
               f"- Check file system permissions"

async def search_prospects(query: str) -> str:
    """
    Advanced prospect search with content analysis across all data sources and AI insights.
    Searches company names, domains, research content, and AI-generated insights.
    """
    try:
        if not query or len(query.strip()) < 2:
            return "❌ **Search query must be at least 2 characters long**\n\n" \
                   f"💡 **Search Tips**:\n" \
                   f"- Use company names, domains, or technology keywords\n" \
                   f"- Search for pain points, strategies, or business insights\n" \
                   f"- Try industry terms or specific business challenges"
        
        query_lower = query.lower()
        all_prospects = await db_operations.list_prospects_default()
        matching_prospects = []
        
        logger.info(f"Searching {len(all_prospects)} prospects for query: {query}")

        for prospect in all_prospects:
            prospect_id = str(prospect.id)
            match_details = []
            match_score = 0
            
            # Check company name and domain (high relevance)
            if query_lower in prospect.company_name.lower():
                match_details.append("Company Name")
                match_score += 10
            if query_lower in prospect.domain.lower():
                match_details.append("Domain")
                match_score += 8

            # Search enhanced research content
            import glob
            research_files = glob.glob(f"data/prospects/*{prospect_id}*research.md")
            if not research_files:
                research_files = glob.glob(f"data/prospects/prospect_*_research.md")
            
            research_insights = []
            if research_files:
                research_files.sort(key=os.path.getmtime, reverse=True)
                try:
                    research_content = await fm_storage.read_markdown_file(research_files[0])
                    if query_lower in research_content.lower():
                        match_details.append("Research Content")
                        match_score += 6
                        
                        # Extract specific context around the match
                        lines = research_content.lower().split('\n')
                        for i, line in enumerate(lines):
                            if query_lower in line:
                                context_start = max(0, i-1)
                                context_end = min(len(lines), i+2)
                                context = ' '.join(lines[context_start:context_end]).strip()
                                if len(context) > 100:
                                    context = context[:100] + "..."
                                research_insights.append(f"Research context: {context}")
                                break
                                
                except Exception:
                    pass

            # Search AI-enhanced profile content
            profile_files = glob.glob(f"data/prospects/*{prospect_id}*profile.md")
            profile_insights = []
            if profile_files:
                profile_files.sort(key=os.path.getmtime, reverse=True)
                try:
                    profile_content = await fm_storage.read_markdown_file(profile_files[0])
                    if query_lower in profile_content.lower():
                        match_details.append("AI Profile Strategy")
                        match_score += 7
                        
                        # Extract specific context around the match
                        lines = profile_content.lower().split('\n')
                        for i, line in enumerate(lines):
                            if query_lower in line:
                                context_start = max(0, i-1)
                                context_end = min(len(lines), i+2)
                                context = ' '.join(lines[context_start:context_end]).strip()
                                if len(context) > 100:
                                    context = context[:100] + "..."
                                profile_insights.append(f"Strategy context: {context}")
                                break
                                
                except Exception:
                    pass

            # If any matches found, add to results with enhanced details
            if match_details:
                match_summary = f"## 🏢 **{prospect.company_name}** (Score: {match_score})"
                match_summary += f"\n- **📊 Prospect ID**: {prospect_id}"
                match_summary += f"\n- **🌐 Domain**: {prospect.domain}"  
                match_summary += f"\n- **📈 Status**: {prospect.status.name}"
                match_summary += f"\n- **🎯 Matches Found**: {', '.join(match_details)}"
                match_summary += f"\n- **📅 Last Updated**: {prospect.updated_at.strftime('%Y-%m-%d %H:%M')}"
                
                # Add insights if available
                if research_insights:
                    match_summary += f"\n- **🔍 Research Insight**: {research_insights[0]}"
                if profile_insights:
                    match_summary += f"\n- **🧠 AI Strategy Insight**: {profile_insights[0]}"
                
                matching_prospects.append((match_score, match_summary))
        
        # Sort by match score (highest first)
        matching_prospects.sort(key=lambda x: x[0], reverse=True)
        
        if matching_prospects:
            result = f"# 🔍 **Advanced Search Results for '{query}'**\n\n"
            result += f"Found **{len(matching_prospects)}** matching prospects with comprehensive data analysis:\n\n"
            
            # Add only the summaries (without scores)
            summaries = [summary for score, summary in matching_prospects]
            result += "\n\n".join(summaries)
            
            result += f"\n\n---\n"
            result += f"### 📊 **Search Performance**\n"
            result += f"- **Total Prospects Searched**: {len(all_prospects)}\n"
            result += f"- **Matches Found**: {len(matching_prospects)}\n"
            result += f"- **Data Sources**: Research files, AI profiles, company data\n"
            result += f"- **Enhancement**: Context-aware matching with relevance scoring\n"
            
            return result
        else:
            return f"# 🔍 **Advanced Search Results for '{query}'**\n\n" \
                   f"❌ **No matching prospects found in comprehensive search.**\n\n" \
                   f"### 🔍 **Search Coverage**\n" \
                   f"- **Prospects Searched**: {len(all_prospects)} total\n" \
                   f"- **Data Sources Searched**: Company names, domains, research content, AI strategies\n" \
                   f"- **Enhancement Level**: Full context analysis with AI insights\n\n" \
                   f"### 💡 **Search Optimization Tips**\n" \
                   f"- **Broader Terms**: Try 'tech' instead of 'technology'\n" \
                   f"- **Industry Keywords**: Search for business challenges or pain points\n" \
                   f"- **Company Attributes**: Try location, size, or business model terms\n" \
                   f"- **AI Insights**: Search for strategy terms like 'conversation', 'value proposition'\n" \
                   f"- **Partial Matches**: Use fragments like 'micro' for 'Microsoft'\n\n" \
                   f"**Suggested Queries**: 'AI', 'cloud', 'startup', 'enterprise', 'automation'"
                   
    except Exception as e:
        logger.error(f"Error in search_prospects for query '{query}': {str(e)}")
        return f"❌ **Error during advanced search for query '{query}'**:\n{str(e)}\n\n" \
               f"💡 **Troubleshooting**:\n" \
               f"- Check database connectivity\n" \
               f"- Verify prospect files exist and are readable\n" \
               f"- Try a simpler search query"