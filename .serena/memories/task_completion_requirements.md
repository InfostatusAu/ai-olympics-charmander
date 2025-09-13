# Task Completion Requirements

## Constitutional Requirements (MANDATORY)

### Test-First Development (TDD)
1. **Write failing test first** - Contract test MUST fail before any implementation
2. **Get approval** - Validate test covers specification acceptance criteria  
3. **Red-Green-Refactor cycle** - Implement minimal code to pass, then refactor
4. **Commit after each task** - `git commit -m "feat: T0XX - description"`

### Quality Gates
- **Contract Tests**: All 4 MCP tools must have failing contract tests before implementation
- **Integration Tests**: Complete 2-step workflow must be tested
- **Performance**: Tool response <200ms, complete workflow <30s
- **Coverage**: Focus on critical paths and MCP tool compliance

### Architecture Compliance
- **4-Library Structure**: Maintain separation of concerns
- **Markdown-First**: Rich content in files, minimal database metadata
- **MCP Protocol**: Standard JSON-RPC 2.0 interface compliance
- **Dependency Order**: database → file_manager → prospect_research → mcp_server

## After Task Completion Checklist

### 1. Run Tests
```bash
# Full test suite
uv run pytest tests/ --tb=short

# Check specific categories
uv run pytest tests/contract/ -v    # Contract tests
uv run pytest tests/integration/ -v # Integration tests
```

### 2. Validate MCP Functionality
```bash
# Test MCP server startup
uv run python -m src.mcp_server.server &
sleep 2 && kill %1

# Test specific tool (if implemented)
uv run python -c "import asyncio; from src.mcp_server.tools import research_prospect; print('Tool available')"
```

### 3. Performance Validation (For Core Features)
```bash
# Tool response time
time uv run python -c "import asyncio; from src.mcp_server.tools import get_prospect_data; asyncio.run(get_prospect_data('test-id'))"

# Database operations
time uv run python -c "from src.database.operations import list_prospects; print('DB responsive')"
```

### 4. Code Quality
```bash
# Check for syntax errors
uv run python -m py_compile src/**/*.py

# Check import structure
uv run python -c "from src.mcp_server.server import main; print('Imports valid')"
```

### 5. Documentation Updates
- Update `PROJECT_OVERVIEW.md` progress tracking if milestone reached
- Mark task as complete in `specs/001-mcp-server-prospect/tasks.md`
- Add any important discoveries to project memories

### 6. Git Commit (MANDATORY)
```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: T0XX - [specific task description]"

# Examples:
# git commit -m "feat: T022 - MCP server with tool registration"  
# git commit -m "test: T005 - Contract test research_prospect MCP tool"
# git commit -m "docs: Update tasks.md with T022 completion"
```

## Error Handling Requirements
- Comprehensive error handling on all operations
- Input validation for all MCP tool parameters
- Structured logging with context for debugging
- No sensitive information in error messages
- Graceful fallbacks where possible

## Performance Standards
- **Tool Response**: <200ms per MCP tool call
- **Workflow Complete**: <30s for complete 2-step research process
- **Database Operations**: <50ms for simple queries
- **File Operations**: <100ms for markdown read/write

## Documentation Standards
- Update task status in `specs/001-mcp-server-prospect/tasks.md`
- Maintain `PROJECT_OVERVIEW.md` for milestone tracking
- Create feature-specific documentation as needed
- Use clear, actionable commit messages