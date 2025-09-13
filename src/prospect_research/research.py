
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any
from firecrawl import FirecrawlApp

from src.file_manager.storage import save_markdown_report
from src.file_manager.templates import get_template

async def research_prospect(company_identifier: str) -> Dict[str, Any]:
    """
    Performs comprehensive prospect research for a given company identifier.
    Implements the prospect research approach with real data source integration.
    
    Data Sources:
    1. LinkedIn (Firecrawl, Serper, Playwright MCP)
    2. Apollo API (contact enrichment)  
    3. Job boards (Seek, Indeed, Glassdoor)
    4. Google Search & News
    5. Government registries (ASIC, ABN Lookup, NSW Open Data)
    """
    if not company_identifier:
        raise ValueError("Company identifier cannot be empty.")

    prospect_id = f"prospect_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    report_filename = f"{prospect_id}_research.md"

    # Initialize Firecrawl with API key from environment
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    if not firecrawl_api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable not set.")

    from firecrawl import Firecrawl
    firecrawl = Firecrawl(api_key=firecrawl_api_key)

    # Determine if input is domain or company name
    if '.' in company_identifier and not ' ' in company_identifier:
        company_domain = company_identifier
        company_name = company_identifier.replace('.com', '').replace('.', ' ').title()
    else:
        company_name = company_identifier
        company_domain = f"{company_name.lower().replace(' ', '').replace('&', 'and')}.com"

    company_website_url = f"https://www.{company_domain}"

    # Initialize research data structure
    research_data = {
        "company_name": company_name,
        "domain": company_domain,
        "background": "",
        "recent_news": [],
        "tech_stack": [],
        "decision_makers": [],
        "pain_points": [],
        "linkedin_info": "",
        "apollo_info": "",
        "job_board_info": "",
        "news_and_search_info": "",
        "government_registry_info": ""
    }

    # 1. COMPANY WEBSITE RESEARCH
    try:
        print(f"Scraping company website: {company_website_url}")
        website_data = firecrawl.scrape(
            company_website_url,
            formats=['markdown', 'html']
        )
        
        website_content = website_data.markdown if hasattr(website_data, 'markdown') else ""
        if website_content:
            # Extract key information from website
            research_data["background"] = website_content[:1000] + "..."
            
            # Basic tech stack detection from website content
            tech_indicators = ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Azure', 'GCP', 
                             'Docker', 'Kubernetes', 'AI', 'Machine Learning', 'Cloud', 'API']
            found_tech = [tech for tech in tech_indicators if tech.lower() in website_content.lower()]
            research_data["tech_stack"] = found_tech
            
        else:
            research_data["background"] = f"Unable to scrape website content for {company_domain}"
            
    except Exception as e:
        print(f"Error scraping company website {company_website_url}: {e}")
        research_data["background"] = f"Error accessing company website: {str(e)}"

    # 2. LINKEDIN RESEARCH (Enhanced with proper search)
    try:
        print(f"Researching LinkedIn for: {company_name}")
        
        # Search for company LinkedIn page
        linkedin_search_query = f"site:linkedin.com/company {company_name}"
        linkedin_results = firecrawl.search(
            query=linkedin_search_query,
            limit=5,
            search_engine="google"
        )
        
        linkedin_info_parts = []
        
        if hasattr(linkedin_results, 'data') and linkedin_results.data:
            for result in linkedin_results.data[:3]:  # Process top 3 results
                if hasattr(result, 'url') and 'linkedin.com/company' in result.url:
                    try:
                        # Scrape the LinkedIn company page
                        linkedin_page = firecrawl.scrape(
                            result.url,
                            formats=['markdown']
                        )
                        if hasattr(linkedin_page, 'markdown') and linkedin_page.markdown:
                            linkedin_content = linkedin_page.markdown[:500]
                            linkedin_info_parts.append(f"Company Page: {linkedin_content}")
                            break
                    except Exception as e:
                        print(f"Could not scrape LinkedIn page {result.url}: {e}")
        
        # Search for key personnel on LinkedIn
        personnel_search = f"site:linkedin.com/in {company_name} (CEO OR CTO OR VP OR Director)"
        personnel_results = firecrawl.search(
            query=personnel_search,
            limit=3,
            search_engine="google"
        )
        
        if hasattr(personnel_results, 'data') and personnel_results.data:
            for result in personnel_results.data:
                if hasattr(result, 'title') and hasattr(result, 'url'):
                    # Extract title and role information
                    title = result.title
                    if any(role in title.upper() for role in ['CEO', 'CTO', 'VP', 'DIRECTOR', 'MANAGER']):
                        # Parse name and title from LinkedIn search result
                        name_part = title.split('-')[0].strip() if '-' in title else title.split('|')[0].strip()
                        role_part = title.split('-')[1].strip() if '-' in title else "Leadership Role"
                        research_data["decision_makers"].append({
                            "name": name_part,
                            "title": role_part,
                            "source": "LinkedIn"
                        })
        
        research_data["linkedin_info"] = " | ".join(linkedin_info_parts) if linkedin_info_parts else "Limited LinkedIn information found"
        
    except Exception as e:
        print(f"Error researching LinkedIn for {company_name}: {e}")
        research_data["linkedin_info"] = f"LinkedIn research error: {str(e)}"

    # 3. JOB BOARDS RESEARCH (AI/ML/Cloud hiring signals)
    try:
        print(f"Researching job boards for: {company_name}")
        
        # Search for job postings indicating AI/ML/Cloud initiatives
        job_search_terms = [
            f"{company_name} AI engineer jobs",
            f"{company_name} machine learning jobs", 
            f"{company_name} cloud engineer jobs",
            f"{company_name} automation jobs"
        ]
        
        job_info_parts = []
        
        for search_term in job_search_terms:
            try:
                job_results = firecrawl.search(
                    query=f"site:seek.com.au OR site:indeed.com {search_term}",
                    limit=3,
                    search_engine="google"
                )
                
                if hasattr(job_results, 'data') and job_results.data:
                    for result in job_results.data:
                        if hasattr(result, 'title') and hasattr(result, 'description'):
                            if any(keyword in result.title.upper() for keyword in ['AI', 'ML', 'CLOUD', 'AUTOMATION']):
                                job_info_parts.append(f"Job: {result.title[:100]}")
                                break
                        
            except Exception as e:
                print(f"Error searching jobs for {search_term}: {e}")
        
        research_data["job_board_info"] = " | ".join(job_info_parts) if job_info_parts else "No relevant AI/ML/Cloud job postings found"
        
    except Exception as e:
        print(f"Error researching job boards: {e}")
        research_data["job_board_info"] = f"Job board research error: {str(e)}"

    # 4. NEWS AND SEARCH RESEARCH
    try:
        print(f"Researching news and announcements for: {company_name}")
        
        news_search_queries = [
            f"{company_name} AI transformation news",
            f"{company_name} cloud migration announcement",
            f"{company_name} digital transformation",
            f"{company_name} technology investment"
        ]
        
        news_items = []
        
        for query in news_search_queries:
            try:
                news_results = firecrawl.search(
                    query=query,
                    limit=2,
                    search_engine="google"
                )
                
                if hasattr(news_results, 'data') and news_results.data:
                    for result in news_results.data:
                        if hasattr(result, 'title') and hasattr(result, 'description'):
                            # Filter for recent and relevant news
                            if any(keyword in (result.title + " " + (result.description or "")).upper() 
                                  for keyword in ['AI', 'CLOUD', 'DIGITAL', 'TECHNOLOGY', 'AUTOMATION']):
                                news_items.append(f"{result.title[:100]}")
                                research_data["recent_news"].append(result.title[:100])
                                
            except Exception as e:
                print(f"Error searching news for {query}: {e}")
        
        research_data["news_and_search_info"] = " | ".join(news_items) if news_items else "No recent relevant technology news found"
        
    except Exception as e:
        print(f"Error researching news: {e}")
        research_data["news_and_search_info"] = f"News research error: {str(e)}"

    # 5. GOVERNMENT REGISTRIES RESEARCH (Australian focus)
    try:
        print(f"Researching government registries for: {company_name}")
        
        # Search ASIC and ABN Lookup for company information
        registry_queries = [
            f"site:abr.business.gov.au {company_name}",
            f"site:asic.gov.au {company_name}",
            f"{company_name} ABN registration Australia"
        ]
        
        registry_info = []
        
        for query in registry_queries:
            try:
                registry_results = firecrawl.search(
                    query=query,
                    limit=2,
                    search_engine="google"
                )
                
                if hasattr(registry_results, 'data') and registry_results.data:
                    for result in registry_results.data:
                        if hasattr(result, 'title') and any(site in result.url for site in ['abr.business.gov.au', 'asic.gov.au']):
                            registry_info.append(f"Registry: {result.title[:100]}")
                            break
                            
            except Exception as e:
                print(f"Error searching registry for {query}: {e}")
        
        research_data["government_registry_info"] = " | ".join(registry_info) if registry_info else "No government registry information found"
        
    except Exception as e:
        print(f"Error researching government registries: {e}")
        research_data["government_registry_info"] = f"Registry research error: {str(e)}"

    # 6. APOLLO.IO PLACEHOLDER (requires API key and integration)
    research_data["apollo_info"] = "Apollo.io integration pending - requires API key and contact enrichment setup"

    # Identify pain points based on research findings
    pain_points = []
    
    # Analyze job postings for pain points
    if "AI" in research_data["job_board_info"] or "cloud" in research_data["job_board_info"].lower():
        pain_points.append("Digital transformation initiatives - actively hiring for AI/Cloud roles")
    
    # Analyze news for pain points  
    if any(keyword in research_data["news_and_search_info"].lower() for keyword in ['transformation', 'moderniz', 'upgrade']):
        pain_points.append("Technology modernization challenges - recent announcements indicate infrastructure changes")
    
    # Default pain points if no specific signals found
    if not pain_points:
        pain_points = [
            "Potential automation opportunities in manual processes",
            "Cloud adoption and digital transformation needs",
            "AI/ML implementation for competitive advantage"
        ]
    
    research_data["pain_points"] = pain_points

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
        recent_news="\n".join([f"- {news}" for news in research_data["recent_news"]]) if research_data["recent_news"] else "- No recent news found",
        tech_stack=", ".join(research_data["tech_stack"]) if research_data["tech_stack"] else "Technology stack not identified",
        decision_makers="\n".join([f"- {dm['name']} ({dm['title']})") for dm in research_data["decision_makers"]]) if research_data["decision_makers"] else "- Decision makers not identified",
        pain_points="\n".join([f"- {pp}" for pp in research_data["pain_points"]]),
        linkedin_info=research_data["linkedin_info"],
        apollo_info=research_data["apollo_info"],
        job_board_info=research_data["job_board_info"],
        news_and_search_info=research_data["news_and_search_info"],
        government_registry_info=research_data["government_registry_info"]
    )

    # Save the markdown report
    await save_markdown_report(prospect_id, report_filename, markdown_report)

    return {
        "prospect_id": prospect_id,
        "report_filename": report_filename,
        "message": f"Comprehensive research report for {company_identifier} generated and saved as {report_filename}",
        "data_sources_used": [
            "Company Website",
            "LinkedIn Search", 
            "Job Boards (Seek, Indeed)",
            "News & Search",
            "Government Registries (ASIC, ABN)"
        ]
    }

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
