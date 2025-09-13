# Workflow Specification: Simplified 2-Step Markdown-First Process

**Date**: September 13, 2025  
**Feature**: MCP Server Prospect Research Workflow  
**Phase**: 1 - Simplified Workflow and Process Design  
**Update**: Merged profile+strategy for 2-step workflow

## Overview

The prospect research automation follows a streamlined 2-step process that creates **human-readable markdown files** with rich business intelligence for Infostatus sales teams.

## Core Architecture

**Database Role**: Minimal metadata tracking only  
**File System Role**: Rich AI-generated content storage  
**Output Focus**: Copy-paste ready markdown reports with centralized calling strategy  

## The Simplified 2-Step Workflow

### Step 1: Comprehensive Research
**Purpose**: Gather research data and generate comprehensive markdown research report  
**Executor**: AI Agent using MCP `research_prospect` tool  
**Database**: Create/update minimal prospect record with research_status='researched'  
**Output**: Rich markdown file `/data/prospects/{id}_research.md`  

### Step 2: Profile + Strategy Generation  
**Purpose**: Transform research into structured mini profile table with conversation strategy  
**Executor**: AI Agent using MCP `create_profile` tool  
**Database**: Update prospect record metadata  
**Output**: Combined markdown file `/data/prospects/{id}_profile.md` containing mini profile table and talking points  

**Process**:
1. AI agent receives company identifier (name or domain)
2. MCP tool gathers data from multiple sources:
   - Direct API calls for official company data
   - Firecrawl for website content and public information
   - Playwright fallback for complex sites
3. AI generates comprehensive markdown research report with:
   - Company overview and background
   - Recent developments and news
   - Technology stack analysis
   - Decision maker identification
   - Pain points and challenges
   - Source attribution and metadata

**Example Output** (`{id}_research.md`):
```markdown
# Company Research: TechCorp Inc

## Company Overview
- **Industry**: SaaS/AI Technology
- **Size**: 150-200 employees
- **Location**: San Francisco, CA
- **Founded**: 2018

## Recent Developments
- Series A $15M funding (March 2024)
- Launched AI features (Q2 2024)
- European market expansion

## Technology Stack
- AWS cloud infrastructure
- React/Node.js stack
- PostgreSQL database

## Decision Makers
- **CEO**: John Smith (LinkedIn: /in/johnsmith)
- **CTO**: Jane Doe (LinkedIn: /in/janedoe)

## Pain Points Identified
- Manual data processing workflows
- Scaling customer support challenges
- Integration complexity with legacy systems

---
*Research completed: 2025-09-13T10:30:00Z*
*Sources: Company website, TechCrunch, LinkedIn*
*Confidence: 0.85*
```

### Step 2: Profile + Strategy Generation  
**Purpose**: Transform research markdown into structured Mini Profile table with conversation strategy  
**Executor**: AI Agent using MCP `create_profile` tool  
**File Input**: Read `/data/prospects/{id}_research.md`  
**Output**: Combined markdown file `/data/prospects/{id}_profile.md`  

**Process**:
1. AI agent reads the research markdown file
2. Analyzes unstructured research content
3. Generates structured Mini Profile with exactly 14 standardized fields (table format)
4. Creates conversation strategy with personalized talking points
5. Combines both sections into single markdown file

**Example Output** (`{id}_profile.md`):
```markdown
## Mini Profile – TechCorp Inc

| Field | Description | Example |
|-------|-------------|---------|
| **Company Name** | Name of the company | "TechCorp Inc" |
| **Size** | Number of employees | 150 |
| **Revenue Range** | Estimated revenue | $10M-$25M |
| **Industry** | Sector | SaaS/AI Technology |
| **Location** | Main location | San Francisco, CA |
| **Hiring Signals** | Job postings | Hiring "Data Scientists" & "AI Engineers" (5 positions) |
| **Tech Adoption** | Cloud/AI/automation | AWS migration, AI/ML implementation |
| **Public & PR Signals** | Press/news | TechCrunch: "TechCorp launches AI features" |
| **Funding & Growth** | Funding info | Series A $15M in March 2024 |
| **Tender/Compliance** | Gov contracts | Not applicable |
| **Decision-Makers** | Key roles | CEO John Smith & CTO Jane Doe identified |
| **Engagement Potential** | Activity | CTO LinkedIn post on AI compliance challenges |
| **Notes** | Other info | Member of San Francisco Tech Council |
| **Pain point(s)** | Inferred/observable outstanding, relevant pain point(s) that Infostatus might help/solve | Manual data processing workflows consuming 20+ hours/week, document handling inefficiencies, scaling challenges with legacy system integrations |

## Conversation Strategy

### Primary Talking Points
1. **🎯 AWS Migration Challenges** (94% relevance)
   "I noticed TechCorp is migrating to AWS infrastructure. During cloud transitions, document processing workflows often become bottlenecks. We've helped similar companies maintain processing speed while scaling on AWS."

2. **🚀 AI Feature Launch Success** (91% relevance)  
   "Congratulations on launching your AI features! Growing AI teams often spend too much time on document preparation instead of model development. Our automation could free up your engineers for higher-value work."

3. **📊 Series A Growth Scaling** (88% relevance)
   "With your Series A funding and rapid growth, operational efficiency becomes critical. We've worked with similar companies to automate their document workflows before they become bottlenecks."

### Conversation Openers
- **CTO LinkedIn Engagement**: "Jane's recent post about AI compliance really resonated..."
- **TechCrunch Feature**: "Saw the TechCrunch feature on your AI innovation..."
- **San Francisco Tech Network**: "Fellow SF tech company..."

### Next Actions
- Target CTO Jane Doe for technical discussion
- Reference Series A growth for timing relevance
- Focus on AWS integration capabilities
```

---
*Profile generated: 2025-09-13T11:15:00Z*
*Confidence: 0.83*
```

## Simplified State Management

### Research Status Tracking
Each prospect has a simple research_status in the database:
- `pending`: Identified but not yet researched
- `researched`: Research completed successfully  
- `failed`: Research attempt failed

### Workflow Progress Determination
Progress is determined by **file existence** rather than complex database states:

```
Step 1 Complete: /data/prospects/{id}_research.md exists
Step 2 Complete: /data/prospects/{id}_profile.md exists (contains mini profile + conversation strategy)
```

### State Transitions
```
pending → researched (when research_prospect completes successfully)
researched → failed (if subsequent steps fail)
any → pending (manual reset for re-research)
```

## File-Based Architecture

### Data Storage Strategy
```
Database: Minimal metadata only
├── prospect_id, company_name, domain
├── research_status, created_at, updated_at
└── (6 total fields)

File System: Rich AI-generated content
├── /data/icp.md (business-managed ICP)
├── /data/prospects/{id}_research.md
└── /data/prospects/{id}_profile.md (mini profile + conversation strategy)
```

### Integration with MCP Architecture
```
AI Agent → MCP Client → MCP Server → File Operations + SQLite
                                 ↓
                           Markdown Files (human-readable)
                                 ↓
                    Copy-paste ready business intelligence
```

### Tool Flow
1. **research_prospect**: Company data → SQLite record + research.md file
2. **generate_profile**: research.md → profile.md file  
3. **create_talking_points**: profile.md → talking_points.md file
4. **get_prospect_data**: SQLite + all markdown files → complete prospect context
5. **search_prospects**: SQLite query + optional file content search

### Error Handling and Recovery
- **Step 1 Failure**: Retry with different data sources, mark research_status='failed'
- **Step 2 Failure**: Keep research file, retry profile generation with adjusted prompts
- **Step 1 Failure**: Mark prospect as 'failed', can retry research
- **Step 2 Failure**: Keep research file, can retry profile+strategy generation  
- **File Corruption**: Regenerate from previous step if source file exists
- **Partial Files**: Validate markdown format and completeness before marking complete

## Success Metrics

### Development Efficiency Metrics
- **Time to complete full 2-step workflow**: Target < 3 minutes per prospect
- **File generation success rate**: Target > 95% for each step
- **Markdown quality scores**: Human readability and completeness ratings
- **Development velocity**: Faster iteration due to file-based debugging

### Business Impact Metrics
- **Sales team adoption**: Usage frequency of generated markdown files
- **Conversion rate improvement**: Effectiveness of talking points in actual calls
- **Time saved vs manual research**: Target 80% time reduction
- **Copy-paste usage**: How often content is directly used in emails/presentations

## Implementation Benefits

### Development Advantages
✅ **Faster Development**: No complex database migrations or schema evolution  
✅ **Easier Debugging**: Open markdown files directly to see AI outputs  
✅ **Simple Testing**: Compare markdown files for quality assessment  
✅ **Version Control**: Track changes to generated content over time  

### Business Advantages  
✅ **Human-Readable Outputs**: Sales team can directly read and use files  
✅ **Copy-Paste Ready**: Content formatted for emails, presentations, CRM  
✅ **Collaborative**: Business team can edit ICP file directly  
✅ **Portable**: Markdown files work across all platforms and tools  

### Operational Advantages
✅ **Simple Backups**: Just copy the /data folder  
✅ **Easy Scaling**: Add file storage without database complexity  
✅ **Template-Driven**: Consistent formatting across all outputs  
✅ **Future-Proof**: Can add database complexity later if needed  

## Example Workflow Execution

### Input
```
Company: "TechCorp Inc"
Domain: "techcorp.com"
```

### File Outputs Created

**1. Research File** (`/data/prospects/abc123_research.md`):
- Comprehensive company background
- Recent funding and developments  
- Technology stack analysis
- Decision maker identification
- Pain points and business challenges

**2. Profile File** (`/data/prospects/abc123_profile.md`):
- Structured 14-field Mini Profile table (exact format specified)
- Conversation strategy with personalized talking points
- Key business intelligence summary
- Engagement timing and approach recommendations

### Database Record
```sql
INSERT INTO prospects VALUES (
  'abc123',
  'TechCorp Inc', 
  'techcorp.com',
  'researched',
  '2025-09-13T10:30:00Z',
  '2025-09-13T11:45:00Z'
);
```

This simplified 2-step workflow specification demonstrates how **markdown-first architecture with merged profile+strategy files** creates more value with less complexity, enabling faster development and better business outcomes.
