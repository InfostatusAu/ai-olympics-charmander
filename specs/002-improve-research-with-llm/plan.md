````markdown
# Implementation Plan: LLM Intelligence Middleware

**Branch**: `002-improve-research-with-llm` | **Date**: September 14, 2025

## Summary
Implement LLM intelligence middleware to replace manual data preparation logic in prospect research tools. The LLM sits between raw data collection from sub-level tools and template generation, providing intelligent analysis instead of hardcoded rules and string manipulation.

**Intelligence Middleware Pattern**: 
```
Sub-level Tools → Raw Data Collection → LLM Analysis → Template-Ready Data → Markdown Generation
```

## Problem Statement: Manual Data Preparation Logic

### Current Issue: Hardcoded Rules and String Manipulation
**Research Tool Current Flow (Inefficient)**:
```
Sub-level Tools → Raw Data → Manual String Processing → Template Filling
   ↓               ↓              ↓                        ↓
Firecrawl      website_html   background = content[:1000]  research_template.md
LinkedIn       search_results  tech_stack = keyword_match   
Job Boards     job_postings    pain_points = manual_rules
News Search    articles        decision_makers = regex_parse
```

**Profile Tool Current Flow (Hardcoded Logic)**:
```
Research Markdown → Manual Parsing → Hardcoded Rules → Profile Template
      ↓                 ↓                ↓                  ↓
research.md       parse_markdown()  if 'ai' in pain_points  profile_template.md
                                   conversation_starter_1()
                                   _generate_value_prop()
```

**Examples of Manual Logic to Replace**:
```python
# CURRENT: Manual string manipulation (TO BE REPLACED)
research_data["background"] = website_content[:1000] + "..."
tech_indicators = ['Python', 'JavaScript', 'React', ...]
found_tech = [tech for tech in tech_indicators if tech.lower() in website_content.lower()]

# CURRENT: Rule-based conversation generation (TO BE REPLACED)
def _generate_conversation_starter_1(parsed_data):
    if 'ai' in pain_points[0].lower():
        return "What's driving your current interest in AI initiatives?"
    elif 'cloud' in pain_points[0].lower():
        return "How are you approaching your cloud transformation?"
```

### Solution: LLM Intelligence Middleware

**Enhanced Research Flow**:
```
Sub-level Tools → Raw Data Collection → LLM Analysis → Template Generation
   ↓                    ↓                    ↓              ↓
Firecrawl           raw_website_data     Analyze content    research_template.md
LinkedIn            raw_linkedin_data    → Extract insights   (AI-filled)
Job Boards          raw_job_data         → Identify patterns
News Search         raw_news_data        → Generate summaries
Government          raw_registry_data    → Business intelligence
```

**Enhanced Profile Flow**:
```
Raw Research Data → LLM Strategy Analysis → Profile Template Generation
       ↓                      ↓                        ↓
All collected data    → Conversation strategies    profile_template.md
Pain points          → Personalized talking points   (AI-generated)
Company insights     → Value proposition alignment
Decision makers      → Timing recommendations
```

## Technical Architecture

### Intelligence Middleware Components

#### 1. LLM Enhancement Module (`llm_enhancer`)
```python
# Core middleware pattern
async def analyze_research_data(raw_data: dict, template_schema: dict) -> dict:
    """Replace manual data preparation with AI analysis"""
    if not llm_enabled:
        return fallback_to_manual_processing(raw_data)
    
    try:
        enhanced = await bedrock_client.analyze(raw_data, template_schema)
        enhanced['enhancement_status'] = 'ai_enhanced'
        return enhanced
    except Exception as e:
        logger.warning(f"LLM analysis failed: {e}")
        fallback_data = fallback_to_manual_processing(raw_data)
        fallback_data['enhancement_status'] = 'manual_fallback'
        return fallback_data
```

#### 2. MCP Server Configuration (LLM Enabled by Default)
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

#### 3. Replacement Strategy
- **research_prospect()**: Replace data preparation with `research_analyzer.analyze()`
- **create_profile()**: Replace rule logic with `profile_analyzer.generate_strategy()`  
- **Helper functions**: Remove hardcoded conversation/value prop generators
- **Template filling**: Same templates, AI-generated content

#### 4. Fallback Strategy
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
    
    # 3. Generate markdown using structured data (same templates)
    return generate_markdown_report(structured_data, enhancement_status)
```

### Environment Configuration
```bash
# Required for Bedrock provider
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx  
AWS_DEFAULT_REGION=ap-southeast-2
```

## Technical Context
**Language**: Python 3.11+  
**Dependencies**: boto3 (AWS Bedrock client)  
**Integration**: Replace manual logic in existing prospect_research library  
**Templates**: Same structure, enhanced content quality
**Platform**: Linux server  
**Performance**: <60 seconds for AI-enhanced tools  
**Default Model**: `apac.anthropic.claude-sonnet-4-20250514-v1:0`

## Constitution Check

**Simplicity**: ✅ Clean middleware pattern, replace manual logic with AI analysis  
**Architecture**: ✅ `llm_enhancer` intelligence middleware with clear interface  
**Testing**: ✅ RED-GREEN-Refactor cycle enforced  
**No Database Changes**: ✅ Existing schema unchanged, middleware operates in-memory  
**Graceful Degradation**: ✅ Fallback to manual processing if LLM unavailable  
**MCP Integration**: ✅ Server parameters control intelligence middleware

## Project Structure

### Enhanced Architecture (Intelligence Middleware Integration)
```
src/
├── database/          # ✅ Existing - SQLite operations (unchanged)
├── file_manager/      # ✅ Existing - Markdown templates (unchanged) 
├── prospect_research/ # 🔄 ENHANCED - Replace manual logic with LLM middleware calls
│   ├── research.py    # Replace string manipulation with AI analysis
│   └── profile.py     # Replace hardcoded rules with AI strategy generation
├── mcp_server/        # 🔄 ENHANCED - Add LLM configuration parameters
└── llm_enhancer/      # 🆕 NEW - Intelligence middleware module
    ├── __init__.py
    ├── client.py      # AWS Bedrock client wrapper
    ├── middleware.py  # Core intelligence coordination
    ├── analyzers.py   # Research and profile AI analyzers
    └── cli.py         # Testing and debugging utilities  
```

### Manual Logic Replacement Strategy
1. **research_prospect()** → Replace data preparation with `research_analyzer.analyze()`
2. **create_profile()** → Replace rule logic with `profile_analyzer.generate_strategy()`  
3. **Helper functions** → Remove hardcoded conversation/value prop generators
4. **Template filling** → Same templates, AI-generated content

## Phase Summary

**Phase 0**: ✅ Research complete - Manual logic patterns identified  
**Phase 1**: ✅ Design complete - Intelligence middleware architecture defined
**Phase 2**: Task planning approach for middleware implementation

### Task Planning Approach
1. **Middleware Creation**: Create `llm_enhancer` with AI analyzers
2. **Research Logic Replacement**: Replace manual data prep with AI analysis  
3. **Profile Logic Replacement**: Replace hardcoded rules with AI strategy
4. **Server Enhancement**: Add LLM parameters to MCP server CLI
5. **Fallback Implementation**: Preserve original logic for graceful degradation
6. **Testing Strategy**: Contract tests for AI vs manual processing
7. **Integration Validation**: End-to-end workflow testing

**Estimated Tasks**: ~18-22 focused tasks covering middleware, replacement, integration

### Key Implementation Points
- **Data Collection**: Keep existing sub-level tool integration (Firecrawl, LinkedIn, etc.)  
- **Intelligence Layer**: Add AI analysis between data collection and template filling
- **Template Compatibility**: No changes to template structure, just better content
- **Fallback Safety**: Maintain original manual processing for error scenarios
- **Performance**: AI analysis within acceptable response time limits
- **Configuration**: MCP server parameters control AI features

## Phase Summary

**Phase 0**: ✅ Research complete - Simple LLM patterns and AWS Bedrock model selection  
**Phase 1**: ✅ Design complete - Minimal configuration, prompts as code, no database changes  
**Phase 2**: Task planning approach described (NOT executed by /plan)

### Task Planning Approach
Create simple LLM enhancement module with prompts as code. Integrate LLM calls into existing `research_prospect` and `create_profile` functions. Focus on TDD: Contract tests → Simple implementation → Integration tests.

**Estimated Tasks**: ~13 focused tasks covering module creation, contract tests, integration, and validation.

**Implementation Pattern**:
```python
# In research.py:
async def research_prospect(company: str):
    raw_data = { ... }  # Current research results
    try:
        enhanced_content = await llm_enhancer.enhance(raw_data, 'research')
    except Exception:
        enhanced_content = generate_static_analysis(raw_data)  # Fallback
```