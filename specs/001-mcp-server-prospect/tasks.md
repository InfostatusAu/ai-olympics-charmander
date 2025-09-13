# Tasks: MCP Server Prospect Research (Simplified)

**Input**: Design documents from `/specs/001-mcp-server-prospect/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Extract: Python 3.11+, MCP Python SDK, SQLite, markdown-first architecture
   → 4 libraries: mcp_server, prospect_research, file_manager, database
2. Load design documents:
   → data-model.md: Minimal Prospect entity → model tasks
   → contracts/: 4 MCP tools → contract test tasks
   → research.md: MCP protocol best practices → setup tasks
3. Generate tasks by category:
   → Setup: project structure, dependencies, MCP server config
   → Tests: MCP tool contract tests, workflow integration tests
   → Core: database models, file operations, AI research logic, MCP tools
   → Integration: MCP server, workflow orchestration, markdown generation
   → Polish: unit tests, performance validation, documentation
4. Apply task rules:
   → Different libraries/files = mark [P] for parallel
   → MCP tool tests before implementation (TDD)
   → Library dependency order: database → file_manager → prospect_research → mcp_server
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph for 4-library architecture
7. Create parallel execution examples for library boundaries
8. Validate: All 4 MCP tools have tests, workflow coverage complete
9. Return: SUCCESS (tasks ready for simplified markdown-first execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project structure**: `src/` at repository root
- **Data storage**: `data/prospects/` for markdown files, `data/database/` for SQLite
- **Tests**: `tests/contract/`, `tests/integration/`, `tests/unit/`

## Phase 3.1: Setup
- [ ] T001 Create simplified project structure per implementation plan
- [ ] T002 Initialize Python project with MCP SDK, SQLite, Click dependencies
- [ ] T003 [P] Configure pytest + pytest-asyncio for TDD with real dependencies
- [ ] T004 [P] Set up data directory structure: data/prospects/, data/database/

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T005 [P] Contract test research_prospect MCP tool in tests/contract/test_research_prospect.py
- [ ] T006 [P] Contract test create_profile MCP tool in tests/contract/test_create_profile.py
- [ ] T007 [P] Contract test get_prospect_data MCP tool in tests/contract/test_get_prospect_data.py
- [ ] T008 [P] Contract test search_prospects MCP tool in tests/contract/test_search_prospects.py
- [ ] T009 [P] Integration test complete 2-step workflow in tests/integration/test_complete_workflow.py
- [ ] T010 [P] Integration test markdown file generation in tests/integration/test_markdown_generation.py
- [ ] T011 [P] Integration test MCP server tool discovery in tests/integration/test_mcp_server.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
### Database Library
- [ ] T012 [P] Prospect model in src/database/models.py
- [ ] T013 [P] Basic SQLite operations in src/database/operations.py
- [ ] T014 [P] Database CLI commands in src/database/cli.py

### File Manager Library  
- [ ] T015 [P] File system operations in src/file_manager/storage.py
- [ ] T016 [P] Markdown template management in src/file_manager/templates.py
- [ ] T017 [P] File management CLI in src/file_manager/cli.py

### Prospect Research Library
- [ ] T018 AI research logic and markdown generation in src/prospect_research/research.py
- [ ] T019 Profile + strategy generation in src/prospect_research/profile.py  
- [ ] T020 [P] Research CLI commands in src/prospect_research/cli.py

### MCP Server Library
- [ ] T021 MCP tool implementations (4 tools) in src/mcp_server/tools.py
- [ ] T022 MCP server with tool registration in src/mcp_server/server.py
- [ ] T023 [P] Server CLI commands in src/mcp_server/cli.py

## Phase 3.4: Integration
- [ ] T024 Connect prospect_research to file_manager for markdown output
- [ ] T025 Connect MCP tools to all underlying libraries 
- [ ] T026 MCP protocol JSON-RPC error handling
- [ ] T027 Structured logging with context for all operations

## Phase 3.5: Polish
- [ ] T028 [P] Unit tests for file operations in tests/unit/test_file_manager.py
- [ ] T029 [P] Unit tests for database operations in tests/unit/test_database.py
- [ ] T030 [P] Unit tests for research logic in tests/unit/test_prospect_research.py
- [ ] T031 [P] Unit tests for MCP tools in tests/unit/test_mcp_tools.py
- [ ] T032 Performance tests (<200ms tool response, <30s complete workflow)
- [ ] T033 [P] Update library documentation in llms.txt format
- [ ] T034 Remove code duplication across libraries
- [ ] T035 Execute quickstart.md user story validation

## Dependencies
- Setup (T001-T004) before tests (T005-T011)
- Tests (T005-T011) before implementation (T012-T023)
- Library order: database (T012-T014) → file_manager (T015-T017) → prospect_research (T018-T020) → mcp_server (T021-T023)
- T018-T019 depend on T015-T016 (research needs file operations)
- T021-T022 depend on T012-T020 (MCP tools need all libraries)
- Integration (T024-T027) depends on core implementation complete
- Polish (T028-T035) after integration complete

## Parallel Example
```
# Launch library tests together after setup:
Task: "Contract test research_prospect MCP tool in tests/contract/test_research_prospect.py"
Task: "Contract test create_profile MCP tool in tests/contract/test_create_profile.py" 
Task: "Contract test get_prospect_data MCP tool in tests/contract/test_get_prospect_data.py"
Task: "Contract test search_prospects MCP tool in tests/contract/test_search_prospects.py"

# Launch library implementations in dependency order:
# First: Database library (foundation)
Task: "Prospect model in src/database/models.py"
Task: "Basic SQLite operations in src/database/operations.py"
Task: "Database CLI commands in src/database/cli.py"

# Then: File manager (depends on data structure)
Task: "File system operations in src/file_manager/storage.py"  
Task: "Markdown template management in src/file_manager/templates.py"
Task: "File management CLI in src/file_manager/cli.py"

# Then: Research logic (depends on file operations)
# Finally: MCP server (depends on all libraries)
```

## Notes
- [P] tasks = different files/libraries, no dependencies within phase
- Verify all MCP tool tests fail before implementing tools
- Markdown-first approach: focus on file generation over complex database operations
- 4-library architecture enables parallel development within dependency constraints
- Each library has CLI for testing and standalone operation
- Commit after each task completion
- Avoid: same file conflicts, implementation before failing tests

## Task Generation Rules
*Applied during main() execution*

1. **From MCP Tool Contracts**:
   - Each of 4 MCP tools → contract test task [P]
   - Each tool → implementation task in tools.py
   
2. **From Data Model**:
   - Minimal Prospect entity → model creation task [P]
   - File operations → storage and template tasks [P]
   
3. **From User Stories (quickstart.md)**:
   - Complete 2-step workflow → integration test [P]
   - Step-by-step execution → workflow validation tests [P]
   - Prospect discovery → search functionality tests [P]

4. **From 4-Library Architecture**:
   - Each library → separate implementation tasks
   - Library dependencies → sequential ordering
   - CLI per library → parallel CLI tasks [P]

5. **Ordering by Simplified Dependencies**:
   - Setup → Tests → Database → File Manager → Research → MCP Server → Integration → Polish
   - Parallel execution within library boundaries
   - TDD: failing tests before any implementation

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All 4 MCP tools (research_prospect, create_profile, get_prospect_data, search_prospects) have contract tests
- [ ] Complete 2-step workflow has integration test coverage
- [ ] All contract tests come before tool implementation  
- [ ] Library dependency order respected (database → file_manager → prospect_research → mcp_server)
- [ ] Parallel tasks truly independent (different files/libraries)
- [ ] Each task specifies exact file path in src/ structure
- [ ] No task modifies same file as another [P] task within same phase
- [ ] Markdown-first architecture maintained (minimal database, rich file generation)
- [ ] User stories from quickstart.md have corresponding integration tests
- [ ] 4 library CLI commands have independent implementation tasks

**Estimated Task Count**: 35 tasks across simplified 4-library markdown-first architecture
**Parallel Opportunities**: 23 tasks marked [P] for efficient execution
**Critical Path**: Setup → Contract Tests → Database → File Manager → Research → MCP Server → Integration → Polish

This task list enables rapid development of the simplified MCP server with focus on AI-generated markdown intelligence and minimal database complexity, following constitutional TDD principles with clear library boundaries for parallel execution.
