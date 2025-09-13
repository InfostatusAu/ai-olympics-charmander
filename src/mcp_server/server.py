#!/usr/bin/env python3
"""
MCP Server with tool registration for prospect research automation.
Implements the Model Context Protocol to expose 4 specialized prospect research tools.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent
from .tools import research_prospect, create_profile, get_prospect_data, search_prospects

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("prospect-research")

# Define available tools
TOOLS = [
    Tool(
        name="research_prospect",
        description="Step 1: Compile comprehensive research and generate markdown research report",
        inputSchema={
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "Company name or domain to research"
                }
            },
            "required": ["company"],
            "additionalProperties": False
        }
    ),
    Tool(
        name="create_profile", 
        description="Step 2: Transform research markdown into structured Mini Profile table with conversation strategy",
        inputSchema={
            "type": "object",
            "properties": {
                "prospect_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "UUID of prospect to generate profile for"
                }
            },
            "required": ["prospect_id"],
            "additionalProperties": False
        }
    ),
    Tool(
        name="get_prospect_data",
        description="Retrieve prospect metadata with all generated markdown files",
        inputSchema={
            "type": "object",
            "properties": {
                "prospect_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "UUID of prospect to retrieve"
                }
            },
            "required": ["prospect_id"],
            "additionalProperties": False
        }
    ),
    Tool(
        name="search_prospects",
        description="Search prospects by metadata and markdown file content",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for prospect content"
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    )
]

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available prospect research tools."""
    return TOOLS

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute prospect research tools.
    
    Args:
        name: The name of the tool to execute
        arguments: Tool-specific arguments
        
    Returns:
        List of text content responses
        
    Raises:
        ValueError: If tool name is unknown or required parameters are missing
    """
    try:
        if name == "research_prospect":
            if "company" not in arguments:
                raise ValueError("Missing required parameter: company")
            result = await research_prospect(arguments["company"])
            return [TextContent(type="text", text=result)]
        
        elif name == "create_profile":
            if "prospect_id" not in arguments:
                raise ValueError("Missing required parameter: prospect_id")
            result = await create_profile(arguments["prospect_id"])
            return [TextContent(type="text", text=result)]
        
        elif name == "get_prospect_data":
            if "prospect_id" not in arguments:
                raise ValueError("Missing required parameter: prospect_id")
            result = await get_prospect_data(arguments["prospect_id"])
            return [TextContent(type="text", text=result)]
        
        elif name == "search_prospects":
            if "query" not in arguments:
                raise ValueError("Missing required parameter: query")
            result = await search_prospects(arguments["query"])
            return [TextContent(type="text", text=result)]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Tool execution failed for {name}: {e}")
        raise

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available prospect resources."""
    return [
        Resource(
            uri="prospect://prospects/",
            name="All Prospects",
            description="List of all prospects with metadata",
            mimeType="application/json"
        ),
        Resource(
            uri="prospect://icp",
            name="Ideal Customer Profile",
            description="Current ICP criteria for prospect qualification", 
            mimeType="text/markdown"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read prospect resources."""
    if uri == "prospect://icp":
        # Read ICP definition
        try:
            with open("data/icp.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "# ICP Definition\n\nICP definition not yet configured."
    
    elif uri == "prospect://prospects/":
        # Return list of all prospects
        from src.database.operations import list_prospects
        try:
            prospects = await list_prospects()
            prospects_data = []
            for prospect in prospects:
                prospects_data.append({
                    "id": str(prospect.id),
                    "company_name": prospect.company_name,
                    "domain": prospect.domain,
                    "status": prospect.status.name,
                    "created_at": prospect.created_at.isoformat()
                })
            import json
            return json.dumps(prospects_data, indent=2)
        except Exception as e:
            return f"Error retrieving prospects: {e}"
    
    else:
        raise ValueError(f"Unknown resource URI: {uri}")

async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting prospect research MCP server...")
    
    # Initialize database on startup
    try:
        from src.database.operations import init_db
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())