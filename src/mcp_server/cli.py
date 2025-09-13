"""
MCP Server CLI for prospect research automation.
Provides commands to run, test, and manage the MCP server.
"""

import asyncio
import click
import json
from typing import Any, Dict
from src.mcp_server.server import main as run_server
from src.mcp_server.tools import research_prospect, create_profile, get_prospect_data, search_prospects

@click.group()
def mcp_cli():
    """MCP Server management commands."""
    pass

@mcp_cli.command("start")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def start(debug: bool):
    """Start the MCP server with stdio transport."""
    if debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        click.echo("Debug logging enabled")
    
    click.echo("Starting MCP server...")
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        click.echo("\nMCP server stopped.")
    except Exception as e:
        click.echo(f"Error starting MCP server: {e}", err=True)
        raise

@mcp_cli.command("test-tool")
@click.argument("tool_name", type=click.Choice(["research_prospect", "create_profile", "get_prospect_data", "search_prospects"]))
@click.argument("arguments", required=False)
def test_tool(tool_name: str, arguments: str = None):
    """Test an individual MCP tool with given arguments.
    
    ARGUMENTS should be a JSON string with the tool parameters.
    
    Examples:
    mcp-cli test-tool research_prospect '{"company": "TestCorp"}'
    mcp-cli test-tool get_prospect_data '{"prospect_id": "123e4567-e89b-12d3-a456-426614174000"}'
    """
    try:
        # Parse arguments
        if arguments:
            try:
                args_dict = json.loads(arguments)
            except json.JSONDecodeError as e:
                click.echo(f"Invalid JSON arguments: {e}", err=True)
                return
        else:
            args_dict = {}
        
        # Select and run the tool
        if tool_name == "research_prospect":
            if "company" not in args_dict:
                click.echo("Error: research_prospect requires 'company' parameter", err=True)
                return
            result = asyncio.run(research_prospect(args_dict["company"]))
        
        elif tool_name == "create_profile":
            if "prospect_id" not in args_dict:
                click.echo("Error: create_profile requires 'prospect_id' parameter", err=True)
                return
            result = asyncio.run(create_profile(args_dict["prospect_id"]))
        
        elif tool_name == "get_prospect_data":
            if "prospect_id" not in args_dict:
                click.echo("Error: get_prospect_data requires 'prospect_id' parameter", err=True)
                return
            result = asyncio.run(get_prospect_data(args_dict["prospect_id"]))
        
        elif tool_name == "search_prospects":
            if "query" not in args_dict:
                click.echo("Error: search_prospects requires 'query' parameter", err=True)
                return
            result = asyncio.run(search_prospects(args_dict["query"]))
        
        # Display result
        click.echo(f"\n=== Tool Result ===")
        click.echo(result)
        
    except Exception as e:
        click.echo(f"Error testing tool {tool_name}: {e}", err=True)
        raise

@mcp_cli.command("info")
def info():
    """Display information about the MCP server and available tools."""
    click.echo("=== MCP Server Information ===")
    click.echo("Server Name: prospect-research")
    click.echo("Protocol: Model Context Protocol (JSON-RPC 2.0)")
    click.echo("Transport: stdio")
    click.echo()
    
    click.echo("=== Available Tools ===")
    tools_info = [
        {
            "name": "research_prospect",
            "description": "Step 1: Compile comprehensive research and generate markdown research report",
            "parameters": ["company (string)"]
        },
        {
            "name": "create_profile", 
            "description": "Step 2: Transform research markdown into structured Mini Profile table with conversation strategy",
            "parameters": ["prospect_id (uuid)"]
        },
        {
            "name": "get_prospect_data",
            "description": "Retrieve prospect metadata with all generated markdown files",
            "parameters": ["prospect_id (uuid)"]
        },
        {
            "name": "search_prospects",
            "description": "Search prospects by metadata and markdown file content",
            "parameters": ["query (string)"]
        }
    ]
    
    for tool in tools_info:
        click.echo(f"• {tool['name']}")
        click.echo(f"  Description: {tool['description']}")
        click.echo(f"  Parameters: {', '.join(tool['parameters'])}")
        click.echo()

@mcp_cli.command("validate")
def validate():
    """Validate the MCP server configuration and dependencies."""
    click.echo("=== Validating MCP Server ===")
    
    # Check imports
    try:
        from src.database.operations import init_db
        from src.file_manager.storage import save_markdown_file
        from src.prospect_research.research import research_prospect
        click.echo("✓ All dependencies importable")
    except ImportError as e:
        click.echo(f"✗ Import error: {e}", err=True)
        return
    
    # Check data directories
    import os
    data_dirs = ["data/prospects", "data/database"]
    for dir_path in data_dirs:
        if os.path.exists(dir_path):
            click.echo(f"✓ Directory exists: {dir_path}")
        else:
            click.echo(f"⚠ Directory missing: {dir_path}")
    
    # Check database connection
    try:
        asyncio.run(init_db())
        click.echo("✓ Database connection successful")
    except Exception as e:
        click.echo(f"✗ Database error: {e}", err=True)
    
    click.echo("\nValidation complete.")

if __name__ == "__main__":
    mcp_cli()
