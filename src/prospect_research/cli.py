import asyncio
import click
import json

from src.prospect_research.research import research_prospect
from src.prospect_research.profile import create_profile

@click.group()
def cli():
    """Prospect Research CLI"""
    pass

@cli.command()
@click.argument("company_identifier")
def research(company_identifier):
    """
    Performs comprehensive prospect research for a given company identifier.
    """
    click.echo(f"Starting research for {company_identifier}...")
    try:
        result = asyncio.run(research_prospect(company_identifier))
        click.echo(json.dumps(result, indent=2))
        click.echo(f"Research report saved to: {result['report_filename']}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}. Make sure 'research_template.md' exists in data/templates.", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred during research: {e}", err=True)

@cli.command()
@click.argument("prospect_id")
@click.argument("research_report_filename")
def profile(prospect_id, research_report_filename):
    """
    Transforms a research markdown report into a structured Mini Profile table.
    """
    click.echo(f"Generating profile for prospect ID: {prospect_id} from report: {research_report_filename}...")
    try:
        result = asyncio.run(create_profile(prospect_id, research_report_filename))
        click.echo(json.dumps(result, indent=2))
        click.echo(f"Profile saved to: {result['profile_filename']}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}. Make sure 'profile_template.md' exists in data/templates.", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred during profile generation: {e}", err=True)

if __name__ == "__main__":
    cli()
