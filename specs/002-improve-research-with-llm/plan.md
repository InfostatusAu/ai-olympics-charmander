m````markdown
# Implementation Plan: LLM Intelligence Middleware

**Branch**: `002-improve-research-with-llm` | **Date**: September 14, 2025

## Summary
Implement LLM intelligence middleware to replace manual data preparation logic in prospect research tools. The LLM sits between raw data collection from sub-level tools and template generation, providing intelligent analysis instead of hardcoded rules and string manipulation.

**Intelligence Middleware Pattern**: 
```
Sub-level Tools → Raw Data Collection → LLM Analysis → Template-Ready Data → Markdown Generation
```

## Problem Statement: Manual Data Preparation Logic + Missing Research Components

### Current Issue: Hardcoded Rules and Incomplete Data Source Coverage
**Research Tool Current Flow (Inefficient + Incomplete)**:
```
Sub-level Tools → Raw Data → Manual String Processing → Template Filling
   ↓               ↓              ↓                        ↓
Firecrawl      website_html   background = content[:1000]  research_template.md
LinkedIn       search_results  tech_stack = keyword_match   
Job Boards     job_postings    pain_points = manual_rules
News Search    articles        decision_makers = regex_parse
```

### Missing Research Components (Per prospect_research_approach.md):
**Critical Gaps Identified**:
1. **Apollo.io Integration** - 🚫 NOT IMPLEMENTED
   - Contact enrichment, email/phone verification, intent data
   - Missing: `POST /people/search`, `/people/enrich`, `/organization/enrich`

2. **Serper API Integration** - 🚫 NOT IMPLEMENTED  
   - Alternative search provider for LinkedIn, general search
   - Rate limit mitigation and enhanced search capabilities

3. **Playwright MCP Browser Tools** - 🚫 NOT IMPLEMENTED
   - Authenticated LinkedIn browsing (login-required content)
   - Job board detailed searches with authentication
   - Social media scraping (X/Twitter, etc.)

4. **Glassdoor Specific Integration** - 🔧 PARTIALLY MISSING
   - Company culture insights, employee reviews
   - Salary data and hiring trends

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

### Solution: LLM Intelligence Middleware + Complete Data Source Coverage

**Enhanced Research Flow with All Data Sources**:
```
Complete Data Sources → Raw Data Collection → LLM Analysis → Template Generation
       ↓                       ↓                   ↓              ↓
1. Firecrawl              raw_website_data     Analyze content    research_template.md
2. Apollo.io API          raw_contact_data   → Extract insights   (AI-filled)
3. Serper API             raw_search_data    → Identify patterns
4. Playwright MCP         raw_browser_data   → Generate summaries
5. LinkedIn (auth)        raw_linkedin_data  → Business intelligence
6. Job Boards (auth)      raw_job_data       → Contact enrichment
7. Glassdoor              raw_review_data    → Decision maker insights
8. News Search            raw_news_data      → Hiring signal detection
9. Government Registries  raw_registry_data  → Company validation
```

**Error Handling & Fallback Strategy**:
```
Source 1 (Firecrawl) → Success ✅ → Continue to Source 2
                    → Failure ❌ → Log error, continue to Source 2
Source 2 (Apollo.io) → Success ✅ → Continue to Source 3  
                    → Failure ❌ → Log error, continue to Source 3
...continue through all sources...
Final Analysis → LLM processes ALL collected data → Enhanced output
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

#### 1. Complete Data Source Integration (`data_sources`)
```python
# New module: src/data_sources/ 
class DataSourceManager:
    """Orchestrates all research data sources with graceful error handling"""
    
    async def collect_all_prospect_data(self, company: str) -> dict:
        """Implements complete prospect_research_approach.md"""
        results = {
            'company_website': None,
            'apollo_data': None, 
            'linkedin_data': None,
            'serper_search': None,
            'playwright_data': None,
            'job_boards': None,
            'glassdoor_data': None,
            'news_data': None,
            'government_data': None,
            'errors': []
        }
        
        # Source 1: Company Website (Firecrawl)
        try:
            results['company_website'] = await self.firecrawl_source.scrape_website(company)
        except Exception as e:
            results['errors'].append(f"Firecrawl failed: {e}")
            logger.warning(f"Firecrawl source failed for {company}: {e}")
        
        # Source 2: Apollo.io Contact Enrichment
        try:
            results['apollo_data'] = await self.apollo_source.enrich_company(company)
        except Exception as e:
            results['errors'].append(f"Apollo.io failed: {e}")
            logger.warning(f"Apollo source failed for {company}: {e}")
            
        # Source 3: LinkedIn (Firecrawl + Playwright MCP fallback)
        try:
            results['linkedin_data'] = await self.linkedin_source.research_company(company)
        except Exception as e:
            results['errors'].append(f"LinkedIn failed: {e}")
            try:
                # Fallback to Playwright MCP for authenticated browsing
                results['linkedin_data'] = await self.playwright_source.browse_linkedin(company)
            except Exception as e2:
                results['errors'].append(f"LinkedIn Playwright fallback failed: {e2}")
        
        # Continue for all sources...
        # Source 4: Serper API (alternative search)
        # Source 5: Job Boards (Seek, Indeed, Glassdoor)
        # Source 6: General Search & News
        # Source 7: Government Registries
        
        return results
```

#### 2. LLM Enhancement Module (`llm_enhancer`)
```python
# Enhanced middleware with complete data processing
async def analyze_research_data(raw_data: dict, template_schema: dict) -> dict:
    """Replace manual data preparation with AI analysis of ALL data sources"""
    if not llm_enabled:
        return fallback_to_manual_processing(raw_data)
    
    try:
        # AI analyzes data from ALL sources, handles missing data gracefully
        enhanced = await bedrock_client.analyze_comprehensive_data(raw_data, template_schema)
        enhanced['enhancement_status'] = 'ai_enhanced'
        enhanced['data_sources_used'] = len([k for k, v in raw_data.items() if v and k != 'errors'])
        enhanced['total_errors'] = len(raw_data.get('errors', []))
        return enhanced
    except Exception as e:
        logger.warning(f"LLM analysis failed: {e}")
        fallback_data = fallback_to_manual_processing(raw_data)
        fallback_data['enhancement_status'] = 'manual_fallback'
        return fallback_data
```

#### 2. MCP Server Configuration (Complete API Integration)
```bash
# Default: Intelligence middleware enabled with ALL data sources
python -m src.mcp_server.cli \
    --llm-enabled true \
    --llm-provider bedrock \
    --model-id apac.anthropic.claude-sonnet-4-20250514-v1:0 \
    --firecrawl-enabled true \
    --apollo-enabled true \
    --serper-enabled true \
    --playwright-enabled true \
    --temperature 0.3 \
    --max-tokens 4000 \
    --timeout-seconds 60

# Environment variables for complete integration
FIRECRAWL_API_KEY=fc-xxx
APOLLO_API_KEY=xxx  
SERPER_API_KEY=xxx
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_DEFAULT_REGION=ap-southeast-2
```

#### 3. Complete Research Integration Strategy
- **research_prospect()**: Replace with `data_source_manager.collect_all_prospect_data()` + `llm_analyzer.analyze()`
- **create_profile()**: Replace rule logic with `profile_analyzer.generate_strategy()`  
- **Data source modules**: Apollo.io API, Serper API, Playwright MCP browser tools
- **Error resilience**: Each source failure logged but doesn't stop the process
- **Template filling**: Same templates, AI-enhanced content from ALL available sources

#### 4. Comprehensive Fallback Strategy
```python
async def research_prospect_with_complete_intelligence(company: str):
    # 1. Collect data from ALL sources (graceful error handling)
    raw_data = await data_source_manager.collect_all_prospect_data(company)
    
    # 2. Try LLM intelligence middleware on ALL collected data
    try:
        if llm_enabled:
            structured_data = await llm_middleware.analyze_comprehensive_research_data(raw_data)
            enhancement_status = "ai_enhanced"
        else:
            structured_data = fallback_to_manual_processing(raw_data)
            enhancement_status = "manual_processing"
    except Exception as e:
        logger.warning(f"LLM analysis failed: {e}")
        structured_data = fallback_to_manual_processing(raw_data)
        enhancement_status = "fallback_manual"
    
    # 3. Generate markdown using ALL available data (enhanced templates)
    structured_data['research_summary'] = {
        'sources_attempted': 9,  # All sources from approach
        'sources_successful': len([k for k, v in raw_data.items() if v and k != 'errors']),
        'sources_failed': len(raw_data.get('errors', [])),
        'enhancement_method': enhancement_status
    }
    
    return generate_enhanced_markdown_report(structured_data, enhancement_status)
```

### Environment Configuration
```bash
# Required for complete research approach implementation
# Core LLM Provider  
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx  
AWS_DEFAULT_REGION=ap-southeast-2

# Data Source APIs (from prospect_research_approach.md)
FIRECRAWL_API_KEY=fc-xxx          # Website scraping
APOLLO_API_KEY=xxx                # Contact enrichment, lead data
SERPER_API_KEY=xxx                # Alternative search provider
LINKEDIN_EMAIL=xxx                # For Playwright MCP authenticated browsing
LINKEDIN_PASSWORD=xxx             # For Playwright MCP authenticated browsing

# Optional: Platform-specific job board credentials
SEEK_EMAIL=xxx                    # For authenticated job searches  
INDEED_EMAIL=xxx                  # For authenticated job searches
GLASSDOOR_EMAIL=xxx               # For company review data
```

## Technical Context
**Language**: Python 3.11+  
**Dependencies**: boto3 (AWS Bedrock), apollo-client, serper-api, playwright-mcp-tools  
**Integration**: Complete prospect_research_approach.md implementation + LLM enhancement  
**Templates**: Enhanced structure with comprehensive data coverage
**Platform**: Linux server  
**Performance**: <120 seconds for complete intelligence analysis (all 9 data sources)  
**Default Model**: `apac.anthropic.claude-sonnet-4-20250514-v1:0`  
**Error Resilience**: Graceful degradation - any single source failure doesn't stop the process

## Constitution Check

**Simplicity**: ✅ Clean middleware pattern, replace manual logic with AI analysis  
**Architecture**: ✅ `llm_enhancer` intelligence middleware with clear interface  
**Testing**: ✅ RED-GREEN-Refactor cycle enforced  
**No Database Changes**: ✅ Existing schema unchanged, middleware operates in-memory  
**Graceful Degradation**: ✅ Fallback to manual processing if LLM unavailable  
**MCP Integration**: ✅ Server parameters control intelligence middleware

## Project Structure

### Enhanced Architecture (Complete Data Source + Intelligence Middleware Integration)
```
src/
├── database/          # ✅ Existing - SQLite operations (unchanged)
├── file_manager/      # ✅ Existing - Markdown templates (unchanged) 
├── prospect_research/ # 🔄 ENHANCED - Complete data source integration + LLM middleware
│   ├── research.py    # Replace with comprehensive data collection + AI analysis
│   └── profile.py     # Replace hardcoded rules with AI strategy generation
├── mcp_server/        # 🔄 ENHANCED - Add complete API configuration parameters
├── data_sources/      # 🆕 NEW - Complete prospect research approach implementation
│   ├── __init__.py
│   ├── firecrawl_source.py     # Website scraping (existing, enhanced)
│   ├── apollo_source.py        # 🆕 Contact enrichment & lead data
│   ├── serper_source.py        # 🆕 Alternative search provider  
│   ├── playwright_source.py    # 🆕 Authenticated browser automation
│   ├── linkedin_source.py      # 🔄 Enhanced LinkedIn research
│   ├── job_boards_source.py    # 🔄 Enhanced job board searches (Seek, Indeed, Glassdoor)
│   ├── news_source.py          # 🔄 Enhanced news & general search
│   ├── government_source.py    # 🔄 Enhanced government registry searches
│   └── manager.py              # Data source orchestration with error handling
└── llm_enhancer/      # 🆕 NEW - Intelligence middleware module
    ├── __init__.py
    ├── client.py      # AWS Bedrock client wrapper
    ├── middleware.py  # Core intelligence coordination
    ├── analyzers.py   # Research and profile AI analyzers
    └── cli.py         # Testing and debugging utilities  
```

### Complete Research Integration Strategy
1. **research_prospect()** → Replace with `data_source_manager.collect_all_prospect_data()` + `llm_analyzer.analyze()`
2. **create_profile()** → Replace rule logic with `profile_analyzer.generate_strategy()`  
3. **Data source integrations** → Apollo.io API, Serper API, Playwright MCP browser tools
4. **Error resilience** → Each source failure logged but doesn't stop the process
5. **Template enhancement** → Same structure, comprehensive content from ALL available sources

### Implementation Priority by Data Source Impact:
**Phase 1: High-Impact Missing Sources**
1. Apollo.io API integration (contact enrichment, decision makers)
2. Playwright MCP browser tools (authenticated LinkedIn, job boards)

**Phase 2: Enhanced Search Capabilities**  
3. Serper API integration (alternative search, rate limit mitigation)
4. Glassdoor specific targeting (company culture, employee insights)

**Phase 3: LLM Intelligence Layer**
5. AI analysis of ALL collected data sources
6. Intelligent synthesis and pattern recognition

## Phase Summary

**Phase 0**: ✅ Research complete - Manual logic patterns identified  
**Phase 1**: ✅ Design complete - Intelligence middleware architecture defined
**Phase 2**: Task planning approach for middleware implementation

### Task Planning Approach
1. **Complete Data Source Implementation**: Create all missing data source modules (Apollo.io, Serper, Playwright MCP)
2. **Data Source Manager**: Orchestrate all 9 data sources with graceful error handling
3. **Research Logic Replacement**: Replace manual data prep with comprehensive data collection + AI analysis  
4. **Profile Logic Replacement**: Replace hardcoded rules with AI strategy based on ALL available data
5. **Server Enhancement**: Add complete API configuration parameters to MCP server CLI
6. **Error Resilience Implementation**: Ensure no single source failure stops the entire process
7. **Testing Strategy**: Contract tests for complete data source coverage + AI vs manual processing
8. **Integration Validation**: End-to-end workflow testing with all data sources

**Estimated Tasks**: ~25-30 focused tasks covering complete data source implementation, middleware, replacement, integration

### Key Implementation Points
- **Complete Data Collection**: Implement ALL 9 data sources from prospect_research_approach.md
- **Error Resilience**: Each source failure logged but process continues with available data
- **Intelligence Layer**: AI analysis of ALL collected data for maximum insight generation
- **Template Compatibility**: Enhanced templates structure to accommodate comprehensive data
- **Fallback Safety**: Maintain original manual processing for any component failure scenarios
- **Performance**: Complete analysis within acceptable response time limits (<120s)
- **Configuration**: MCP server parameters control ALL data source and AI features
- **Authentication Handling**: Secure credential management for authenticated data sources

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
# In research.py - Complete data source integration:
async def research_prospect(company: str):
    # Collect from ALL 9 data sources with graceful error handling
    raw_data = await data_source_manager.collect_all_prospect_data(company)
    
    try:
        # LLM analyzes ALL available data (even if some sources failed)
        enhanced_content = await llm_enhancer.analyze_comprehensive_data(raw_data, 'research')
        enhancement_status = 'ai_enhanced'
    except Exception as e:
        # Fallback: manual processing of whatever data was collected
        enhanced_content = generate_comprehensive_manual_analysis(raw_data)
        enhancement_status = 'manual_fallback'
        
    # Generate report showing data source success/failure rates
    enhanced_content['research_summary'] = {
        'sources_attempted': 9,
        'sources_successful': raw_data['successful_sources_count'],
        'enhancement_method': enhancement_status,
        'data_quality_score': calculate_data_completeness(raw_data)
    }
    
    return enhanced_content
```

**Data Source Priority**: Apollo.io (contact enrichment) → Playwright MCP (authenticated browsing) → Serper (search enhancement) → Glassdoor (company insights) → LLM Analysis (intelligent synthesis)