# Data Model: Simple LLM Enhancement

**Date**: September 14, 2025  
**Feature**: Improve Research with LLM  

## Approach: No Database Changes

**Configuration**: Environment variables only
**Prompts**: Python files (version controlled)
**Storage**: Existing prospect database unchanged
**Processing**: In-memory enhancement with graceful fallback

## Environment Variables

```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_DEFAULT_REGION=ap-southeast-2

# LLM Control
LLM_ENHANCEMENT_ENABLED=true
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
BEDROCK_TEMPERATURE=0.3
BEDROCK_MAX_TOKENS=2000
BEDROCK_TIMEOUT_SECONDS=30
```

## Prompts as Code

```python
# src/llm_enhancer/prompts.py
RESEARCH_ENHANCEMENT_PROMPT = """
Analyze company research data and generate business insights:
1. Technology readiness assessment
2. Competitive positioning analysis
3. Specific pain points based on signals

Research data: {research_data}
Generate enhanced insights in markdown format.
"""

PROFILE_ENHANCEMENT_PROMPT = """
Create sales conversation strategies:
1. Personalized conversation starters
2. Decision maker approach strategies
3. Value proposition alignment

Research data: {research_data}
Format as conversation strategy in markdown.
"""
```

## Enhancement Pattern

```python
async def enhance_content(raw_data: dict, prompt_type: str) -> dict:
    if not config.LLM_ENHANCEMENT_ENABLED:
        return raw_data
    
    try:
        enhanced = await bedrock_client.enhance(raw_data, prompt_type)
        enhanced['enhancement_status'] = 'enhanced'
        return enhanced
    except Exception as e:
        logger.warning(f"LLM enhancement failed: {e}")
        raw_data['enhancement_status'] = 'fallback'
        return raw_data
```

## Database Schema (Unchanged)

```python
# src/database/models.py - NO MODIFICATIONS
class Prospect(Base):
    __tablename__ = "prospects"
    id: str = Field(primary_key=True)
    company_name: str = Field(max_length=200)
    status: ProspectStatus = Field(default=ProspectStatus.CREATED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # NO new LLM fields - enhancement tracked in-memory only
```  

## Configuration Management

### Environment Variables Only
```bash
# AWS Bedrock (existing pattern)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_DEFAULT_REGION=ap-southeast-2

# LLM Feature Control (new)
LLM_ENHANCEMENT_ENABLED=true

# Model Settings (new, with defaults)
BEDROCK_MODEL_ID=apac.anthropic.claude-sonnet-4-20250514-v1:0
BEDROCK_TEMPERATURE=0.3
BEDROCK_MAX_TOKENS=2000
BEDROCK_TIMEOUT_SECONDS=30
```

### Prompts as Code (No Database)
```python
# src/llm_enhancer/prompts.py
"""Prompts stored as code, version controlled with git"""

RESEARCH_ENHANCEMENT_PROMPT = """
You are a B2B sales intelligence analyst. Analyze the provided company research data 
and generate sophisticated business insights.

Focus on:
1. Technology readiness assessment
2. Digital transformation indicators  
3. Competitive positioning analysis
4. Specific pain points based on data signals

Research data:
{research_data}

Generate enhanced insights in markdown format with clear sections.
"""

PROFILE_ENHANCEMENT_PROMPT = """
You are a sales strategy expert. Based on the research data, create actionable 
conversation strategies for sales outreach.

Generate:
1. Personalized conversation starters
2. Decision maker approach strategies  
3. Optimal timing recommendations
4. Value proposition alignment

Research data:
{research_data}

Format as conversation strategy in markdown.
"""

# Version control through git commits, not database
PROMPT_VERSION = "1.0.0"  # Updated manually with changes
```

## Data Flow (No Database Changes)

### Simple Enhancement Pattern
```python
async def enhance_research_content(raw_research_data: dict) -> dict:
    """Enhance research without changing database schema"""
    
    # 1. Check if enhancement enabled
    if not os.getenv('LLM_ENHANCEMENT_ENABLED', 'false').lower() == 'true':
        return raw_research_data  # Return original
    
    # 2. Try LLM enhancement
    try:
        enhanced_insights = await bedrock_client.enhance(
            raw_research_data, 
            RESEARCH_ENHANCEMENT_PROMPT
        )
        
        # 3. Merge enhanced content with original
        enhanced_data = raw_research_data.copy()
        enhanced_data['ai_business_insights'] = enhanced_insights
        enhanced_data['enhancement_status'] = 'enhanced'
        
        return enhanced_data
    
    except Exception as e:
        # 4. Graceful fallback to original
        logger.warning(f"LLM enhancement failed: {e}")
        fallback_data = raw_research_data.copy()
        fallback_data['enhancement_status'] = 'fallback'
        return fallback_data
```

### Template Integration (File-Based)
```python
# Modified template filling - no database changes needed
def fill_research_template(research_data: dict) -> str:
    """Fill template with enhanced or original content"""
    
    template = load_template('research_template.md')
    
    # Enhanced sections (if available)
    if research_data.get('ai_business_insights'):
        template_vars = {
            **research_data,  # Original fields
            'ai_insights': research_data['ai_business_insights'],
            'enhancement_badge': '🤖 AI-Enhanced'
        }
    else:
        # Original sections only
        template_vars = {
            **research_data,
            'ai_insights': '*(Analysis in progress...)*',
            'enhancement_badge': '📊 Standard Analysis'
        }
    
    return template.format(**template_vars)
```

## Existing Database Schema (Unchanged)

### Prospect Model (No Changes)
```python
# src/database/models.py - NO MODIFICATIONS NEEDED
class Prospect(Base):
    __tablename__ = "prospects"
    
    # All existing fields remain exactly the same
    id: str = Field(primary_key=True)
    company_name: str = Field(max_length=200)
    status: ProspectStatus = Field(default=ProspectStatus.CREATED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # NO new LLM tracking fields added
    # Enhancement status tracked in-memory only during processing
```

### File Output (Existing Pattern)
```markdown
<!-- Enhanced research template -->
# Prospect Research: {company_name} {enhancement_badge}

## Company Overview
{basic_company_info}

## AI Business Intelligence Analysis
{ai_insights}

## Technology Stack
{tech_stack_info}

## Contact Information  
{linkedin_info}

---
*Research generated on {timestamp}*
*Enhancement status: {enhancement_status}*
```

## Error Handling Strategy

### Simple Fallback Logic
```python
class LLMEnhancer:
    """Simple enhancement with graceful degradation"""
    
    async def enhance_or_fallback(self, content: dict, prompt_type: str) -> dict:
        """Always returns content, enhanced or original"""
        
        # Feature flag check
        if not self.is_enabled():
            return self._add_status(content, 'disabled')
        
        # AWS credentials check  
        if not self._has_aws_credentials():
            logger.warning("AWS credentials not found, using original content")
            return self._add_status(content, 'no_credentials')
        
        # Enhancement attempt
        try:
            enhanced = await self._call_bedrock(content, prompt_type)
            return self._add_status(enhanced, 'enhanced')
        
        except TimeoutError:
            logger.warning("LLM request timeout, using original content")
            return self._add_status(content, 'timeout')
        
        except Exception as e:
            logger.warning(f"LLM enhancement failed: {e}")
            return self._add_status(content, 'error')
    
    def _add_status(self, content: dict, status: str) -> dict:
        """Add status without modifying database"""
        result = content.copy()
        result['enhancement_status'] = status
        return result
```

## Configuration Validation

### Environment Setup Check
```python
# src/llm_enhancer/config.py
"""Simple configuration validation"""

import os
from typing import Optional

class LLMConfig:
    """Simple config from environment variables only"""
    
    @property
    def enabled(self) -> bool:
        return os.getenv('LLM_ENHANCEMENT_ENABLED', 'false').lower() == 'true'
    
    @property
    def model_id(self) -> str:
        return os.getenv(
            'BEDROCK_MODEL_ID', 
            'apac.anthropic.claude-sonnet-4-20250514-v1:0'
        )
    
    @property  
    def temperature(self) -> float:
        return float(os.getenv('BEDROCK_TEMPERATURE', '0.3'))
    
    @property
    def max_tokens(self) -> int:
        return int(os.getenv('BEDROCK_MAX_TOKENS', '2000'))
    
    @property
    def timeout_seconds(self) -> int:
        return int(os.getenv('BEDROCK_TIMEOUT_SECONDS', '30'))
    
    def validate(self) -> list[str]:
        """Return list of validation errors, empty if valid"""
        errors = []
        
        if self.enabled:
            if not os.getenv('AWS_ACCESS_KEY_ID'):
                errors.append("AWS_ACCESS_KEY_ID required when LLM enabled")
            if not os.getenv('AWS_SECRET_ACCESS_KEY'):
                errors.append("AWS_SECRET_ACCESS_KEY required when LLM enabled")
            if not os.getenv('AWS_DEFAULT_REGION'):
                errors.append("AWS_DEFAULT_REGION required when LLM enabled")
        
        if not 0.0 <= self.temperature <= 1.0:
            errors.append("BEDROCK_TEMPERATURE must be between 0.0 and 1.0")
        
        if not 100 <= self.max_tokens <= 8000:
            errors.append("BEDROCK_MAX_TOKENS must be between 100 and 8000")
        
        return errors
```

## Constitutional Compliance

**Simplicity**: ✅ No database complexity, environment variables only  
**Library-First**: ✅ `llm_enhancer` module with clear interface  
**Test-First**: ✅ Contract tests for enhancement behavior  
**No Database Changes**: ✅ Existing schema completely unchanged  
**Graceful Degradation**: ✅ Always returns content, enhanced or original  
**Version Control**: ✅ Prompts in Python files, tracked with git

## Implementation Benefits

1. **Zero Migration Risk**: No database schema changes
2. **Simple Configuration**: Environment variables only
3. **Easy Rollback**: Disable with single environment variable
4. **Version Control**: Prompts managed like code
5. **Testable**: In-memory enhancement logic easy to test
6. **Performance**: No database queries for LLM configuration
7. **Cost Control**: Simple to disable/enable without data migration
