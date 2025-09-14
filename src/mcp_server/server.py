#!/usr/bin/env python3
"""
MCP Server with tool registration for prospect research automation.
Implements the Model Context Protocol to expose 4 specialized prospect research tools.
Enhanced with complete data source integration and LLM intelligence middleware.
"""

import asyncio
import json
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent
from .tools import research_prospect, create_profile, get_prospect_data, search_prospects, initialize_tools_with_config

# Import structured logging
from src.logging_config import get_logger, OperationContext, setup_logging

# Configure structured logging
setup_logging(level="INFO", structured=True)
logger = get_logger(__name__)

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
    """Execute prospect research tools with structured logging and context tracking.
    
    Args:
        name: The name of the tool to execute
        arguments: Tool-specific arguments
        
    Returns:
        List of text content responses
        
    Raises:
        ValueError: If tool name is unknown or required parameters are missing
        RuntimeError: If tool execution fails due to internal errors
    """
    # Extract prospect_id if available for context tracking
    prospect_id = arguments.get("prospect_id") or arguments.get("company", "unknown")
    
    with OperationContext(operation=f"mcp_tool_{name}", prospect_id=str(prospect_id), tool_name=name):
        try:
            # Validate tool name
            if name not in ["research_prospect", "create_profile", "get_prospect_data", "search_prospects"]:
                logger.warning("Unknown tool requested", tool_name=name, available_tools=["research_prospect", "create_profile", "get_prospect_data", "search_prospects"])
                raise ValueError(f"Unknown tool: {name}")
            
            # Tool-specific parameter validation and execution
            if name == "research_prospect":
                if "company" not in arguments:
                    logger.warning("Missing required parameter for research_prospect", required_param="company", provided_args=list(arguments.keys()))
                    raise ValueError("Missing required parameter: company")
                
                company = arguments["company"]
                logger.info("Starting prospect research", company=company, data_sources=["LinkedIn", "Apollo", "Job Boards", "News", "Gov Registries"])
                
                result = await research_prospect(company)
                
                logger.info("Prospect research completed successfully", 
                          company=company, 
                          result_length=len(result),
                          contains_error="❌" in result)
                return [TextContent(type="text", text=result)]
            
            elif name == "create_profile":
                if "prospect_id" not in arguments:
                    logger.warning("Missing required parameter for create_profile", required_param="prospect_id", provided_args=list(arguments.keys()))
                    raise ValueError("Missing required parameter: prospect_id")
                
                prospect_id = arguments["prospect_id"]
                logger.info("Starting profile creation", prospect_id=prospect_id)
                
                result = await create_profile(prospect_id)
                
                logger.info("Profile creation completed successfully",
                          prospect_id=prospect_id,
                          result_length=len(result),
                          contains_error="❌" in result)
                return [TextContent(type="text", text=result)]
            
            elif name == "get_prospect_data":
                if "prospect_id" not in arguments:
                    logger.warning("Missing required parameter for get_prospect_data", required_param="prospect_id", provided_args=list(arguments.keys()))
                    raise ValueError("Missing required parameter: prospect_id")
                
                prospect_id = arguments["prospect_id"]
                logger.info("Retrieving prospect data", prospect_id=prospect_id)
                
                result = await get_prospect_data(prospect_id)
                
                logger.info("Prospect data retrieval completed successfully",
                          prospect_id=prospect_id,
                          result_length=len(result),
                          contains_research="Research Report" in result,
                          contains_profile="Prospect Profile" in result)
                return [TextContent(type="text", text=result)]
            
            elif name == "search_prospects":
                if "query" not in arguments:
                    logger.warning("Missing required parameter for search_prospects", required_param="query", provided_args=list(arguments.keys()))
                    raise ValueError("Missing required parameter: query")
                
                query = arguments["query"]
                logger.info("Starting prospect search", query=query, query_length=len(query))
                
                result = await search_prospects(query)
                
                # Extract match count from result
                match_count = 0
                if "Found **" in result:
                    try:
                        match_count = int(result.split("Found **")[1].split("**")[0])
                    except (IndexError, ValueError):
                        pass
                
                logger.info("Prospect search completed successfully",
                          query=query,
                          result_length=len(result),
                          matches_found=match_count)
                return [TextContent(type="text", text=result)]
                
        except ValueError as ve:
            # Client errors - invalid input, missing parameters, etc.
            logger.warning("Client error during tool execution", 
                         error_type="ValueError",
                         error_message=str(ve),
                         tool_name=name,
                         arguments=arguments)
            raise ve  # Re-raise to let MCP framework handle properly
            
        except (OSError, PermissionError) as file_error:
            # File system errors
            logger.exception("File system error during tool execution",
                           error_type=type(file_error).__name__,
                           tool_name=name)
            raise RuntimeError(f"File system error: Unable to access required files for {name}")
            
        except (ConnectionError, TimeoutError) as network_error:
            # Network connectivity issues (for external API calls)
            logger.exception("Network error during tool execution",
                           error_type=type(network_error).__name__,
                           tool_name=name)
            raise RuntimeError(f"Network error: Unable to connect to external services for {name}")
            
        except Exception as e:
            # Top-level handler for any unexpected errors
            logger.exception("Unexpected error during tool execution",
                           error_type=type(e).__name__,
                           error_message=str(e),
                           tool_name=name,
                           arguments=arguments)
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
    """Read prospect resources with structured logging and comprehensive error handling."""
    with OperationContext(operation="mcp_read_resource", tool_name="read_resource"):
        try:
            logger.info("Reading resource", uri=uri, resource_type=uri.split("://")[0] if "://" in uri else "unknown")
            
            if uri == "prospect://icp":
                # Read ICP definition
                try:
                    with open("data/icp.md", "r") as f:
                        content = f.read()
                        logger.info("Successfully read ICP definition", 
                                  content_length=len(content),
                                  file_path="data/icp.md")
                        return content
                except FileNotFoundError:
                    logger.warning("ICP definition file not found, returning default content",
                                 file_path="data/icp.md",
                                 default_content=True)
                    return "# ICP Definition\n\nICP definition not yet configured."
                except (OSError, PermissionError) as e:
                    logger.exception("File system error reading ICP definition",
                                   file_path="data/icp.md",
                                   error_type=type(e).__name__)
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
                    logger.info("Successfully retrieved prospects from database",
                              prospect_count=len(prospects_data),
                              result_length=len(result),
                              status_breakdown={status.name: sum(1 for p in prospects if p.status == status) 
                                              for status in set(p.status for p in prospects)})
                    return result
                    
                except Exception as e:
                    logger.exception("Error retrieving prospects from database",
                                   operation="list_prospects",
                                   error_type=type(e).__name__,
                                   error_message=str(e))
                    raise RuntimeError(f"Database error: Unable to retrieve prospects - {str(e)}")
            
            else:
                logger.warning("Unknown resource URI requested",
                             uri=uri,
                             supported_uris=["prospect://icp", "prospect://prospects/"])
                raise ValueError(f"Unknown resource URI: {uri}")
                
        except ValueError as ve:
            # Client errors - invalid URI
            logger.warning("Client error for resource request",
                         error_type="ValueError",
                         error_message=str(ve),
                         uri=uri)
            raise ve  # Re-raise to let MCP framework handle properly
            
        except RuntimeError as re:
            # Already handled internal errors
            raise re
            
        except Exception as e:
            # Top-level handler for any unexpected errors
            logger.exception("Unexpected error reading resource",
                           error_type=type(e).__name__,
                           error_message=str(e),
                           uri=uri)
            raise RuntimeError(f"Internal server error: Unable to read resource {uri} - {str(e)}")

async def main():
    """Main entry point for the MCP server with structured logging and comprehensive error handling."""
    with OperationContext(operation="mcp_server_startup"):
        try:
            logger.info("Starting prospect research MCP server",
                      server_name="prospect-research",
                      tools_count=len(TOOLS),
                      protocol="MCP")
            
            # Initialize database on startup
            try:
                from src.database.operations import init_db
                logger.info("Initializing database", operation="database_init")
                await init_db()
                logger.info("Database initialized successfully",
                          operation="database_init",
                          success=True)
            except (OSError, PermissionError) as file_error:
                logger.exception("File system error during database initialization",
                               operation="database_init",
                               error_type=type(file_error).__name__)
                raise RuntimeError("Unable to initialize database: file system error")
            except Exception as e:
                logger.exception("Database initialization failed",
                               operation="database_init",
                               error_type=type(e).__name__,
                               error_message=str(e))
                raise RuntimeError(f"Database initialization failed: {str(e)}")
            
            # Initialize tools with configuration from environment
            try:
                config_str = os.getenv('MCP_SERVER_CONFIG', '{}')
                config = json.loads(config_str) if config_str else {}
                
                # Add default configuration if not provided
                default_config = {
                    'llm_enabled': True,
                    'llm_provider': 'bedrock',
                    'model_id': 'apac.anthropic.claude-sonnet-4-20250514-v1:0',
                    'aws_region': 'ap-southeast-2',
                    'temperature': 0.3,
                    'max_tokens': 4000,
                    'timeout_seconds': 60,
                    'data_sources': {
                        'firecrawl_enabled': True,
                        'apollo_enabled': True,
                        'serper_enabled': True,
                        'playwright_enabled': True,
                        'linkedin_auth': False,
                        'job_boards_auth': False
                    },
                    'fallback_mode': 'graceful'
                }
                
                # Merge with defaults
                final_config = {**default_config, **config}
                
                logger.info("Initializing tools with complete configuration",
                          operation="tools_init",
                          llm_enabled=final_config['llm_enabled'],
                          data_sources_count=len(final_config['data_sources']))
                
                initialize_tools_with_config(final_config)
                
                logger.info("Tools initialized successfully with enhanced capabilities",
                          operation="tools_init",
                          success=True)
            except Exception as e:
                logger.warning("Tools initialization failed, using defaults",
                             operation="tools_init",
                             error_type=type(e).__name__,
                             error_message=str(e))
                # Initialize with empty config as fallback
                initialize_tools_with_config({})
            
            # Start the MCP server
            logger.info("Starting MCP server with stdio transport",
                      transport="stdio",
                      server_capabilities=["tools", "resources"])
            
            async with stdio_server() as (read_stream, write_stream):
                try:
                    logger.info("MCP server listening for connections")
                    await server.run(
                        read_stream,
                        write_stream,
                        server.create_initialization_options()
                    )
                    logger.info("MCP server started successfully and ready for requests")
                    
                except (ConnectionError, BrokenPipeError) as conn_error:
                    logger.exception("Connection error during server operation",
                                   error_type=type(conn_error).__name__,
                                   transport="stdio")
                    raise RuntimeError("Server connection error")
                except Exception as e:
                    logger.exception("Server runtime error",
                                   error_type=type(e).__name__,
                                   error_message=str(e))
                    raise RuntimeError(f"Server failed during operation: {str(e)}")
                    
        except KeyboardInterrupt:
            logger.info("Server shutdown requested by user",
                      shutdown_reason="KeyboardInterrupt",
                      graceful=True)
            return
        except RuntimeError as re:
            logger.error("Server startup failed",
                       error_type="RuntimeError",
                       error_message=str(re),
                       startup_phase="initialization")
            raise
        except Exception as e:
            logger.exception("Unexpected error during server startup",
                           error_type=type(e).__name__,
                           error_message=str(e),
                           startup_phase="unknown")
            raise RuntimeError(f"Fatal server error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())