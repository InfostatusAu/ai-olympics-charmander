# Implementation Plan: MCP Server Prospect Research (Simplified)

**Branch**: `001-mcp-server-prospect` | **Date**: September 13, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-server-prospect/spec.md`
**Update**: Simplified markdown-first architecture with minimal database operations

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
MCP Server for automated prospect research that generates AI-powered markdown intelligence reports. Simplified architecture focuses on markdown-first output with minimal database operations. The server provides 4 core tools for a streamlined 2-step workflow: research_prospect (Step 1: comprehensive research markdown), create_profile (Step 2: structured profile + talking points), plus data access tools for retrieval and search. Primary value is AI-generated markdown content stored as files, with SQLite for basic metadata tracking only.

## Technical Context
**Language/Version**: Python 3.11+ 
**Primary Dependencies**: MCP Python SDK, asyncio, Click, structlog, SQLite (built-in)
**Storage**: SQLite for minimal metadata + file system for markdown content
**Testing**: pytest + pytest-asyncio for TDD with real dependencies
**Target Platform**: Local development with cross-platform compatibility
**Project Type**: single (MCP server application)
**Performance Goals**: <200ms tool response time, <30s complete 2-step workflow
**Constraints**: Markdown-first design, minimal database complexity, real AI assistant integration
**Scale/Scope**: 4 MCP tools, 2-step research workflow, file-based content storage

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (MCP server only - meets constitutional limit)
- Using framework directly? YES (MCP Python SDK used directly, no wrapper classes)
- Single data model? YES (minimal Prospect entity only, no DTOs)
- Avoiding patterns? YES (no Repository/UoW - direct file operations and simple SQLite)

**Architecture**:
- EVERY feature as library? YES (4 libraries: mcp_server, prospect_research, file_manager, database)
- Libraries listed: 
  - mcp_server: MCP protocol implementation and tool registration
  - prospect_research: AI-powered research and profile generation logic
  - file_manager: Markdown file operations and content management
  - database: Minimal SQLite operations for metadata tracking
- CLI per library: research-cli, profile-cli, server-cli with --help/--version/--format
- Library docs: llms.txt format planned for all 4 libraries

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? YES (tests written first, must fail, then implement)
- Git commits show tests before implementation? YES (constitutional requirement)
- Order: Contract→Integration→E2E→Unit strictly followed? YES
- Real dependencies used? YES (actual SQLite, file system, MCP protocol - no mocks)
- Integration tests for: MCP tool contracts, file operations, database schemas? YES
- FORBIDDEN: Implementation before test, skipping RED phase

**Observability**:
- Structured logging included? YES (structlog for all operations)
- Frontend logs → backend? N/A (MCP server only)
- Error context sufficient? YES (JSON-RPC error handling with context)

**Versioning**:
- Version number assigned? YES (1.0.0 - initial release)
- BUILD increments on every change? YES (1.0.1, 1.0.2 for patches)
- Breaking changes handled? YES (MCP contract versioning, file format migration)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Simplified single project structure (Option 1)
src/
├── mcp_server/          # MCP protocol implementation library
│   ├── __init__.py
│   ├── server.py        # Main MCP server with tool registration
│   ├── tools.py         # Tool implementations (4 tools)
│   └── cli.py           # Server CLI commands
├── prospect_research/   # AI research and profile generation library
│   ├── __init__.py
│   ├── research.py      # Research logic and AI integration
│   ├── profile.py       # Profile + strategy generation
│   └── cli.py           # Research CLI commands
├── file_manager/        # Markdown file operations library
│   ├── __init__.py
│   ├── storage.py       # File system operations
│   ├── templates.py     # Markdown template management
│   └── cli.py           # File management CLI
└── database/            # Minimal SQLite operations library
    ├── __init__.py
    ├── models.py        # Prospect entity (minimal)
    ├── operations.py    # Basic CRUD operations
    └── cli.py           # Database CLI commands

tests/
├── contract/            # MCP tool contract tests
├── integration/         # End-to-end workflow tests  
├── unit/               # Individual library tests
└── fixtures/           # Test data and markdown samples

data/                   # Data storage (created at runtime)
├── prospects/          # Generated markdown files
├── templates/          # Markdown templates
└── database/           # SQLite database file
```

**Structure Decision**: Option 1 (single project) - MCP server application with 4 focused libraries

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/bash/update-agent-context.sh copilot` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks focused on simplified 4-library architecture
- Prioritize markdown-first workflow with minimal database operations
- Each MCP tool → contract test task [P]
- Each library → unit test task [P]
- Integration tasks for 2-step workflow validation
- File system operations and template management tasks

**Ordering Strategy**:
- TDD order: Contract tests → Integration tests → Library implementations
- Library dependency order: database → file_manager → prospect_research → mcp_server
- Mark [P] for parallel execution within library boundaries
- Focus on markdown content generation over complex database operations

**Estimated Output**: 15-20 simplified, focused tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - Simplified approach validated
- [x] Phase 1: Design complete (/plan command) - Markdown-first architecture defined  
- [x] Phase 2: Task planning complete (/plan command - simplified task approach described)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS - Simplified 4-library structure approved
- [x] Post-Design Constitution Check: PASS - Markdown-first approach reduces complexity
- [x] All NEEDS CLARIFICATION resolved - Simplified technical stack defined
- [ ] Complexity deviations documented - None required for simplified approach

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*