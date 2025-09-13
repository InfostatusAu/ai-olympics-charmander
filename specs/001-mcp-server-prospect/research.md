# Research: MCP Server Implementation

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine

## Best Practices and Patterns

### MCP Protocol Implementation
- **Capability Exchange**: Implement proper handshake with protocol version "2025-06-18"
- **Tool Discovery**: Expose tools through `ListToolsRequest` with complete schemas
- **Resource Management**: Use structured URIs like `prospect://data/prospect/{id}`
- **Error Handling**: Return proper JSON-RPC 2.0 error responses with meaningful messages
- **Async Operations**: Use `asyncio` throughout for non-blocking I/O operations

### Database Operations
- **Connection Management**: Use SQLAlchemy async engine with connection pooling
- **Transaction Handling**: Implement proper async context managers for transactions
- **Migration Strategy**: Use Supabase migrations for schema versioning
- **Query Optimization**: Create indexes for search operations, use prepared statements

### Data Acquisition Tier Strategy
1. **API First**: Always attempt direct API calls for official data sources
2. **Firecrawl Fallback**: Use structured web extraction for public company information
3. **Browser Automation**: Final fallback for complex interactive content only
4. **Caching Layer**: Store successful extractions to minimize external calls

### Error Handling and Resilience
- **Exponential Backoff**: Implement for all external API calls
- **Circuit Breaker**: Fail fast when services are consistently unavailable
- **Graceful Degradation**: Continue operation with partial data when possible
- **Structured Logging**: Use structured logs for debugging and monitoring

### Testing Strategy
- **Test-Driven Development**: Write tests before implementation
- **Real Dependencies**: Test against actual PostgreSQL and MCP protocol
- **Constitutional Compliance**: Validate ethical guidelines in automated tests
- **Integration Testing**: End-to-end MCP client interaction scenarios

## Research Tasks Completed

### 1. Model Context Protocol (MCP) Implementation
**Decision**: Use official MCP Python SDK with JSON-RPC 2.0 stdio transport  
**Rationale**: 
- Official SDK provides standardized implementation with proper protocol compliance
- Supports tools, resources, logging, and prompts capabilities
- Built-in JSON Schema validation and error handling
- Protocol version "2025-06-18" with proper capability negotiation

**Alternatives considered**:
- Custom JSON-RPC implementation: Rejected due to protocol complexity
- HTTP transport: Stdio transport preferred for AI assistant integration

**Best Practices**:
- Implement capability negotiation: tools (listChanged: true), resources (listChanged: true)
- Use proper JSON-RPC 2.0 error codes (-32000 to -32099 for tool errors)
- Tool schemas must include name, title, description, and inputSchema
- Resource URIs follow pattern: `prospect://collection/id` format

### 2. PostgreSQL with Supabase Local Stack
**Decision**: Use asyncpg with SQLAlchemy async engine for PostgreSQL via Supabase CLI  
**Rationale**:
- Supabase CLI provides complete PostgreSQL environment with migrations
- asyncpg offers the fastest async PostgreSQL driver for Python
- SQLAlchemy async provides ORM benefits with proper async patterns
- Local development matches production capabilities with minimal configuration

**Alternatives considered**:
- Direct PostgreSQL: Manual setup complexity and migration management
- SQLite: Insufficient for concurrent connections and enterprise features
- psycopg3 async: asyncpg has better performance characteristics

**Best Practices**:
- Use `create_async_engine` with asyncpg dialect: `postgresql+asyncpg://`
- Implement connection pooling: `pool_size=5, max_overflow=10`
- Use Supabase migrations: `supabase migration new` and `supabase db push`
- Async session management with `AsyncSession` and `async with` patterns

### 3. Firecrawl API for Web Data
**Decision**: Use Firecrawl Python SDK for structured web data extraction with markdown output  
**Rationale**:
- Official Python SDK provides robust crawling with rate limiting and error handling
- Markdown output format is structured and LLM-friendly for prospect analysis
- Built-in respect for robots.txt and rate limiting prevents server overload
- JavaScript rendering capability ensures modern website compatibility

**Alternatives considered**:
- BeautifulSoup + requests: Manual rate limiting, no JS rendering, robots.txt handling
- Scrapy: Over-engineered for single-page extraction, complex setup
- Playwright direct: No rate limiting, manual content extraction logic

**Best Practices**:
- Initialize with API key: `firecrawl = FirecrawlApp(api_key=api_key)`
- Use scrape_url with markdown extraction: `formats=['markdown']`
- Implement exponential backoff: Handle `TimeoutError` and `HTTPError` exceptions
- Respect rate limits: Built-in throttling, monitor quota usage

### 4. Playwright MCP as Fallback Browser Automation
**Decision**: Use Playwright MCP server for browser automation fallback via accessibility snapshots  
**Rationale**:
- MCP-compatible server provides standardized browser automation interface
- Accessibility snapshots offer structured page representation without direct DOM access
- Element interaction through refs enables reliable automation
- Background process management for complex JavaScript interactions

**Alternatives considered**:
- Direct Playwright: Manual setup, MCP protocol implementation complexity
- Selenium: Less reliable element interaction, no MCP integration
- Puppeteer: Node.js dependency, manual MCP wrapper needed

**Best Practices**:
- Use `browser_navigate` for page loading: Standard URL navigation
- Capture structure with `browser_snapshot`: Returns accessibility tree with element refs
- Interact via refs: `browser_click`, `browser_type` using element references from snapshots
- Handle dynamic content: `browser_wait_for` with text or time-based waiting

### 5. Testing Strategy with Real Dependencies
**Decision**: TDD with actual PostgreSQL and API connections  
**Rationale**:
- Constitutional requirement for real dependencies in tests
- Integration tests validate actual MCP protocol compliance
- Database tests ensure data integrity and performance
- API tests validate external service integration

**Alternatives considered**:
- Mock-based testing: Violates constitutional requirements
- Unit-only testing: Insufficient for integration validation

**Best Practices**:
- Test database setup/teardown for each test suite
- Use test-specific database schemas to avoid conflicts
- Implement contract tests for MCP tool schemas
- Create end-to-end tests simulating AI assistant workflows

### 6. Performance and Concurrency
**Decision**: Async/await pattern with connection pooling  
**Rationale**:
- MCP protocol supports multiple concurrent tool calls
- Database connection pooling essential for multi-client support
- Async pattern enables non-blocking external API calls
- Supports <200ms response time requirement

**Best Practices**:
- Use asyncio for MCP server implementation
- Implement connection pooling with configurable limits
- Add request queuing for external API rate limiting
- Monitor and log performance metrics

## Technology Stack Finalized

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| MCP Server | Python MCP SDK | Latest | Protocol implementation |
| Database | PostgreSQL | 15+ | Data persistence |
| Local Stack | Supabase CLI | Latest | Development environment |
| Web Scraping | Firecrawl API | v1 | Intelligent content extraction |
| Browser Automation | Playwright MCP | Latest | JavaScript-heavy site handling |
| Testing | pytest + pytest-asyncio | Latest | TDD framework |
| CLI Framework | Click | Latest | Command-line interfaces |
| Database ORM | SQLAlchemy + asyncpg | Latest | Async database operations |
| Logging | structlog | Latest | Structured logging |

## Architecture Decisions

### Data Flow
```
AI Assistant → MCP Client → MCP Server → Tool Libraries → Data Sources
                                    ↓
                              PostgreSQL Database
```

### Tool Execution Pattern
1. MCP Client discovers available tools
2. AI Assistant selects appropriate tool based on user query
3. MCP Server validates tool parameters using JSON schema
4. Tool library executes business logic with error handling
5. Results returned through MCP protocol to AI Assistant

### Database Schema Approach
- Normalized schema for prospect entities
- JSONB fields for flexible research data storage
- Indexes on search fields for performance
- Migration scripts for schema evolution

## Unknowns Resolved

All technical contexts have been researched and verified through context7:
- ✅ MCP protocol implementation approach confirmed with Python SDK capabilities
- ✅ Database technology and async patterns verified with SQLAlchemy + asyncpg
- ✅ Data acquisition methods validated with Firecrawl Python SDK and Playwright MCP
- ✅ Supabase CLI capabilities confirmed for local development workflow
- ✅ Library architecture patterns aligned with async/await best practices
- ✅ Testing approach with pytest-asyncio confirmed for real dependency testing
- ✅ Performance requirements mapped to connection pooling and caching strategies

## Technical Specification Accuracy

Context7 verification completed - all technical decisions validated against:
- MCP Python SDK documentation and capabilities
- Supabase CLI local development features
- Firecrawl API Python integration patterns  
- Playwright MCP server automation capabilities
- PostgreSQL async driver performance characteristics

## Next Phase Prerequisites Met

Phase 0 complete - all NEEDS CLARIFICATION items resolved with verified technical accuracy. Ready to proceed to Phase 1 design and contracts.
