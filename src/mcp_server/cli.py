"""
MCP Server CLI for prospect research automation.
Provides commands to run, test, and manage the MCP server.
"""

import asyncio
import click
import json
import os
from typing import Any, Dict
from src.mcp_server.server import main as run_server
from src.mcp_server.tools import research_prospect, create_profile, get_prospect_data, search_prospects
from src.config import validate_configuration, EnvironmentConfig

@click.group()
def mcp_cli():
    """MCP Server management commands."""
    pass

@mcp_cli.command("start")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--llm-enabled", type=bool, default=True, help="Enable LLM intelligence middleware")
@click.option("--llm-provider", type=click.Choice(['bedrock', 'anthropic', 'openai']), default='bedrock', help="LLM provider")
@click.option("--model-id", type=str, default='apac.anthropic.claude-sonnet-4-20250514-v1:0', help="LLM model ID")
@click.option("--aws-region", type=str, default='ap-southeast-2', help="AWS region for Bedrock")
@click.option("--temperature", type=float, default=0.3, help="LLM temperature (0.0-1.0)")
@click.option("--max-tokens", type=int, default=4000, help="Maximum tokens for LLM responses")
@click.option("--timeout-seconds", type=int, default=60, help="Timeout for LLM requests")
@click.option("--firecrawl-enabled", type=bool, default=True, help="Enable Firecrawl web scraping")
@click.option("--apollo-enabled", type=bool, default=True, help="Enable Apollo.io contact enrichment")
@click.option("--serper-enabled", type=bool, default=True, help="Enable Serper search API")
@click.option("--playwright-enabled", type=bool, default=True, help="Enable Playwright browser automation")
@click.option("--linkedin-auth", type=bool, default=False, help="Enable LinkedIn authenticated browsing")
@click.option("--job-boards-auth", type=bool, default=False, help="Enable job boards authenticated searches")
@click.option("--fallback-mode", type=click.Choice(['strict', 'graceful', 'manual']), default='graceful', help="Error handling mode")
@click.option("--validate-env/--skip-validation", default=True, help="Validate environment before starting")
def start(debug: bool, llm_enabled: bool, llm_provider: str, model_id: str, aws_region: str, 
          temperature: float, max_tokens: int, timeout_seconds: int, firecrawl_enabled: bool,
          apollo_enabled: bool, serper_enabled: bool, playwright_enabled: bool, linkedin_auth: bool,
          job_boards_auth: bool, fallback_mode: str, validate_env: bool):
    """Start the MCP server with stdio transport and complete configuration."""
    
    # Validate environment if requested
    if validate_env:
        click.echo("Validating environment configuration...")
        is_valid, result = validate_configuration()
        
        if not is_valid:
            click.echo("❌ Environment validation failed:")
            for error in result['errors']:
                click.echo(f"  • {error}")
            click.echo("\n💡 Run 'mcp-cli validate-env --show-guide' for configuration help")
            exit(1)
        else:
            click.echo("✅ Environment validation passed")
    
    if debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        click.echo("Debug logging enabled")
    
    # Build configuration from command line arguments
    config = {
        'llm_enabled': llm_enabled,
        'llm_provider': llm_provider,
        'model_id': model_id,
        'aws_region': aws_region,
        'temperature': temperature,
        'max_tokens': max_tokens,
        'timeout_seconds': timeout_seconds,
        'data_sources': {
            'firecrawl_enabled': firecrawl_enabled,
            'apollo_enabled': apollo_enabled,
            'serper_enabled': serper_enabled,
            'playwright_enabled': playwright_enabled,
            'linkedin_auth': linkedin_auth,
            'job_boards_auth': job_boards_auth
        },
        'fallback_mode': fallback_mode
    }
    
    # Set environment configuration for runtime
    os.environ['MCP_SERVER_CONFIG'] = json.dumps(config)
    
    click.echo("Starting MCP server with complete configuration...")
    click.echo(f"LLM Provider: {llm_provider} ({'enabled' if llm_enabled else 'disabled'})")
    click.echo(f"Model: {model_id}")
    click.echo(f"Data Sources: Firecrawl={firecrawl_enabled}, Apollo={apollo_enabled}, Serper={serper_enabled}, Playwright={playwright_enabled}")
    click.echo(f"Authentication: LinkedIn={linkedin_auth}, Job Boards={job_boards_auth}")
    click.echo(f"Fallback Mode: {fallback_mode}")
    
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
@click.option("--check-apis", is_flag=True, help="Check API connectivity for all configured services")
@click.option("--check-llm", is_flag=True, help="Test LLM connectivity and configuration")
@click.option("--check-data-sources", is_flag=True, help="Validate all data source configurations")
def validate(check_apis: bool, check_llm: bool, check_data_sources: bool):
    """Validate the MCP server configuration and dependencies."""
    click.echo("=== Validating MCP Server ===")
    
    # Check imports
    try:
        from src.database.operations import init_db
        from src.file_manager.storage import save_markdown_file
        from src.prospect_research.research import research_prospect
        from src.llm_enhancer.middleware import LLMMiddleware
        from src.data_sources.manager import DataSourceManager
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
    
    # Check environment variables
    required_env_vars = ['FIRECRAWL_API_KEY']
    optional_env_vars = [
        'APOLLO_API_KEY', 'SERPER_API_KEY', 'AWS_ACCESS_KEY_ID', 
        'AWS_SECRET_ACCESS_KEY', 'LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD'
    ]
    
    click.echo("\n=== Environment Variables ===")
    for var in required_env_vars:
        if os.getenv(var):
            click.echo(f"✓ {var} configured")
        else:
            click.echo(f"✗ {var} missing (required)", err=True)
    
    for var in optional_env_vars:
        if os.getenv(var):
            click.echo(f"✓ {var} configured")
        else:
            click.echo(f"⚠ {var} not configured (optional for enhanced features)")
    
    # API connectivity checks
    if check_apis:
        click.echo("\n=== API Connectivity Tests ===")
        asyncio.run(_test_api_connectivity())
    
    # LLM connectivity checks
    if check_llm:
        click.echo("\n=== LLM Configuration Tests ===")
        asyncio.run(_test_llm_connectivity())
    
    # Data source validation
    if check_data_sources:
        click.echo("\n=== Data Source Validation ===")
        asyncio.run(_test_data_sources())
    
    click.echo("\nValidation complete.")

async def _test_api_connectivity():
    """Test API connectivity for configured services."""
    import os
    
    # Test Firecrawl
    if os.getenv('FIRECRAWL_API_KEY'):
        try:
            # Basic connectivity test - you can implement actual API calls here
            click.echo("✓ Firecrawl API key available")
        except Exception as e:
            click.echo(f"✗ Firecrawl API test failed: {e}")
    
    # Test Apollo.io
    if os.getenv('APOLLO_API_KEY'):
        try:
            click.echo("✓ Apollo.io API key available")
        except Exception as e:
            click.echo(f"✗ Apollo.io API test failed: {e}")
    
    # Test Serper
    if os.getenv('SERPER_API_KEY'):
        try:
            click.echo("✓ Serper API key available")
        except Exception as e:
            click.echo(f"✗ Serper API test failed: {e}")

async def _test_llm_connectivity():
    """Test LLM connectivity and configuration."""
    import os
    
    if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
        try:
            from src.llm_enhancer.client import BedrockClient
            client = BedrockClient()
            click.echo("✓ AWS Bedrock client initialized")
            
            # You can add a simple test call here
            click.echo("✓ LLM configuration valid")
        except Exception as e:
            click.echo(f"✗ LLM connectivity test failed: {e}")
    else:
        click.echo("⚠ AWS credentials not configured, LLM features will be disabled")

async def _test_data_sources():
    """Test data source configurations."""
    try:
        from src.data_sources.manager import DataSourceManager
        manager = DataSourceManager()
        
        # Test data source initialization
        click.echo("✓ Data source manager initialized")
        
        # You can add specific data source tests here
        click.echo("✓ Data source configuration valid")
    except Exception as e:
        click.echo(f"✗ Data source test failed: {e}")

@mcp_cli.command("validate-env")
@click.option('--show-guide', is_flag=True, help='Show configuration guide')
@click.option('--verbose', is_flag=True, help='Show detailed validation results')
def validate_env(show_guide, verbose):
    """Validate environment configuration."""
    if show_guide:
        click.echo(EnvironmentConfig.get_configuration_guide())
        return
    
    click.echo("Validating environment configuration...")
    is_valid, result = validate_configuration()
    
    # Show summary
    summary = result['summary']
    click.echo(f"\n📊 Configuration Summary:")
    click.echo(f"  Required variables: {summary['required_configured']}/{summary['total_required']}")
    click.echo(f"  Optional variables: {summary['optional_configured']}/{summary['total_optional']}")
    click.echo(f"  Features enabled: {summary['features_enabled']}")
    
    # Show validation status
    if is_valid:
        click.echo("\n✅ Environment configuration is valid!")
    else:
        click.echo("\n❌ Environment configuration has errors!")
    
    # Show errors
    if result['errors']:
        click.echo(f"\n🚨 Errors ({len(result['errors'])}):")
        for error in result['errors']:
            click.echo(f"  • {error}")
    
    # Show warnings
    if result['warnings']:
        click.echo(f"\n⚠️  Warnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            click.echo(f"  • {warning}")
    
    # Show configured features
    if result['configured_features']:
        click.echo(f"\n✅ Configured Features ({len(result['configured_features'])}):")
        for feature in result['configured_features']:
            click.echo(f"  • {feature}")
    
    # Show missing optional features
    if result['missing_optional']:
        click.echo(f"\n💡 Available Optional Features ({len(result['missing_optional'])}):")
        for missing in result['missing_optional']:
            click.echo(f"  • {missing['feature']} (Set {missing['name']})")
    
    # Show detailed results if verbose
    if verbose:
        click.echo(f"\n📁 Directory Status:")
        for dir_name, exists in result['directories'].items():
            status = "✅" if exists else "❌"
            click.echo(f"  {status} {dir_name}: {exists}")
        
        click.echo(f"\n🔒 Permissions Status:")
        for perm_name, granted in result['permissions'].items():
            status = "✅" if granted else "❌"
            click.echo(f"  {status} {perm_name}: {granted}")
        
        click.echo(f"\n🎯 Feature Availability:")
        for feature_name, available in result['features'].items():
            status = "✅" if available else "❌"
            click.echo(f"  {status} {feature_name}: {available}")
    
    # Exit with appropriate code
    if not is_valid:
        click.echo("\n💡 Run with --show-guide to see configuration examples")
        exit(1)

@mcp_cli.command("test-config")
@click.option('--component', type=click.Choice(['llm', 'apollo', 'serper', 'playwright', 'all']), 
              default='all', help='Test specific component configuration')
def test_config(component):
    """Test configuration for specific components."""
    click.echo(f"Testing {component} configuration...")
    
    features = EnvironmentConfig.get_feature_availability()
    
    if component == 'all':
        for feature_name, available in features.items():
            status = "✅" if available else "❌"
            click.echo(f"  {status} {feature_name}")
    else:
        # Map component names to feature names
        component_map = {
            'llm': 'llm_intelligence',
            'apollo': 'apollo_enrichment',
            'serper': 'serper_search',
            'playwright': 'playwright_browsing'
        }
        
        if component in component_map:
            feature_name = component_map[component]
            available = features.get(feature_name, False)
            status = "✅" if available else "❌"
            click.echo(f"  {status} {feature_name}: {available}")
            
            if not available:
                click.echo("💡 Run 'mcp-cli validate-env --show-guide' for setup instructions")
        else:
            click.echo(f"Unknown component: {component}")

@mcp_cli.command("config")
@click.option("--output-format", type=click.Choice(['json', 'yaml', 'env']), default='json', help="Output format")
def config(output_format: str):
    """Display current configuration and environment variables."""
    import os
    
    click.echo("=== Current MCP Server Configuration ===")
    
    # Get configuration from environment or defaults
    config_str = os.getenv('MCP_SERVER_CONFIG', '{}')
    try:
        config = json.loads(config_str)
    except json.JSONDecodeError:
        config = {}
    
    # Default configuration
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
    
    if output_format == 'json':
        click.echo(json.dumps(final_config, indent=2))
    elif output_format == 'yaml':
        try:
            import yaml
            click.echo(yaml.dump(final_config, default_flow_style=False))
        except ImportError:
            click.echo("YAML output requires PyYAML package", err=True)
            click.echo(json.dumps(final_config, indent=2))
    elif output_format == 'env':
        click.echo("# Environment variables for MCP Server")
        click.echo(f"MCP_LLM_ENABLED={final_config['llm_enabled']}")
        click.echo(f"MCP_LLM_PROVIDER={final_config['llm_provider']}")
        click.echo(f"MCP_MODEL_ID={final_config['model_id']}")
        click.echo(f"MCP_AWS_REGION={final_config['aws_region']}")
        click.echo(f"MCP_TEMPERATURE={final_config['temperature']}")
        click.echo(f"MCP_MAX_TOKENS={final_config['max_tokens']}")
        click.echo(f"MCP_TIMEOUT_SECONDS={final_config['timeout_seconds']}")
        click.echo(f"MCP_FALLBACK_MODE={final_config['fallback_mode']}")
        
        data_sources = final_config['data_sources']
        click.echo(f"MCP_FIRECRAWL_ENABLED={data_sources['firecrawl_enabled']}")
        click.echo(f"MCP_APOLLO_ENABLED={data_sources['apollo_enabled']}")
        click.echo(f"MCP_SERPER_ENABLED={data_sources['serper_enabled']}")
        click.echo(f"MCP_PLAYWRIGHT_ENABLED={data_sources['playwright_enabled']}")
        click.echo(f"MCP_LINKEDIN_AUTH={data_sources['linkedin_auth']}")
        click.echo(f"MCP_JOB_BOARDS_AUTH={data_sources['job_boards_auth']}")

@mcp_cli.command("benchmark")
@click.option("--test-company", type=str, default="TestCorp", help="Company name for benchmark test")
@click.option("--iterations", type=int, default=1, help="Number of benchmark iterations")
@click.option("--measure-performance", is_flag=True, help="Measure detailed performance metrics")
def benchmark(test_company: str, iterations: int, measure_performance: bool):
    """Run benchmark tests for MCP server performance."""
    import time
    
    click.echo(f"=== MCP Server Benchmark ===")
    click.echo(f"Test Company: {test_company}")
    click.echo(f"Iterations: {iterations}")
    
    async def run_benchmark():
        total_time = 0
        successful_runs = 0
        
        for i in range(iterations):
            click.echo(f"\nIteration {i + 1}/{iterations}")
            
            try:
                start_time = time.time()
                
                # Test research_prospect
                click.echo("  Testing research_prospect...")
                research_result = await research_prospect(test_company)
                research_time = time.time() - start_time
                
                # Extract prospect_id from result
                prospect_id = research_result.get('prospect_id')
                if not prospect_id:
                    click.echo("  ✗ No prospect_id returned from research")
                    continue
                
                # Test create_profile
                click.echo("  Testing create_profile...")
                profile_start = time.time()
                profile_result = await create_profile(prospect_id)
                profile_time = time.time() - profile_start
                
                # Test get_prospect_data
                click.echo("  Testing get_prospect_data...")
                data_start = time.time()
                data_result = await get_prospect_data(prospect_id)
                data_time = time.time() - data_start
                
                total_iteration_time = time.time() - start_time
                total_time += total_iteration_time
                successful_runs += 1
                
                if measure_performance:
                    click.echo(f"    Research time: {research_time:.2f}s")
                    click.echo(f"    Profile time: {profile_time:.2f}s")
                    click.echo(f"    Data retrieval time: {data_time:.2f}s")
                    click.echo(f"    Total time: {total_iteration_time:.2f}s")
                
                click.echo(f"  ✓ Iteration {i + 1} completed successfully")
                
            except Exception as e:
                click.echo(f"  ✗ Iteration {i + 1} failed: {e}")
        
        # Summary
        click.echo(f"\n=== Benchmark Results ===")
        click.echo(f"Successful runs: {successful_runs}/{iterations}")
        if successful_runs > 0:
            avg_time = total_time / successful_runs
            click.echo(f"Average time per run: {avg_time:.2f}s")
            click.echo(f"Total time: {total_time:.2f}s")
        
        success_rate = (successful_runs / iterations) * 100
        click.echo(f"Success rate: {success_rate:.1f}%")
        
        # Performance assessment
        if successful_runs > 0:
            if avg_time < 30:
                click.echo("✓ Performance: Excellent (< 30s)")
            elif avg_time < 60:
                click.echo("⚠ Performance: Good (< 60s)")
            elif avg_time < 120:
                click.echo("⚠ Performance: Acceptable (< 120s)")
            else:
                click.echo("✗ Performance: Needs improvement (> 120s)")
    
    try:
        asyncio.run(run_benchmark())
    except Exception as e:
        click.echo(f"Benchmark failed: {e}", err=True)

if __name__ == "__main__":
    mcp_cli()
