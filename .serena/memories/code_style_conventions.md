# Code Style and Conventions

## Python Style
- **Type hints**: Required for all function signatures
- **Docstrings**: Google style docstrings for all classes and functions
- **Import order**: Standard library, third-party, local imports
- **Line length**: 100 characters maximum
- **Async/await**: Use async patterns consistently

## Naming Conventions
- **Functions/methods**: snake_case
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE
- **Files/modules**: snake_case
- **Variables**: snake_case

## Project Structure Patterns
- Each library has `__init__.py`, `cli.py` and core modules
- All CLI commands use Click framework
- Async functions for I/O operations
- Error handling with proper exceptions

## Testing Patterns
- Contract tests for MCP tools (tests/contract/)
- Integration tests for workflows (tests/integration/)
- Unit tests for individual modules (tests/unit/)
- Use fixtures for common test setup
- Assert specific error messages

## MCP Implementation
- Use MCP SDK properly with JSON-RPC 2.0
- Tool functions should be async
- Proper error handling with MCP error types
- Clear tool descriptions and parameter types

## Database Patterns
- SQLAlchemy models with proper relationships
- Async database operations
- Migrations support
- Minimal metadata, rich markdown content

## File Management
- Markdown-first approach for content
- Template-based file generation
- Proper file system error handling
- UTF-8 encoding for all text files