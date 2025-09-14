"""Common CLI utilities and shared command patterns."""
import click
from typing import Any, Callable

def common_options(func: Callable) -> Callable:
    """Decorator to add common CLI options to commands."""
    func = click.option('--debug', is_flag=True, help='Enable debug logging')(func)
    func = click.option('--version', is_flag=True, help='Show version and exit')(func)
    return func

def handle_common_options(debug: bool, version: bool, app_name: str, app_version: str = "1.0.0"):
    """Handle common CLI options processing."""
    if version:
        click.echo(f"{app_name} version {app_version}")
        raise click.Exit(0)
    
    if debug:
        # Enable debug logging
        import logging
        logging.basicConfig(level=logging.DEBUG)
        click.echo("Debug logging enabled")

def async_command(func: Callable) -> Callable:
    """Decorator to handle async command functions."""
    import asyncio
    
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    
    return wrapper

def error_handler(func: Callable) -> Callable:
    """Decorator to add consistent error handling to CLI commands."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Exit(1)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Exit(1)
        except Exception as e:
            click.echo(f"Unexpected error: {e}", err=True)
            raise click.Exit(1)
    
    return wrapper

def success_message(message: str):
    """Display a success message with consistent formatting."""
    click.echo(click.style(f"✅ {message}", fg='green'))

def warning_message(message: str):
    """Display a warning message with consistent formatting."""
    click.echo(click.style(f"⚠️  {message}", fg='yellow'))

def error_message(message: str):
    """Display an error message with consistent formatting."""
    click.echo(click.style(f"❌ {message}", fg='red'), err=True)

def info_message(message: str):
    """Display an info message with consistent formatting."""
    click.echo(click.style(f"ℹ️  {message}", fg='blue'))

class CommonGroup(click.Group):
    """Custom Group class with common functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_settings = dict(help_option_names=['-h', '--help'])
    
    def format_help(self, ctx, formatter):
        """Custom help formatting."""
        formatter.write_heading('Commands')
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None:
                continue
            if cmd.hidden:
                continue
            commands.append((subcommand, cmd.get_short_help_str(limit=45)))
        
        if commands:
            with formatter.section('Available Commands'):
                formatter.write_dl(commands)
        
        # Write epilog if present
        if self.epilog:
            formatter.write_paragraph()
            formatter.write_text(self.epilog)
