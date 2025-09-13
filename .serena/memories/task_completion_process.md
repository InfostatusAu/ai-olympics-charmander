# Task Completion Workflow

## When a Task is Completed

### 1. Run Tests
```bash
# Always run tests after implementation
uv run pytest tests/ --tb=short

# For specific areas:
uv run pytest tests/contract/ --tb=short  # MCP tool contracts
uv run pytest tests/integration/ --tb=short  # Workflow tests
uv run pytest tests/unit/ --tb=short  # Module tests
```

### 2. Validate Implementation
- Check that implementation meets specification acceptance criteria
- Verify MCP tools work correctly with protocol
- Ensure markdown generation follows templates
- Validate error handling works properly

### 3. Update Task Status
- Mark task as completed in `specs/001-mcp-server-prospect/tasks.md`
- Update any relevant documentation

### 4. Commit Changes
```bash
# Stage all changes
git add .

# Commit with conventional message format
git commit -m "feat: T0XX - descriptive task name"

# Examples:
# git commit -m "feat: T022 - implement MCP server with tool registration"
# git commit -m "feat: T024 - connect prospect research to file manager"
```

### 5. Prepare for Next Task
- Check dependencies for next tasks
- Ensure parallel tasks can be executed
- Review any integration requirements

## Quality Gates
- **Tests Pass**: All existing tests continue to pass
- **New Tests**: New functionality has appropriate test coverage
- **MCP Compliance**: Tools follow MCP protocol correctly
- **Performance**: Response times meet requirements (<200ms per tool)
- **Documentation**: Any new features are documented

## Error Recovery
If tests fail:
1. Review error messages carefully
2. Check implementation against specification
3. Verify dependencies are correct
4. Fix issues before committing
5. Re-run tests to confirm fixes