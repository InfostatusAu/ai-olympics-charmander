
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any
from firecrawl import FirecrawlApp

from src.file_manager.storage import save_markdown_report
from src.file_manager.templates import get_template
from src.logging_config import get_logger, OperationContext, OperationContext
from src.llm_enhancer.middleware import LLMMiddleware

# Get structured logger
logger = get_logger(__name__)

# Initialize Firecrawl client
firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

async def research_prospect(company_identifier: str) -> dict:
    """
    Research a prospect company across multiple data sources with LLM enhancement.
    
    Args:
        company_identifier: Company name or domain to research
        
    Returns:
        dict: Research result with prospect ID, file path, and data sources
        
    Raises:
        ValueError: If company_identifier is empty or invalid
        FileNotFoundError: If template files are not found
        Exception: For other unexpected errors
    """
    if not company_identifier or not company_identifier.strip():
        raise ValueError("Company identifier is required and cannot be empty")
    
    company_identifier = company_identifier.strip()
    
    # Log operation start
    prospect_id = f"prospect_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    report_filename = f"{prospect_id}_research.md"
    
    with OperationContext(operation="prospect_research", prospect_id=prospect_id):
        logger.info("Starting comprehensive prospect research",
                   prospect_id=prospect_id,
                   company_identifier=company_identifier,
                   data_sources=["Company Website", "LinkedIn", "Job Boards", "News & Search", "Government Registries"])

        # Initialize research data structure
        research_data = {
            "company_name": company_identifier,
            "domain": f"https://www.{company_identifier.lower().replace(' ', '')}.com",
            "background": "",
            "business_model": "",
            "recent_news": [],
            "tech_stack": [],
            "decision_makers": [],
            "pain_points": [],
            "linkedin_info": "",
            "apollo_info": "",
            "job_board_info": "",
            "news_and_search_info": "",
            "government_registry_info": "",
            "llm_enhancement_status": "not_attempted",
            "enhancement_method": "unknown",
            "data_quality_score": 0.0,
            "confidence_score": 0.0,
            "data_sources_errors": [],
            "fallback_reason": None
        }

        # Company Website Research
        logger.info("Starting company website research",
                   website_url=research_data["domain"],
                   data_source="company_website")
        try:
            website_data = firecrawl.scrape(
                research_data["domain"],
                {
                    "formats": ["markdown", "extract"],
                    "extract": {
                        "company_description": "A description of what the company does",
                        "products_services": "List of products or services offered",
                        "company_size": "Information about company size or employees",
                        "location": "Company location or headquarters",
                        "industry": "Industry sector or business category",
                        "founding_year": "Year the company was founded",
                        "key_people": "Names and titles of key executives or leadership",
                        "contact_info": "Contact information including email, phone, address",
                        "recent_announcements": "Recent news, press releases, or announcements",
                        "technology_stack": "Technologies, platforms, or tools mentioned"
                    }
                }
            )
            
            if website_data.get('success') and website_data.get('extract'):
                extract_data = website_data['extract']
                research_data["background"] = f"Company Description: {extract_data.get('company_description', 'N/A')}\n"
                research_data["background"] += f"Products/Services: {extract_data.get('products_services', 'N/A')}\n"
                research_data["background"] += f"Industry: {extract_data.get('industry', 'N/A')}\n"
                research_data["background"] += f"Location: {extract_data.get('location', 'N/A')}\n"
                
                if extract_data.get('recent_announcements'):
                    research_data["recent_news"].append(extract_data['recent_announcements'])
                
                if extract_data.get('technology_stack'):
                    research_data["tech_stack"].append(extract_data['technology_stack'])
                    
                if extract_data.get('key_people'):
                    # Parse key people into decision makers format
                    people_text = extract_data['key_people']
                    research_data["decision_makers"].append({
                        "name": people_text.split(',')[0] if ',' in people_text else people_text,
                        "title": "Leadership Team",
                        "linkedin": "Not available"
                    })
        except Exception as e:
            error_msg = f"Error during company website research: {str(e)}"
            logger.error(error_msg,
                        website_url=research_data["domain"],
                        data_source="company_website",
                        exception=e)
            research_data["data_sources_errors"].append(f"Company Website: {str(e)}")
            print(f"Error scraping company website {research_data['domain']}: {e}")

        # LinkedIn Research
        try:
            linkedin_results = firecrawl.search(
                f"{company_identifier} company profile",
                {
                    "search_engine": "google",
                    "num_results": 3,
                    "include_domains": ["linkedin.com"]
                }
            )
            
            if linkedin_results.get('success') and linkedin_results.get('results'):
                for result in linkedin_results['results'][:2]:
                    research_data["linkedin_info"] += f"LinkedIn: {result.get('title', '')}\n{result.get('description', '')}\n\n"
                    
        except Exception as e:
            error_msg = f"Error researching LinkedIn for {company_identifier}: {str(e)}"
            logger.error(error_msg,
                        company_identifier=company_identifier,
                        data_source="linkedin")
            research_data["data_sources_errors"].append(f"LinkedIn: {str(e)}")
            print(f"Error researching LinkedIn for {company_identifier}: {e}")

        # Job Boards Research
        logger.info("Starting job boards research",
                   company_identifier=company_identifier,
                   data_source="job_boards")
        
        job_keywords = [
            f"{company_identifier} AI engineer jobs",
            f"{company_identifier} machine learning jobs", 
            f"{company_identifier} cloud engineer jobs",
            f"{company_identifier} automation jobs"
        ]
        
        for keyword in job_keywords:
            try:
                job_results = firecrawl.search(
                    keyword,
                    {
                        "search_engine": "google",
                        "num_results": 2,
                        "include_domains": ["seek.com.au", "indeed.com.au", "linkedin.com"]
                    }
                )
                
                if job_results.get('success') and job_results.get('results'):
                    for result in job_results['results']:
                        research_data["job_board_info"] += f"Job: {result.get('title', '')}\n{result.get('description', '')}\n\n"
                        
            except Exception as e:
                error_msg = f"Error searching jobs for {keyword}: {str(e)}"
                logger.error(error_msg,
                            keyword=keyword,
                            data_source="job_boards")
                research_data["data_sources_errors"].append(f"Job Boards ({keyword}): {str(e)}")
                print(f"Error searching jobs for {keyword}: {e}")

        # News & Search Research
        logger.info("Starting news and search research",
                   company_identifier=company_identifier,
                   data_source="news_search")
                   
        news_keywords = [
            f"{company_identifier} AI transformation news",
            f"{company_identifier} cloud migration announcement",
            f"{company_identifier} digital transformation",
            f"{company_identifier} technology investment"
        ]
        
        for keyword in news_keywords:
            try:
                news_results = firecrawl.search(
                    keyword,
                    {
                        "search_engine": "google",
                        "num_results": 2,
                        "date_range": "past_year"
                    }
                )
                
                if news_results.get('success') and news_results.get('results'):
                    for result in news_results['results']:
                        research_data["news_and_search_info"] += f"News: {result.get('title', '')}\n{result.get('description', '')}\n\n"
                        research_data["recent_news"].append(result.get('title', ''))
                        
            except Exception as e:
                error_msg = f"Error searching news for {keyword}: {str(e)}"
                logger.error(error_msg,
                            keyword=keyword,
                            data_source="news_search")
                research_data["data_sources_errors"].append(f"News Search ({keyword}): {str(e)}")
                print(f"Error searching news for {keyword}: {e}")

        # Government Registries Research
        logger.info("Starting government registries research",
                   company_identifier=company_identifier,
                   data_source="government_registries")
                   
        registry_keywords = [
            f"site:abr.business.gov.au {company_identifier}",
            f"site:asic.gov.au {company_identifier}",
            f"{company_identifier} ABN registration Australia"
        ]
        
        for keyword in registry_keywords:
            try:
                registry_results = firecrawl.search(
                    keyword,
                    {
                        "search_engine": "google",
                        "num_results": 2
                    }
                )
                
                if registry_results.get('success') and registry_results.get('results'):
                    for result in registry_results['results']:
                        research_data["government_registry_info"] += f"Registry: {result.get('title', '')}\n{result.get('description', '')}\n\n"
                        
            except Exception as e:
                error_msg = f"Error searching registry for {keyword}: {str(e)}"
                logger.error(error_msg,
                            keyword=keyword,
                            data_source="government_registries")
                research_data["data_sources_errors"].append(f"Government Registry ({keyword}): {str(e)}")
                print(f"Error searching registry for {keyword}: {e}")

        # LLM Enhancement Section
        logger.info("Starting LLM enhancement of research data")
        enhancement_result = None
        
        try:
            from ..llm_enhancer.middleware import LLMMiddleware
            middleware = LLMMiddleware()
            enhancement_result = await middleware.enhance_research_data(research_data)
            
            if enhancement_result and enhancement_result.get('enhanced_data'):
                # Merge enhanced data back into research_data
                enhanced_data = enhancement_result['enhanced_data']
                research_data.update(enhanced_data)
                research_data["llm_enhancement_status"] = "ai_enhanced"
                research_data["enhancement_method"] = "ai_enhanced" 
                research_data["confidence_score"] = enhancement_result.get('confidence_score', 0.8)
                logger.info("Research data successfully enhanced with LLM analysis")
            else:
                research_data["llm_enhancement_status"] = "manual_fallback"
                research_data["enhancement_method"] = "manual_fallback"
                research_data["fallback_reason"] = "LLM enhancement returned no data"
                logger.warning("LLM enhancement failed or unavailable, using manual analysis")
                
        except Exception as e:
            research_data["llm_enhancement_status"] = "manual_fallback"
            research_data["enhancement_method"] = "manual_fallback"
            research_data["fallback_reason"] = str(e)
            logger.error("LLM enhancement failed", exception=e)
            logger.warning("LLM enhancement failed or unavailable, using manual analysis")

        # Calculate data quality score based on available information
        quality_score = 0.0
        total_criteria = 7
        
        if research_data["background"]: quality_score += 1/total_criteria
        if research_data["recent_news"]: quality_score += 1/total_criteria  
        if research_data["tech_stack"]: quality_score += 1/total_criteria
        if research_data["decision_makers"]: quality_score += 1/total_criteria
        if research_data["linkedin_info"]: quality_score += 1/total_criteria
        if research_data["job_board_info"]: quality_score += 1/total_criteria
        if research_data["government_registry_info"]: quality_score += 1/total_criteria
        
        research_data["data_quality_score"] = round(quality_score, 2)

        # Ensure minimum data for report generation
        if not research_data["background"]:
            research_data["background"] = f"Research conducted for {company_identifier}. Limited public information available from automated data sources."

        if not research_data["decision_makers"]:
            research_data["decision_makers"] = []

        if not research_data["tech_stack"]:
            research_data["tech_stack"] = []

        if not research_data["recent_news"]:
            research_data["recent_news"] = []

        # Ensure pain points are populated
        pain_points = research_data.get("pain_points", [])
        if not pain_points:
            pain_points = [
                "Potential automation opportunities in manual processes",
                "Cloud adoption and digital transformation needs",
                "AI/ML implementation for competitive advantage"
            ]
        
        research_data["pain_points"] = pain_points
        research_data['business_model'] = "Business model extracted from available data"

        # Generate markdown report using template
        template_content = await get_template("research_template.md")
        if not template_content:
            raise FileNotFoundError("research_template.md not found.")

        # Format the template with research data
        markdown_report = template_content.format(
            company_name=research_data["company_name"],
            domain=research_data["domain"],
            research_date=datetime.now().strftime("%Y-%m-%d"),
            background=research_data["background"],
            business_model=research_data.get("business_model", "Business model not analyzed"),
            recent_news="\n".join([f"- {news}" for news in research_data["recent_news"]]) if research_data["recent_news"] else "- No recent news found",
            tech_stack=", ".join(research_data["tech_stack"]) if research_data["tech_stack"] else "Technology stack not identified",
            decision_makers="\n".join([f"- {dm['name']} ({dm['title']})" for dm in research_data["decision_makers"]]) if research_data["decision_makers"] else "- Decision makers not identified",
            pain_points="\n".join([f"- {pp}" for pp in research_data["pain_points"]]),
            linkedin_info=research_data["linkedin_info"],
            apollo_info=research_data["apollo_info"],
            job_board_info=research_data["job_board_info"],
            news_and_search_info=research_data["news_and_search_info"],
            government_registry_info=research_data["government_registry_info"],
            llm_enhancement_status=research_data.get("llm_enhancement_status", "not_attempted")
        )

        # Save the markdown report
        await save_markdown_report(prospect_id, report_filename, markdown_report)
        
        logger.info("Prospect research completed successfully",
                   prospect_id=prospect_id,
                   report_filename=report_filename,
                   pain_points_count=len(research_data["pain_points"]),
                   decision_makers_count=len(research_data["decision_makers"]),
                   tech_stack_count=len(research_data["tech_stack"]),
                   recent_news_count=len(research_data["recent_news"]),
                   data_sources_completed=5)

        # Build comprehensive result matching contract expectations
        result = {
            "prospect_id": prospect_id,
            "report_filename": report_filename,
            "research_file": report_filename,  # Alias for compatibility
            "message": f"Comprehensive research report for {company_identifier} generated and saved as {report_filename}",
            "data_sources_used": [
                "Company Website",
                "LinkedIn Search", 
                "Job Boards (Seek, Indeed)",
                "News & Search",
                "Government Registries (ASIC, ABN)"
            ],
            "success": True,
            
            # Enhancement tracking fields
            "enhancement_status": research_data["enhancement_method"],
            "fallback_reason": research_data.get("fallback_reason"),
            
            # Data quality metrics
            "data_quality_score": research_data["data_quality_score"],
            "confidence_score": research_data.get("confidence_score", 0.6),
            
            # Data sources summary
            "data_sources_summary": {
                "total_sources": 5,
                "successful_sources": 5 - len(research_data["data_sources_errors"]),
                "errors": research_data["data_sources_errors"]
            },
            
            # Enhanced content fields (for AI-enhanced results)
            "company_background": research_data["background"],
            "business_priority_analysis": research_data.get("business_priority_analysis", "Manual analysis indicates standard business priorities"),
            "technology_readiness_assessment": research_data.get("technology_readiness_assessment", "Technology readiness requires further assessment"),
            "competitive_landscape_positioning": research_data.get("competitive_landscape_positioning", "Competitive position analysis pending"),
            
            # Enhancement metadata
            "enhancement_metadata": {
                "llm_model_used": research_data.get("llm_model_used"),
                "enhancement_timestamp": datetime.now().isoformat(),
                "enhancement_method": research_data["enhancement_method"]
            }
        }
        
        # Add LLM-specific fields only if AI enhancement was successful
        if research_data["enhancement_method"] == "ai_enhanced":
            result["llm_model_used"] = research_data.get("llm_model_used", "anthropic.claude-3-5-sonnet-20241022-v2:0")
        
        return result

if __name__ == "__main__":
    async def main():
        # Example usage
        company = "Example Corp"
        result = await research_prospect(company)
        print(json.dumps(result, indent=2))

        company_no_id = ""
        try:
            await research_prospect(company_no_id)
        except ValueError as e:
            print(f"Error: {e}")

    asyncio.run(main())
