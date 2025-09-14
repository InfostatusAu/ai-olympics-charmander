````markdown
# Implementation Plan: LLM Intelligence Middleware

**Branch**: `002-improve-research-with-llm` | **Date**: September 14, 2025

## Summary
Implement LLM intelligence middleware to replace manual data preparation logic in prospect research tools. The LLM sits between raw data collection from sub-level tools and template generation, providing intelligent analysis instead of hardcoded rules and string manipulation.

**Intelligence Middleware Pattern**: 
```
Sub-level Tools → Raw Data Collection → LLM Analysis → Template-Ready Data → Markdown Generation
```

## Problem Statement
**Current Issue**: Manual data preparation with hardcoded logic
- Research: `website_content[:1000] + "..."` truncation  
- Profile: `if 'ai' in pain_points[0].lower():` rule-based conversations
- Tech Stack: `[tech for tech in keywords if tech in content]` keyword matching
- Pain Points: Manual extraction with regex and string operations

**Solution**: LLM intelligence middleware for smart analysis
- Research: AI analyzes full context → generates business insights
- Profile: AI creates personalized conversation strategies  
- Tech Stack: AI identifies technology patterns and implications
- Pain Points: AI extracts business challenges from comprehensive data

## Technical Context
**Language**: Python 3.11+  
**Dependencies**: boto3 (AWS Bedrock client)  
**Integration**: Replace manual logic in existing prospect_research library  
**Templates**: Same structure, enhanced content quality
**Platform**: Linux server  
**Performance**: <60 seconds for AI-enhanced tools  
**Default Model**: `apac.anthropic.claude-sonnet-4-20250514-v1:0`

## Constitution Check

**Simplicity**: ✅ Replace complex manual logic with clean AI middleware  
**Architecture**: ✅ `llm_enhancer` intelligence middleware library  
**Testing**: ✅ RED-GREEN-Refactor cycle enforced  
**No Breaking Changes**: ✅ Same templates and MCP interfaces
**Observability**: ✅ Structured logging for AI analysis performance

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