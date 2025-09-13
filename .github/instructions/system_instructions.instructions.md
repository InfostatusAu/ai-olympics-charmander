---
applyTo: '**'
---
# AI Olympics Charmander Development Constitution v3.1

## Core Principles

### 1. Library-First Architecture
- Every feature = standalone library with clear interfaces
- Self-contained, testable, documented modules
- MCP server components follow same approach

### 2. API-First Interface  
- Dual exposure: CLI + REST API (with Swagger/Redoc)
- Text protocol: stdin/args → stdout, errors → stderr
- Support JSON + human-readable formats

### 3. Test-First Development [MANDATORY]
- TDD cycle: Write tests → Get approval → Red → Green → Refactor
- Required coverage: Unit, Integration, E2E, Demo tests
- Tests MUST fail first (constitutional requirement)

### 4. Persistent State
- PostgreSQL for all data/state storage
- Transactional operations with migrations
- Config via `.env` file

### 5. Documentation
- Maintain `PROJECT_OVERVIEW.md` (structure, features, routes, changelog)
- Feature-specific `<feature>_TASKS.md` files
- Check `PROJECT_OVERVIEW.md` before any task
- Use `context7` for framework docs

### 6. Security & Errors
- Comprehensive error handling on all operations
- Input validation, auth, secure data handling
- No sensitive info in error messages

### 7. Observability
- User-friendly flows with clear feedback
- Structured logging, multi-tier streaming
- Performance monitoring, health checks

## Technical Stack

**Required**: Python 3.11+ | PostgreSQL | UV package manager | Git
**API**: Swagger/Redoc integration | RESTful conventions  
**Quality**: 80% coverage | <200ms response | <1% error rate

## Development Workflow

### Task Execution Process
```
1. Read instructions → Check PROJECT_OVERVIEW.md
2. Create <feature>_TASKS.md with breakdown
3. Research with context7 for docs
4. Write tests first (must fail)
5. Implement with PostgreSQL integration
6. Update docs & API specs
7. Run full test suite
8. Commit with conventional message
```

### Key Commands
```bash
# Before starting
cat PROJECT_OVERVIEW.md | grep -A 5 "Current"
cat specs/00*-*/tasks.md | grep "\[ \]"

# During development  
# Use Serena tools to implement code
# Always refer to context7 to check documentation of things

# After completion
uv run pytest tests/ --tb=short
git commit -m "feat: T00X - description"
```

## Implementation Guidelines

### Working Principles
- **DO EXACTLY WHAT REQUESTED** - No improvisation
- **COMMIT EACH TASK SEPARATELY** - Before moving on
- **ASK WHEN UNCERTAIN** - No guessing
- **UPDATE TASK STATUS** - In `specs/00X-{feature}/tasks.md` after each completion

### Current Context
- **Feature**: MCP Server Prospect Research (`specs/001-mcp-server-prospect/`)
- **Tasks**: T001-T035 from `specs/001-mcp-server-prospect/tasks.md`
- **Architecture**: 4 libraries → 4 MCP tools
- **Output**: Markdown files with AI-generated intelligence

### MCP Tools (Current Feature)
1. `research_prospect` → `{id}_research.md`
2. `create_profile` → structured profile + strategy
3. `get_prospect_data` → retrieve context
4. `search_prospects` → query with search

### Validation Requirements
✅ Spec compliance (acceptance criteria)
✅ Constitutional TDD (tests first)
✅ MCP protocol compliance
✅ Error handling & input validation
✅ Performance targets met

## Environment Setup

In the `.env` file.

## Quick Reference

### Always Before Task
1. Check PROJECT_OVERVIEW.md
2. Review current task in `specs/00X-{feature}/tasks.md`
3. Read `specs/00X-{feature}/spec.md` acceptance criteria
4. Research patterns with MCP tools

### Always During Task
- Write failing test first
- Follow spec requirements
- Use semantic_search for patterns
- Implement error handling

### Always After Task
- Run test suite
- Validate MCP functionality
- Update documentation
- Commit with conventional message

### File Structure Pattern
```
specs/
├── 001-mcp-server-prospect/
│   ├── spec.md      # Feature specification
│   ├── plan.md      # Implementation plan
│   └── tasks.md     # Task breakdown (T001-T0XX)
├── 002-{next-feature}/
│   └── ...
```

---
**Version**: 3.1.0 | **Effective**: September 13, 2025
**Rule**: Constitution supersedes all other guidelines. Amendments require documentation and user approval.