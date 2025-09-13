"""Shared configuration constants and paths for the prospect research system."""
import os
from pathlib import Path

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
