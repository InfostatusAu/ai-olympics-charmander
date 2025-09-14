"""CLI utilities for LLM enhancer testing and debugging."""

import asyncio
import json
import logging
from typing import Dict, Any

import click

from .middleware import LLMMiddleware

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """LLM enhancer CLI utilities."""
    pass


@cli.command()
@click.option('--company', required=True, help='Company name to test')
@click.option('--config-file', help='Configuration file path')
def test_research(company: str, config_file: str = None):
    """Test research enhancement with LLM."""
    click.echo(f"Testing research enhancement for: {company}")
    
    # Load config if provided
    config = {}
    if config_file:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception as e:
            click.echo(f"Failed to load config: {e}")
    
    # Run test
    asyncio.run(_test_research_enhancement(company, config))


@cli.command()
@click.option('--research-file', required=True, help='Research data JSON file')
@click.option('--config-file', help='Configuration file path')
def test_profile(research_file: str, config_file: str = None):
    """Test profile enhancement with LLM."""
    click.echo(f"Testing profile enhancement from: {research_file}")
    
    # Load research data
    try:
        with open(research_file, 'r') as f:
            research_data = json.load(f)
    except Exception as e:
        click.echo(f"Failed to load research data: {e}")
        return
    
    # Load config if provided
    config = {}
    if config_file:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception as e:
            click.echo(f"Failed to load config: {e}")
    
    # Run test
    asyncio.run(_test_profile_enhancement(research_data, config))


async def _test_research_enhancement(company: str, config: Dict[str, Any]):
    """Test research enhancement."""
    try:
        middleware = LLMMiddleware(config)
        
        # Mock raw data for testing
        raw_data = {
            'company_website': {'company': company, 'status': 'mock'},
            'apollo_data': {'company': company, 'status': 'mock'},
            'successful_sources_count': 2,
            'failed_sources_count': 0,
            'total_sources': 7,
            'errors': []
        }
        
        enhanced_data = await middleware.enhance_research_data(raw_data)
        
        click.echo("Enhanced Research Data:")
        click.echo(json.dumps(enhanced_data, indent=2))
        
    except Exception as e:
        click.echo(f"Research enhancement test failed: {e}")
        logger.error(f"Research enhancement test failed: {e}")


async def _test_profile_enhancement(research_data: Dict[str, Any], config: Dict[str, Any]):
    """Test profile enhancement."""
    try:
        middleware = LLMMiddleware(config)
        
        enhanced_strategy = await middleware.enhance_profile_strategy(research_data)
        
        click.echo("Enhanced Profile Strategy:")
        click.echo(json.dumps(enhanced_strategy, indent=2))
        
    except Exception as e:
        click.echo(f"Profile enhancement test failed: {e}")
        logger.error(f"Profile enhancement test failed: {e}")


if __name__ == '__main__':
    cli()
