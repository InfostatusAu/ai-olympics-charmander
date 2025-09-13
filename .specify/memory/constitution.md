# AI Olympics Charmander Constitution

## Core Principles

### I. Library-First Development
Every feature starts as a standalone library with clear interfaces and dependencies. Libraries must be self-contained, independently testable, and well-documented. Each library serves a specific purpose - no organizational-only libraries. MCP server components follow the same library-first approach for modularity and testability.

### II. API-First Interface
Every library exposes functionality via both CLI and API endpoints. API documentation must be available through Swagger/Redoc. Text in/out protocol: stdin/args → stdout, errors → stderr. Support JSON + human-readable formats. All API endpoints follow RESTful conventions and include proper error handling.

### III. Test-First Development (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement. Red-Green-Refactor cycle strictly enforced. Every feature requires comprehensive test coverage including:
- Unit tests for individual functions
- Integration tests for API endpoints
- End-to-end tests demonstrating complete user workflows
- "How it works" demonstration tests for each feature

### IV. Data Persistence & State Management
Always store relevant data, application states, and user states in PostgreSQL database. All data operations must be transactional and include proper error handling. Database schema changes require migration scripts. Use environment variables for configuration stored in `.env` file.

### V. Documentation & Project Management
Always maintain `PROJECT_OVERVIEW.md` with current project structure, features, dependencies, API routes, and changelog. Create feature-specific `<feature_name>_TASKS.md` files for task management. Check `PROJECT_OVERVIEW.md` before starting any new task. Use `context7` for studying dependencies and frameworks documentation.

### VI. Security & Error Handling
Implement comprehensive error catching handlers for all operations. Follow security best practices including input validation, authentication, authorization, and secure data handling. All API endpoints must validate inputs and handle edge cases gracefully. Never expose sensitive information in error messages.

### VII. User Experience & Observability
Implement user-friendly flows with clear feedback and status indicators. Structured logging required for all operations. Multi-tier log streaming for debugging. Performance monitoring and health checks mandatory for production systems.

## Technical Standards

### Technology Stack Requirements
- **Programming Language**: Python (>=3.11)
- **Database**: PostgreSQL via local stack
- **Configuration**: Environment variables in `.env` file
- **API Documentation**: Swagger/Redoc integration mandatory
- **Package Management**: UV for dependency management
- **Version Control**: Git with conventional commits

### Development Environment
- Local PostgreSQL stack for development and testing
- Environment isolation using virtual environments
- Configuration management through `.env` files
- API documentation served alongside application
- Automated dependency resolution and updates

### Quality Standards
- Code coverage minimum 80% for all modules
- API response times under 200ms for standard operations
- Database queries optimized with proper indexing
- Error rates below 1% in production
- Security scanning for all dependencies

## Development Workflow

### Feature Development Process
1. **Planning Phase**: Read Serena's initial instructions, check `PROJECT_OVERVIEW.md`
2. **Specification**: Create feature specification following template
3. **Task Management**: Create `<feature_name>_TASKS.md` with todo breakdown
4. **Research**: Use `context7` to study relevant documentation
5. **Test Design**: Write comprehensive tests before implementation
6. **Implementation**: Follow TDD cycle with PostgreSQL integration
7. **Documentation**: Update `PROJECT_OVERVIEW.md` and API docs
8. **Testing**: Run full test suite including integration tests
9. **Commit**: Commit completed feature with conventional commit message

### Code Review Requirements
- All code must pass automated tests
- Security review for external integrations
- Performance review for database operations
- Documentation review for completeness
- API contract validation

### Deployment Gates
- All tests pass (unit, integration, e2e)
- API documentation updated
- Database migrations tested
- Security scan clean
- Performance benchmarks met

## Governance

Constitution supersedes all other development practices and guidelines. All code reviews and pull requests must verify compliance with constitutional principles. 

### Amendment Process
- Amendments require full documentation of changes and impact analysis
- All dependent templates and documentation must be updated
- Migration plan required for breaking changes
- User approval required for constitutional changes

### Compliance Requirements
- All feature implementations must demonstrate constitutional compliance
- Regular constitutional reviews during sprint planning
- Complexity additions must be justified against simplicity principles
- Use Serena's guidance for runtime development decisions

### Version Control & Change Management
- MAJOR.MINOR.PATCH versioning for constitution updates
- Breaking changes require major version increment
- All changes tracked in constitution history
- Template synchronization required for each update

**Version**: 3.0.0 | **Ratified**: September 13, 2025 | **Last Amended**: September 13, 2025