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
        RuntimeError: If tool execution fails due to internal errors
    """
    try:
        # Validate tool name
        if name not in ["research_prospect", "create_profile", "get_prospect_data", "search_prospects"]:
            logger.warning(f"Unknown tool requested: {name}")
            raise ValueError(f"Unknown tool: {name}")
        
        # Tool-specific parameter validation and execution
        if name == "research_prospect":
            if "company" not in arguments:
                logger.warning(f"Missing required parameter 'company' for tool: {name}")
                raise ValueError("Missing required parameter: company")
            
            logger.info(f"Executing research_prospect for company: {arguments['company']}")
            result = await research_prospect(arguments["company"])
            logger.info(f"Successfully completed research_prospect for: {arguments['company']}")
            return [TextContent(type="text", text=result)]
        
        elif name == "create_profile":
            if "prospect_id" not in arguments:
                logger.warning(f"Missing required parameter 'prospect_id' for tool: {name}")
                raise ValueError("Missing required parameter: prospect_id")
            
            logger.info(f"Executing create_profile for prospect_id: {arguments['prospect_id']}")
            result = await create_profile(arguments["prospect_id"])
            logger.info(f"Successfully completed create_profile for: {arguments['prospect_id']}")
            return [TextContent(type="text", text=result)]
        
        elif name == "get_prospect_data":
            if "prospect_id" not in arguments:
                logger.warning(f"Missing required parameter 'prospect_id' for tool: {name}")
                raise ValueError("Missing required parameter: prospect_id")
            
            logger.info(f"Executing get_prospect_data for prospect_id: {arguments['prospect_id']}")
            result = await get_prospect_data(arguments["prospect_id"])
            logger.info(f"Successfully completed get_prospect_data for: {arguments['prospect_id']}")
            return [TextContent(type="text", text=result)]
        
        elif name == "search_prospects":
            if "query" not in arguments:
                logger.warning(f"Missing required parameter 'query' for tool: {name}")
                raise ValueError("Missing required parameter: query")
            
            logger.info(f"Executing search_prospects with query: {arguments['query']}")
            result = await search_prospects(arguments["query"])
            logger.info(f"Successfully completed search_prospects for query: {arguments['query']}")
            return [TextContent(type="text", text=result)]
            
    except ValueError as ve:
        # Client errors - invalid input, missing parameters, etc.
        logger.warning(f"Client error for tool {name}: {ve}")
        raise ve  # Re-raise to let MCP framework handle properly
        
    except (OSError, PermissionError) as file_error:
        # File system errors
        logger.exception(f"File system error during {name} execution")
        raise RuntimeError(f"File system error: Unable to access required files for {name}")
        
    except (ConnectionError, TimeoutError) as network_error:
        # Network connectivity issues (for external API calls)
        logger.exception(f"Network error during {name} execution")
        raise RuntimeError(f"Network error: Unable to connect to external services for {name}")
        
    except Exception as e:
        # Top-level handler for any unexpected errors
        logger.exception(f"Unexpected error during {name} execution")
        raise RuntimeError(f"Internal server error: {name} execution failed - {str(e)}")

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
    """Read prospect resources with comprehensive error handling."""
    try:
        logger.info(f"Reading resource: {uri}")
        
        if uri == "prospect://icp":
            # Read ICP definition
            try:
                with open("data/icp.md", "r") as f:
                    content = f.read()
                    logger.info("Successfully read ICP definition")
                    return content
            except FileNotFoundError:
                logger.warning("ICP definition file not found, returning default content")
                return "# ICP Definition\n\nICP definition not yet configured."
            except (OSError, PermissionError):
                logger.exception("File system error reading ICP definition")
                raise RuntimeError("Unable to access ICP definition file")
        
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
                result = json.dumps(prospects_data, indent=2)
                logger.info(f"Successfully retrieved {len(prospects_data)} prospects")
                return result
                
            except Exception as e:
                logger.exception("Error retrieving prospects from database")
                raise RuntimeError(f"Database error: Unable to retrieve prospects - {str(e)}")
        
        else:
            logger.warning(f"Unknown resource URI requested: {uri}")
            raise ValueError(f"Unknown resource URI: {uri}")
            
    except ValueError as ve:
        # Client errors - invalid URI
        logger.warning(f"Client error for resource {uri}: {ve}")
        raise ve  # Re-raise to let MCP framework handle properly
        
    except RuntimeError as re:
        # Already handled internal errors
        raise re
        
    except Exception as e:
        # Top-level handler for any unexpected errors
        logger.exception(f"Unexpected error reading resource {uri}")
        raise RuntimeError(f"Internal server error: Unable to read resource {uri} - {str(e)}")

async def main():
    """Main entry point for the MCP server with comprehensive error handling."""
    try:
        logger.info("Starting prospect research MCP server...")
        
        # Initialize database on startup
        try:
            from src.database.operations import init_db
            await init_db()
            logger.info("Database initialized successfully")
        except (OSError, PermissionError) as file_error:
            logger.exception("File system error during database initialization")
            raise RuntimeError("Unable to initialize database: file system error")
        except Exception as e:
            logger.exception("Database initialization failed")
            raise RuntimeError(f"Database initialization failed: {str(e)}")
        
        # Start the MCP server
        logger.info("Starting MCP server with stdio transport...")
        async with stdio_server() as (read_stream, write_stream):
            try:
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options()
                )
                logger.info("MCP server started successfully")
            except (ConnectionError, BrokenPipeError) as conn_error:
                logger.exception("Connection error during server operation")
                raise RuntimeError("Server connection error")
            except Exception as e:
                logger.exception("Server runtime error")
                raise RuntimeError(f"Server failed during operation: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
        return
    except RuntimeError as re:
        logger.error(f"Server startup failed: {re}")
        raise
    except Exception as e:
        logger.exception("Unexpected error during server startup")
        raise RuntimeError(f"Fatal server error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())