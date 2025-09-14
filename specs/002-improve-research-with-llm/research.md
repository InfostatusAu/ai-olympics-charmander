# Research: Simple LLM Enhancement Module

**Date**: September 14, 2025  
**Feature**: Improve Research with LLM  

## Key Decision: Simplified Approach

**What we're doing**:
- Single LLM enhancement module with prompts as code
- Direct integration into existing research/profile functions
- Simple fallback to original content on LLM failure
- AWS credentials via environment variables only

## Research Findings

### 1. AWS Bedrock Model Selection

**Model ID**: `anthropic.claude-3-5-sonnet-20241022-v2:0`  
**Rationale**: Claude 3.5 Sonnet V2 provides best balance of quality, speed, and availability

### 2. Integration Pattern

```python
async def research_prospect(company: str):
    # 1. Run existing research (unchanged)
    raw_research_data = await existing_research_logic(company)
    
    # 2. Enhance with LLM (new)
    try:
        enhanced_content = await llm_enhancer.enhance(raw_research_data, 'research')
        research_data.update(enhanced_content)
    except Exception as e:
        logger.warning(f"LLM enhancement failed: {e}, using original content")
    
    # 3. Generate markdown (existing logic)
    return await generate_markdown_report(research_data)
```

### 3. Prompts as Code Strategy

```python
# src/llm_enhancer/prompts.py
RESEARCH_ENHANCEMENT_PROMPT = """
Analyze company research data and generate business insights:
1. Technology readiness assessment
2. Competitive positioning analysis
3. Specific pain points based on data signals

Research data: {research_data}
Generate enhanced insights in markdown format.
"""
```

### 4. Configuration

**Environment Variables**:
```bash
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_DEFAULT_REGION=ap-southeast-2
LLM_ENHANCEMENT_ENABLED=true
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### 5. Error Handling

**Approach**: Fail gracefully, always return content
- LLM failure → log warning, use original content
- Invalid response → log error, use original content  
- Timeout → log timeout, use original content
- No AWS credentials → log error, use original content

## Implementation Architecture

### Module Structure
```
src/llm_enhancer/
├── __init__.py          # Module exports
├── enhancer.py          # Main enhancement logic
├── prompts.py           # Prompts as code
├── client.py            # AWS Bedrock client wrapper
└── llms.txt             # Module documentation
```

### Dependencies
- `boto3` (AWS SDK) - only new dependency needed
