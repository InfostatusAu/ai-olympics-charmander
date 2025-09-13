# Implementation Plan: MCP Server: Prospect Research Automation Engine

**Branch**: `001-mcp-server-prospect` | **Date**: September 13, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-server-prospect/spec.md`

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
The MCP server serves as the core intelligence layer for automated prospect identification and research, designed to eliminate the manual effort of qualifying cold calling opportunities. It provides four specialized tools (find_new_prospect, research_prospect, save_prospect, retrieve_prospect) working together to create a complete prospect research workflow. The system uses Python with PostgreSQL via Supabase local stack for data persistence, API-first data acquisition with Firecrawl/Playwright fallbacks, and seamless Gemini CLI integration through MCP protocol.

## Technical Context
**Language/Version**: Python 3.11+  
**Primary Dependencies**: Model Context Protocol (MCP), PostgreSQL, Supabase local stack, Firecrawl API, Playwright (API or MCP)  
**Storage**: PostgreSQL via Supabase local stack  
**Testing**: pytest with TDD approach  
**Target Platform**: Linux server with MCP protocol support  
**Project Type**: single (MCP server with modular tool libraries)  
**Performance Goals**: <200ms API response times, support multiple concurrent AI assistant connections  
**Constraints**: Seamless MCP protocol compliance, enterprise-grade database capabilities, minimal configuration overhead  
**Scale/Scope**: Multi-client MCP server, tiered data acquisition approach, future CRM integration scalability  

**Technical Implementation Details from User**:
- Architecture employs PostgreSQL via Supabase local stack for data persistence
- Data acquisition follows tiered approach: APIs (primary) → Firecrawl (intelligent web scraping) → Playwright (JavaScript-heavy sites fallback)
- Seamless Gemini CLI integration through MCP protocol for AI agent orchestration
- Specs-driven development with clear component contracts
- Modular architecture supporting component enhancement/replacement without system disruption

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (MCP server) - PASS
- Using framework directly? Yes (MCP protocol, PostgreSQL) - PASS
- Single data model? Yes (Prospect entities with normalized schema) - PASS
- Avoiding patterns? Direct data access, no unnecessary abstractions - PASS

**Architecture**:
- EVERY feature as library? Yes (find_prospect, research_prospect, save_prospect, retrieve_prospect as separate libraries) - PASS
- Libraries listed: 
  - prospect_finder (find_new_prospect tool + ICP matching)
  - prospect_researcher (research_prospect tool + data aggregation)
  - prospect_storage (save_prospect/retrieve_prospect + database operations)
  - mcp_server (protocol implementation + tool orchestration)
- CLI per library: Each library exposes CLI commands with --help/--version/--format - PLANNED
- Library docs: llms.txt format planned for each component - PLANNED

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? YES (tests written first, must fail) - COMMITTED
- Git commits show tests before implementation? YES (TDD workflow) - COMMITTED
- Order: Contract→Integration→E2E→Unit strictly followed? YES - COMMITTED
- Real dependencies used? YES (actual PostgreSQL, real API calls) - COMMITTED
- Integration tests for: MCP protocol compliance, database operations, API integrations - PLANNED
- FORBIDDEN: Implementation before test, skipping RED phase - ACKNOWLEDGED

**Observability**:
- Structured logging included? YES (operation tracking, tool call logging) - PLANNED
- Frontend logs → backend? N/A (server-side only with MCP client logging) 
- Error context sufficient? YES (detailed error responses, tool failure handling) - PLANNED

**Versioning**:
- Version number assigned? 1.0.0 (initial MCP server implementation) - ASSIGNED
- BUILD increments on every change? YES (semantic versioning) - COMMITTED
- Breaking changes handled? YES (MCP protocol versioning, migration strategies) - PLANNED

## Project Structure

### Documentation (this feature)
```
specs/001-mcp-server-prospect/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: Option 1 (Single project) - MCP server with modular tool libraries

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
- Load `/templates/tasks-template.md` as base structure
- Generate tasks from Phase 1 design artifacts:
  * data-model.md → database model creation tasks
  * contracts/mcp-tools.md → MCP tool implementation tasks  
  * contracts/openapi.json → contract test generation tasks
  * quickstart.md → integration test scenario tasks
- Follow constitutional TDD order: Contract tests → Integration tests → Implementation
- Each MCP tool becomes 3-4 tasks: contract test [P], integration test, tool implementation, CLI wrapper
- Database models follow entity dependencies: base entities → relationships → indexes

**Ordering Strategy**:
- **Phase A (Parallel Foundation)**: Database models, contract tests, tool schemas [P]
- **Phase B (Sequential Integration)**: MCP server setup, protocol implementation, tool registration
- **Phase C (Parallel Tools)**: Individual tool implementations [P] following failing tests
- **Phase D (Sequential Validation)**: Integration tests, quickstart validation, performance testing

**Estimated Task Breakdown**:
1. **Database Tasks (6 tasks)**: Models, migrations, seeders, indexes [P]
2. **Contract Tasks (8 tasks)**: JSON schemas, contract tests for 4 tools [P]  
3. **MCP Server Tasks (4 tasks)**: Protocol setup, capability negotiation, error handling
4. **Tool Implementation (12 tasks)**: 4 tools × 3 tasks each (test, implement, CLI) [P per tool]
5. **Integration Tasks (5 tasks)**: End-to-end tests, quickstart validation, performance tests
6. **Documentation Tasks (3 tasks)**: API docs, library docs, deployment guide

**Total Estimated Tasks**: 38 numbered, prioritized tasks with clear dependencies

**Parallel Execution Groups**:
- Database models can be implemented simultaneously [P]
- Contract tests are independent per tool [P]
- Tool implementations are independent after MCP server exists [P]
- Integration tests must run sequentially for proper validation

**Constitutional Compliance Verification**:
- Every implementation task has corresponding test task
- Tests must be written first and fail before implementation
- Library structure enforced with CLI interfaces
- Real database connections in all integration tests

**IMPORTANT**: This task generation phase will be executed by the `/tasks` command, NOT by the current `/plan` command.

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
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS  
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none required)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*