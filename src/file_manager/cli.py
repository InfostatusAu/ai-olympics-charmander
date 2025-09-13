import click
import os

@click.group()
def cli():
    """File Manager CLI"""
    pass

@cli.command()
@click.argument("path", type=click.Path())
def create_dir(path):
    """Creates a directory."""
    if os.path.exists(path):
        click.echo(f"Directory already exists: {path}")
    else:
        os.makedirs(path)
        click.echo(f"Directory created: {path}")
