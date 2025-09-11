# Product Requirements Document: AI Lead Generation System
**Team Charmander | 3-Day MVP Development**

---

## 1. Executive Summary

Development of an AI-powered lead generation system that integrates prospect identification, research automation, and lead qualification scoring to enhance cold calling effectiveness. The solution leverages MCP Server architecture with Gemini CLI as the primary agentic workflow platform.

## 2. Problem Statement

Sales teams lack systematic, AI-driven approaches to:
- Identify high-value prospects matching ideal customer profiles
- Conduct comprehensive prospect research at scale  
- Generate qualified leads with actionable conversation starters
- Maintain centralized prospect intelligence for future outreach

## 3. Product Objectives

**Primary Objective**: Deploy a functional AI agentic workflow that automates prospect research and qualification within 3 days.

**Secondary Objectives**: 
- Establish foundation for future CRM integration
- Create reusable evaluation framework for lead quality assessment  
- Demonstrate measurable improvement in cold calling preparation efficiency

---

## 4. Solution Architecture
<img width="1100" height="695" alt="image" src="https://github.com/user-attachments/assets/1b3d7b9b-c536-4c0c-81b7-9e86de332ad0" />


## 5. Core Product Deliverables

### 5.1 **Agentic Workflow System**
*Primary deliverable combining Gemini CLI with custom MCP tools*

The core "agent" is an orchestrated workflow design that combines:

| Component | Description | Implementation |
|-----------|-------------|----------------|
| **Gemini CLI** | Primary agent interface and orchestration engine | Custom `settings.json` + workflow prompts |
| **Custom MCP Server** | Prospect research and data management tools | Python-based server with 4 core tools |
| **Workflow Templates** | Structured prompts and instruction sets | Modular prompt design in `templates/` |
| **Data Integration** | External APIs + web scraping capabilities | Firecrawl + Playwright fallback |

### 5.2 **MCP Server Tools**
*Custom-built prospect research automation*

```python
# Core Tool Specifications
def find_new_prospect(query: str, limit: int) -> List[ProspectRecord]
def research_prospect(name: str, company: str) -> ProspectIntelligence  
def save_prospect(record: ProspectRecord) -> DatabaseResult
def retrieve_prospect(filters: SearchFilters) -> List[ProspectRecord]
```

### 5.3 **Lead Qualification System**
*Automated scoring and prioritization engine*

**LQS Framework** *(Lead Qualification Score)*
- **Fit Score** (0-5): Alignment with ICP criteria
- **Intent Score** (0-5): Buying signals and engagement indicators
- **Recency Score** (0-5): Recent company activities and news
- **Usefulness Score** (0-5): Quality of available contact information

### 5.4 **Documentation Package**
*Complete setup and evaluation materials*

> **Setup Documentation**
> - `README.md`: Installation and configuration guide
> - `ICP.md`: Ideal Customer Profile definitions
> - `data_sources.md`: Research source specifications

> **Evaluation Framework**
> - `rubric.md`: Human evaluation criteria
> - `ai_judge_prompt.md`: Automated assessment protocols
> - Sample prospect evaluation dataset

---

## 6. Technical Specifications

### 6.1 Technology Stack
- **Development Language**: Python
- **Development Methodology**: Specs-driven development
- **Database**: PostgreSQL via Supabase local stack
- **Web Scraping**: Firecrawl primary, Playwright fallback
- **Agent Platform**: Gemini CLI with MCP integration

### 6.2 Data Flow Architecture

```
User Input → Gemini CLI → MCP Tool Selection → Data Retrieval → 
LQS Processing → Database Storage → Research Card Generation → 
Call Opener Creation → Formatted Output
```

### 6.3 Repository Structure
```
cold-call-intelligence-charmander/
├── README.md
├── .gemini/
│   ├── settings.json              # Gemini CLI configuration
│   └── specs_driven/              # Development specifications
├── docs/
│   ├── ICP.md                     # Ideal Customer Profiles
│   ├── data_sources.md            # Research sources
│   └── evaluation_guideline.md    # Quality assessment
├── mcp_server/                    # Core MCP implementation
├── prospect_agent/                # Agentic workflow design
│   ├── templates/                 # Workflow prompts
│   └── prospect_flow.yaml         # Process orchestration
├── data/samples/                  # Test datasets
└── solution_tests/                # Evaluation framework
```

---

## 7. Acceptance Criteria

### 7.1 Technical Validation

**✓ Core Functionality**
- [ ] MCP server responds to all 4 tool calls successfully
- [ ] Gemini CLI executes complete prospect research workflow  
- [ ] Database maintains persistent prospect records with CRUD operations
- [ ] LQS scoring produces consistent, trackable results

**✓ Integration Requirements**
- [ ] Agentic workflow seamlessly combines multiple MCP tools
- [ ] Data sources provide reliable prospect information
- [ ] Generated outputs follow consistent formatting standards

### 7.2 Business Validation

**✓ Output Quality**
- [ ] Generated prospect research cards contain actionable intelligence
- [ ] Conversation starters demonstrate relevance to prospect context
- [ ] Human evaluators validate lead quality scores align with business judgment

**✓ Operational Efficiency** 
- [ ] System demonstrates measurable time savings vs. manual research process
- [ ] Workflow complexity remains manageable for non-technical users
- [ ] Documentation enables independent system operation

---

## 8. Team Responsibilities

| Role | Primary Deliverables | Key Activities |
|------|---------------------|----------------|
| **Hieu (Technical Lead)** | • MCP server implementation<br>• Gemini CLI integration<br>• LQS scoring algorithm | Code development, system architecture, technical documentation |
| **Cameron (Domain Expert)** | • ICP definition<br>• Data source mapping<br>• Quality evaluation rubric | Business requirements, lead qualification criteria, human evaluation |
| **Tra (Business Analyst)** | • Process documentation<br>• Acceptance criteria validation<br>• User experience design | Requirements analysis, testing coordination, workflow optimization |

---

**Document Version**: 1.0  
**Development Approach**: Specs-driven development with Python implementation  
**Target Environment**: Local development with Supabase stack
