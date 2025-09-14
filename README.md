# AI Olympics Charmander: MCP Prospect Research Server

**Team Charmander - Infostatus AI Olympics 2025**  
**Status**: 🔄 **ENHANCING WITH AI** - Developing LLM Intelligence Middleware  
**Current Phase**: ⏳ Deliverable 3 - Intelligence Middleware for Enhanced Research Quality  

## 🎯 Challenge Achievement

![AI Olympics Challenge](Challenge_W1.jpeg)

This project is our solution to the **Infostatus AI Olympics 2025 Challenge** - Week 1.

## 🚀 What This MCP Server Can Do **RIGHT NOW** + **Coming Soon**

Our **Model Context Protocol (MCP) Server** provides 4 powerful prospect research tools that work today, with AI intelligence enhancements in development:

### ✅ **research_prospect** - Company Research ⏳ **ENHANCING WITH AI**
- **Current**: 5-source research with manual data preparation
- **Enhancement**: LLM intelligence middleware for business analysis
- **Input**: Company domain or name (e.g., "example.com" or "Acme Corp")
- **Output**: Comprehensive research report (soon with AI business insights)
- **Data Sources**: Company website, LinkedIn, job boards, news, government registries

### ✅ **create_profile** - Profile Generation ⏳ **ENHANCING WITH AI**  
- **Current**: Rule-based conversation generation with hardcoded logic
- **Enhancement**: AI-powered conversation strategy and personalized talking points
- **Input**: Prospect ID from research_prospect
- **Output**: Strategic Mini Profile (soon with AI conversation strategies)

### ✅ **get_prospect_data** - Context Retrieval (Enhanced Content)
- **Input**: Any prospect ID (UUID or timestamp-based)
- **Output**: Complete prospect context (will include AI-enhanced content)

### ✅ **search_prospects** - Content Search (Unchanged)
- **Input**: Search query (company name, industry, keywords)
- **Output**: Matching prospects with snippets and relevance scoring

## 🎯 Project Overview

This project builds an AI-powered lead generation system using **Spec-Driven Development (SDD)** with **5 sequential deliverables**:

1. ✅ **ICP & Sales Process** (Complete - see `gemini-docs/`)
2. ✅ **MCP Server** (COMPLETE - Full production server with 4 tools)
3. ⏳ **LLM Intelligence Middleware** (**IN PROGRESS** - `specs/002-improve-research-with-llm/`)
4. ⏳ **Agentic Pipeline** (Future - will be `specs/003-agentic-pipeline/`)
5. ⏳ **Evaluation System** (Future - will be `specs/004-evaluation/`)

## 🚀 Quick Start - Continue Development

## 🚀 **Quick Start - Clone & Setup MCP Server**

### **Method 1: Complete Setup (Recommended)**

```bash
# 1. Clone repository
git clone https://github.com/your-org/ai-olympics-charmander.git
cd ai-olympics-charmander

# 2. Install Python 3.11+ and UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Create environment file
cp .env.example .env
# Edit .env and add your API keys (see Configuration section below)

# 5. Initialize database and directories
uv run python -c "
from src.database.operations import initialize_database
from src.file_manager.storage import ensure_directories
initialize_database()
ensure_directories()
print('✅ Setup complete!')
"

# 6. Test the MCP server
uv run python -m src.mcp_server.server

# You should see: "MCP Prospect Research Server starting..."
# Press Ctrl+C to stop
```

### **Method 2: Quick Test (Demo Mode)**

```bash
# Skip API keys - use demo mode with mock data
git clone [repo] && cd ai-olympics-charmander
uv sync
uv run python -c "
from src.database.operations import initialize_database
from src.file_manager.storage import ensure_directories
initialize_database()
ensure_directories()
"

# Test immediately with demo data
uv run python -m src.mcp_server.server
```

## ⚙️ **Configuration**

### **Required Files**

Create `.env` file in project root:
```env
# Required for full functionality
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Required for LLM intelligence middleware (Deliverable 3)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=ap-southeast-2

# Optional (demo mode works without these)
APOLLO_API_KEY=your_apollo_api_key_here

# Database (auto-created)
DATABASE_URL=sqlite:///data/database/prospects.db
```

### **Get API Keys**

1. **Firecrawl API** (recommended): Visit [firecrawl.dev](https://firecrawl.dev) for web scraping
2. **AWS Bedrock** (for AI enhancements): Set up AWS account with Bedrock access in ap-southeast-2 region
3. **Apollo API** (optional): Visit [apollo.io](https://apollo.io) for enhanced data

**Note**: The server works in demo mode without any API keys - it generates realistic mock data for testing.

## 🔧 **Connecting to MCP Clients**

### **MCP Configuration for coding assistants**

Add to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "prospect-research": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.mcp_server.server"],
      "cwd": "/path/to/ai-olympics-charmander"
    }
  }
}
```

### **Other MCP Clients**

The server follows MCP protocol specifications and works with any compliant client:

- **Transport**: stdio (JSON-RPC 2.0)
- **Capabilities**: tools, resources
- **Startup Command**: `uv run python -m src.mcp_server.server`
- **Working Directory**: Project root

## 🏗️ **Architecture & Technical Details**

### **Enhanced Architecture (Intelligence Middleware)**
```
src/
├── database/          # SQLite operations & models (SQLAlchemy ORM)
├── file_manager/      # Markdown templates & file I/O  
├── prospect_research/ # 5-source research engine (🔄 AI-enhanced)
├── mcp_server/        # MCP protocol implementation (🔄 LLM config)
└── llm_enhancer/      # 🆕 Intelligence middleware module
```

### **Intelligence Middleware Flow**
1. **Data Collection**: Sub-level tools (Firecrawl, LinkedIn, etc.) gather raw data
2. **AI Analysis**: LLM middleware processes raw data for business insights
3. **Template Generation**: Same templates, dramatically better content quality
4. **Fallback Safety**: Graceful degradation to manual processing if LLM unavailable

### **Data Flow**
1. **Research**: `research_prospect` → Saves to `data/prospects/{id}_research.md`
2. **Profile**: `create_profile` → Generates `{id}_profile.md` 
3. **Retrieve**: `get_prospect_data` → Returns combined research + profile
4. **Search**: `search_prospects` → Queries database + file content

### **Tech Stack**
- **Python 3.11+** with UV package manager
- **SQLite Database** with SQLAlchemy ORM  
- **MCP Protocol** (JSON-RPC 2.0 over stdio)
- **Firecrawl API** for web scraping (with demo mode fallback)
- **AWS Bedrock** with Claude Sonnet for intelligence middleware
- **Markdown-First** file storage for human readability

## 📈 **Current Capabilities vs Goals**

### ✅ **Strengths (What Works Today)**
- **Complete MCP Implementation**: All 4 tools working, protocol compliant
- **Demo Mode**: Full functionality without API keys for testing
- **Structured Output**: Markdown files with consistent formatting
- **Error Handling**: Comprehensive validation and graceful failures  
- **Fast Performance**: 2-5 second research times
- **Flexible ID Support**: Handles both UUID and timestamp-based IDs
- **Search Capability**: Content search across all prospect data

### ⏳ **Current Development (Intelligence Middleware)**
- **Manual Logic Replacement**: Replacing hardcoded rules with AI analysis
- **Business Intelligence**: LLM-powered insights instead of string manipulation
- **Conversation Strategy**: AI-generated personalized talking points
- **Fallback Safety**: Graceful degradation to original logic if LLM fails

### ⚠️ **Current Limitations**
- **Data Sources**: Only Firecrawl web scraping (vs planned 5 sources)
- **Storage**: SQLite file database (vs planned PostgreSQL)
- **Demo Data**: Mock data quality could be more realistic
- **No REST API**: MCP-only interface (vs planned dual CLI/API)

### 🎯 **Original Goals (from Specs)**
- **5 Data Sources**: Company, LinkedIn, Apollo, job boards, news, government
- **PostgreSQL**: Enterprise database with migrations
- **REST API**: Swagger/OpenAPI with dual CLI/API access
- **Production Scale**: Enterprise-ready with monitoring
- **Advanced Intelligence**: ML-powered lead scoring and recommendations

## 🧪 **Testing & Validation**

```bash
# Run all tests
uv run pytest tests/ --tb=short

# Test specific components
uv run pytest tests/unit/ -v          # Unit tests
uv run pytest tests/integration/ -v   # Integration tests  
uv run pytest tests/contract/ -v      # Contract tests (some need fixes)

# Test MCP server manually
uv run python -c "
from src.mcp_server.tools import research_prospect
result = research_prospect('example.com')
print(f'✅ Research generated: {result}')
"
```

## 🤝 **For Contributors & Developers**

### **Development Workflow**
1. Read `PROJECT_OVERVIEW.md` for current status
2. Check `specs/001-mcp-server-prospect/tasks.md` for task breakdown
3. Follow constitutional TDD: Write failing tests first
4. Use Serena MCP tools for codebase navigation
5. Commit each "small win" separately

### **Key Files**
- `specs/001-mcp-server-prospect/spec.md` - Feature requirements
- `specs/001-mcp-server-prospect/tasks.md` - Task breakdown (T001-T035)
- `PROJECT_OVERVIEW.md` - Implementation status and changelog
- `.github/instructions/system_instructions.instructions.md` - Development constitution
## 📁 **Repository Structure**

```
ai-olympics-charmander/
├── src/                           # 5-library MCP server implementation
│   ├── database/                  # SQLite operations & models  
│   ├── file_manager/              # Markdown templates & storage
│   ├── prospect_research/         # Research engine & profiling (🔄 AI-enhanced)
│   ├── mcp_server/                # MCP protocol server & tools (🔄 LLM config)
│   └── llm_enhancer/              # 🆕 Intelligence middleware module
├── specs/001-mcp-server-prospect/ # Feature specification & 35 tasks (✅ complete)
├── specs/002-improve-research-with-llm/ # Intelligence middleware spec (⏳ active)
├── tests/                         # Unit, integration, contract tests
├── data/                          # SQLite DB & generated markdown files
├── gemini-docs/                   # Original requirements & design
├── PROJECT_OVERVIEW.md            # Implementation progress tracker
├── GEMINI.md                      # Original Gemini CLI guide
└── .env                           # API keys configuration file
```

## 📚 **Documentation & Next Steps**

### **Key Documentation**
- **`PROJECT_OVERVIEW.md`** - Current implementation status and deliverable progress
- **`specs/001-mcp-server-prospect/spec.md`** - MCP Server requirements & acceptance criteria (✅ complete)
- **`specs/001-mcp-server-prospect/tasks.md`** - MCP Server task breakdown (T001-T035) (✅ complete)
- **`specs/002-improve-research-with-llm/spec.md`** - Intelligence middleware specification (⏳ active)
- **`specs/002-improve-research-with-llm/plan.md`** - Intelligence middleware architecture (⏳ active)
- **`.github/instructions/system_instructions.instructions.md`** - Development constitution

### **Future Deliverables (After Intelligence Middleware)**
- **Deliverable 4**: Agentic Pipeline (`specs/003-agentic-pipeline/`) - Multi-agent workflow
- **Deliverable 5**: Evaluation System (`specs/004-evaluation/`) - Performance metrics & validation

## 🏆 **Challenge Success Summary**

**✅ Deliverable 2 COMPLETE - MCP Server:**
- ✅ 4 fully functional MCP tools
- ✅ SQLite database integration with markdown file storage
- ✅ Error handling, validation, and demo mode
- ✅ Protocol compliance with JSON-RPC 2.0 over stdio
- ✅ 2-5 second research performance with structured output

**⏳ Deliverable 3 IN PROGRESS - Intelligence Middleware:**
- ✅ Specification complete: Problem analysis and solution architecture
- ✅ Planning complete: Intelligence middleware pattern defined
- ⏳ Task breakdown: Creating implementation roadmap
- ⏳ Implementation: Replacing manual logic with AI analysis

**🎯 Enhanced Capabilities (Coming Soon):**
- AI business intelligence analysis instead of string manipulation
- Personalized conversation strategies instead of hardcoded rules
- Same templates with dramatically improved content quality
- Graceful fallback to original logic for reliability

---

**Team Charmander - Infostatus AI Olympics 2025**  
**Status**: ⏳ **Intelligence Middleware Development** - Enhancing Research Quality with AI  
**Next**: Complete LLM intelligence middleware, then Agentic Pipeline (Deliverable 4)
