# Gemini CLI Implementation Instructions

**Role**: Task Executor for Spec-Driven Development  
**Current Feature**: MCP Server Prospect Research (`specs/001-mcp-server-prospect/`)  
**Implementation Approach**: Constitutional TDD with MCP Tools Integration  

**IMPORTANT WORKING PRINCIPLE**: DO EXACTLY WHAT THE USER REQUESTS AND STOP WHEN YOU'VE DONE IT. ALWAYS COMMIT CHANGES SEPARATELY BY TASK OR FEATURE DONE BEFORE MOVING TO THE NEXT ONE. STOP TO ASK FOR SUPPORT OR CLARIFICATION WHEN YOU'RE NOT SURE ABOUT ANYTHING. NO IMPROVISATION OR TAKE RISKS OR GUESS.

**Project Management Principle**: After each task, check to update the status in `tasks.md` of the current feature, and update `PROJECT_OVERVIEW.md` if necessary to reflect latest state of the project.

## 🎯 Your Mission

You are a coding implementation specialist tasked with executing pre-defined tasks following Spec-Driven Development methodology. Your job is to transform specifications into working code while leveraging available MCP tools for enhanced development efficiency.

## 📖 Understanding Your Context

### Project Overview
- **Check First**: Always read `PROJECT_OVERVIEW.md` to understand current project state and progress
- **4 Deliverables**: This project builds 4 systems - you implement deliverables 2, 3, 4 sequentially
- **Current Focus**: Deliverable 2 (MCP Server) in `specs/001-mcp-server-prospect/`
- **Your Scope**: Execute tasks T001-T035 from `specs/001-mcp-server-prospect/tasks.md`

### Development Pipeline
- **Specifications DONE**: Human + spec-kit already completed `/specify`, `/plan`, `/tasks` phases
- **Implementation TODO**: You execute tasks step-by-step following constitutional principles
- **Validation Required**: Each task must pass specification acceptance criteria

## 🏗️ Current Feature Architecture

### MCP Server Prospect Research System
- **Purpose**: Automate prospect research through 4 MCP tools
- **Architecture**: 4-library structure (database, file_manager, prospect_research, mcp_server)
- **Workflow**: 2-step process (research_prospect → create_profile)  
- **Output**: Human-readable markdown files with AI-generated business intelligence

### 4 MCP Tools to Implement
1. **research_prospect**: Company research → `{id}_research.md`
2. **create_profile**: Research → structured profile + conversation strategy  
3. **get_prospect_data**: Retrieve complete prospect context
4. **search_prospects**: Query prospects with content search

## 📋 Implementation Instructions

### ALWAYS Before Starting Any Task

```bash
# Step 1: Check project status and current task
cat PROJECT_OVERVIEW.md | grep -A 5 "Current Feature"
cat specs/001-mcp-server-prospect/tasks.md | grep -A 3 "T00X"

# Step 2: Review specifications for current task context
cat specs/001-mcp-server-prospect/spec.md | head -30
cat specs/001-mcp-server-prospect/plan.md | head -20

# Step 3: Use MCP tools for development context and patterns
/semantic_search "current implementation status"
/mcp_context7_resolve-library-id "relevant_framework_name"
```

### ALWAYS During Implementation

#### Constitutional Development Principles
* **Always validate against specs/001-mcp-server-prospect/spec.md acceptance criteria**
* **Always write failing tests before implementation (constitutional TDD requirement)**
* **Always use `/semantic_search` for discovering existing code patterns**
* **Always use `/mcp_context7_get-library-docs` for framework documentation**
* **Always follow markdown-first architecture (rich content in files, minimal database)**
* **Always implement comprehensive error handling and input validation**
* **Always test MCP tools with real JSON-RPC calls**
* **Always validate output formats against template requirements**

#### MCP Tools Integration Workflow
```bash
# Research implementation patterns
/semantic_search "SQLite async operations with Python"
/semantic_search "MCP server tool registration"

# Get framework documentation
/mcp_context7_resolve-library-id "MCP Python SDK"
/mcp_context7_get-library-docs "/modelcontextprotocol/python-sdk" --topic "tools"

# Find code usage examples
/list_code_usages "specific_function_name"
```

### ALWAYS After Each Task Completion

```bash
# Step 1: Run constitutional validation tests
uv run pytest tests/contract/ -k "current_feature" --tb=short
uv run pytest tests/integration/ -k "workflow" --tb=short

# Step 2: Validate MCP server functionality
uv run python -m src.mcp_server.cli status
uv run python -m src.mcp_server.cli list-tools

# Step 3: Check output quality and format compliance
ls -la data/prospects/
head -20 data/prospects/*.md

# Step 4: Update project documentation
echo "✅ Completed T00X: [Description]" >> implementation_log.md
```

### ALWAYS Commit Working Code
```bash
# After each completed task
git add .
git commit -m "feat: T00X - [specific task description]

- Implemented [specific functionality]
- Tests passing: [test results]
- Validates against: [spec requirements]"
```

## 🔧 Development Environment Setup

### Required Dependencies
```bash
# Check current task requirements
cat specs/001-mcp-server-prospect/tasks.md | head -10

# Install dependencies as specified in current feature tasks
# Follow setup tasks from tasks.md file
```

### Environment Configuration
```bash
# Create environment file based on current feature requirements
# Check specs/001-mcp-server-prospect/plan.md for environment variables needed
```

## 📝 Task Execution Workflow

### 1. Task Analysis Phase
```bash
# Read and understand next pending task
cat specs/001-mcp-server-prospect/tasks.md | grep -A 3 "\[ \]"

# Research implementation approach using MCP tools
/semantic_search "relevant implementation pattern for current task"
/mcp_context7_resolve-library-id "framework_needed"
```

### 2. Constitutional TDD Cycle
```bash
# Phase 2.1: Write failing test first (CRITICAL REQUIREMENT)
# Create appropriate test file based on current task
# Test MUST fail initially - validates constitutional TDD

# Phase 2.2: Implement minimal functionality to pass test
# Create implementation file based on current task requirements

# Phase 2.3: Validate and refactor
uv run pytest [test_file] -v --tb=short
```

### 3. Integration & Specification Validation
```bash
# Test implementation against specifications
# Validate MCP protocol compliance if implementing MCP tools
# Check against specification acceptance criteria from spec.md
```

## 🎮 Quick Start Commands

### Begin Implementation Session
```bash
# Step 1: Understand current state
cat PROJECT_OVERVIEW.md
cat specs/001-mcp-server-prospect/tasks.md | head -20

# Step 2: Check specifications for context
cat specs/001-mcp-server-prospect/spec.md | grep -A 10 "Acceptance Criteria"

# Step 3: Research with MCP tools
/semantic_search "relevant patterns for current feature"
/mcp_context7_resolve-library-id "MCP Python SDK"

# Step 4: Execute next pending task from tasks.md
# Follow the task description and implement according to specifications
```

### Test and Validate Current Implementation
```bash
# Run tests based on what's been implemented
uv run pytest tests/ --tb=short

# Check functionality based on current feature requirements
# Follow validation steps specified in current tasks
```

## 🏆 Success Criteria

### Each Task Must Achieve
✅ **Specification Compliance**: Implementation matches acceptance criteria from spec.md  
✅ **Constitutional TDD**: Tests written first and pass after implementation  
✅ **MCP Protocol**: Tools respond correctly to JSON-RPC calls (if applicable)  
✅ **Quality Output**: Files and functionality meet specification requirements  
✅ **Error Handling**: Graceful failures with informative messages  

### System Integration Must Achieve (When Complete)
✅ **Feature Workflow**: Complete feature workflow functions end-to-end  
✅ **External Integration**: System works with specified external clients  
✅ **Specification Compliance**: All acceptance criteria from spec.md met  
✅ **Performance Requirements**: Meets performance targets specified in plan.md  

## 📚 Documentation Requirements

### ALWAYS Update After Each Task
* **Update PROJECT_OVERVIEW.md**: Current implementation status and progress
* **Create/Update feature_implementation.md**: Detailed progress for current feature
* **Record decisions**: Document any deviations from specifications with justification
* **Track metrics**: Record performance and quality metrics as specified

---

**Remember**: You are implementing pre-defined specifications, not creating them. Focus on flawless execution of tasks from `specs/{current_feature}/tasks.md` while leveraging MCP tools for enhanced development efficiency. Every implementation must pass constitutional validation before proceeding to the next task.

## Technical Requirements
- Programming language: Python 3.11+
- Database: SQLite (minimal metadata tracking)
- File storage: Markdown files in /data/prospects/
- MCP Protocol: JSON-RPC 2.0 with Model Context Protocol Python SDK
- Testing: pytest with TDD approach (contract tests must fail first)
- Dependencies: Click for CLI, asyncio for MCP server, SQLAlchemy for database
- External APIs: Firecrawl for web scraping, Playwright for fallback

## Environment Variables (Development)
```
# Create .env file in project root
DATABASE_URL="sqlite:///data/database/prospects.db"
FIRECRAWL_API_KEY="your_firecrawl_key"
MCP_SERVER_HOST="localhost"
MCP_SERVER_PORT="3000"
```

## Current Project State Analysis
**✅ Completed**: Specifications (Phase 1), Implementation Plan (Phase 2), Task List (Phase 3)  
**📍 Current**: Ready for task execution following specs/001-mcp-server-prospect/tasks.md  
**🔄 Next**: Implement 4-library architecture with constitutional TDD methodology

## SDD Task Execution Instructions

### Phase 3.1: Setup Foundation (T001-T004)
*Execute these tasks first to establish development environment*

```bash
# ALWAYS start by checking current project state
/semantic_search "current implementation status"
/list_code_usages "main.py"

# T001: Create simplified project structure
mkdir -p src/{database,file_manager,prospect_research,mcp_server}
mkdir -p tests/{contract,integration,unit}  
mkdir -p data/{prospects,database}
touch src/{database,file_manager,prospect_research,mcp_server}/__init__.py

# T002: Initialize Python project dependencies
uv add mcp click sqlalchemy aiosqlite pytest pytest-asyncio
uv add firecrawl-py playwright --group dev

# T003: Configure pytest with real dependencies (no mocks)
# T004: Set up data directory structure
```

### Phase 3.2: Constitutional TDD Implementation (T005-T011)
*CRITICAL: Write tests that MUST FAIL before any implementation*

```bash
# ALWAYS use Context7 for testing patterns research
/mcp_context7_resolve-library-id "pytest"
/mcp_context7_get-library-docs "/pytest-dev/pytest" --topic "async testing"

# T005-T008: Create contract tests for all 4 MCP tools
# Each test MUST fail initially - this validates TDD approach
uv run pytest tests/contract/test_research_prospect.py -v  # MUST FAIL
uv run pytest tests/contract/test_create_profile.py -v     # MUST FAIL  
uv run pytest tests/contract/test_get_prospect_data.py -v  # MUST FAIL
uv run pytest tests/contract/test_search_prospects.py -v   # MUST FAIL

# T009-T011: Integration tests for complete workflow
uv run pytest tests/integration/test_complete_workflow.py -v  # MUST FAIL
uv run pytest tests/integration/test_markdown_generation.py -v # MUST FAIL
uv run pytest tests/integration/test_mcp_server.py -v         # MUST FAIL
```

### Phase 3.3: Library Implementation (T012-T023)
*Implement in dependency order: database → file_manager → prospect_research → mcp_server*

```bash
# ALWAYS use MCP tools for implementation guidance
/semantic_search "SQLite async operations"
/mcp_context7_get-library-docs "/sqlalchemy/sqlalchemy" --topic "async"

# T012-T014: Database Library (Foundation)
# Implement src/database/models.py (minimal Prospect entity)
# Implement src/database/operations.py (basic CRUD)
# Implement src/database/cli.py (database management)

# T015-T017: File Manager Library (Depends on data structure)  
# Implement src/file_manager/storage.py (markdown file operations)
# Implement src/file_manager/templates.py (template management)
# Implement src/file_manager/cli.py (file operations)

# T018-T020: Prospect Research Library (Depends on file operations)
# Implement src/prospect_research/research.py (AI research logic)
# Implement src/prospect_research/profile.py (profile generation)
# Implement src/prospect_research/cli.py (research commands)

# T021-T023: MCP Server Library (Depends on all libraries)
# Implement src/mcp_server/tools.py (4 MCP tools)
# Implement src/mcp_server/server.py (MCP protocol server)
# Implement src/mcp_server/cli.py (server management)
```

### Phase 3.4: Integration & Validation (T024-T027)
*Connect all libraries and validate complete system*

```bash
# T024-T027: System integration
uv run pytest tests/contract/ --tb=short   # ALL TESTS MUST PASS
uv run pytest tests/integration/ --tb=short # Workflow validation
uv run pytest tests/unit/ --tb=short       # Library validation

# Start MCP server for external testing
uv run python -m src.mcp_server.cli start --host localhost --port 3000
```

### Phase 3.5: Polish & Documentation (T028-T035)
*Performance validation and documentation updates*

```bash
# T028-T035: Final validation and cleanup
uv run pytest --cov=src tests/              # Code coverage check
uv run python scripts/performance_test.py   # <200ms tool response validation
uv run python scripts/workflow_validation.py # <30s complete workflow check
```

## Implementation Instructions

### Always Before Starting Any Task
```bash
# Check current specifications and project state
cat specs/001-mcp-server-prospect/spec.md | head -30
cat specs/001-mcp-server-prospect/plan.md | head -20
cat specs/001-mcp-server-prospect/tasks.md | grep -A 5 "Phase 3"

# Use MCP tools for context and research
/semantic_search "current implementation patterns"
/mcp_context7_resolve-library-id "relevant_library_name"
```

### Always During Implementation
* Always validate against specs/001-mcp-server-prospect/spec.md acceptance criteria
* Always write failing tests before implementation (constitutional TDD)
* Always use /semantic_search for existing code patterns
* Always use /mcp_context7_get-library-docs for dependency documentation
* Always implement error handling and input validation
* Always follow markdown-first architecture (rich content in files, minimal database)
* Always test MCP tools with real JSON-RPC calls
* Always validate output against template requirements
* Always commit after completing each task completely

### Always After Each Task  
```bash
# Validate implementation against specs
uv run pytest tests/contract/ -k "current_feature" --tb=short
uv run pytest tests/integration/ -k "workflow" --tb=short

# Check MCP server functionality
uv run python -m src.mcp_server.cli status
uv run python -m src.mcp_server.cli list-tools

# Validate markdown output quality
ls -la data/prospects/
head -20 data/prospects/*.md
```

### Always Update Documentation
* Always update PROJECT_OVERVIEW.md with current implementation status
* Always create/update feature_implementation.md for each completed feature  
* Always document any deviations from specs with justification
* Always record MCP tool testing results and performance metrics

## Development Workflow Pattern

### 1. Task Analysis & Planning
```bash
# Read next task from tasks.md
cat specs/001-mcp-server-prospect/tasks.md | grep -A 3 "T00X"

# Research implementation patterns  
/semantic_search "relevant implementation pattern"
/mcp_context7_resolve-library-id "framework_name"
/mcp_context7_get-library-docs "/org/project" --topic "specific_topic"
```

### 2. TDD Implementation Cycle
```bash
# Write failing test first (constitutional requirement)
# Implement minimal functionality to pass test
# Refactor and improve
# Validate against specifications

uv run pytest tests/contract/test_specific_feature.py -v --tb=short
```

### 3. Integration & Validation
```bash
# Test complete workflow
uv run python -m src.prospect_research.cli research "test-company"
uv run python -m src.prospect_research.cli profile "test-prospect-id"

# Validate MCP protocol compliance
uv run python -m src.mcp_server.cli test-tool research_prospect '{"company": "TestCorp"}'
```

### 4. Documentation & Commit
```bash
# Update documentation
echo "Completed [task]: [description]" >> implementation_log.md

# Commit working implementation
git add .
git commit -m "feat: implement [task] - [description]"
```

## 🏆 Success Criteria

## File Structure (Implementation Target)
```
├── specs/001-mcp-server-prospect/     # SDD specifications (read-only)
│   ├── spec.md                        # Feature requirements & acceptance criteria
│   ├── plan.md                        # Technical implementation approach  
│   ├── tasks.md                       # 35 executable tasks (T001-T035)
│   └── contracts/                     # MCP tool contracts & OpenAPI
├── src/                               # Implementation (create this)
│   ├── database/                      # T012-T014: Minimal SQLite operations
│   ├── file_manager/                  # T015-T017: Markdown file operations
│   ├── prospect_research/             # T018-T020: AI research logic
│   └── mcp_server/                    # T021-T023: MCP protocol implementation
├── tests/                             # Constitutional TDD validation
│   ├── contract/                      # T005-T008: MCP tool contracts (MUST FAIL FIRST)
│   ├── integration/                   # T009-T011: Complete workflow tests
│   └── unit/                          # T028-T031: Library-specific tests
├── data/                              # Generated content & database
│   ├── prospects/                     # AI-generated markdown files
│   └── database/                      # SQLite database file
├── PROJECT_OVERVIEW.md                # Always update after each task
└── implementation_log.md              # Track progress and decisions
```

## Success Validation Criteria

### Each Task Must Achieve
✅ **Specification Compliance**: Implementation matches acceptance criteria  
✅ **Test Coverage**: Appropriate tests pass (contract/integration/unit)  
✅ **MCP Protocol**: Tools respond correctly to JSON-RPC calls  
✅ **Markdown Quality**: Output files are human-readable and well-formatted  
✅ **Performance**: <200ms tool response, <30s complete workflow  
✅ **Error Handling**: Graceful failure with informative error messages  

### System Integration Must Achieve  
✅ **Complete 2-Step Workflow**: research_prospect → create_profile works end-to-end  
✅ **External MCP Client**: Can connect via Claude Desktop or VS Code  
✅ **Database Operations**: Minimal metadata tracking with file-based rich content  
✅ **Template Consistency**: All markdown outputs follow specification format  

---

## Quick Start Commands

```bash
# Begin implementation (start with T001)
cat specs/001-mcp-server-prospect/tasks.md | head -20
/semantic_search "project setup patterns"
mkdir -p src/{database,file_manager,prospect_research,mcp_server}

# Check specifications for current task
cat specs/001-mcp-server-prospect/spec.md | grep -A 10 "Acceptance Criteria"

# Research implementation approach  
/mcp_context7_resolve-library-id "MCP Python SDK"
/mcp_context7_get-library-docs "/modelcontextprotocol/python-sdk"

# Start constitutional TDD cycle
uv run pytest tests/contract/ --tb=short  # MUST FAIL INITIALLY
```
