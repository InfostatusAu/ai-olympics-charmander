# AI Olympics Charmander: Project Purpose & Tech Stack

## Project Purpose
AI-powered lead generation system that develops 4 deliverables using Spec-Driven Development (SDD) with Model Context Protocol (MCP) integration. The current focus is **Deliverable 2: MCP Server** that exposes 4 specialized prospect research tools for automating AI-generated prospect intelligence.

## Core Mission
- **Input**: Company name/domain
- **Process**: AI-driven research using multiple data sources (LinkedIn, Apollo, job boards, Google, government registries)
- **Output**: Markdown-first intelligence reports and structured profiles
- **Protocol**: Model Context Protocol (MCP) JSON-RPC 2.0 interface

## Technology Stack

### Core Technologies
- **Language**: Python 3.11+
- **Protocol**: Model Context Protocol (MCP) with JSON-RPC 2.0
- **Database**: SQLite with SQLAlchemy (minimal metadata storage)
- **Storage**: Markdown files in `/data/prospects/` (rich content)
- **Testing**: pytest + pytest-asyncio (constitutional TDD required)
- **Package Manager**: UV (fast Python package management)

### Key Dependencies
- **mcp>=1.14.0**: Model Context Protocol Python SDK
- **sqlalchemy>=2.0.43**: Database ORM for SQLite
- **aiosqlite>=0.21.0**: Async SQLite operations
- **click>=8.2.1**: CLI interface framework
- **firecrawl-py>=4.3.6**: Web scraping for research (dev dependency)
- **playwright>=1.55.0**: Browser automation fallback (dev dependency)

### Architecture Pattern
- **4-Library Structure**: `database`, `file_manager`, `prospect_research`, `mcp_server`
- **Markdown-First**: Rich content in human-readable files, minimal database complexity
- **Dependency Order**: database → file_manager → prospect_research → mcp_server
- **2-Step Workflow**: research_prospect → create_profile

### Data Sources Integration
- LinkedIn (Firecrawl, Serper, Playwright MCP)
- Apollo API for contact enrichment
- Job boards (Seek, Indeed, Glassdoor)
- Google Search & News
- Government registries (ASIC, ABN Lookup, NSW Open Data)

## MCP Tools Exposed
1. **research_prospect**: Company research and markdown generation (Step 1)
2. **create_profile**: Transform research to profile+strategy (Step 2)  
3. **get_prospect_data**: Retrieve complete prospect context
4. **search_prospects**: Query prospects with content search