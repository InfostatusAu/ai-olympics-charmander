import asyncio
import click
from src.database.operations import init_db
from src.config import validate_configuration, EnvironmentConfig

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

@db_cli.command("validate-env")
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

if __name__ == '__main__':
    db_cli()