# Implementation Plan: Improve Research with LLM

**Branch**: `002-improve-research-with-llm` | **Date**: September 14, 2025

## Summary
Create a simple LLM module using AWS Bedrock that enhances existing research data with Claude intelligence. No database changes, prompts as code, direct content enhancement only.

**Core Pattern**: 
```
raw_data → LLM_enhance(raw_data, prompt_type) → enhanced_content
```

## Technical Context
**Language**: Python 3.11+  
**Dependencies**: boto3 (AWS Bedrock client)  
**Storage**: File-based markdown reports  
**Platform**: Linux server  
**Performance**: <5 seconds for LLM enhancement  
**Model**: `anthropic.claude-3-5-sonnet-20241022-v2:0`

## Constitution Check

**Simplicity**: ✅ Single enhancement module, no complex patterns  
**Architecture**: ✅ `llm_enhancer` library with CLI for testing  
**Testing**: ✅ RED-GREEN-Refactor cycle enforced  
**Observability**: ✅ Structured logging for LLM calls, failures, response times

## Project Structure

### Source Code
```
src/
├── llm_enhancer/      # NEW - Simple LLM enhancement module
│   ├── __init__.py
│   ├── enhancer.py    # Main enhancement logic
│   ├── prompts.py     # Prompts as code (version controlled)
│   ├── client.py      # Simple AWS Bedrock client
│   └── llms.txt       # Simple module documentation
└── prospect_research/ # ENHANCED - Add LLM calls to existing functions
```

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