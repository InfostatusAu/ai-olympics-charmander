# Tasks: LLM Intelligence Middleware

**Input**: Design documents from `/specs/002-improve-research-with-llm/`
**Prerequisites**: plan.md (✅), spec.md (✅)

## Execution Flow (main)
```
1. Load plan.md from feature directory ✅
   → Extract: tech stack (Python 3.11+, AWS Bedrock, boto3), 5-library structure
   → Architecture: Intelligence middleware between raw data and template generation
2. Load spec.md ✅
   → Extract: 8 functional requirements for LLM enhancement
   → Target: research_prospect and create_profile tools enhancement
3. Generate tasks by category:
   → Setup: LLM module creation, AWS Bedrock integration
   → Tests: Enhanced tool tests with AI vs manual comparison
   → Core: Intelligence middleware, enhanced research/profile logic
   → Integration: MCP server configuration, fallback handling
   → Polish: Performance validation, documentation updates
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup
- [x] T001 Create data_sources module structure in src/data_sources/
- [x] T002 Create llm_enhancer module structure in src/llm_enhancer/
- [x] T003 [P] Install complete dependencies (AWS Bedrock, Apollo, Serper, Playwright MCP) in pyproject.toml
- [x] T004 [P] Configure environment variables for complete integration in .env.example

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T005 [P] Complete data source integration test in tests/integration/test_complete_data_sources.py
- [x] T006 [P] Enhanced research_prospect contract test in tests/contract/test_research_prospect_llm.py
- [x] T007 [P] Enhanced create_profile contract test in tests/contract/test_create_profile_llm.py
- [x] T008 [P] LLM middleware integration test in tests/integration/test_llm_middleware.py
- [x] T009 [P] Fallback mechanism test in tests/integration/test_llm_fallback.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
### Data Source Implementation
- [x] T010 [P] Apollo.io API integration in src/data_sources/apollo_source.py
- [x] T011 [P] Serper API integration in src/data_sources/serper_source.py
- [x] T012 [P] Playwright MCP browser tools in src/data_sources/playwright_source.py
- ✅ T013 [P] Enhanced LinkedIn source in src/data_sources/linkedin_source.py
- ✅ T014 [P] Enhanced job boards source in src/data_sources/job_boards_source.py
- ✅ T015 [P] Enhanced news source in src/data_sources/news_source.py
- ✅ T016 [P] Enhanced government registries source in src/data_sources/government_source.py
- ✅ T017 Data source manager with error handling in src/data_sources/manager.py

### LLM Intelligence Implementation
- [x] T018 [P] AWS Bedrock client wrapper in src/llm_enhancer/client.py
- [x] T019 [P] Research data analyzer in src/llm_enhancer/analyzers.py
- [x] T020 [P] Intelligence middleware coordinator in src/llm_enhancer/middleware.py
- [x] T021 [P] LLM enhancer CLI utilities in src/llm_enhancer/cli.py

### Enhanced Research Logic
- [x] T022 Enhanced research logic with complete data collection + LLM analysis in src/prospect_research/research.py
- [x] T023 Enhanced profile logic with AI strategy generation in src/prospect_research/profile.py

## Phase 3.4: Integration
- [x] T024 MCP server complete API configuration parameters in src/mcp_server/cli.py
- [x] T025 Enhanced MCP tools with complete data integration + LLM in src/mcp_server/tools.py
- [x] T026 Graceful fallback handling in src/llm_enhancer/middleware.py
- [x] T027 Environment configuration validation in src/config.py

## Phase 3.5: Polish
- [x] T028 [P] Unit tests for data source modules in tests/unit/test_data_sources.py
- [x] T029 [P] Unit tests for LLM client in tests/unit/test_llm_client.py
- [x] T030 [P] Unit tests for analyzers in tests/unit/test_llm_analyzers.py
- [x] T031 [P] Performance tests for complete workflow in tests/unit/test_complete_performance.py
- [ ] T032 [P] Update llms.txt documentation for all enhanced modules
- [ ] T033 Integration validation with complete data source + LLM workflow testing

## Dependencies
- Setup (T001-T004) before Tests (T005-T009)
- Tests (T005-T009) before Core Implementation (T010-T023)
- Data Sources (T010-T017) before LLM Implementation (T018-T021)
- T017 (data source manager) blocks T022 (enhanced research logic)
- T018 (LLM client) blocks T019, T020 (analyzers, middleware)
- T022, T023 (enhanced logic) require T017 (data manager) and T020 (middleware)
- Core (T010-T023) before Integration (T024-T027)
- Integration before Polish (T028-T033)

## Parallel Example
```bash
# Launch setup tasks together:
Task: "Create data_sources module structure in src/data_sources/"
Task: "Create llm_enhancer module structure in src/llm_enhancer/"
Task: "Install complete dependencies (AWS Bedrock, Apollo, Serper, Playwright MCP) in pyproject.toml"
Task: "Configure environment variables for complete integration in .env.example"

# Launch contract tests together:
Task: "Complete data source integration test in tests/integration/test_complete_data_sources.py"
Task: "Enhanced research_prospect contract test in tests/contract/test_research_prospect_llm.py"
Task: "Enhanced create_profile contract test in tests/contract/test_create_profile_llm.py"
Task: "LLM middleware integration test in tests/integration/test_llm_middleware.py"

# Launch data source implementations together:
Task: "Apollo.io API integration in src/data_sources/apollo_source.py"
Task: "Serper API integration in src/data_sources/serper_source.py"
Task: "Playwright MCP browser tools in src/data_sources/playwright_source.py"
Task: "Enhanced LinkedIn source in src/data_sources/linkedin_source.py"
Task: "Enhanced job boards source in src/data_sources/job_boards_source.py"

# Launch LLM module files together:
Task: "AWS Bedrock client wrapper in src/llm_enhancer/client.py"
Task: "Research data analyzer in src/llm_enhancer/analyzers.py"
Task: "LLM enhancer CLI utilities in src/llm_enhancer/cli.py"
```

## Task Generation Rules Applied

### From plan.md Analysis:
- **Intelligence Middleware Pattern**: LLM sits between raw data collection and template generation
- **Complete Data Source Integration**: Implement ALL 9 missing data sources (Apollo.io, Serper, Playwright MCP, etc.)
- **Manual Logic Replacement**: Replace hardcoded rules in research.py and profile.py
- **6-Library Architecture**: Add data_sources and llm_enhancer to existing 4 libraries
- **Fallback Strategy**: Graceful degradation to manual processing
- **AWS Bedrock Integration**: Claude Sonnet model with boto3

### From spec.md Analysis:
- **FR-001, FR-002**: Enhanced research_prospect and create_profile (T012, T013)
- **FR-003, FR-004**: search_prospects and get_prospect_data unchanged (no tasks)
- **FR-005**: Backward compatible MCP tool interfaces (T015)
- **FR-006**: Configurable LLM providers with fallback (T008, T016)
- **FR-007**: Response times under 10 seconds (T020)
- **FR-008**: Intelligent error handling (T016)

### Implementation Strategy:
1. **Setup Phase**: Create data source infrastructure and LLM infrastructure
2. **TDD Phase**: Contract tests ensuring complete data collection + enhanced intelligence
3. **Data Source Phase**: Implement all 9 missing data sources with error handling
4. **LLM Phase**: Intelligence middleware and AI-enhanced analysis
5. **Enhanced Logic Phase**: Replace manual logic with data source manager + LLM analysis
6. **Integration Phase**: MCP server configuration and fallback mechanisms
7. **Polish Phase**: Performance validation and comprehensive testing

## Enhanced Tools Coverage:
- ✅ **research_prospect**: Replace with complete data source collection + LLM business intelligence (T022)
- ✅ **create_profile**: Replace hardcoded rules with AI conversation strategy based on comprehensive data (T023)
- ✅ **get_prospect_data**: Returns enhanced content from above tools (no changes needed)
- ✅ **search_prospects**: Unchanged functionality (no changes needed)

## Key Implementation Files:
- **New Data Sources Module**: `src/data_sources/` (T001, T010-T017)
- **New LLM Module**: `src/llm_enhancer/` (T002, T018-T021)
- **Enhanced Research**: `src/prospect_research/research.py` (T022)
- **Enhanced Profile**: `src/prospect_research/profile.py` (T023)
- **MCP Integration**: `src/mcp_server/tools.py`, `src/mcp_server/cli.py` (T024-T025)
- **Configuration**: `src/config.py`, `.env.example` (T004, T027)

## Validation Checklist
*GATE: Checked before marking complete*

- [x] All enhanced tools have contract tests (T006-T007)
- [x] Complete data source integration tested (T005)
- [x] LLM middleware has integration tests (T008-T009)
- [x] Tests come before implementation (TDD enforced)
- [x] Parallel tasks target different files
- [x] Each task specifies exact file path
- [x] Fallback mechanisms tested (T009, T026)
- [x] Performance requirements validated (T031)
- [x] All 9 data sources implemented (T010-T016)

## Notes
- **Manual Logic Target**: Replace string manipulation and hardcoded rules with comprehensive data + AI analysis
- **Complete Data Coverage**: Implement ALL 9 data sources from prospect_research_approach.md
- **Template Compatibility**: No template changes, dramatically improved content quality
- **Error Resilience**: Each data source failure logged but process continues
- **Constitutional TDD**: Tests must fail before implementation begins
- **Commit Strategy**: Each task completion requires separate commit

---
**Total Tasks**: 33 focused tasks covering complete data source + intelligence middleware implementation
**Estimated Complexity**: High (adds new data sources module + LLM enhancement)
**Key Risk Mitigation**: Comprehensive fallback strategy ensures system reliability
**Performance Target**: <120 seconds for complete analysis (all 9 sources), graceful degradation
