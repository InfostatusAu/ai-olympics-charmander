# Quickstart: LLM-Enhanced Prospect Research

**Date**: September 14, 2025  
**Feature**: Improve Research with LLM

## Prerequisites

### Environment Setup
```bash
# AWS Credentials for Bedrock
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"  
export AWS_DEFAULT_REGION="us-west-2"

# LLM Configuration
export BEDROCK_MODEL_ID="anthropic.claude-3-5-sonnet-20241022-v2:0"
export LLM_ENHANCEMENT_ENABLED="true"
```

### Dependencies
```bash
uv add boto3 botocore
uv run python -c "import boto3; print('AWS SDK ready')"
```

## Test Scenarios

### Scenario 1: Enhanced Research Generation
```bash
uv run python -m src.mcp_server.cli research-prospect "TechCorp Inc"

# Expected indicators:
# ✅ Research completed for TechCorp Inc
# 🤖 LLM Enhanced: true
# 📄 Report: prospect_[timestamp]_research.md
```

**Validation**: Generated markdown contains LLM-enhanced sections:
- Business Intelligence Analysis
- Competitive Positioning  
- Technology Readiness Assessment
- Pain Point Analysis

### Scenario 2: Enhanced Profile Creation
```bash
uv run python -m src.mcp_server.cli create-profile "[prospect_id]"

# Expected indicators:
# ✅ Profile created for TechCorp Inc
# 🤖 LLM Enhanced: true
# 🎯 Strategy: AI-generated conversation strategies included
```

**Validation**: Profile contains LLM-enhanced sections:
- AI-Generated Conversation Strategies
- Decision Maker Psychology Insights
- Personalized Approach Recommendations

### Scenario 3: Unchanged Data Retrieval Tools
```bash
# These should remain unchanged (no LLM processing)
uv run python -m src.mcp_server.cli get-prospect-data "[prospect_id]"
uv run python -m src.mcp_server.cli search-prospects "technology AI"
```

### Scenario 4: Fallback Mechanism
```bash
# Test with LLM disabled
export LLM_ENHANCEMENT_ENABLED="false"
uv run python -m src.mcp_server.cli research-prospect "FallbackTest Corp"

# Expected:
# ⚠️ LLM enhancement disabled - using static analysis
# ✅ Research completed with original analysis
```

### Scenario 5: Error Handling
```bash
# Test with invalid credentials
export AWS_ACCESS_KEY_ID="invalid"
uv run python -m src.mcp_server.cli research-prospect "ErrorTest Corp"

# Expected:
# ❌ LLM enhancement failed: AWS authentication error
# ✅ Falling back to static analysis
```

## Performance Validation

```bash
# Response time test
time uv run python -m src.mcp_server.cli research-prospect "PerformanceTest Corp"
# Expected: Total time < 10 seconds, LLM enhancement < 5 seconds
```

## Success Criteria

### Functional Requirements
- [x] FR-001: `research_prospect` generates LLM-enhanced business intelligence
- [x] FR-002: `create_profile` creates AI-generated conversation strategies  
- [x] FR-003: `search_prospects` preserves original functionality
- [x] FR-004: `get_prospect_data` preserves original functionality
- [x] FR-007: Response times under 10 seconds for enhanced tools
- [x] FR-008: Intelligent error handling with fallback to static analysis

### Performance Benchmarks
- Response time: research_prospect < 10s, create_profile < 8s
- Fallback reliability: 100% success rate when LLM unavailable
- Error handling: Graceful degradation in all failure scenarios

## Troubleshooting

### Common Issues
1. **AWS Authentication**: Verify credentials and region configuration
2. **Model Access**: Ensure Bedrock model access is enabled in AWS account
3. **Rate Limits**: Check AWS Bedrock quotas and request limits
4. **Network Issues**: Verify connectivity to AWS Bedrock endpoints

### Debug Commands
```bash
# Test AWS connectivity
uv run python -c "import boto3; client = boto3.client('bedrock-runtime'); print('Connected')"

# Check database status
uv run python -m src.database.cli status
```
