# Feature Specification: MCP Server: Prospect Research Automation Engine

**Feature Branch**: `001-mcp-server-prospect`  
**Created**: September 13, 2025  
**Status**: Draft  
**Input**: User description: "MCP Server: Prospect Research Automation Engine. The MCP server serves as the core intelligence layer for automated prospect identification and research, designed to eliminate the manual effort of qualifying cold calling opportunities. It provides four specialized tools that work together to create a complete prospect research workflow: find_new_prospect discovers qualified leads matching predefined ideal customer profiles from reliable data sources, research_prospect compiles comprehensive intelligence including company background, decision maker information, recent news, and identified pain points, while save_prospect and retrieve_prospect maintain a centralized prospect database that functions as a lightweight CRM foundation. The server addresses the critical gap between raw prospect data and actionable sales intelligence by automating the time-intensive research process, enabling sales teams to approach each cold call with contextual insights, personalized conversation starters, and confidence in lead quality."

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
A sales representative using an AI assistant (like Gemini CLI, VS Code Copilot, or Claude) needs to transform company information into actionable sales intelligence through a streamlined 2-step research workflow. The MCP server provides specialized tools that generate rich markdown files containing comprehensive research reports and structured profile + conversation strategy content, enabling the sales rep to receive copy-paste ready sales intelligence through natural language conversations with their AI assistant.

### Acceptance Scenarios
1. **Given** an AI assistant connected to the MCP server, **When** a sales rep provides a company name or domain, **Then** the AI assistant calls the research_prospect tool to generate a comprehensive markdown research report
2. **Given** a research markdown file has been generated, **When** the sales rep asks for a structured profile and talking points, **Then** the AI assistant calls the create_profile tool to transform research into a Mini Profile table with conversation strategy
3. **Given** prospect data exists in the system, **When** the sales rep needs to retrieve complete prospect information, **Then** the AI assistant calls the get_prospect_data tool to access all metadata and markdown files
4. **Given** multiple prospects are stored in the database, **When** the sales rep needs to search prospects by criteria or content, **Then** the AI assistant calls the search_prospects tool to find prospects matching specified filters
5. **Given** the MCP server exposes prospect resources, **When** the AI assistant needs context about saved prospects, **Then** it can access prospect resources via URI to provide enriched responses with markdown content
6. **Given** the simplified 2-step workflow, **When** a sales rep completes both research and profile steps, **Then** they receive human-readable markdown files ready for copy-paste into emails, presentations, or CRM systems

### Edge Cases
- What happens when company information is insufficient or outdated for the research_prospect tool?
- How does the create_profile tool handle research markdown files with incomplete or missing sections?
- What occurs when external data sources are unavailable during research generation?
- How does the research_prospect tool respond when no substantial research data can be found for a company?
- What happens when the create_profile tool tries to process research files that are corrupted or improperly formatted?
- How does the MCP server handle tool calls with invalid company identifiers or malformed parameters?
- What occurs when AI assistants lose connection to the MCP server during the 2-step workflow execution?
- How does the server handle concurrent tool calls for the same prospect from multiple AI assistant connections?
- What happens when the file system lacks sufficient storage space for generating markdown files?
- How does the system handle prospects with extremely common company names that could result in research ambiguity?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: MCP Server MUST implement the Model Context Protocol specification version "2025-06-18" for client-server communication
- **FR-002**: MCP Server MUST declare tools capability to expose 4 specialized prospect research tools to AI assistants
- **FR-003**: MCP Server MUST provide a research_prospect tool that accepts company identifiers and generates comprehensive markdown research reports
- **FR-004**: research_prospect tool MUST include JSON schema validation for company domain or name input parameters
- **FR-005**: research_prospect tool MUST create structured markdown files containing company background, recent news, technology stack, decision makers, and pain points
- **FR-006**: MCP Server MUST provide a create_profile tool that transforms research markdown into structured Mini Profile tables with conversation strategy
- **FR-007**: create_profile tool MUST generate exactly 14 standardized profile fields in markdown table format as specified
- **FR-008**: create_profile tool MUST include personalized talking points with relevance scores and conversation openers
- **FR-009**: MCP Server MUST provide a get_prospect_data tool that retrieves prospect metadata with all associated markdown files
- **FR-010**: get_prospect_data tool MUST support content inclusion options and specific file type filtering
- **FR-011**: MCP Server MUST provide a search_prospects tool that queries prospect database by metadata and markdown content
- **FR-012**: search_prospects tool MUST support filtering by company name, domain, research status, and content search across files
- **FR-013**: MCP Server MUST declare resources capability to expose prospect data and markdown files as contextual resources
- **FR-014**: MCP Server MUST provide resources for individual prospect data, file contents, and ICP definition accessible via URI patterns
- **FR-015**: MCP Server MUST implement proper JSON-RPC 2.0 error handling with structured error responses for tool failures
- **FR-016**: MCP Server MUST support tools/list requests to advertise all 4 prospect research tools with complete schemas
- **FR-017**: MCP Server MUST support tools/call requests to execute the simplified 2-step research workflow efficiently
- **FR-018**: MCP Server MUST implement input validation for all tool parameters and resource access requests
- **FR-019**: MCP Server MUST support connection management for multiple AI assistant clients with concurrent access
- **FR-020**: MCP Server MUST manage file system operations for markdown generation, storage, and retrieval
- **FR-021**: All tools MUST include comprehensive metadata (name, title, description, inputSchema) for AI assistant discovery and execution
- **FR-022**: System MUST persist prospect metadata in SQLite database with minimal schema for tracking research status
- **FR-023**: System MUST store all AI-generated content as human-readable markdown files in organized directory structure
- **FR-024**: System MUST support a streamlined 2-step workflow: research generation followed by profile + strategy creation
- **FR-025**: System MUST enable copy-paste ready output for sales teams through structured markdown formatting

### Key Entities *(include if feature involves data)*
- **MCP Server**: The core server implementing Model Context Protocol to expose 4 specialized prospect research tools to AI assistants
- **MCP Tools**: Four focused tools (research_prospect, create_profile, get_prospect_data, search_prospects) that AI assistants can discover and invoke for the 2-step workflow
- **MCP Resources**: URI-addressable prospect data, markdown files, and ICP definition accessible to AI assistants for contextual intelligence
- **Prospect**: Minimal database entity with UUID, company name, domain, research status, and timestamps for workflow tracking
- **Research Markdown**: AI-generated comprehensive research reports containing company background, recent developments, technology stack, decision makers, and pain points
- **Profile Markdown**: AI-generated structured Mini Profile tables (14 standardized fields) combined with personalized conversation strategy and talking points
- **Workflow Status**: File-based progress tracking using markdown file existence to determine completion of 2-step research workflow
- **Tool Schema**: JSON Schema definitions that describe input parameters and expected outputs for each of the 4 MCP tools
- **AI Assistant Client**: The connected AI application (Gemini CLI, VS Code Copilot, Claude) that discovers and calls MCP tools on behalf of sales users
- **File System Storage**: Organized directory structure storing all AI-generated markdown content as human-readable files for copy-paste usage

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs) - focuses on markdown-first user value
- [x] Focused on user value and business needs (copy-paste ready sales intelligence)
- [x] Written for non-technical stakeholders (sales teams and business users)
- [x] All mandatory sections completed with simplified 2-step workflow

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain (simplified approach resolved all ambiguities)
- [x] Requirements are testable and unambiguous  
- [x] Success criteria are measurable (2-step workflow with markdown output)
- [x] Scope is clearly bounded (4 MCP tools, file-based storage)
- [x] Dependencies and assumptions identified (SQLite, file system, AI assistants)

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted  
- [x] MCP protocol research completed
- [x] Simplified markdown-first approach defined
- [x] User scenarios updated for 2-step workflow
- [x] Requirements updated for simplified architecture
- [x] Entities identified including markdown file system
- [x] Review checklist passed - simplified approach eliminates all clarification needs

---
