# AI Olympics Charmander - Gemini CLI Context

**Project**: MCP Server: Prospect Research Automation Engine  
**Current Feature**: 001-mcp-server-prospect  
**Version**: 1.0.0  
**Updated**: September 13, 2025

## Project Overview

Library-first MCP server implementation providing automated prospect research capabilities through four specialized tools. Built with Python 3.11+, PostgreSQL via Supabase local stack, and tiered data acquisition approach (APIs → Firecrawl → Playwright).

## Current Architecture

### Core Libraries
- **prospect_finder**: ICP matching and lead discovery
- **prospect_researcher**: Data aggregation and intelligence compilation  
- **prospect_storage**: Database operations and CRUD functionality
- **mcp_server**: Protocol implementation and tool orchestration

### Technology Stack
- **Language**: Python 3.11+ with asyncio for MCP protocol
- **Database**: PostgreSQL 15+ via Supabase local stack with connection pooling
- **Data Sources**: API-first approach → Firecrawl API → Playwright MCP fallback
- **Testing**: pytest with TDD approach, real dependencies (no mocks)
- **MCP Protocol**: JSON-RPC 2.0 with tools, resources, logging, prompts capabilities

### MCP Tools Implemented
1. `find_new_prospect` - Discover qualified leads matching ICP criteria
2. `research_prospect` - Compile comprehensive company intelligence
3. `save_prospect` - Persist prospect profiles to database
4. `retrieve_prospect` - Query stored prospect data with filtering

## Constitutional Compliance

### Library-First Development ✅
- Each tool implemented as independent library with CLI interface
- Clear separation of concerns and boundaries
- Modular architecture supporting component replacement

### API-First Interface ✅  
- All libraries expose CLI commands with --help, --version, --format
- OpenAPI schema defined for MCP tool contracts
- JSON and human-readable format support

### Test-First Development ✅
- TDD cycle enforced: Tests → User approval → Implementation
- Real database connections in integration tests
- Contract tests for MCP protocol compliance
- End-to-end tests simulating AI assistant workflows

### Data Persistence ✅
- PostgreSQL database with proper indexing and constraints
- JSONB fields for flexible research data storage
- Migration scripts for schema evolution
- Environment variables in .env configuration

## Recent Changes (Last 3 Features)

### 001-mcp-server-prospect (Current)
- **Added**: Complete MCP server specification and design
- **Tech**: Model Context Protocol, Supabase local stack, tiered data acquisition
- **Status**: Phase 1 complete (design and contracts)

## Development Commands

### Setup and Testing
```bash
# Environment setup
uv sync
supabase start
uv run alembic upgrade head

# Run tests (TDD workflow)
uv run pytest tests/contract/  # Contract tests first
uv run pytest tests/integration/  # Integration tests
uv run pytest tests/unit/  # Unit tests last

# Start MCP server
uv run python -m mcp_server.main
```

### Library CLI Commands
```bash
# Prospect finder library
uv run python -m prospect_finder --help
uv run python -m prospect_finder find --icp "tech-startups" --limit 10

# Prospect researcher library  
uv run python -m prospect_researcher --help
uv run python -m prospect_researcher research --domain "techcorp.com"

# Prospect storage library
uv run python -m prospect_storage --help
uv run python -m prospect_storage save --file prospect.json
```

### Database Operations
```bash
# Database management
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
uv run python scripts/seed_icps.py
```

## Key Patterns

### MCP Protocol Implementation
- JSON-RPC 2.0 server with capability negotiation
- Tool schema validation using JSON Schema
- Resource URI pattern: `prospect://prospects/{id}`
- Structured error responses with retry logic

### Data Acquisition Tiering
1. **Primary**: Structured APIs (Apollo, Clearbit) with rate limiting
2. **Secondary**: Firecrawl API for intelligent web scraping
3. **Fallback**: Playwright MCP for JavaScript-heavy sites

### Database Design
- Normalized schema with JSONB for flexibility
- Composite indexes for query performance
- Referential integrity with cascade/restrict patterns
- Audit trails and soft deletes where appropriate

## Performance Requirements

- **Response Time**: <200ms for MCP tool calls (excluding external APIs)
- **Concurrency**: Multiple AI assistant connections supported
- **Database**: Connection pooling with configurable limits
- **Rate Limiting**: Respectful external API usage with backoff

## Security Considerations

- **Input Validation**: JSON Schema validation for all tool parameters
- **SQL Injection**: Parameterized queries with SQLAlchemy
- **API Security**: Environment variable configuration for keys
- **Error Handling**: No sensitive information in error responses

## Next Phase

Ready for Phase 2 task generation. The `/tasks` command will create detailed implementation tasks based on:
- Contract tests for each MCP tool
- Database model creation following data-model.md
- Integration tests for user story validation  
- Library implementation following TDD principles

<!-- AUTO-UPDATED SECTION - DO NOT EDIT MANUALLY -->
<!-- RECENT_CHANGES_START -->
<!-- RECENT_CHANGES_END -->
<!-- TECH_ADDITIONS_START -->
<!-- TECH_ADDITIONS_END -->
<!-- AUTO-UPDATED SECTION END -->
