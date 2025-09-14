````markdown
# Data Model: LLM Intelligence Middleware

**Date**: September 14, 2025  
**Feature**: Improve Research with LLM  

## Approach: Intelligence Middleware Pattern

**Architecture**: LLM as intelligent middleware between raw data and templates  
**Storage**: Existing prospect database unchanged  
**Processing**: Replace manual data preparation with AI analysis  
**Integration**: Enhance existing research and profile generation logic

## Current Problem: Manual Data Preparation

### Research Tool Current Flow (Inefficient)
```
Sub-level Tools → Raw Data → Manual String Processing → Template Filling
   ↓               ↓              ↓                        ↓
Firecrawl      website_html   background = content[:1000]  research_template.md
LinkedIn       search_results  tech_stack = keyword_match   
Job Boards     job_postings    pain_points = manual_rules
News Search    articles        decision_makers = regex_parse
```

### Profile Tool Current Flow (Hardcoded Logic)
```
Research Markdown → Manual Parsing → Hardcoded Rules → Profile Template
      ↓                 ↓                ↓                  ↓
research.md       parse_markdown()  if 'ai' in pain_points  profile_template.md
                                   conversation_starter_1()
                                   _generate_value_prop()
```

## Solution: LLM Intelligence Middleware

### Enhanced Research Flow  
```
Sub-level Tools → Raw Data Collection → LLM Analysis → Template Generation
   ↓                    ↓                    ↓              ↓
Firecrawl           raw_website_data     Analyze content    research_template.md
LinkedIn            raw_linkedin_data    → Extract insights   (AI-filled)
Job Boards          raw_job_data         → Identify patterns
News Search         raw_news_data        → Generate summaries
Government          raw_registry_data    → Business intelligence
```

### Enhanced Profile Flow
```
Raw Research Data → LLM Strategy Analysis → Profile Template Generation
       ↓                      ↓                        ↓
All collected data    → Conversation strategies    profile_template.md
Pain points          → Personalized talking points   (AI-generated)
Company insights     → Value proposition alignment
Decision makers      → Timing recommendations
```

## LLM Intelligence Middleware Architecture

### Core Middleware Pattern
```python
# Current manual approach (TO BE REPLACED)
research_data = {
    "background": website_content[:1000] + "...",  # Truncation
    "tech_stack": [tech for tech in keywords if tech in content],  # Keyword matching
    "pain_points": manual_rule_based_extraction(),  # Hardcoded rules
}

# New LLM middleware approach  
raw_data = {
    "website_content": full_website_scrape,      # Complete data
    "linkedin_results": all_linkedin_data,       # All findings
    "job_postings": complete_job_listings,       # Full job details
    "news_articles": complete_news_content,      # Full articles
    "registry_info": complete_registry_data      # All registry findings
}

enhanced_data = await llm_enhancer.analyze_for_template(
    raw_data=raw_data,
    template_type="research",
    template_structure=research_template_schema
)
```

### Intelligence Middleware Components

#### 1. Research Intelligence 
- **Input**: Raw data from all 5 sub-level tools
- **Processing**: AI analysis of business context, technology signals, pain points
- **Output**: Structured data matching research_template.md requirements

#### 2. Profile Intelligence
- **Input**: Complete research context + company insights  
- **Processing**: AI strategy generation, conversation planning, personalization
- **Output**: Structured data matching profile_template.md requirements

#### 3. Template-Aware Processing
- **Template Schema Understanding**: LLM knows what each template field needs
- **Content Optimization**: Generate content specifically for template structure  
- **Context Preservation**: Maintain research context across template sections

## MCP Server Configuration (LLM Enabled by Default)

### Enhanced Server Arguments
```bash
# Default: Intelligence middleware enabled
python -m src.mcp_server.cli \
    --llm-enabled true \
    --llm-provider bedrock \
    --model-id apac.anthropic.claude-sonnet-4-20250514-v1:0 \
    --temperature 0.3 \
    --max-tokens 4000 \
    --timeout-seconds 60

# Disable for fallback mode
python -m src.mcp_server.cli --llm-enabled false
```

### Server Parameter Schema
- `--llm-enabled`: Enable intelligence middleware (default: `true`)
- `--llm-provider`: AI service provider (default: `bedrock`) 
- `--model-id`: Model for analysis (default: `apac.anthropic.claude-sonnet-4-20250514-v1:0`)
- `--temperature`: Analysis creativity (default: `0.3`)
- `--max-tokens`: Analysis response limit (default: `4000`)
- `--timeout-seconds`: Analysis timeout (default: `60`)

### Environment Variables (AWS Credentials)
```bash
# Required for Bedrock provider
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx  
AWS_DEFAULT_REGION=ap-southeast-2
```

## Updated Architecture Integration

### Library Structure (Intelligence Middleware Added)
```
src/
├── database/          # ✅ Existing - SQLite operations (unchanged)
├── file_manager/      # ✅ Existing - Markdown templates (unchanged)  
├── prospect_research/ # 🔄 ENHANCED - Replace manual logic with LLM calls
├── mcp_server/        # 🔄 ENHANCED - Add LLM configuration parameters
└── llm_enhancer/      # 🆕 NEW - Intelligence middleware module
    ├── __init__.py
    ├── client.py      # Bedrock client wrapper
    ├── middleware.py  # Core intelligence processing
    ├── analyzers.py   # Research and profile analyzers
    └── cli.py         # Testing utilities
```

### Updated Tool Logic Flow
```
MCP Tool Request
    ↓
Sub-level Data Collection (Firecrawl, LinkedIn, etc.)
    ↓
Raw Data Aggregation
    ↓
LLM Intelligence Middleware (NEW)
    ↓  
Template-Ready Structured Data
    ↓
Markdown Generation (template filling)
```

## Replacement Strategy

### Functions to Replace with LLM Intelligence

#### Research Tool - Manual Data Preparation
```python
# CURRENT: Manual string manipulation (TO BE REPLACED)
research_data["background"] = website_content[:1000] + "..."
tech_indicators = ['Python', 'JavaScript', 'React', ...]
found_tech = [tech for tech in tech_indicators if tech.lower() in website_content.lower()]
research_data["tech_stack"] = found_tech

# NEW: LLM intelligent analysis
analyzed_data = await llm_middleware.analyze_research_data(
    raw_data=all_collected_data,
    template_fields=research_template_schema
)
```

#### Profile Tool - Hardcoded Conversation Logic  
```python
# CURRENT: Rule-based conversation generation (TO BE REPLACED)
def _generate_conversation_starter_1(parsed_data):
    if 'ai' in pain_points[0].lower():
        return "What's driving your current interest in AI initiatives?"
    elif 'cloud' in pain_points[0].lower():
        return "How are you approaching your cloud transformation?"
    # ... hardcoded rules

# NEW: LLM intelligent strategy generation
conversation_strategy = await llm_middleware.generate_profile_strategy(
    research_context=complete_research_data,
    template_fields=profile_template_schema
)
```

### Database Schema (Unchanged)
```python
# src/database/models.py - NO MODIFICATIONS NEEDED
class Prospect(Base):
    __tablename__ = "prospects"
    
    # All existing fields remain exactly the same
    id: str = Field(primary_key=True)
    company_name: str = Field(max_length=200)
    status: ProspectStatus = Field(default=ProspectStatus.CREATED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # NO new LLM tracking fields - middleware operates in-memory
```

## Fallback Strategy

### Graceful Degradation Pattern
```python
async def research_prospect_with_intelligence(company: str):
    # 1. Collect raw data (existing sub-level tools)
    raw_data = await collect_all_data_sources(company)
    
    # 2. Try LLM intelligence middleware
    try:
        if llm_enabled:
            structured_data = await llm_middleware.analyze_research_data(raw_data)
            enhancement_status = "ai_enhanced"
        else:
            structured_data = fallback_to_manual_processing(raw_data)
            enhancement_status = "manual_processing"
    except Exception as e:
        logger.warning(f"LLM analysis failed: {e}")
        structured_data = fallback_to_manual_processing(raw_data)
        enhancement_status = "fallback_manual"
    
    # 3. Generate markdown using structured data
    return generate_markdown_report(structured_data, enhancement_status)
```

### Enhanced Template Structure (Same Templates, Better Content)
```markdown
<!-- research_template.md - NO CHANGES to structure -->
# Prospect Research Report: {company_name}

## Company Background
{background}                    <!-- LLM: Intelligent business summary -->

## Recent News  
{recent_news}                   <!-- LLM: Relevant news analysis -->

## Technology Stack
{tech_stack}                    <!-- LLM: Tech infrastructure insights -->

## Key Decision Makers
{decision_makers}               <!-- LLM: Leadership analysis -->

## Identified Pain Points
{pain_points}                   <!-- LLM: Business challenge identification -->
```

## Constitutional Compliance

**Simplicity**: ✅ Clean middleware pattern, replace manual logic with AI analysis  
**Library-First**: ✅ `llm_enhancer` intelligence middleware with clear interface  
**Test-First**: ✅ Contract tests for AI vs manual processing behavior  
**No Database Changes**: ✅ Existing schema unchanged, middleware operates in-memory  
**Graceful Degradation**: ✅ Fallback to manual processing if LLM unavailable  
**MCP Integration**: ✅ Server parameters control intelligence middleware

## Implementation Benefits

1. **Intelligence Upgrade**: Replace hardcoded rules with AI analysis
2. **Same Templates**: No template changes needed, just better content
3. **Fallback Safety**: Manual processing available if LLM fails
4. **Zero Migration Risk**: No database or template structural changes
5. **Client Control**: MCP server parameters control AI features
6. **Performance Improvement**: Better quality output with same performance targets
7. **Maintainability**: Remove complex manual data preparation code
````
