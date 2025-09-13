import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any

from src.file_manager.storage import read_markdown_file, save_markdown_report, get_prospect_report_path
from src.file_manager.templates import get_template

async def create_profile(prospect_id: str, research_report_filename: str) -> Dict[str, Any]:
    """
    Transforms a research markdown report into a structured Mini Profile table
    with conversation strategy and saves it as a markdown file.
    """
    if not prospect_id or not research_report_filename:
        raise ValueError("Prospect ID and research report filename cannot be empty.")

    # Read the research markdown report
    research_report_path = await get_prospect_report_path(prospect_id, research_report_filename)
    research_content = await read_markdown_file(research_report_path)

    # Placeholder for parsing logic
    # In a real scenario, this would involve more sophisticated parsing
    # to extract structured data from the markdown content.
    parsed_data = parse_research_markdown(research_content)

    profile_filename = f"{prospect_id}_profile.md"

    # Generate profile markdown using a template
    template_content = await get_template("profile_template.md")
    if not template_content:
        raise FileNotFoundError("profile_template.md not found.")

    # Populate the profile fields and talking points
    profile_data = {
        "company_name": parsed_data.get("company_name", "N/A"),
        "domain": parsed_data.get("domain", "N/A"),
        "industry": "Placeholder Industry",
        "company_size": "Placeholder Size",
        "headquarters": "Placeholder HQ",
        "key_contact": parsed_data.get("decision_makers", [{"name": "N/A"}])[0].get("name", "N/A"),
        "contact_title": parsed_data.get("decision_makers", [{"title": "N/A"}])[0].get("title", "N/A"),
        "recent_news_summary": "Summary of recent news from research report.",
        "tech_stack_summary": ", ".join(parsed_data.get("tech_stack", ["N/A"])),
        "pain_points_summary": "Summary of pain points from research report.",
        "conversation_starter_1": "How do you currently handle [pain point 1]?",
        "conversation_starter_2": "What are your thoughts on [recent news item]?",
        "value_proposition": "Our solution helps with [pain point] by [benefit].",
        "relevance_score": "8/10"
    }

    markdown_profile = template_content.format(
        **profile_data
    )

    await save_markdown_report(prospect_id, profile_filename, markdown_profile)

    return {
        "prospect_id": prospect_id,
        "profile_filename": profile_filename,
        "message": f"Profile for {prospect_id} generated and saved as {profile_filename}"
    }

def parse_research_markdown(markdown_content: str) -> Dict[str, Any]:
    """
    Parses the research markdown content to extract structured data.
    This is a simplified parser and needs to be enhanced for robust extraction.
    """
    parsed_data = {}
    # Example of very basic parsing - needs to be improved
    if "**Company Name**" in markdown_content:
        parsed_data["company_name"] = markdown_content.split("**Company Name**:")[1].split("\n")[0].strip()
    if "**Domain**" in markdown_content:
        parsed_data["domain"] = markdown_content.split("**Domain**:")[1].split("\n")[0].strip()
    if "## Company Background" in markdown_content:
        parsed_data["background"] = markdown_content.split("## Company Background")[1].split("##")[0].strip()
    if "## Recent News" in markdown_content:
        news_section = markdown_content.split("## Recent News")[1].split("##")[0]
        parsed_data["recent_news"] = [line.strip("- ") for line in news_section.split("\n") if line.strip().startswith("-")]
    if "## Technology Stack" in markdown_content:
        tech_section = markdown_content.split("## Technology Stack")[1].split("##")[0]
        parsed_data["tech_stack"] = [item.strip() for item in tech_section.split(",") if item.strip()]
    if "## Key Decision Makers" in markdown_content:
        dm_section = markdown_content.split("## Key Decision Makers")[1].split("##")[0]
        decision_makers = []
        for line in dm_section.split("\n"):
            if "(" in line and ")" in line:
                name = line.split("(")[0].strip("- ")
                title = line.split("(")[1].strip(")")
                decision_makers.append({"name": name, "title": title})
        parsed_data["decision_makers"] = decision_makers
    if "## Identified Pain Points" in markdown_content:
        pp_section = markdown_content.split("## Identified Pain Points")[1].split("##")[0]
        parsed_data["pain_points"] = [line.strip("- ") for line in pp_section.split("\n") if line.strip().startswith("-")]

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
