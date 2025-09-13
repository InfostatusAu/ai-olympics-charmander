# AI Olympics Charmander - Project Overview

## Project Purpose
AI-powered lead generation system with MCP (Model Context Protocol) integration. Currently implementing a prospect research MCP server that exposes 4 tools for automated prospect research and profile generation.

## Tech Stack
- **Language**: Python 3.11+
- **Database**: SQLite with SQLAlchemy
- **Async**: aiosqlite, asyncio
- **Protocol**: Model Context Protocol (MCP) JSON-RPC 2.0
- **CLI**: Click for command-line interfaces
- **Testing**: pytest with pytest-asyncio
- **External APIs**: Firecrawl, Playwright (dev dependencies)

## Architecture
4-library structure with markdown-first approach:
1. **database**: SQLite operations and models
2. **file_manager**: Markdown file operations and templates  
3. **prospect_research**: AI research logic and profile generation
4. **mcp_server**: MCP protocol implementation with 4 tools

## MCP Tools
1. `research_prospect`: Company research and markdown generation
2. `create_profile`: Transform research to profile+strategy
3. `get_prospect_data`: Retrieve complete prospect context
4. `search_prospects`: Query prospects with content search

## Development Approach
- **Constitutional TDD**: Contract tests must fail before implementation
- **Markdown-First**: Rich content in human-readable files, minimal database
- **Spec-Driven**: Following specifications in `specs/001-mcp-server-prospect/`
- **Small Commits**: Each task committed separately for transparency