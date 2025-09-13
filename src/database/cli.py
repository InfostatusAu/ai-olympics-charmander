import asyncio
import click
from src.database.operations import init_db

@click.group()
def db_cli():
    """Database management commands."""
    pass

@db_cli.command("init")
@click.confirmation_option(prompt='Drop all existing tables and create new ones?')
def init():
    """Initialize the database, dropping existing tables if they exist."""
    click.echo("Initializing database...")
    asyncio.run(init_db())
    click.echo("Database initialized.")

if __name__ == '__main__':
    db_cli()