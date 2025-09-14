import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any

from src.file_manager.storage import read_markdown_file, save_markdown_report, get_prospect_report_path
from src.file_manager.templates import get_template
from src.logging_config import get_logger, OperationContext

# Get structured logger
logger = get_logger(__name__)

async def create_profile(prospect_id: str, research_report_filename: str) -> Dict[str, Any]:
    """
    Transforms a research markdown report into a structured Mini Profile table
    with intelligent conversation strategy based on comprehensive research data.
    """
    if not prospect_id or not research_report_filename:
        raise ValueError("Prospect ID and research report filename cannot be empty.")

    with OperationContext(operation="profile_creation", prospect_id=prospect_id):
        logger.info("Starting profile creation from research report",
                   prospect_id=prospect_id,
                   research_filename=research_report_filename)

        # Read the research markdown report
        research_report_path = await get_prospect_report_path(prospect_id, research_report_filename)
        research_content = read_markdown_file(research_report_path)  # read_markdown_file is not async
        
        logger.info("Research report loaded successfully",
                   report_path=research_report_path,
                   content_length=len(research_content))

        # Parse the research content with enhanced parsing
        parsed_data = parse_research_markdown(research_content)
        
        logger.info("Research content parsed",
                   parsed_fields=list(parsed_data.keys()),
                   pain_points_found=len(parsed_data.get("pain_points", [])),
                   decision_makers_found=len(parsed_data.get("decision_makers", [])))

        # Generate the Mini Profile template data - match template field names
        profile_data = {
            "company_name": parsed_data.get("company_name", "N/A"),
            "domain": parsed_data.get("domain", "N/A"),
            "industry": _determine_industry(parsed_data),
            "company_size": _estimate_company_size(parsed_data),
            "headquarters": _extract_headquarters(parsed_data),
            "key_contact": _get_primary_contact(parsed_data),  # Changed to match template
            "contact_title": _get_primary_contact_title(parsed_data),  # Changed to match template
            "recent_news_summary": _summarize_recent_news(parsed_data),
            "tech_stack_summary": _summarize_tech_stack(parsed_data),
            "pain_points_summary": _summarize_pain_points(parsed_data),
            "conversation_starter_1": _generate_conversation_starter_1(parsed_data),
            "conversation_starter_2": _generate_conversation_starter_2(parsed_data),
            "value_proposition": _generate_value_proposition(parsed_data),
            "relevance_score": _calculate_relevance_score(parsed_data),
            "research_date": datetime.now().strftime("%Y-%m-%d"),
            "prospect_id": prospect_id
        }
        
        logger.info("Profile data generated",
                   relevance_score=profile_data["relevance_score"],
                   industry=profile_data["industry"],
                   company_size=profile_data["company_size"],
                   conversation_starters_generated=2)

        # Get the Mini Profile template and format it
        template_content = await get_template("profile_template.md")  # get_template is async
        if not template_content:
            logger.error("Profile template not found",
                        template_name="profile_template.md",
                        expected_location="data/templates/")
            raise ValueError("Mini Profile template not found. Please ensure profile_template.md exists in data/templates/")

        # Format the template with profile data
        markdown_profile = template_content.format(**profile_data)

        # Save the profile as a markdown file
        profile_filename = f"{prospect_id}_profile.md"
        await save_markdown_report(prospect_id, profile_filename, markdown_profile)
        
        logger.info("Profile creation completed successfully",
                   profile_filename=profile_filename,
                   profile_length=len(markdown_profile),
                   template_formatted=True)

        return {
            "prospect_id": prospect_id,
            "profile_filename": profile_filename,
            "strategy_summary": f"Outreach strategy based on {len(parsed_data.get('pain_points', []))} pain points and {len(parsed_data.get('recent_news', []))} recent developments",
            "message": f"Intelligent profile for {parsed_data.get('company_name', 'prospect')} generated and saved as {profile_filename}"
        }

def _determine_industry(parsed_data: Dict[str, Any]) -> str:
    """Determine industry based on research data."""
    background = parsed_data.get("background", "").lower()
    tech_stack = " ".join(parsed_data.get("tech_stack", [])).lower()
    job_info = parsed_data.get("job_board_info", "").lower()
    
    # Industry detection logic
    if any(keyword in background + tech_stack + job_info for keyword in ['bank', 'finance', 'fintech', 'payment']):
        return "Financial Services"
    elif any(keyword in background + tech_stack + job_info for keyword in ['health', 'medical', 'hospital', 'clinic']):
        return "Healthcare"
    elif any(keyword in background + tech_stack + job_info for keyword in ['retail', 'ecommerce', 'shop', 'store']):
        return "Retail & E-commerce"
    elif any(keyword in background + tech_stack + job_info for keyword in ['manufact', 'factory', 'production']):
        return "Manufacturing"
    elif any(keyword in background + tech_stack + job_info for keyword in ['education', 'university', 'school', 'learning']):
        return "Education"
    elif any(keyword in background + tech_stack + job_info for keyword in ['tech', 'software', 'saas', 'platform']):
        return "Technology"
    else:
        return "General Business"

def _estimate_company_size(parsed_data: Dict[str, Any]) -> str:
    """Estimate company size based on available indicators."""
    job_info = parsed_data.get("job_board_info", "").lower()
    linkedin_info = parsed_data.get("linkedin_info", "").lower()
    
    # Simple heuristics based on hiring activity and mentions
    if any(indicator in job_info + linkedin_info for indicator in ['enterprise', 'large', 'global', 'multinational']):
        return "Large Enterprise (1000+ employees)"
    elif any(indicator in job_info + linkedin_info for indicator in ['medium', 'growing', 'expanding']):
        return "Medium Business (100-1000 employees)"
    else:
        return "Small-Medium Business (10-500 employees)"

def _extract_headquarters(parsed_data: Dict[str, Any]) -> str:
    """Extract headquarters information from research."""
    registry_info = parsed_data.get("government_registry_info", "")
    background = parsed_data.get("background", "")
    
    # Look for Australian location indicators
    if any(location in (registry_info + background).lower() for location in ['sydney', 'melbourne', 'brisbane', 'perth', 'adelaide']):
        for city in ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide']:
            if city.lower() in (registry_info + background).lower():
                return f"{city}, Australia"
    
    if 'australia' in (registry_info + background).lower():
        return "Australia"
    
    return "Location TBD"

def _get_primary_contact(parsed_data: Dict[str, Any]) -> str:
    """Get primary contact from decision makers."""
    decision_makers = parsed_data.get("decision_makers", [])
    if decision_makers:
        # Prefer CEO, then CTO, then other titles
        for dm in decision_makers:
            if 'ceo' in dm.get("title", "").lower():
                return dm.get("name", "N/A")
        for dm in decision_makers:
            if any(title in dm.get("title", "").lower() for title in ['cto', 'coo', 'vp']):
                return dm.get("name", "N/A")
        return decision_makers[0].get("name", "N/A")
    return "Contact TBD"

def _get_primary_contact_title(parsed_data: Dict[str, Any]) -> str:
    """Get primary contact title."""
    decision_makers = parsed_data.get("decision_makers", [])
    if decision_makers:
        for dm in decision_makers:
            if 'ceo' in dm.get("title", "").lower():
                return dm.get("title", "N/A")
        for dm in decision_makers:
            if any(title in dm.get("title", "").lower() for title in ['cto', 'coo', 'vp']):
                return dm.get("title", "N/A")
        return decision_makers[0].get("title", "N/A")
    return "Leadership Role"

def _summarize_recent_news(parsed_data: Dict[str, Any]) -> str:
    """Summarize recent news findings."""
    recent_news = parsed_data.get("recent_news", [])
    if recent_news:
        return f"Recent developments: {recent_news[0][:100]}..." if recent_news[0] else "Recent news monitoring active"
    return "No recent news identified"

def _summarize_tech_stack(parsed_data: Dict[str, Any]) -> str:
    """Summarize technology stack."""
    tech_stack = parsed_data.get("tech_stack", [])
    if tech_stack:
        return ", ".join(tech_stack[:5])  # Limit to top 5 technologies
    return "Technology stack under assessment"

def _summarize_pain_points(parsed_data: Dict[str, Any]) -> str:
    """Summarize identified pain points."""
    pain_points = parsed_data.get("pain_points", [])
    if pain_points:
        return pain_points[0][:100] + "..." if len(pain_points[0]) > 100 else pain_points[0]
    return "Pain points assessment in progress"

def _generate_conversation_starter_1(parsed_data: Dict[str, Any]) -> str:
    """Generate first conversation starter based on research."""
    pain_points = parsed_data.get("pain_points", [])
    if pain_points:
        if 'ai' in pain_points[0].lower() or 'automation' in pain_points[0].lower():
            return "What's driving your current interest in AI and automation initiatives?"
        elif 'cloud' in pain_points[0].lower():
            return "How are you approaching your cloud transformation journey?"
        elif 'digital' in pain_points[0].lower():
            return "What digital transformation challenges are you currently prioritizing?"
        else:
            return f"I noticed your focus on {pain_points[0][:50]}... - how is this impacting your operations?"
    return "What technology initiatives are you most excited about this year?"

def _generate_conversation_starter_2(parsed_data: Dict[str, Any]) -> str:
    """Generate second conversation starter based on recent news."""
    recent_news = parsed_data.get("recent_news", [])
    job_info = parsed_data.get("job_board_info", "")
    
    if recent_news:
        return f"I saw the recent news about {recent_news[0][:50]}... - how is this shaping your strategy?"
    elif 'ai' in job_info.lower() or 'ml' in job_info.lower():
        return "I noticed you're actively hiring for AI/ML roles - what capabilities are you looking to build?"
    elif 'cloud' in job_info.lower():
        return "Your cloud engineering hiring suggests major infrastructure changes - what's driving this?"
    else:
        return "What technology trends are you seeing as most relevant to your industry?"

def _generate_value_proposition(parsed_data: Dict[str, Any]) -> str:
    """Generate tailored value proposition."""
    pain_points = parsed_data.get("pain_points", [])
    industry = _determine_industry(parsed_data)
    
    if pain_points:
        primary_pain = pain_points[0].lower()
        if 'ai' in primary_pain or 'automation' in primary_pain:
            return f"Our AI automation platform helps {industry.lower()} companies reduce manual processes by 60% while improving accuracy"
        elif 'cloud' in primary_pain:
            return f"Our cloud migration expertise helps {industry.lower()} companies achieve 40% cost reduction and 3x faster deployment"
        elif 'digital' in primary_pain:
            return f"Our digital transformation solutions help {industry.lower()} companies modernize operations and improve customer experience"
        else:
            return f"Our technology solutions help {industry.lower()} companies optimize operations and drive growth"
    return "Our solutions help companies leverage technology for competitive advantage and operational efficiency"

def _calculate_relevance_score(parsed_data: Dict[str, Any]) -> str:
    """Calculate relevance score based on research quality."""
    score = 5  # Base score
    
    # Add points for data richness
    if parsed_data.get("decision_makers"):
        score += 1
    if parsed_data.get("recent_news"):
        score += 1
    if parsed_data.get("tech_stack"):
        score += 1
    if parsed_data.get("pain_points"):
        score += 1
    
    # Add points for AI/Cloud/Automation signals
    all_text = (
        " ".join(parsed_data.get("pain_points", [])) +
        parsed_data.get("job_board_info", "") +
        parsed_data.get("news_search_info", "")
    ).lower()
    
    if any(keyword in all_text for keyword in ['ai', 'artificial intelligence', 'machine learning']):
        score += 1
    if any(keyword in all_text for keyword in ['cloud', 'aws', 'azure', 'gcp']):
        score += 1
    if any(keyword in all_text for keyword in ['automation', 'digital transformation']):
        score += 1
    
    return f"{min(score, 10)}/10"

def parse_research_markdown(markdown_content: str) -> Dict[str, Any]:
    """
    Enhanced parsing of research markdown content to extract structured data.
    Handles the comprehensive research format with all data sources.
    """
    parsed_data = {
        "company_name": "N/A",
        "domain": "N/A", 
        "background": "",
        "recent_news": [],
        "tech_stack": [],
        "decision_makers": [],
        "pain_points": [],
        "linkedin_info": "",
        "apollo_info": "",
        "job_board_info": "",
        "news_search_info": "",
        "government_registry_info": ""
    }
    
    try:
        # Extract company name
        if "**Company Name**:" in markdown_content:
            company_line = markdown_content.split("**Company Name**:")[1].split("\n")[0].strip()
            parsed_data["company_name"] = company_line
        
        # Extract domain
        if "**Domain**:" in markdown_content:
            domain_line = markdown_content.split("**Domain**:")[1].split("\n")[0].strip()
            parsed_data["domain"] = domain_line
            
        # Extract company background
        if "## Company Background" in markdown_content:
            background_section = markdown_content.split("## Company Background")[1].split("##")[0].strip()
            parsed_data["background"] = background_section[:500] + "..." if len(background_section) > 500 else background_section
        
        # Extract recent news
        if "## Recent News" in markdown_content:
            news_section = markdown_content.split("## Recent News")[1].split("##")[0]
            news_items = []
            for line in news_section.split("\n"):
                if line.strip().startswith("- ") and line.strip() != "- No recent news found":
                    news_items.append(line.strip("- ").strip())
            parsed_data["recent_news"] = news_items
        
        # Extract technology stack  
        if "## Technology Stack" in markdown_content:
            tech_section = markdown_content.split("## Technology Stack")[1].split("##")[0].strip()
            if tech_section and tech_section != "Technology stack not identified":
                # Handle both comma-separated and individual items
                if "," in tech_section:
                    tech_items = [item.strip() for item in tech_section.split(",") if item.strip()]
                else:
                    tech_items = [item.strip() for item in tech_section.split() if item.strip()]
                parsed_data["tech_stack"] = tech_items
        
        # Extract decision makers
        if "## Key Decision Makers" in markdown_content:
            dm_section = markdown_content.split("## Key Decision Makers")[1].split("##")[0]
            decision_makers = []
            for line in dm_section.split("\n"):
                if line.strip().startswith("- ") and "(" in line and ")" in line:
                    try:
                        # Parse "- Name (Title)" format
                        content = line.strip("- ").strip()
                        if "(" in content and ")" in content:
                            name = content.split("(")[0].strip()
                            title = content.split("(")[1].split(")")[0].strip()
                            decision_makers.append({"name": name, "title": title})
                    except:
                        continue
            parsed_data["decision_makers"] = decision_makers
        
        # Extract pain points
        if "## Identified Pain Points" in markdown_content:
            pp_section = markdown_content.split("## Identified Pain Points")[1].split("##")[0]
            pain_points = []
            for line in pp_section.split("\n"):
                if line.strip().startswith("- "):
                    pain_points.append(line.strip("- ").strip())
            parsed_data["pain_points"] = pain_points
        
        # Extract data source information
        if "## LinkedIn Information" in markdown_content:
            linkedin_section = markdown_content.split("## LinkedIn Information")[1].split("##")[0].strip()
            parsed_data["linkedin_info"] = linkedin_section[:200] + "..." if len(linkedin_section) > 200 else linkedin_section
        
        if "## Apollo.io Information" in markdown_content:
            apollo_section = markdown_content.split("## Apollo.io Information")[1].split("##")[0].strip()
            parsed_data["apollo_info"] = apollo_section
        
        if "## Public Job Boards Information" in markdown_content:
            job_section = markdown_content.split("## Public Job Boards Information")[1].split("##")[0].strip()
            parsed_data["job_board_info"] = job_section[:200] + "..." if len(job_section) > 200 else job_section
        
        if "## General Search and News Information" in markdown_content:
            news_search_section = markdown_content.split("## General Search and News Information")[1].split("##")[0].strip()
            parsed_data["news_search_info"] = news_search_section[:200] + "..." if len(news_search_section) > 200 else news_search_section
        
        if "## Government & Business Registries Information" in markdown_content:
            registry_section = markdown_content.split("## Government & Business Registries Information")[1].split("##")[0].strip()
            parsed_data["government_registry_info"] = registry_section
            
    except Exception as e:
        print(f"Warning: Error parsing research markdown: {e}")
    
    return parsed_data

if __name__ == "__main__":
    async def main():
        # Example usage (requires a research report to exist)
        # First, run research.py to generate a sample report
        # Then, use the prospect_id and filename here
        sample_prospect_id = "prospect_20250914120000" # Replace with an actual ID from research.py output
        sample_research_filename = "prospect_20250914120000_research.md" # Replace with actual filename

        # Create a dummy research report for testing if it doesn't exist
        dummy_report_path = await get_prospect_report_path(sample_prospect_id, sample_research_filename)
        if not os.path.exists(dummy_report_path):
            print(f"Creating dummy research report at {dummy_report_path}")
            dummy_content = """
# Prospect Research Report: Dummy Corp

**Company Name**: Dummy Corp
**Domain**: dummycorp.com
**Date of Research**: 2025-09-14

## Company Background
This is a dummy company for testing purposes.

## Recent News
- Dummy news item 1
- Dummy news item 2

## Technology Stack
Python, Flask, MongoDB

## Key Decision Makers
- Alice (CEO)
- Bob (CFO)

## Identified Pain Points
- High operational costs
- Inefficient data processing
"""
            await save_markdown_report(sample_prospect_id, sample_research_filename, dummy_content)

        try:
            result = await create_profile(sample_prospect_id, sample_research_filename)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error generating profile: {e}")

    asyncio.run(main())
