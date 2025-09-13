# Code Style & Conventions

## Python Code Style

### Type Hints (Required)
- All functions must have type hints for parameters and return values
- Use `from typing import` for complex types
- Use `Optional[Type]` or `Type | None` for nullable values
- Example:
```python
async def research_prospect(company: str) -> str:
    """Research prospect and return markdown report."""
```

### Docstrings (Required)
- All public functions, classes, and modules must have docstrings
- Use triple quotes `"""`
- First line: Brief description
- Include parameter descriptions for complex functions
- Example:
```python
def create_profile(prospect_id: str) -> dict[str, str]:
    """
    Transform research markdown into structured profile.
    
    Args:
        prospect_id: UUID of prospect to generate profile for
        
    Returns:
        Dictionary containing profile data and strategy
    """
```

### Naming Conventions
- **Functions**: snake_case (`research_prospect`, `create_profile`)
- **Variables**: snake_case (`company_name`, `prospect_data`)
- **Constants**: UPPER_SNAKE_CASE (`TOOLS`, `DEFAULT_TIMEOUT`)
- **Classes**: PascalCase (`ProspectModel`, `ResearchEngine`)
- **Modules**: snake_case (`file_manager`, `prospect_research`)

### Error Handling (Constitutional Requirement)
- Comprehensive error handling on all operations
- No sensitive info in error messages
- Use structured logging with context
- Example:
```python
try:
    result = await research_prospect(company)
except Exception as e:
    logger.error(f"Research failed for {company}: {e}")
    raise ValueError(f"Unable to research company: {company}")
```

### Async/Await Patterns
- All MCP tool functions are async
- Use `async def` for database operations
- Use `await` for I/O operations (file, network, database)
- Example:
```python
async def save_research(prospect_id: str, content: str) -> None:
    """Save research content to markdown file."""
    async with aiofiles.open(f"data/prospects/{prospect_id}_research.md", "w") as f:
        await f.write(content)
```

## File Organization

### Library Structure (4-Library Architecture)
```
src/
├── database/           # SQLite operations, models
├── file_manager/       # Markdown file operations  
├── prospect_research/  # AI research logic
└── mcp_server/        # MCP protocol implementation
```

### Import Organization
```python
# Standard library imports
import asyncio
import logging
from typing import Optional

# Third-party imports  
from mcp.server import Server
from sqlalchemy import create_engine

# Local imports
from src.database.models import Prospect
from .storage import save_markdown
```

### Configuration
- Use environment variables for sensitive data
- Store config in `.env` file (not committed)
- Use `data/` directory for generated content
- Keep database minimal, focus on markdown files

## Testing Conventions

### Test File Naming
- Contract tests: `test_[tool_name].py` in `tests/contract/`
- Integration tests: `test_[workflow_name].py` in `tests/integration/`
- Unit tests: `test_[library_name].py` in `tests/unit/`

### Test Function Naming
- Start with `test_`
- Descriptive names: `test_research_prospect_creates_markdown_file`
- Use `async def` for async tests

### Constitutional TDD Requirements
- Tests MUST be written first
- Tests MUST fail before implementation
- Contract tests validate MCP tool compliance
- Integration tests validate complete workflows
- Unit tests validate library functionality