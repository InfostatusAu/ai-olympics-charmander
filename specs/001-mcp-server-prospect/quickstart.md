# Quickstart: MCP Prospect Research Server - Simplified Markdown-First

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine  
**Phase*3. **📊 Document Processing Scale** (Relevance: 89%)
   "With TechCorp's rapid growth to 150 employees, manual document workflows become expensive quickly. We've seen similar companies reduce processing costs by 60% while improving accuracy."

**Complete Intelligence Package Ready!**
- Research report: 24.5 KB of comprehensive intelligence
- Profile + Strategy: 14.7 KB with structured table and personalized talking points
- All files saved with `{prospect_id}_` naming convention for future reference

TechCorp Inc is now ready for personalized outreach with complete markdown intelligence package.
```

**Expected Result**: Complete prospect intelligence package ready for sales engagement with structured 14-field profile table and integrated conversation strategy.ation Guide and User Stories  
**Update**: Simplified Markdown-First Architecture

## Overview

This quickstart guide demonstrates how to set up and use the simplified MCP Prospect Research Server with AI assistants. The server provides a streamlined 2-step research workflow that generates rich markdown files with minimal database complexity:

1. **Step 1: Research** - Generate comprehensive research markdown report
2. **Step 2: Profile + Strategy** - Create structured profile and talking points from research

The complete workflow produces two markdown files containing actionable sales intelligence.

## Prerequisites

- Python 3.11+ installed
- SQLite (built-in with Python)
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
# Initialize SQLite database (automatic on first run)
mkdir -p data/prospects
mkdir -p data/database

# No additional setup required - SQLite database created automatically
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

### Story 1: Complete 2-Step Prospect Research Workflow
**Goal**: Transform a company name into actionable sales intelligence through the complete research workflow

**Scenario**: Sales rep needs complete prospect intelligence for "TechCorp Inc" outreach

**AI Assistant Conversation**:
```
User: "I need complete prospect intelligence for TechCorp Inc. Please run the full research workflow."

AI Assistant: I'll run the complete 2-step prospect research workflow for TechCorp Inc. Let me start with comprehensive research.

[Step 1: Research - AI calls research_prospect tool]

AI Assistant: ✅ Step 1 Complete - Research markdown file created:

**File Generated**: `/data/prospects/techcorp-inc_research.md` (24.5 KB)

**Research Summary:**
- Company background, history, and business model analysis
- Recent news, partnerships, and strategic developments  
- Leadership team profiles (Jane Smith - CTO, Mike Johnson - CEO)
- Technology stack assessment and infrastructure analysis
- Market position and competitive landscape
- 6 detailed research sections with 85% confidence score

Now generating structured Profile + Conversation Strategy from research data...

[Step 2: Profile + Strategy - AI calls create_profile tool]

AI Assistant: ✅ Step 2 Complete - Profile + Strategy markdown generated:

**File Generated**: `/data/prospects/techcorp-inc_profile.md` (14.7 KB)

**Mini Profile Table:**
| Field | Description | Example |
|-------|-------------|---------|
| Company Name | Official company name | TechCorp Inc |
| Employee Count | Number of employees | 150 |
| Revenue Range | Annual revenue estimate | $50M-$100M |
| Industry | Primary industry sector | Software Development - AI/ML Platform |
| Location | Headquarters location | San Francisco, CA |
| Hiring Signals | Current hiring activity | 5 AI engineer positions, scaling team |
| Tech Adoption | Technology usage patterns | AWS migration in progress, ML pipelines |
| Public PR Signals | Recent news and announcements | $10M Series A, Microsoft partnership |
| Funding Growth | Financial growth indicators | 60% YoY growth, expanding to Austin |
| Tender Compliance | Government/compliance activity | SOC 2 certification in progress |
| Decision Makers | Key decision-maker contacts | Jane Smith (CTO), Mike Johnson (CEO) |
| Engagement Potential | Social media and industry presence | CTO active on LinkedIn, CEO speaker |
| General Notes | Additional observations | Strong technical team, scaling challenges |
| Infostatus Pain Points | Specific problems we can solve | Manual document workflows, AWS integration |

**Conversation Strategy:**

**🎯 Primary Talking Points:**

1. **AWS Migration Pain Points** (Relevance: 94%)
   "I noticed TechCorp is migrating to AWS infrastructure. During cloud transitions, document processing workflows often become bottlenecks. We've helped similar companies maintain processing speed while scaling on AWS."

2. **🚀 AI Engineering Team Growth** (Relevance: 92%)  
   "Congratulations on expanding your AI engineering team! Growing teams often spend too much time on document preparation instead of model development. Our automation could free up your engineers for higher-value work."

3. **� Document Processing Scale** (Relevance: 89%)
   "With TechCorp's rapid growth to 150 employees, manual document workflows become expensive quickly. We've seen similar companies reduce processing costs by 60% while improving accuracy."

**Complete Intelligence Package Ready!**
- Research report: 24.5 KB of comprehensive intelligence
- Structured profile: Key decision makers and pain points identified  
- Personalized talking points: 8 conversation starters with relevance scores
- All files saved in `/data/prospects/techcorp-inc/` for future reference

TechCorp Inc is now ready for personalized outreach with complete markdown intelligence package.
```

**Expected Result**: Complete prospect intelligence package ready for sales engagement with structured profile and personalized talking points.

### Story 2: Step-by-Step Workflow Execution
**Goal**: Understand each step of the workflow individually

**AI Assistant Conversation**:
```
User: "Let me understand each step. First, just do the research step for DataStream Inc."

AI Assistant: I'll start with Step 1 - comprehensive research for DataStream Inc.

[AI calls research_prospect tool with company "DataStream Inc"]

AI Assistant: ✅ **Step 1 - Research Complete** for DataStream Inc:

**File Generated**: `/data/prospects/datastream-inc_research.md` (18.7 KB)

**Research Summary:**
- Company founded 2019, data analytics platform focus
- Microsoft Azure partnership announced Q3 2025
- Leadership: Tom Wilson (CEO), Lisa Zhang (CTO) 
- Technology stack: Azure-native, real-time streaming architecture
- 89 employees, Austin TX headquarters
- Recent growth: 60% YoY, bootstrapped funding model
- 6 comprehensive research sections completed

The research markdown file contains detailed intelligence ready for profile generation. Would you like me to proceed to Step 2?

User: "Yes, generate the Profile + Strategy now"

AI Assistant: Moving to Step 2 - generating structured Profile + Conversation Strategy from research markdown.

[AI calls create_profile tool using the research data]

AI Assistant: ✅ **Step 2 - Profile + Strategy Complete** for DataStream Inc:

**File Generated**: `/data/prospects/datastream-inc_profile.md` (12.3 KB)

**Mini Profile Table:**
| Field | Description | Example |
|-------|-------------|---------|
| Company Name | Official company name | DataStream Inc |
| Employee Count | Number of employees | 89 |
| Revenue Range | Annual revenue estimate | $25M-$50M |
| Industry | Primary industry sector | Data Analytics Platform |
| Location | Headquarters location | Austin, TX |
| Hiring Signals | Current hiring activity | Expanding engineering team |
| Tech Adoption | Technology usage patterns | Azure-native, real-time streaming |
| Public PR Signals | Recent news and announcements | Microsoft Azure partnership Q3 2025 |
| Funding Growth | Financial growth indicators | 60% YoY growth, bootstrapped |
| Tender Compliance | Government/compliance activity | SOC 2 compliance planning |
| Decision Makers | Key decision-maker contacts | Tom Wilson (CEO), Lisa Zhang (CTO) |
| Engagement Potential | Social media and industry presence | CTO active on tech Twitter |
| General Notes | Additional observations | Strong Azure focus, privacy-first |
| Infostatus Pain Points | Specific problems we can solve | Scaling processing, compliance docs |

**Conversation Strategy:**

**🎯 Primary Talking Points:**

1. **Microsoft Partnership Leverage** (Relevance: 94%)
   "Congratulations on the Microsoft Azure partnership! As you scale your real-time analytics platform, document processing often becomes a bottleneck. Our Azure-native solutions integrate seamlessly with Event Hubs and Stream Analytics."

2. **Real-time Processing Optimization** (Relevance: 91%)
   "I noticed DataStream focuses on real-time analytics. With 60% YoY growth, maintaining low-latency document processing while scaling becomes critical. We've helped similar platforms maintain <100ms processing times at enterprise scale."

3. **Data Privacy Leadership** (Relevance: 87%)
   "Tom's thought leadership on data privacy really resonates. As streaming platforms grow, automated compliance documentation becomes essential. Our privacy-first approach helps maintain audit trails without slowing down processing."

**Complete 2-Step Workflow Package:**
- Research: 18.7 KB comprehensive intelligence
- Profile + Strategy: 12.3 KB with structured table and conversation starters
- Total: 31.0 KB of actionable sales intelligence

All files saved with `{prospect_id}_` naming convention for future reference and CRM integration.
```

**Expected Result**: Understanding of each workflow step with clear progression from research to integrated profile+strategy output.

### Story 3: Prospect Discovery and Pipeline Management
**Goal**: Find qualified prospects and manage them through the workflow pipeline

**AI Assistant Conversation**:
```
User: "Show me all prospects and their current status. I want to see where each one is in the research process."

AI Assistant: I'll retrieve all prospects with their current workflow status and file progress.

[AI calls search_prospects tool for pipeline overview]

AI Assistant: Here's your prospect pipeline with workflow status:

**Workflow Status Overview:**

📋 **Complete Workflow (Ready for Outreach):** 3 prospects
- **TechCorp Inc** - Both files ready (39.2 KB total intelligence)
  - techcorp-inc_research.md (24.5 KB), techcorp-inc_profile.md (14.7 KB)
- **DataStream Inc** - Both files ready (31.0 KB total)
  - datastream-inc_research.md (18.7 KB), datastream-inc_profile.md (12.3 KB)
- **CloudBridge Analytics** - Both files ready (33.8 KB total)
  - cloudbridge-analytics_research.md (21.2 KB), cloudbridge-analytics_profile.md (12.6 KB)

🔍 **Research Complete (Need Profile+Strategy):** 3 prospects  
- **TechFlow Solutions** - research.md ✅ (22.1 KB), profile.md ❌
- **DataBridge Corp** - research.md ✅ (19.8 KB), profile.md ❌
- **APIFirst Ltd** - research.md ✅ (16.4 KB), profile.md ❌

⏳ **Research Only:** 4 prospects
- **CloudSync Technologies** - Only basic metadata, no files yet

**Recommended Actions:**
1. Generate profiles for TechFlow, DataBridge, and APIFirst (3 prospects)  
2. 3 prospects ready for immediate outreach with complete intelligence packages

Would you like me to batch-process any of these workflow steps to complete the pipeline?

User: "Yes, complete the profile for StreamLine Software"

AI Assistant: I'll generate the profile+strategy for StreamLine Software using their existing research.

[AI calls create_profile tool for StreamLine Software]

AI Assistant: ✅ **Profile + Strategy Generated** for StreamLine Software:

**File Created**: `/data/prospects/streamline-software_profile.md` (13.4 KB)

**Pipeline Update**: StreamLine Software now has complete workflow:
- streamline-software_research.md ✅ (21.3 KB) 
- streamline-software_profile.md ✅ (13.4 KB) with table + talking points
- **Total Intelligence**: 34.7 KB ready for outreach

**Top Talking Points Included:**
1. **CI/CD Pipeline Optimization** (96% relevance)
2. **Developer Productivity Focus** (93% relevance)  
3. **Infrastructure Scaling Challenges** (89% relevance)

StreamLine Software is now ready for personalized outreach. Would you like me to complete profiles for the "Research Complete" prospects next?
```

**Expected Result**: Clear pipeline visibility with 2-step workflow progress tracking and actionable completion steps.

### Story 4: Accessing Prospect Intelligence 
**Goal**: Retrieve complete prospect data with all generated markdown files

**AI Assistant Conversation**:
```
User: "Show me everything we have on TechCorp Inc - I want to see all the research and profile+strategy"

AI Assistant: I'll retrieve the complete intelligence package for TechCorp Inc with all markdown files.

[AI calls get_prospect_data tool with include_content=true]

AI Assistant: Here's the complete TechCorp Inc intelligence package:

**📊 Prospect Overview**
- **Company**: TechCorp Inc  
- **Domain**: techcorp.com
- **Status**: Complete workflow (both files generated)
- **Created**: 2025-09-13 14:22:15
- **Last Updated**: 2025-09-13 14:35:42

**📄 Generated Files Summary**
- **techcorp-inc_research.md**: 24.5 KB (comprehensive intelligence)
- **techcorp-inc_profile.md**: 14.7 KB (structured profile + conversation strategy)
- **Total Intelligence**: 39.2 KB

**🔍 Research Highlights** (from techcorp-inc_research.md):
```markdown
# TechCorp Inc - Comprehensive Research Report

## Company Overview
TechCorp Inc is a 150-employee software development company specializing in AI/ML platforms...

## Recent Developments  
- AWS infrastructure migration in progress (Q4 2025)
- Raised $10M Series A funding (August 2025)
- Expanding AI engineering team (5 open positions)

## Leadership Team
- **Jane Smith, CTO**: 8 years experience, active on LinkedIn about AI compliance
- **Mike Johnson, CEO**: Former Facebook engineer, speaking at ML conferences

## Technology Stack
- Cloud Infrastructure: Migrating from on-premise to AWS
- AI/ML Stack: TensorFlow, PyTorch, custom ML pipelines
- Data Processing: Currently manual workflows causing bottlenecks
```

**👤 Profile + Strategy Summary** (from techcorp-inc_profile.md):
```markdown
# TechCorp Inc - Profile + Conversation Strategy

## Mini Profile
| Field | Description | Example |
|-------|-------------|---------|
| Company Name | Official company name | TechCorp Inc |
| Employee Count | Number of employees | 150 |
| Revenue Range | Annual revenue estimate | $50M-$100M |
| Industry | Primary industry sector | Software Development - AI/ML Platform |
| Location | Headquarters location | San Francisco, CA |
| Decision Makers | Key decision-maker contacts | Jane Smith (CTO), Mike Johnson (CEO) |
| Infostatus Pain Points | Specific problems we can solve | Manual document workflows, AWS integration |

## Conversation Strategy
**Infostatus Fit Score**: 8.7/10

**🎯 Primary Talking Points:**
1. **AWS Migration Pain Points** (94% relevance)
2. **AI Engineering Team Growth** (92% relevance)  
3. **Document Processing Scale** (89% relevance)
```

**Complete intelligence package ready for sales engagement.** All files are available using `{prospect_id}_` naming for CRM integration or export.
```

**Expected Result**: Complete prospect intelligence with integrated profile+strategy markdown ready for sales team usage.

### Story 5: Prospect Search and Filtering
**Goal**: Search prospects by metadata and content across all markdown files

**AI Assistant Conversation**:
```
User: "Find all prospects in the fintech industry who we've researched about API integration challenges"

AI Assistant: I'll search prospects by industry and content across all markdown files.

[AI calls search_prospects tool with industry filter and content search]

AI Assistant: Found 4 fintech prospects with API integration content:

**Search Results:**

1. **PaymentFlow Corp** - Complete workflow ✅
   - **Industry**: Fintech - Payment Processing
   - **Files**: Both files ready (paymentflow-corp_research.md, paymentflow-corp_profile.md)
   - **Match**: Research mentions "API gateway bottlenecks" and "payment processor integration complexity"
   - **Intelligence**: 41.8 KB total content
   - **Status**: Ready for outreach

2. **CreditAnalytics Inc** - Research only 📊
   - **Industry**: Fintech - Credit Scoring  
   - **Files**: creditanalytics-inc_research.md ✅, profile.md ❌
   - **Match**: Research highlights "third-party API orchestration challenges"
   - **Intelligence**: 19.3 KB research data
   - **Status**: Need profile+strategy generation

3. **LendingBridge** - Research only 📊
   - **Industry**: Fintech - Lending Platform
   - **Files**: lendingbridge_research.md ✅, profile.md ❌
   - **Match**: Research section on "API rate limiting issues with banking partners"
   - **Intelligence**: 19.2 KB research data
   - **Status**: Need profile+strategy generation

4. **FinTechFlow** - Research only 📊
   - **Industry**: Fintech - Data Aggregation
   - **Files**: fintechflow_research.md ✅, profile.md ❌
   - **Match**: Research covers "API standardization challenges across financial institutions"
   - **Intelligence**: 16.8 KB research data  
   - **Status**: Need profile+strategy generation

**Content Search Summary:**
- **Total Prospects Searched**: 47 in database
- **Fintech Prospects**: 12 total  
- **API Integration Mentions**: 4 matches found
- **Search Time**: 127ms (including markdown file content scan)

**Recommended Action Plan:**
1. **Immediate Outreach**: PaymentFlow Corp (complete intelligence ready)
2. **Pipeline Development**: Generate profiles+strategy for CreditAnalytics, LendingBridge, and FinTechFlow

Would you like me to complete the missing workflow steps for any of these prospects?
```

**Expected Result**: Targeted prospect list with content-based matching and clear next actions for 2-step workflow.

### Story 5: Complete End-to-End Workflow  
**Goal**: Full prospect discovery to outreach preparation with markdown intelligence

**AI Assistant Conversation**:
### Story 6: Complete End-to-End Workflow  
**Goal**: Full prospect discovery to outreach preparation with markdown intelligence

**AI Assistant Conversation**:
```
User: "I need to prepare for outreach to a SaaS company. Find a good prospect, research them completely, and prepare everything I need for the sales call."

AI Assistant: I'll help you find a qualified SaaS prospect and prepare complete intelligence. Let me start by researching a promising company.

[AI calls research_prospect with "CloudSync Technologies"]

✅ **Step 1 Complete** - Found excellent SaaS prospect:

**Initial Research**: CloudSync Technologies
- **Domain**: cloudsync.tech
- **Industry**: SaaS - Cloud Infrastructure Management
- **Size**: 156 employees, Series B funded
- **Generated**: `/data/prospects/cloudsync-technologies_research.md` (27.3 KB)

Now generating structured profile + conversation strategy...

[AI calls create_profile for CloudSync Technologies]

✅ **Step 2 Complete** - Profile + Strategy Generated:

**Generated**: `/data/prospects/cloudsync-technologies_profile.md` (17.5 KB)

**Mini Profile Table:**
| Field | Description | Example |
|-------|-------------|---------|
| Company Name | Official company name | CloudSync Technologies |
| Employee Count | Number of employees | 156 |
| Revenue Range | Annual revenue estimate | $25M-$50M |
| Industry | Primary industry sector | SaaS - Cloud Infrastructure Management |
| Location | Headquarters location | Seattle, WA |
| Hiring Signals | Current hiring activity | 12 engineering positions open |
| Tech Adoption | Technology usage patterns | Multi-cloud, K8s, compliance-focused |
| Public PR Signals | Recent news and announcements | $15M Series B, SOC 2 certification |
| Funding Growth | Financial growth indicators | 40% YoY growth, expanding Q4 |
| Tender Compliance | Government/compliance activity | SOC 2, preparing for FedRAMP |
| Decision Makers | Key decision-maker contacts | Sarah Chen (CTO), David Park (VP Eng) |
| Engagement Potential | Social media and industry presence | CTO speaks at CloudNativeCon |
| General Notes | Additional observations | Strong DevOps culture, remote-first |
| Infostatus Pain Points | Specific problems we can solve | Compliance docs, audit automation |

**Conversation Strategy:**
**Infostatus Fit**: 9.2/10 (excellent document automation fit)

**🎯 Primary Talking Points:**
1. **SOC 2 Compliance Challenge** (97% relevance)
2. **Engineering Team Efficiency** (94% relevance)
3. **Q4 Tooling Budget** (91% relevance)

## 🎯 Complete Sales Call Package Ready

**Prospect**: CloudSync Technologies
**Total Intelligence**: 44.8 KB of actionable insights

**📞 Pre-Call Brief:**
- **Primary Contact**: Sarah Chen, CTO (sarah.chen@cloudsync.tech)
- **Company Focus**: Multi-cloud infrastructure management platform
- **Immediate Need**: Compliance documentation automation
- **Budget Cycle**: Q4 2025 tool evaluation in progress
- **Competition**: Manual processes, considering Compliance.io

**💬 Top 3 Conversation Starters:**
1. **SOC 2 Compliance Challenge** (97% relevance)
   "I saw CloudSync recently completed SOC 2 certification. Managing compliance documentation across 50+ cloud environments manually is incredibly time-intensive. We've helped similar multi-cloud platforms reduce audit prep time by 80%."

2. **Engineering Team Efficiency** (94% relevance)
   "With 156 employees and rapid growth, your engineering teams probably spend significant time on documentation instead of feature development. Our automation integrates with your existing DevOps pipeline to eliminate manual doc generation."

3. **Q4 Tooling Budget** (91% relevance)
   "I understand CloudSync is evaluating new tooling solutions for Q4. Perfect timing - we typically see 6-month ROI for companies your size, and our implementation team can have you operational before year-end."

**📊 Company Intelligence Highlights:**
- AWS, Azure, GCP multi-cloud architecture
- Docker/Kubernetes container orchestration  
- 40% YoY growth, hiring DevOps engineers
- Recent $15M Series B funding
- Compliance-heavy customer base (healthcare, finance)

**🎯 Call Objectives:**
1. Confirm compliance documentation pain points
2. Demonstrate multi-cloud integration capabilities  
3. Schedule technical deep-dive with engineering team
4. Establish budget and timeline for Q4 decision

**Complete prospect intelligence package ready for sales engagement!** All files saved with `{prospect_id}_` naming convention for future reference.
```

**Expected Result**: Complete sales-ready package with research, integrated profile+strategy table, and call preparation guidance - all generated from 2-step AI-powered markdown workflow.

**Expected Result**: Complete sales-ready package with research, structured profile, talking points, and call preparation guidance - all generated from AI-powered markdown intelligence.

## Validation Tests

### Functional Validation  
Each user story above can be executed as an integration test:

1. **3-Step Workflow Test**: Validate complete research → profile → talking points workflow with markdown file generation
2. **Tool Discovery Test**: Verify AI assistant can discover all 5 simplified MCP tools
3. **Research Quality Test**: Confirm research_prospect generates comprehensive markdown reports with proper file structure
4. **Profile Generation Test**: Ensure generate_profile creates structured Mini Profile markdown from research files
5. **Talking Points Test**: Validate create_talking_points generates relevant conversation starters from profile markdown
6. **Data Retrieval Test**: Ensure get_prospect_data returns complete prospect metadata and file contents
7. **Search Functionality Test**: Validate search_prospects filters by metadata and searches markdown content
8. **File System Test**: Confirm proper directory structure and markdown file persistence
9. **Workflow Status Test**: Verify file existence determines workflow completion status
10. **Error Handling Test**: Verify graceful handling of missing files and invalid inputs

### Performance Validation
- **Response Time**: All tool calls complete within <200ms (excluding external API calls)
- **Workflow Completion**: Full 3-step process completes within <30 seconds
- **File Generation**: Markdown files created within <100ms per step
- **Content Quality**: Research reports average >20KB, profile summaries >7KB
- **Search Performance**: Content search across all prospects completes within <500ms

### File System Validation
- **Directory Structure**: Proper `/data/prospects/{company-name}/` folder creation
- **File Persistence**: Markdown files survive server restarts
- **Content Integrity**: No data corruption in markdown generation and storage
- **File Size Optimization**: Generated files are human-readable but efficient

## Troubleshooting

## Troubleshooting

### Common Workflow Issues

**Issue**: Workflow step fails with "research file not found"
**Solution**: Ensure research_prospect completed successfully before generate_profile. Check `/data/prospects/{company-name}/research.md` exists

**Issue**: Profile generation produces empty or minimal content
**Solution**: Verify research.md file has sufficient content (>15KB recommended). Re-run research with deeper focus areas

**Issue**: Talking points seem generic or irrelevant
**Solution**: Check profile.md contains specific pain points and decision-maker details. Ensure profile generation completed successfully

**Issue**: Files not persisting between server restarts
**Solution**: Verify data directory permissions and ensure `/data/prospects/` is writable

### Common Setup Issues

**MCP Server Not Responding**:
```bash
# Check server logs with verbose output
uv run python -m mcp_server.main --verbose

# Verify basic tool discovery
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  uv run python -m mcp_server.main
```

**File System Issues**:
```bash
# Check data directory structure
ls -la data/prospects/

# Verify directory permissions  
mkdir -p data/prospects && chmod 755 data/prospects

# Check available disk space
df -h
```

**SQLite Database Issues**:
```bash
# Check database file creation
ls -la data/database/prospects.db

# Test database connectivity
sqlite3 data/database/prospects.db ".tables"
```

### Performance Monitoring
```bash
# Monitor file system usage
du -sh data/prospects/

# Check markdown file generation performance
find data/prospects/ -name "*.md" -exec wc -l {} + | tail -1

# Monitor database size and performance
sqlite3 data/database/prospects.db ".dbinfo"
```

## Next Steps

After completing this quickstart:

1. **Configure Data Sources**: Add API keys for external research providers (optional for basic functionality)
2. **Customize Templates**: Modify markdown templates for research reports, profiles, and talking points
3. **Set Up File Management**: Configure backup and archival policies for prospect markdown files
4. **Tune Content Generation**: Adjust AI prompt templates for industry-specific research and talking points
5. **Scale Infrastructure**: Configure file system monitoring and cleanup policies for production use
6. **Integrate CRM**: Connect prospect metadata and markdown files to existing sales systems
7. **Train Sales Team**: Provide training on using AI-generated markdown intelligence effectively

For detailed implementation guide, see [Implementation Tasks](./tasks.md) (available after running `/tasks` command).

This quickstart demonstrates the complete value proposition of the simplified 3-step workflow: transforming basic company information into rich markdown intelligence files with minimal database complexity, all integrated seamlessly with AI assistant workflows.
