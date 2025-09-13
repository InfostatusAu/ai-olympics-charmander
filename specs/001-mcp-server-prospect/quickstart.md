# Quickstart: MCP Prospect Research Server

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine  
**Phase**: 1 - Integration Guide and User Stories

## Overview

This quickstart guide demonstrates how to set up and use the MCP Prospect Research Server with AI assistants like Gemini CLI, VS Code Copilot, or Claude. The server provides automated prospect research capabilities through four specialized tools that work together to streamline cold calling preparation.

## Prerequisites

- Python 3.11+ installed
- PostgreSQL 15+ or Supabase CLI
- AI assistant with MCP support (Gemini CLI, VS Code Copilot, Claude, etc.)
- API keys for data sources (optional but recommended)

## Setup

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd mcp-prospect-server

# Install dependencies using UV
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Database Setup
```bash
# Start Supabase local stack
supabase start

# Run database migrations
uv run alembic upgrade head

# Seed with default ICP templates
uv run python scripts/seed_icps.py
```

### 3. MCP Server Configuration
```bash
# Start the MCP server
uv run python -m mcp_server.main

# Server will listen on stdio for MCP connections
# Or use TCP mode for remote AI assistants:
uv run python -m mcp_server.main --transport tcp --port 8000
```

### 4. AI Assistant Configuration

#### For Gemini CLI
```bash
# Add MCP server to Gemini CLI configuration
gemini config add-mcp-server prospect-research \
  --command "uv run python -m mcp_server.main" \
  --description "Prospect research automation tools"

# Verify connection
gemini mcp list-tools
```

#### For VS Code Copilot
Add to `.vscode/settings.json`:
```json
{
  "mcp.servers": {
    "prospect-research": {
      "command": "uv",
      "args": ["run", "python", "-m", "mcp_server.main"],
      "cwd": "/path/to/mcp-prospect-server"
    }
  }
}
```

#### For Claude Desktop
Add to Claude configuration:
```json
{
  "mcpServers": {
    "prospect-research": {
      "command": "uv",
      "args": ["run", "python", "-m", "mcp_server.main"],
      "cwd": "/path/to/mcp-prospect-server"
    }
  }
}
```

## User Story Walkthroughs

### Story 1: Finding New Prospects
**Goal**: Discover qualified prospects matching ideal customer profile

**AI Assistant Conversation**:
```
User: "I need to find new prospects for our SaaS product targeting tech startups with 50-200 employees"

AI Assistant: I'll help you find qualified prospects using the prospect research tools. Let me search for companies matching your criteria.

[AI discovers and calls find_new_prospect tool]

AI Assistant: I found 15 qualified prospects matching your tech startup criteria. Here are the top 5 prospects with highest match scores:

1. **TechFlow Solutions** (techflow.com) - 87% match
   - 125 employees, Software Development
   - San Francisco, CA
   - Recent Series A funding

2. **DataStream Inc** (datastream.io) - 84% match  
   - 89 employees, Data Analytics
   - Austin, TX
   - Growing customer base

[Additional prospects listed...]

Would you like me to research any of these prospects in detail?
```

**Expected Result**: List of qualified prospects with match scores and basic company information.

### Story 2: Researching a Specific Prospect
**Goal**: Compile comprehensive intelligence on a target prospect

**AI Assistant Conversation**:
```
User: "Research TechFlow Solutions in detail, I want to understand their pain points and decision makers"

AI Assistant: I'll gather comprehensive research on TechFlow Solutions for you.

[AI calls research_prospect tool with domain "techflow.com"]

AI Assistant: Here's the detailed research on TechFlow Solutions:

**Company Overview:**
- Founded in 2020, 125 employees
- SaaS platform for workflow automation
- Recently raised $8M Series A (June 2025)
- Headquarters: San Francisco, CA

**Key Decision Makers:**
- **Sarah Chen** - CEO (primary decision maker)
  - Email: sarah.chen@techflow.com
  - LinkedIn: linkedin.com/in/sarahchen-ceo
- **Mike Rodriguez** - CTO (technical decision maker)
  - Email: mike.r@techflow.com

**Identified Pain Points:**
1. Struggling with customer data integration across multiple platforms
2. Manual reporting processes slowing down customer success team
3. Need for better analytics to track user engagement

**Recent News:**
- Launched new API platform (August 2025)
- Expanding engineering team by 40%
- Partnership with CloudCorp announced

**Technology Stack:**
- AWS, Python, React, PostgreSQL
- Using Salesforce for CRM
- Slack for team communication

This gives you strong talking points about data integration challenges and how your solution could help with their scaling efforts.
```

**Expected Result**: Comprehensive prospect intelligence with actionable insights for sales conversations.

### Story 3: Saving Prospect Data
**Goal**: Store research findings in the prospect database

**AI Assistant Conversation**:
```
User: "Save all the TechFlow Solutions research to our prospect database and mark them as qualified"

AI Assistant: I'll save the complete TechFlow Solutions profile to your prospect database.

[AI calls save_prospect tool with all gathered data]

AI Assistant: ✅ Successfully saved TechFlow Solutions to your prospect database:

**Saved Data:**
- Company profile with 125 employees, Series A status
- 2 key decision makers (Sarah Chen - CEO, Mike Rodriguez - CTO)
- 5 research notes covering pain points, recent news, tech stack
- Qualification status: Qualified
- Matched to ICP: "tech-startups-growth-stage"

**Prospect ID**: a1b2c3d4-e5f6-7890-abcd-123456789012

The prospect is now available for future reference and you can retrieve this information anytime. Would you like me to find similar prospects or research another company?
```

**Expected Result**: Prospect data persisted with confirmation and unique identifier for future reference.

### Story 4: Retrieving Saved Prospects
**Goal**: Query stored prospect data for follow-up activities

**AI Assistant Conversation**:
```
User: "Show me all qualified prospects in the software industry that we haven't contacted yet"

AI Assistant: I'll search your prospect database for qualified software companies.

[AI calls retrieve_prospect tool with filters]

AI Assistant: Found 8 qualified software prospects that haven't been contacted:

**Active Qualified Prospects:**

1. **TechFlow Solutions** - Last updated: Sep 13, 2025
   - 125 employees, Workflow automation
   - Pain points: Data integration, manual reporting
   - Decision makers: Sarah Chen (CEO), Mike Rodriguez (CTO)

2. **CloudBridge Analytics** - Last updated: Sep 12, 2025
   - 78 employees, Business intelligence
   - Pain points: Scaling data infrastructure
   - Decision maker: Jennifer Wang (Head of Engineering)

3. **StreamLine Software** - Last updated: Sep 11, 2025
   - 156 employees, DevOps tools
   - Pain points: Multi-cloud management complexity
   - Decision makers: Alex Thompson (CTO), Maria Garcia (VP Engineering)

[Additional prospects...]

**Summary**: 8 qualified prospects, total database contains 45 prospects across all industries.

Would you like me to prioritize these by company size, recent funding, or specific pain points that match your solution?
```

**Expected Result**: Filtered list of prospects with key information for sales prioritization.

### Story 5: End-to-End Workflow
**Goal**: Complete prospect research workflow from discovery to contact preparation

**AI Assistant Conversation**:
```
User: "I need to prepare for cold outreach to fintech companies with 100-500 employees. Find prospects, research the top 3, and save them to our database"

AI Assistant: I'll help you prepare a complete fintech prospect pipeline. Let me start by finding qualified companies.

[AI calls find_new_prospect with fintech ICP]

Found 12 qualified fintech prospects. Let me research the top 3 with highest match scores:

[AI sequentially calls research_prospect for top 3 prospects]

[AI calls save_prospect for each researched prospect]

## Complete Fintech Prospect Pipeline Ready

**1. PayFlow Technologies** (payflow.tech) - 95% ICP match
- **Contact**: David Kim, CEO (david@payflow.tech)
- **Pain Point**: Struggling with payment processor integration complexity
- **Opportunity**: Just raised Series B, expanding payment rails
- **Talking Point**: Your API could simplify their multi-processor strategy
- **Status**: Saved as qualified prospect

**2. CreditSense Analytics** (creditsense.io) - 91% ICP match  
- **Contact**: Lisa Martinez, CTO (lisa.martinez@creditsense.io)
- **Pain Point**: Real-time fraud detection performance issues
- **Opportunity**: Processing 50M+ transactions monthly, need faster decisioning
- **Talking Point**: Your low-latency solution could reduce false positives
- **Status**: Saved as qualified prospect

**3. LendingBridge Corp** (lendingbridge.com) - 88% ICP match
- **Contact**: Robert Chen, VP Engineering (r.chen@lendingbridge.com)  
- **Pain Point**: Regulatory reporting automation challenges
- **Opportunity**: Recent compliance audit highlighted manual processes
- **Talking Point**: Automated reporting could reduce compliance overhead
- **Status**: Saved as qualified prospect

**Next Steps Recommended:**
1. Start with PayFlow (highest match, clear pain point alignment)
2. Personalize outreach mentioning their Series B and processor integration challenges  
3. Follow up with CreditSense focusing on performance optimization
4. Schedule LendingBridge demo around regulatory automation features

All prospects are now in your database for tracking and follow-up. Would you like me to draft personalized email templates for each prospect?
```

**Expected Result**: Complete sales pipeline with research, pain points, contact information, and recommended approach for each prospect.

## Validation Tests

### Functional Validation
Each user story above can be executed as an integration test:

1. **Tool Discovery Test**: Verify AI assistant can discover all 4 MCP tools
2. **Find Prospects Test**: Validate find_new_prospect returns qualified leads
3. **Research Quality Test**: Confirm research_prospect gathers comprehensive data
4. **Data Persistence Test**: Ensure save_prospect stores data correctly
5. **Query Functionality Test**: Validate retrieve_prospect filtering and search
6. **Error Handling Test**: Verify graceful handling of invalid inputs and API failures

### Performance Validation
- **Response Time**: All tool calls complete within <200ms (excluding external API calls)
- **Concurrent Users**: Support multiple AI assistant connections simultaneously
- **Data Quality**: Research confidence scores above 0.8 for successful operations

### Security Validation
- **Input Sanitization**: All tool parameters validated against JSON schemas
- **Database Security**: SQL injection prevention through parameterized queries
- **API Key Protection**: External service credentials properly secured

## Troubleshooting

### Common Issues

**MCP Server Not Responding**:
```bash
# Check server logs
uv run python -m mcp_server.main --verbose

# Verify database connection
psql -h localhost -p 54322 -U postgres -d postgres
```

**Tool Discovery Fails**:
```bash
# Test MCP protocol directly
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  uv run python -m mcp_server.main
```

**External API Errors**:
```bash
# Check API key configuration
uv run python -c "from mcp_server.config import settings; print(settings.api_keys)"

# Test data source connectivity
uv run python -m mcp_server.cli test-sources
```

### Performance Monitoring
```bash
# Monitor server performance
uv run python -m mcp_server.cli monitor --duration 60

# Check database query performance
uv run python -m mcp_server.cli db-stats
```

## Next Steps

After completing this quickstart:

1. **Customize ICPs**: Create industry-specific ideal customer profiles
2. **Configure Data Sources**: Add API keys for premium data providers
3. **Set Up Monitoring**: Enable structured logging and performance tracking
4. **Scale Infrastructure**: Configure connection pooling for production use
5. **Integrate CRM**: Connect prospect data to existing sales systems

For detailed implementation guide, see [Implementation Tasks](./tasks.md) (available after running `/tasks` command).

This quickstart demonstrates the complete value proposition of automated prospect research, from discovery through qualification to sales preparation, all integrated seamlessly with AI assistant workflows.
