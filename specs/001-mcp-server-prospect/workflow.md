# Workflow Specification: 3-Step Prospect Research Process

**Date**: September 13, 2025  
**Feature**: MCP Server Prospect Research Workflow  
**Phase**: 1 - Workflow and Process Design  
**Update**: Critical workflow redesign based on user requirements

## Overview

The prospect research automation follows a structured 3-step process that transforms unstructured research into actionable business intelligence for Infostatus sales teams.

## The 3-Step Workflow

### Step 1: Comprehensive Research
**Purpose**: Gather comprehensive unstructured research data about the prospect company  
**Executor**: AI Agent (Gemini CLI) using MCP tools and external sources  
**Output**: Unstructured research data stored in database  

**Process**:
1. AI agent receives prospect company identifier (name, domain, or basic info)
2. Uses MCP `research_prospect` tool to gather data from multiple sources:
   - Direct API calls for official company data
   - Firecrawl API for website content and public information
   - Playwright MCP for complex JavaScript-heavy sites (fallback)
3. Stores all findings as unstructured `ResearchNote` entries with different types:
   - `company_background`
   - `recent_news` 
   - `pain_points`
   - `competitive_analysis`
   - `decision_makers`
   - `technology_stack`

**Tools Used**:
- `research_prospect(company_name, research_scope)`
- `store_research(prospect_id, research_data)`

### Step 2: Structured Analysis - Mini Profile Generation
**Purpose**: Transform unstructured research into structured Mini Profile template  
**Executor**: AI Agent with specialized analysis capabilities  
**Output**: Structured 13-field Mini Profile stored in database  

**Process**:
1. AI agent retrieves all unstructured research for a prospect
2. Uses MCP `generate_profile` tool to analyze and structure data into Mini Profile template
3. Creates structured `ProspectProfile` entity with specific fields:

#### Mini Profile Template Fields

| Field | Database Column | Type | Description |
|-------|----------------|------|-------------|
| **Company Name** | `company_name` | VARCHAR(255) | Official company name |
| **Size** | `employee_count` | INTEGER | Number of employees |
| **Revenue Range** | `revenue_range` | VARCHAR(50) | Estimated annual revenue |
| **Industry** | `industry` | VARCHAR(100) | Primary business sector |
| **Location** | `location` | VARCHAR(255) | Main headquarters location |
| **Hiring Signals** | `hiring_signals` | TEXT | Recent job postings and hiring activity |
| **Tech Adoption** | `tech_adoption` | TEXT | Cloud/AI/automation technology usage |
| **Public & PR Signals** | `public_pr_signals` | TEXT | Press releases, news mentions, public statements |
| **Funding & Growth** | `funding_growth` | TEXT | Funding rounds, growth indicators, financial news |
| **Tender/Compliance** | `tender_compliance` | TEXT | Government contracts, compliance activities |
| **Decision-Makers** | `decision_makers` | TEXT | Key decision-maker roles and identified contacts |
| **Engagement Potential** | `engagement_potential` | TEXT | Social media activity, industry engagement |
| **Notes** | `general_notes` | TEXT | Additional observations and context |
| **Pain Points** | `infostatus_pain_points` | TEXT | **Critical**: Specific pain points Infostatus can address |

**Tools Used**:
- `get_prospect_research(prospect_id)`
- `generate_profile(prospect_id, research_data)`

### Step 3: Personalized Talking Points Generation
**Purpose**: Create conversation starters and engagement opportunities  
**Executor**: AI Agent with personalization capabilities  
**Output**: Personalized talking points stored as separate entities  

**Process**:
1. AI agent uses the structured Mini Profile data
2. Uses MCP `create_talking_points` tool to generate personalized conversation starters
3. Creates multiple `TalkingPoint` entries categorized by type:
   - Personal/professional connections
   - Industry trends and challenges
   - Technology adoption opportunities
   - Recent company developments
   - Infostatus solution alignments

**Talking Point Categories**:
- `personal_professional`: Personal or professional connection opportunities
- `industry_trends`: Relevant industry developments for conversation
- `technology_opportunities`: Tech adoption talking points
- `company_developments`: Recent company news/changes to reference
- `solution_alignment`: How Infostatus solutions address identified pain points

**Tools Used**:
- `get_prospect_profile(prospect_id)`
- `create_talking_points(prospect_id, profile_data)`

## Workflow State Management

### Workflow Status Tracking
Each prospect goes through defined workflow states:

```
initial → researching → research_complete → analyzing → profile_complete → generating_points → workflow_complete
```

**State Definitions**:
- `initial`: Prospect identified, no research started
- `researching`: Step 1 in progress - gathering unstructured data
- `research_complete`: Step 1 done - research data stored
- `analyzing`: Step 2 in progress - generating structured profile
- `profile_complete`: Step 2 done - Mini Profile created
- `generating_points`: Step 3 in progress - creating talking points
- `workflow_complete`: All 3 steps complete - ready for sales engagement

### Workflow Triggers

**Manual Triggers**:
- Sales team requests research on new prospect
- Re-research requested for existing prospect (starts from Step 1)
- Profile update requested (starts from Step 2)

**Automated Triggers**:
- Scheduled re-research for prospects (configurable intervals)
- New public information detected for tracked prospects
- ICP criteria changes requiring re-analysis

## Integration with MCP Architecture

### Tool Flow
```
AI Agent → MCP Client → MCP Server → Tool Libraries → External APIs/Data
                                 ↓
                           PostgreSQL Database
                                 ↓
                        Structured Profile + Talking Points
```

### Database Integration
- **Step 1**: Populates `ResearchNote` table with unstructured findings
- **Step 2**: Creates `ProspectProfile` entity with structured Mini Profile data  
- **Step 3**: Creates multiple `TalkingPoint` entities with conversation starters
- **Tracking**: Updates `Prospect.workflow_status` throughout process

### Error Handling and Recovery
- **Step 1 Failure**: Retry with different data sources, fallback to manual research
- **Step 2 Failure**: Re-run analysis with adjusted prompts, manual profile creation
- **Step 3 Failure**: Generate generic talking points, flag for manual review
- **Partial Completion**: Allow workflow to resume from last successful step

## Success Metrics

### Workflow Completion Metrics
- Time to complete full 3-step workflow
- Success rate for each step individually
- Data quality scores for generated profiles
- Talking point relevance and usability ratings

### Business Impact Metrics
- Sales team engagement with generated profiles
- Conversion rate improvement with talking points
- Time saved vs. manual prospect research
- Accuracy of pain point identification for Infostatus solutions

## Constitutional Compliance

### Ethical Guidelines
- Respect prospect privacy and public information boundaries
- Use only publicly available information sources
- Provide opt-out mechanisms for prospects
- Ensure data accuracy and source attribution
- Regular compliance audits for information gathering practices

### Data Governance
- Clear data retention policies for research data
- GDPR compliance for prospect information storage
- Audit trails for all workflow steps and data sources
- Regular data quality assessments and corrections

## Example Workflow Execution

### Input
```
Company: "ABC Financial Services"
Domain: "abcfinancial.com.au"
```

### Step 1 Output (Research)
- Company background research note
- Recent news and press coverage
- Technology stack analysis
- Decision maker identification
- Industry competitive analysis

### Step 2 Output (Mini Profile)
```
Company Name: ABC Financial Services
Size: 300 employees
Revenue Range: $120M
Industry: Financial Services
Location: Sydney, NSW
Hiring Signals: Hiring "Data Scientist" & "Head of Innovation"
Tech Adoption: Migrating to AWS, exploring predictive analytics
Public & PR Signals: AFR: "ABC invests in AI fraud detection"
Funding & Growth: Series B $15M in 2023
Tender/Compliance: Listed in NSW eTendering for financial IT project
Decision-Makers: CIO & CFO identified
Engagement Potential: CFO LinkedIn post on AI compliance
Notes: Member of FinTech Australia
Pain Points: Needs to speed up banking document automation tasks
```

### Step 3 Output (Talking Points)
1. **Industry Trends**: "Noticed ABC is investing in AI fraud detection - this aligns with the broader FinTech trend toward automated compliance."
2. **Technology Opportunity**: "Your AWS migration could benefit from our document processing solutions for cloud-native workflows."
3. **Personal Connection**: "Saw the CFO's LinkedIn post about AI compliance - we've helped similar financial services navigate this challenge."
4. **Solution Alignment**: "Based on your NSW government tender for financial IT, our document automation could streamline your public sector documentation requirements."

This workflow specification provides the framework for transforming the current MCP server from a general research tool into a specialized 3-step prospect intelligence engine focused on generating actionable sales insights.
