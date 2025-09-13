# AI Olympics Charmander: AI Lead Generation System

**Team Charmander - Infostatus AI Olympics 2025**  
**Status**: Ready for Implementation with Gemini CLI  
**Current Phase**: Deliverable 2 - MCP Server Development  

## � Challenge Statement

![AI Olympics Challenge](Challenge_W1.jpeg)

This project is our solution to the **Infostatus AI Olympics 2025 Challenge** - Week 1.

## �🎯 Project Overview

This project builds an AI-powered lead generation system using a **Spec-Driven Development (SDD)** approach with **4 sequential deliverables**:

1. ✅ **ICP & Sales Process** (Complete - see `gemini-docs/`)
2. 🔄 **MCP Server** (Ready for Implementation - see `specs/001-mcp-server-prospect/`)
3. ⏳ **Agentic Pipeline** (Future - will be `specs/002-agentic-pipeline/`)
4. ⏳ **Evaluation System** (Future - will be `specs/003-evaluation/`)

## 🚀 Quick Start - Continue Development

### For New Contributors Using Gemini CLI

**Prerequisites**: 
- [Gemini CLI installed](https://github.com/google-gemini/gemini-cli) 
- Python 3.11+
- Git
- [UV package manager](https://docs.astral.sh/uv/)

```bash
# 1. Clone and setup
git clone [this-repo]
cd ai-olympics-charmander

# 2. Install dependencies
uv sync

# 3. First-time setup (creates directories, database, .env template)
python setup.py

# 4. Configure API keys
# Edit .env file and add your Firecrawl API key (required)
# Apollo API key is optional but recommended

# 5. Verify setup
uv run pytest tests/ --tb=short

# 6. Understand current state
cat PROJECT_OVERVIEW.md              # Read project status
cat GEMINI.md                        # Read implementation instructions

# 7. Start Gemini CLI with project context
gemini --include-directories .

# 8. Begin implementation (Gemini CLI will guide you)
# Gemini CLI will read GEMINI.md automatically and follow the instructions
```

### What Gemini CLI Will Do

When you start Gemini CLI in this project, it will:

1. **Read `GEMINI.md`** - Implementation instructions and workflow
2. **Check `PROJECT_OVERVIEW.md`** - Current project state and progress  
3. **Execute tasks from `specs/001-mcp-server-prospect/tasks.md`** - 35 tasks (T001-T035)
4. **Use constitutional TDD** - Write failing tests before implementation
5. **Leverage MCP tools** - Use `/semantic_search`, `/mcp_context7_*` for enhanced development

## 📁 Repository Structure

```
ai-olympics-charmander/
├── README.md                          # This file - getting started guide
├── PROJECT_OVERVIEW.md                # 📊 Project status & deliverables tracking
├── GEMINI.md                          # 🤖 Gemini CLI implementation instructions
├── gemini-docs/                       # ✅ Deliverable 1: ICP & Sales Process (DONE)
│   ├── PRD.md                         # Product requirements
│   ├── ICP.md                         # Ideal customer profiles
│   └── requirements.md                # Business requirements
├── specs/001-mcp-server-prospect/     # 🔄 Deliverable 2: MCP Server (CURRENT)
│   ├── spec.md                        # ✅ 25 functional requirements
│   ├── plan.md                        # ✅ Technical implementation plan
│   ├── tasks.md                       # ✅ 35 executable tasks (T001-T035)
│   ├── workflow.md                    # ✅ 2-step process design
│   └── contracts/                     # ✅ MCP tool contracts
├── src/                               # 🔄 Implementation (Gemini CLI creates this)
├── tests/                             # 🔄 Tests (Gemini CLI creates this)
├── data/                              # 🔄 Generated content (Gemini CLI creates this)
└── main.py                            # Entry point
```

## 🛠️ Development Workflow

### Phase A: Specifications (COMPLETED ✅)
- **Done by**: Human + GitHub spec-kit
- **Process**: `/specify` → `/plan` → `/tasks`
- **Output**: Complete `specs/001-mcp-server-prospect/` folder
- **Status**: All 25 requirements, technical plan, and 35 tasks defined

### Phase B: Implementation (CURRENT 🔄)
- **Done by**: Gemini CLI following `GEMINI.md` instructions
- **Process**: Execute tasks T001-T035 from `tasks.md`
- **Output**: Working MCP server with 4 tools
- **Status**: Ready to begin - just start Gemini CLI

## 🎯 Current Implementation Target

**Feature**: MCP Server for Prospect Research  
**Architecture**: 4-library structure (database, file_manager, prospect_research, mcp_server)  
**Workflow**: 2-step process (research_prospect → create_profile)  
**Output**: Human-readable markdown files with AI business intelligence  

### 4 MCP Tools to Implement
1. **research_prospect**: Company research → markdown report
2. **create_profile**: Research → structured profile + conversation strategy
3. **get_prospect_data**: Retrieve complete prospect context  
4. **search_prospects**: Query prospects with content search

## 📋 For Project Maintainers

### How to Update Instructions for New Features

When moving to future deliverables (003-agentic-pipeline, 004-evaluation):

1. **Create new specs folder**: `specs/00X-feature-name/`
2. **Run spec-kit process**: Generate spec.md, plan.md, tasks.md
3. **Update PROJECT_OVERVIEW.md**: Change current focus and progress
4. **Update GEMINI.md if needed**: Usually no changes needed (task-agnostic)

### How to Monitor Progress

```bash
# Check current implementation status
cat PROJECT_OVERVIEW.md | grep -A 10 "Progress"

# See what tasks are completed
cat specs/001-mcp-server-prospect/tasks.md | grep "✅"

# Check implementation log
cat implementation_log.md
```

## 🔧 Technology Stack

**Current Feature (MCP Server)**:
- Python 3.11+ with asyncio
- SQLite (minimal metadata)
- Markdown files (rich content)
- Model Context Protocol (JSON-RPC 2.0)
- pytest with constitutional TDD

## 🤝 Contributing

### For Developers
1. Clone repo and start Gemini CLI
2. Follow `GEMINI.md` instructions
3. Execute tasks from `specs/001-mcp-server-prospect/tasks.md`
4. Use constitutional TDD (tests must fail first)
5. Commit after each completed task

### For Product Managers  
1. Review `PROJECT_OVERVIEW.md` for current status
2. Check `specs/001-mcp-server-prospect/spec.md` for requirements
3. Monitor progress through task completion in `tasks.md`

## 📖 Key Files to Understand

| File | Purpose | When to Read |
|------|---------|--------------|
| `PROJECT_OVERVIEW.md` | Project status & deliverables | First - understand big picture |
| `GEMINI.md` | Implementation instructions | Before starting Gemini CLI |
| `specs/001-*/spec.md` | Feature requirements | When understanding current feature |
| `specs/001-*/tasks.md` | Executable tasks | When implementing with Gemini CLI |
| `specs/001-*/plan.md` | Technical approach | When understanding architecture |

## 🆘 Troubleshooting

### "I don't know where to start"
→ Read `PROJECT_OVERVIEW.md` then start Gemini CLI with `gemini --include-directories .`

### "Gemini CLI isn't following instructions"  
→ Ensure `GEMINI.md` is in project root and start Gemini CLI from project directory

### "Tasks aren't clear"
→ Check `specs/001-mcp-server-prospect/tasks.md` for detailed task descriptions

### "Implementation differs from specs"
→ Always validate against `specs/001-mcp-server-prospect/spec.md` acceptance criteria

### First-time Setup Issues

#### "Database not found" or "No such file or directory"
```bash
# Run the setup script
python setup.py
```

#### "Import errors" or "Module not found"
```bash
# Ensure dependencies are installed
uv sync
```

#### "API tests failing"
```bash
# Check if .env file exists and has valid API keys
cat .env
# Add your Firecrawl API key to .env file
```

#### "Permission denied" errors
```bash
# Ensure setup script is executable
chmod +x setup.py
```

#### "Tests failing on fresh machine"
```bash
# Complete setup and verification process
python setup.py
uv run pytest tests/ --tb=short
```

---

**Ready to Continue?** Start Gemini CLI and it will guide you through implementing the MCP server following the specifications! 🚀
