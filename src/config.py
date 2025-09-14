"""Shared configuration constants and paths for the prospect research system."""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_ROOT = PROJECT_ROOT / "data"

# Directory paths
DATABASE_DIR = DATA_ROOT / "database"
PROSPECTS_DIR = DATA_ROOT / "prospects"
TEMPLATES_DIR = DATA_ROOT / "templates"

# Database configuration
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_DIR}/prospects.db"

# File patterns
RESEARCH_FILE_PATTERN = "{prospect_id}_research.md"
PROFILE_FILE_PATTERN = "{prospect_id}_profile.md"

# Template names
RESEARCH_TEMPLATE = "research_template.md"
PROFILE_TEMPLATE = "profile_template.md"

# Environment variable configuration
class EnvironmentConfig:
    """Environment variable configuration and validation."""
    
    # Required environment variables
    REQUIRED_VARS = {
        'FIRECRAWL_API_KEY': {
            'description': 'API key for Firecrawl web scraping service',
            'pattern': r'^fc-[a-zA-Z0-9]{32,}$',
            'example': 'fc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        }
    }
    
    # Optional environment variables for enhanced features
    OPTIONAL_VARS = {
        'APOLLO_API_KEY': {
            'description': 'API key for Apollo.io contact enrichment',
            'pattern': r'^[a-zA-Z0-9]{40,}$',
            'example': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'feature': 'Contact enrichment and lead data'
        },
        'SERPER_API_KEY': {
            'description': 'API key for Serper search service',
            'pattern': r'^[a-zA-Z0-9]{32,}$',
            'example': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'feature': 'Enhanced search capabilities'
        },
        'AWS_ACCESS_KEY_ID': {
            'description': 'AWS access key for Bedrock LLM services',
            'pattern': r'^AKIA[A-Z0-9]{16}$',
            'example': 'AKIAXXXXXXXXXXXXXXXX',
            'feature': 'LLM intelligence middleware'
        },
        'AWS_SECRET_ACCESS_KEY': {
            'description': 'AWS secret key for Bedrock LLM services',
            'pattern': r'^[A-Za-z0-9/+=]{40}$',
            'example': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'feature': 'LLM intelligence middleware'
        },
        'AWS_DEFAULT_REGION': {
            'description': 'AWS region for Bedrock services',
            'pattern': r'^[a-z]{2}-[a-z]+-[0-9]$',
            'example': 'ap-southeast-2',
            'feature': 'LLM intelligence middleware',
            'default': 'ap-southeast-2'
        },
        'LINKEDIN_EMAIL': {
            'description': 'LinkedIn email for authenticated browsing',
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'example': 'user@example.com',
            'feature': 'LinkedIn authenticated data collection'
        },
        'LINKEDIN_PASSWORD': {
            'description': 'LinkedIn password for authenticated browsing',
            'pattern': r'^.{8,}$',
            'example': 'secure_password',
            'feature': 'LinkedIn authenticated data collection',
            'sensitive': True
        }
    }
    
    # LLM configuration variables
    LLM_CONFIG_VARS = {
        'MCP_LLM_ENABLED': {
            'description': 'Enable LLM intelligence middleware',
            'pattern': r'^(true|false)$',
            'example': 'true',
            'default': 'true',
            'type': 'boolean'
        },
        'MCP_LLM_PROVIDER': {
            'description': 'LLM provider selection',
            'pattern': r'^(bedrock|anthropic|openai)$',
            'example': 'bedrock',
            'default': 'bedrock',
            'type': 'choice'
        },
        'MCP_MODEL_ID': {
            'description': 'LLM model identifier',
            'pattern': r'^[a-zA-Z0-9._:-]+$',
            'example': 'apac.anthropic.claude-sonnet-4-20250514-v1:0',
            'default': 'apac.anthropic.claude-sonnet-4-20250514-v1:0'
        },
        'MCP_TEMPERATURE': {
            'description': 'LLM temperature setting (0.0-1.0)',
            'pattern': r'^0?\.[0-9]+$|^1\.0$|^0$',
            'example': '0.3',
            'default': '0.3',
            'type': 'float'
        },
        'MCP_MAX_TOKENS': {
            'description': 'Maximum tokens for LLM responses',
            'pattern': r'^[1-9][0-9]{2,4}$',
            'example': '4000',
            'default': '4000',
            'type': 'integer'
        }
    }
    
    @classmethod
    def validate_environment(cls) -> Tuple[bool, Dict[str, Any]]:
        """Validate all environment variables and return status report."""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'configured_features': [],
            'missing_optional': [],
            'summary': {}
        }
        
        # Check required variables
        for var_name, var_config in cls.REQUIRED_VARS.items():
            value = os.getenv(var_name)
            if not value:
                validation_result['valid'] = False
                validation_result['errors'].append(
                    f"Required variable {var_name} is not set. {var_config['description']}"
                )
            elif not re.match(var_config['pattern'], value):
                validation_result['valid'] = False
                validation_result['errors'].append(
                    f"Required variable {var_name} has invalid format. Expected pattern: {var_config['example']}"
                )
            else:
                validation_result['configured_features'].append(f"Core: {var_config['description']}")
        
        # Check optional variables
        for var_name, var_config in cls.OPTIONAL_VARS.items():
            value = os.getenv(var_name)
            if value:
                if not re.match(var_config['pattern'], value):
                    validation_result['warnings'].append(
                        f"Optional variable {var_name} has invalid format. Expected pattern: {var_config['example']}"
                    )
                else:
                    validation_result['configured_features'].append(f"Enhanced: {var_config['feature']}")
            else:
                validation_result['missing_optional'].append({
                    'name': var_name,
                    'feature': var_config['feature'],
                    'example': var_config['example']
                })
        
        # Check LLM configuration
        llm_config_valid = True
        for var_name, var_config in cls.LLM_CONFIG_VARS.items():
            value = os.getenv(var_name, var_config.get('default', ''))
            if value and not re.match(var_config['pattern'], value):
                validation_result['warnings'].append(
                    f"LLM config variable {var_name} has invalid format. Expected: {var_config['example']}"
                )
                llm_config_valid = False
        
        if llm_config_valid:
            validation_result['configured_features'].append("LLM: Intelligence middleware configuration")
        
        # Generate summary
        validation_result['summary'] = {
            'total_required': len(cls.REQUIRED_VARS),
            'required_configured': len(cls.REQUIRED_VARS) - len([e for e in validation_result['errors'] if 'Required variable' in e]),
            'total_optional': len(cls.OPTIONAL_VARS),
            'optional_configured': len(cls.OPTIONAL_VARS) - len(validation_result['missing_optional']),
            'features_enabled': len(validation_result['configured_features']),
            'has_errors': len(validation_result['errors']) > 0,
            'has_warnings': len(validation_result['warnings']) > 0
        }
        
        return validation_result['valid'], validation_result
    
    @classmethod
    def get_configuration_guide(cls) -> str:
        """Get a comprehensive configuration guide."""
        guide = [
            "# Environment Configuration Guide",
            "",
            "## Required Variables (Essential for basic functionality)",
            ""
        ]
        
        for var_name, var_config in cls.REQUIRED_VARS.items():
            guide.extend([
                f"### {var_name}",
                f"- **Description**: {var_config['description']}",
                f"- **Example**: `{var_name}={var_config['example']}`",
                f"- **Required**: Yes",
                ""
            ])
        
        guide.extend([
            "## Optional Variables (Enhanced features)",
            ""
        ])
        
        for var_name, var_config in cls.OPTIONAL_VARS.items():
            guide.extend([
                f"### {var_name}",
                f"- **Description**: {var_config['description']}",
                f"- **Feature**: {var_config['feature']}",
                f"- **Example**: `{var_name}={var_config['example']}`",
                f"- **Required**: No",
                ""
            ])
        
        guide.extend([
            "## LLM Configuration Variables",
            ""
        ])
        
        for var_name, var_config in cls.LLM_CONFIG_VARS.items():
            default_info = f" (Default: {var_config['default']})" if 'default' in var_config else ""
            guide.extend([
                f"### {var_name}",
                f"- **Description**: {var_config['description']}",
                f"- **Example**: `{var_name}={var_config['example']}`{default_info}",
                f"- **Required**: No",
                ""
            ])
        
        return "\n".join(guide)
    
    @classmethod
    def get_feature_availability(cls) -> Dict[str, bool]:
        """Check which features are available based on environment configuration."""
        features = {
            'core_research': bool(os.getenv('FIRECRAWL_API_KEY')),
            'apollo_enrichment': bool(os.getenv('APOLLO_API_KEY')),
            'serper_search': bool(os.getenv('SERPER_API_KEY')),
            'llm_intelligence': bool(os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY')),
            'linkedin_auth': bool(os.getenv('LINKEDIN_EMAIL') and os.getenv('LINKEDIN_PASSWORD')),
            'playwright_browsing': True,  # No API key required
            'database_storage': True,  # Always available
            'file_storage': True  # Always available
        }
        
        return features

def validate_configuration() -> Tuple[bool, Dict[str, Any]]:
    """Validate complete system configuration."""
    is_valid, env_result = EnvironmentConfig.validate_environment()
    
    # Check directory structure
    directory_status = {
        'database_dir': DATABASE_DIR.exists(),
        'prospects_dir': PROSPECTS_DIR.exists(),
        'templates_dir': TEMPLATES_DIR.exists()
    }
    
    # Check file permissions
    permissions_status = {
        'database_writable': os.access(DATABASE_DIR.parent, os.W_OK),
        'prospects_writable': os.access(PROSPECTS_DIR.parent, os.W_OK)
    }
    
    # Compile complete validation result
    complete_result = {
        **env_result,
        'directories': directory_status,
        'permissions': permissions_status,
        'features': EnvironmentConfig.get_feature_availability()
    }
    
    # Update validity based on directory and permissions
    if not all(directory_status.values()):
        complete_result['warnings'].append("Some data directories are missing (will be created automatically)")
    
    if not all(permissions_status.values()):
        complete_result['valid'] = False
        complete_result['errors'].append("Insufficient file system permissions for data directories")
    
    return complete_result['valid'], complete_result

# Ensure directories exist
def ensure_directories():
    """Create all required data directories."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    PROSPECTS_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# Auto-create directories on import
ensure_directories()

# Helper functions for path construction
def get_prospect_dir(prospect_id: str) -> Path:
    """Get the directory path for a specific prospect."""
    return PROSPECTS_DIR / prospect_id

def get_research_file_path(prospect_id: str) -> Path:
    """Get the full path for a prospect's research file."""
    return get_prospect_dir(prospect_id) / RESEARCH_FILE_PATTERN.format(prospect_id=prospect_id)

def get_profile_file_path(prospect_id: str) -> Path:
    """Get the full path for a prospect's profile file.""" 
    return get_prospect_dir(prospect_id) / PROFILE_FILE_PATTERN.format(prospect_id=prospect_id)

def get_template_path(template_name: str) -> Path:
    """Get the full path for a template file."""
    return TEMPLATES_DIR / template_name

# For backward compatibility with string paths
def get_prospect_dir_str(prospect_id: str) -> str:
    """Get the directory path for a specific prospect as string."""
    return str(get_prospect_dir(prospect_id))

def get_research_file_path_str(prospect_id: str) -> str:
    """Get the full path for a prospect's research file as string."""
    return str(get_research_file_path(prospect_id))

def get_profile_file_path_str(prospect_id: str) -> str:
    """Get the full path for a prospect's profile file as string."""
    return str(get_profile_file_path(prospect_id))

def get_template_path_str(template_name: str) -> str:
    """Get the full path for a template file as string."""
    return str(get_template_path(template_name))
