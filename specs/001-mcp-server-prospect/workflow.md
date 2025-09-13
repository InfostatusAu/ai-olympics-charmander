# Workflow Specification: Simplified 3-Step Markdown-First Process

**Date**: September 13, 2025  
**Feature**: MCP Server Prospect Research Workflow  
**Phase**: 1 - Simplified Workflow and Process Design  
**Update**: Refactored for markdown-first, minimal database approach

## Overview

The prospect research automation follows a streamlined 3-step process that creates **human-readable markdown files** with rich business intelligence for Infostatus sales teams.

## Core Architecture

**Database Role**: Minimal metadata tracking only  
**File System Role**: Rich AI-generated content storage  
**Output Focus**: Copy-paste ready markdown reports  

## The Simplified 3-Step Workflow

### Step 1: Comprehensive Research
**Purpose**: Gather research data and generate comprehensive markdown research report  
**Executor**: AI Agent using MCP `research_prospect` tool  
**Database**: Create/update minimal prospect record with research_status='researched'  
**Output**: Rich markdown file `/data/prospects/{id}_research.md`  

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

### Step 2: Structured Analysis - Mini Profile Generation  
**Purpose**: Transform research markdown into structured Mini Profile template  
**Executor**: AI Agent using MCP `generate_profile` tool  
**File Input**: Read `/data/prospects/{id}_research.md`  
**Output**: Structured markdown profile `/data/prospects/{id}_profile.md`  

**Process**:
1. AI agent reads the research markdown file
2. Analyzes unstructured research content
3. Generates structured Mini Profile with standardized fields:
   - Company metadata (size, revenue, location)
   - Business intelligence (hiring, tech adoption, funding)
   - Engagement signals (PR activity, decision maker activity)
   - Infostatus-specific pain points analysis

**Example Output** (`{id}_profile.md`):
```markdown
# Mini Profile: TechCorp Inc

| Field | Value |
|-------|--------|
| **Company** | TechCorp Inc |
| **Industry** | SaaS/AI |
| **Size** | 150-200 employees |
| **Revenue** | $10M-$25M (estimated) |
| **Location** | San Francisco, CA |
| **Funding** | Series A, $15M (March 2024) |
| **Tech Stack** | AWS, React, Node.js |
| **Hiring Signals** | Data Scientists, AI Engineers (5 positions) |
| **Tech Adoption** | AWS migration, AI/ML implementation |
| **Recent PR** | TechCrunch AI innovation feature |
| **Decision Makers** | CEO John Smith, CTO Jane Doe |
| **Engagement** | CTO LinkedIn post on AI compliance |
| **Infostatus Fit** | High - automation pain points identified |

## Key Pain Points for Infostatus
- Manual data processing workflows (20+ hours/week)
- Document handling inefficiencies
- Scaling operational processes

---
*Profile generated: 2025-09-13T11:15:00Z*
*Confidence: 0.83*
```

### Step 3: Personalized Talking Points Generation
**Purpose**: Create conversation starters from Mini Profile  
**Executor**: AI Agent using MCP `create_talking_points` tool  
**File Input**: Read `/data/prospects/{id}_profile.md`  
**Output**: Conversation starters `/data/prospects/{id}_talking_points.md`  

**Process**:
1. AI agent reads the structured Mini Profile
2. Generates personalized talking points across categories:
   - Business challenges and pain points
   - Technology opportunities and trends
   - Recent company news and developments
   - Personal/professional connection opportunities
   - Infostatus solution alignment points

**Example Output** (`{id}_talking_points.md`):
```markdown
# Conversation Starters: TechCorp Inc

## 🎯 Business Challenges
**Best for: Opening conversation about pain points**
- "I noticed you're scaling rapidly after your Series A - many companies your size struggle with manual data operations. How is TechCorp handling the increased volume?"
- "AWS migration is exciting - we often see companies face document processing challenges during cloud transitions..."

## 🔧 Technology Opportunities  
**Best for: Technical decision maker discussions**
- "Your React/Node.js stack aligns perfectly with our TypeScript SDK - integration typically takes under a week..."
- "With your AI/ML focus, automated document processing could free up your data scientists for higher-value work..."

## 📰 Recent Company News
**Best for: Warm conversation starters**
- "Congratulations on the Series A funding! That TechCrunch feature on your AI innovation was impressive..."
- "Saw the announcement about European expansion - data localization must be top of mind..."

## 👥 Personal Connections
**Best for: LinkedIn outreach**
- "Jane Doe's background in distributed systems is impressive - she'll appreciate our scalable architecture..."
- "I noticed John's previous experience at DataCorp - we've helped several similar companies..."

## ✅ Best Opening Lines
1. **Series A + scaling challenges** (Relevance: 0.92)
2. **AWS migration + document processing** (Relevance: 0.88)
3. **AI hiring + efficiency optimization** (Relevance: 0.85)

---
*Generated: 2025-09-13T11:45:00Z*
*Categories: 5 | Total points: 12*
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
Step 2 Complete: /data/prospects/{id}_profile.md exists  
Step 3 Complete: /data/prospects/{id}_talking_points.md exists
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
├── /data/prospects/{id}_profile.md
└── /data/prospects/{id}_talking_points.md
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
- **Step 3 Failure**: Keep profile file, generate generic talking points or retry
- **File Corruption**: Regenerate from previous step if source file exists
- **Partial Files**: Validate markdown format and completeness before marking complete

## Success Metrics

### Development Efficiency Metrics
- **Time to complete full 3-step workflow**: Target < 5 minutes per prospect
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
- Structured 13-field Mini Profile table
- Key business intelligence summary
- Infostatus-specific pain point analysis
- Engagement timing recommendations

**3. Talking Points File** (`/data/prospects/abc123_talking_points.md`):
- 8-12 categorized conversation starters
- Relevance scoring for each point
- Best opening lines recommendations
- Context for different conversation types

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

This simplified workflow specification demonstrates how **markdown-first architecture** creates more value with less complexity, enabling faster development and better business outcomes.
