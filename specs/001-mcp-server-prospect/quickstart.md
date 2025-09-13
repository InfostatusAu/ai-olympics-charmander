# Quickstart: MCP Prospect Research Server - 3-Step Workflow

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine  
**Phase**: 1 - Integration Guide and User Stories  
**Update**: 3-Step Workflow Implementation

## Overview

This quickstart guide demonstrates how to set up and use the MCP Prospect Research Server with AI assistants like Gemini CLI, VS Code Copilot, or Claude. The server provides a comprehensive 3-step prospect research workflow that transforms basic company information into actionable sales intelligence:

1. **Step 1: Research** - Gather comprehensive unstructured data
2. **Step 2: Mini Profile** - Generate structured 13-field prospect profile  
3. **Step 3: Talking Points** - Create personalized conversation starters

The complete workflow produces structured prospect intelligence ready for sales engagement.

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

## User Story Walkthroughs

### Story 1: Complete 3-Step Prospect Research Workflow
**Goal**: Transform a company name into actionable sales intelligence through the complete research workflow

**Scenario**: Sales rep needs complete prospect intelligence for "TechCorp Inc" outreach

**AI Assistant Conversation**:
```
User: "I need complete prospect intelligence for TechCorp Inc. Please run the full research workflow."

AI Assistant: I'll run the complete 3-step prospect research workflow for TechCorp Inc. Let me start with comprehensive research.

[Step 1: Research - AI calls research_prospect tool]

AI Assistant: ✅ Step 1 Complete - Research gathered from multiple sources:
- Company background and history
- Recent news and developments  
- Decision makers identified (Jane Smith - CTO, Mike Johnson - CEO)
- Technology stack analysis
- 6 research notes created with 85% confidence

Now generating structured Mini Profile...

[Step 2: Profile Generation - AI calls generate_profile tool]

AI Assistant: ✅ Step 2 Complete - Mini Profile generated:

**TechCorp Inc Mini Profile**
- **Size**: 150 employees
- **Revenue Range**: $50M-$100M  
- **Industry**: Software Development
- **Location**: San Francisco, CA
- **Hiring Signals**: Hiring Data Scientists & AI Engineers (5 open positions)
- **Tech Adoption**: Migrating to AWS cloud infrastructure, implementing AI/ML pipelines
- **Public & PR Signals**: Featured in TechCrunch for AI innovation, CEO speaking at ML conferences
- **Funding & Growth**: Series A $10M raised Aug 2025, 40% YoY growth
- **Decision-Makers**: Jane Smith (CTO), Mike Johnson (CEO) - both active on LinkedIn
- **Engagement Potential**: CTO posted about AI compliance challenges last week
- **Pain Points**: Manual data processing workflows, document handling inefficiencies

Now creating personalized talking points...

[Step 3: Talking Points - AI calls create_talking_points tool]

AI Assistant: ✅ Step 3 Complete - Personalized talking points generated:

**Conversation Starters for TechCorp Inc**

1. **🎯 AI Compliance Trend** (High relevance: 92%)
   "I noticed TechCorp was featured in TechCrunch for AI innovation. The fintech space is really embracing AI compliance frameworks - we've helped similar companies navigate the regulatory landscape while maintaining innovation speed."

2. **☁️ AWS Migration Opportunity** (High relevance: 88%)  
   "Saw you're migrating to AWS infrastructure. During cloud migrations, we often see companies struggle with document processing workflows. Our AWS-native solutions have helped similar companies reduce processing time by 70%."

3. **🚀 Series A Growth** (High relevance: 85%)
   "Congratulations on the Series A funding! With 40% YoY growth, scaling operational processes becomes critical. We've worked with several Series A companies to automate their document workflows before they become bottlenecks."

4. **👨‍💼 Hiring Data Scientists** (High relevance: 90%)
   "I see you're hiring data scientists and AI engineers. One challenge growing teams face is spending too much time on manual data preparation instead of actual modeling. Our document automation could free up your team for higher-value work."

**Workflow Complete!** TechCorp Inc is now ready for personalized outreach with structured intelligence and conversation starters.
```

**Expected Result**: Complete prospect intelligence package ready for sales engagement with structured profile and personalized talking points.

### Story 2: Step-by-Step Workflow Execution
**Goal**: Understand each step of the workflow individually

**AI Assistant Conversation**:
```
User: "Research TechFlow Solutions in detail, I want to understand their pain points and decision makers"

AI Assistant: I'll gather comprehensive research on TechFlow Solutions for you.

```
User: "Let me understand each step. First, just do the research step for DataStream Inc."

AI Assistant: I'll start with Step 1 - comprehensive research for DataStream Inc.

[AI calls research_prospect tool with company "DataStream Inc"]

AI Assistant: ✅ **Step 1 - Research Complete** for DataStream Inc:

**Research Summary:**
- 6 research notes created from multiple sources (Firecrawl, LinkedIn, news APIs)
- Company background: Data analytics platform, founded 2019
- Recent developments: New partnership with Microsoft Azure
- Decision makers identified: Tom Wilson (CEO), Lisa Zhang (CTO)
- Technology focus: Real-time analytics, cloud infrastructure
- Workflow Status: **research_complete**

The research data is now ready for profile generation. Would you like me to proceed to Step 2?

User: "Yes, generate the Mini Profile now"

AI Assistant: Moving to Step 2 - generating structured Mini Profile from research data.

[AI calls generate_profile tool using the research data]

AI Assistant: ✅ **Step 2 - Mini Profile Complete** for DataStream Inc:

**Mini Profile Generated:**
- **Company Name**: DataStream Inc
- **Size**: 89 employees  
- **Revenue Range**: $25M-$50M
- **Industry**: Data Analytics
- **Location**: Austin, TX
- **Hiring Signals**: Hiring Senior Data Engineers and Product Managers
- **Tech Adoption**: Azure-native architecture, real-time streaming
- **Public & PR Signals**: Microsoft partnership announcement, Austin Business Journal feature
- **Funding & Growth**: Bootstrapped, 60% YoY growth
- **Decision-Makers**: Tom Wilson (CEO), Lisa Zhang (CTO)
- **Engagement Potential**: CTO active on tech Twitter, CEO posts about data privacy
- **Pain Points**: Scaling real-time processing, compliance automation needs

The structured profile is ready. Would you like me to create talking points (Step 3)?

User: "Perfect, now create the talking points"

AI Assistant: Proceeding to Step 3 - generating personalized talking points.

[AI calls create_talking_points tool using the Mini Profile]

AI Assistant: ✅ **Step 3 - Talking Points Complete** for DataStream Inc:

**Personalized Conversation Starters:**

1. **Microsoft Partnership** (Relevance: 94%)
   "Congratulations on the Microsoft Azure partnership! We've worked with several Azure-native companies to streamline their compliance automation as they scale their data processing capabilities."

2. **Real-time Processing Scale** (Relevance: 91%)
   "I saw you're focusing on real-time analytics. One challenge we often see with streaming data platforms is managing document processing at scale - our automation tools integrate directly with Azure Event Hubs."

3. **Data Privacy Leadership** (Relevance: 87%)
   "Tom's posts about data privacy really resonate. With 60% YoY growth, maintaining compliance while scaling can be challenging - we've helped similar companies automate their data governance workflows."

**Complete 3-Step Workflow Finished!** DataStream Inc is now ready for personalized outreach with full intelligence package.
```

**Expected Result**: Understanding of each workflow step with clear progression and specialized outputs.

### Story 3: Finding New Prospects with ICP Matching
**Goal**: Discover qualified prospects matching ideal customer profile criteria

**AI Assistant Conversation**:
```
User: "Find new prospects for our document automation solution targeting tech companies with 50-200 employees"

AI Assistant: I'll search for qualified prospects matching your ICP criteria for document automation solutions.

[AI calls find_new_prospect tool with ICP parameters]

AI Assistant: Found 12 qualified prospects for document automation solutions:

**Top Matched Prospects:**

1. **TechFlow Solutions** (techflow.com) - 87% match
   - 125 employees, SaaS/Workflow automation
   - San Francisco, CA
   - Pain point indicators: Manual processes, scaling operations

2. **DataBridge Corp** (databridge.io) - 84% match  
   - 89 employees, Data integration platform
   - Seattle, WA
   - Pain point indicators: Document processing bottlenecks

3. **CloudSync Technologies** (cloudsync.tech) - 81% match
   - 156 employees, Cloud infrastructure
   - Denver, CO
   - Pain point indicators: Compliance documentation needs

Would you like me to run the complete 3-step workflow on any of these prospects to get full intelligence and talking points?
```

**Expected Result**: List of qualified prospects with match scores ready for detailed research workflow.

### Story 4: Workflow Status Tracking and Management  
**Goal**: Monitor and manage prospects through different workflow stages

**AI Assistant Conversation**:
```
User: "Show me all prospects and their workflow status. I want to see where each one is in the research process."

AI Assistant: I'll retrieve all prospects with their current workflow status.

[AI calls retrieve_prospect tool with workflow status focus]

AI Assistant: Here's your prospect pipeline with workflow status:

**Workflow Status Overview:**

📋 **Workflow Complete (Ready for Outreach):** 5 prospects
- TechCorp Inc - Profile + 6 talking points ready
- DataStream Inc - Profile + 4 talking points ready  
- CloudBridge Analytics - Profile + 5 talking points ready

📊 **Profile Complete (Need Talking Points):** 3 prospects
- StreamLine Software - Mini Profile ready, waiting for talking points
- DevOps Masters - Mini Profile ready, waiting for talking points

🔍 **Research Complete (Need Profile):** 4 prospects  
- TechFlow Solutions - 6 research notes ready for analysis
- DataBridge Corp - 5 research notes ready for analysis

⏳ **Initial/Researching:** 8 prospects
- CloudSync Technologies - Research in progress
- APIFirst Ltd - Research scheduled

**Recommended Actions:**
1. Complete talking points for 3 "Profile Complete" prospects
2. Generate profiles for 4 "Research Complete" prospects  
3. 5 prospects ready for immediate outreach

Would you like me to batch-process any of these workflow steps?
```

**Expected Result**: Clear pipeline visibility with actionable next steps for workflow progression.

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

1. **3-Step Workflow Test**: Validate complete research → profile → talking points workflow
2. **Tool Discovery Test**: Verify AI assistant can discover all 8 MCP tools
3. **Find Prospects Test**: Validate find_new_prospect returns qualified leads  
4. **Research Quality Test**: Confirm research_prospect gathers comprehensive data with workflow status tracking
5. **Profile Generation Test**: Ensure generate_profile creates structured Mini Profile from research
6. **Talking Points Test**: Validate create_talking_points generates relevant conversation starters
7. **Data Persistence Test**: Ensure save_prospect stores complete workflow data correctly
8. **Query Functionality Test**: Validate retrieve_prospect filtering with workflow status support
9. **Workflow Status Test**: Confirm proper workflow state transitions and status tracking
10. **Error Handling Test**: Verify graceful handling of invalid inputs and API failures

### Performance Validation
- **Response Time**: All tool calls complete within <200ms (excluding external API calls)
- **Workflow Completion**: Full 3-step process completes within <30 seconds
- **Concurrent Users**: Support multiple AI assistant connections simultaneously  
- **Data Quality**: Research confidence scores above 0.8, profile completeness above 85%
- **Talking Point Relevance**: Average relevance scores above 0.8

### Security Validation
- **Input Sanitization**: All tool parameters validated against JSON schemas
- **Database Security**: SQL injection prevention through parameterized queries
- **API Key Protection**: External service credentials properly secured
- **Workflow Integrity**: Prevent workflow step skipping, maintain data consistency

## Troubleshooting

### Common Workflow Issues

**Issue**: Workflow stuck at "research_complete" status
**Solution**: Check research data completeness - ensure minimum 3 research notes created before profile generation

**Issue**: Profile generation fails with low confidence
**Solution**: Review research data quality, run additional research with different focus areas

**Issue**: Talking points seem generic  
**Solution**: Verify Mini Profile has sufficient specific details, especially in pain points and engagement potential fields

### Common Workflow Issues

**Issue**: Workflow stuck at "research_complete" status
**Solution**: Check research data completeness - ensure minimum 3 research notes created before profile generation

**Issue**: Profile generation fails with low confidence
**Solution**: Review research data quality, run additional research with different focus areas

**Issue**: Talking points seem generic  
**Solution**: Verify Mini Profile has sufficient specific details, especially in pain points and engagement potential fields

**Issue**: Workflow status not updating
**Solution**: Check database connectivity and ensure workflow status transitions are properly committed

### Common Setup Issues

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

# Check database query performance and workflow metrics
uv run python -m mcp_server.cli db-stats --include-workflow

# Monitor workflow completion rates
uv run python -m mcp_server.cli workflow-stats
```

## Next Steps

After completing this quickstart:

1. **Customize ICPs**: Create industry-specific ideal customer profiles for better prospect matching
2. **Configure Data Sources**: Add API keys for premium data providers (Apollo, ZoomInfo, etc.)
3. **Tune Workflow Parameters**: Adjust confidence thresholds and analysis focus areas
4. **Set Up Monitoring**: Enable structured logging and performance tracking for workflow steps
5. **Scale Infrastructure**: Configure connection pooling and caching for production use
6. **Integrate CRM**: Connect prospect profiles and talking points to existing sales systems
7. **Train Sales Team**: Provide training on using AI-generated talking points effectively

For detailed implementation guide, see [Implementation Tasks](./tasks.md) (available after running `/tasks` command).

This quickstart demonstrates the complete value proposition of the 3-step automated prospect research workflow: transforming basic company information into structured intelligence with personalized conversation starters, all integrated seamlessly with AI assistant workflows.
