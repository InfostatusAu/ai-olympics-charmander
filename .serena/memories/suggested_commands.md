# Development Commands & Workflow

## Essential Commands

### Environment & Dependencies
```bash
# Python environment check
python --version  # Should be 3.11+

# Install dependencies
uv sync

# Development dependencies
uv sync --group dev
```

### Testing (Constitutional TDD Required)
```bash
# Run all tests
uv run pytest tests/ --tb=short

# Run specific test categories
uv run pytest tests/contract/ -v     # Contract tests (MCP tools)
uv run pytest tests/integration/ -v # Integration tests
uv run pytest tests/unit/ -v        # Unit tests

# Test with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

### MCP Server Operations
```bash
# Start MCP server (development)
uv run python -m src.mcp_server.server

# Test MCP server functionality
uv run python -c "import asyncio; from src.mcp_server.tools import research_prospect; print(asyncio.run(research_prospect('example.com')))"
```

### Database Operations
```bash
# Database CLI commands
uv run python -m src.database.cli --help

# File manager operations
uv run python -m src.file_manager.cli --help

# Research operations
uv run python -m src.prospect_research.cli --help
```

### Git Workflow (Constitutional Requirement)
```bash
# Check current task status
cat specs/001-mcp-server-prospect/tasks.md | grep "^\- \[ \]" | head -5

# Commit after each task completion
git add .
git commit -m "feat: T0XX - [task description]"

# Check implementation status
git log --oneline | head -10
```

### Project Structure Commands
```bash
# View project structure
tree -I '__pycache__|*.pyc|.git' -L 3

# Check current implementation status
ls -la src/*/
ls -la tests/*/
ls -la data/*/
```

### Performance Validation
```bash
# Tool response time validation (<200ms requirement)
time uv run python -c "import asyncio; from src.mcp_server.tools import get_prospect_data; print(asyncio.run(get_prospect_data('test-id')))"

# Complete workflow timing (<30s requirement)  
time uv run python main.py research example-company.com
```

## Development Workflow

### Constitutional TDD Process
1. **Read Task**: Check `specs/001-mcp-server-prospect/tasks.md`
2. **Write Test**: Contract test MUST fail first
3. **Get Approval**: Validate test covers acceptance criteria
4. **Red**: Confirm test fails
5. **Green**: Implement minimal code to pass
6. **Refactor**: Clean up while keeping tests green
7. **Commit**: `git commit -m "feat: T0XX - description"`

### Task Execution Order
```bash
# Check current phase
grep -A 10 "## Phase 3\." specs/001-mcp-server-prospect/tasks.md

# Check parallel opportunities
grep "\[P\]" specs/001-mcp-server-prospect/tasks.md
```