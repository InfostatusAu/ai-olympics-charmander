# MCP Tool Contracts

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine  
**Phase**: 1 - API Contracts and Schemas  
**Update**: Extended for 3-Step Prospect Research Workflow

## MCP Server Capabilities

The server implements all four MCP capabilities:
- **tools**: Exposes 3-step prospect research workflow operations
- **resources**: Provides access to prospect database, profiles, and talking points
- **logging**: Structured operation logging
- **prompts**: Research workflow templates

## 3-Step Workflow Tool Overview

The MCP server provides 7 tools supporting the complete prospect research workflow:

### Step 1: Research Tools
- `research_prospect` - Gather comprehensive unstructured research data
- `store_research` - Persist research findings to database

### Step 2: Profile Generation Tools  
- `generate_profile` - Transform research into structured Mini Profile
- `get_prospect_research` - Retrieve research data for analysis

### Step 3: Talking Points Tools
- `create_talking_points` - Generate personalized conversation starters
- `get_prospect_profile` - Retrieve structured profile data

### Utility Tools
- `find_new_prospect` - Discover qualified leads (unchanged)
- `retrieve_prospect` - Query stored data with full workflow support

## Tool Contracts

### 1. find_new_prospect

Discovers qualified leads matching predefined ideal customer profiles.

**Tool Schema**:
```json
{
  "name": "find_new_prospect",
  "title": "Find New Prospect",
  "description": "Discover qualified leads matching ideal customer profile criteria",
  "inputSchema": {
    "type": "object",
    "properties": {
      "icp_name": {
        "type": "string",
        "description": "Name of the Ideal Customer Profile to match against",
        "minLength": 1,
        "maxLength": 255
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of prospects to return",
        "minimum": 1,
        "maximum": 100,
        "default": 10
      },
      "exclude_domains": {
        "type": "array",
        "description": "Company domains to exclude from results",
        "items": {
          "type": "string",
          "format": "hostname"
        },
        "maxItems": 50
      },
      "additional_criteria": {
        "type": "object",
        "description": "Additional filtering criteria beyond ICP",
        "properties": {
          "min_employees": {"type": "integer", "minimum": 1},
          "max_employees": {"type": "integer", "minimum": 1},
          "industries": {
            "type": "array",
            "items": {"type": "string"}
          },
          "locations": {
            "type": "array", 
            "items": {"type": "string"}
          }
        },
        "additionalProperties": false
      }
    },
    "required": ["icp_name"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospects": [
    {
      "company_name": "TechCorp Inc",
      "domain": "techcorp.com",
      "industry": "Software",
      "employee_count": 150,
      "location": "San Francisco, CA",
      "match_score": 85.5,
      "matching_criteria": ["employee_count", "industry", "location"],
      "website_url": "https://techcorp.com"
    }
  ],
  "total_found": 25,
  "icp_matched": "tech-startups-v1",
  "search_metadata": {
    "sources_used": ["apollo", "clearbit"],
    "search_time_ms": 1250,
    "rate_limits_hit": false
  }
}
```

**Error Responses**:
- `InvalidICP`: ICP name not found or inactive
- `RateLimitExceeded`: External data source rate limits hit
- `DataSourceUnavailable`: No data sources available

### 2. research_prospect (Step 1: Research)

Compiles comprehensive unstructured intelligence for a specific prospect using tiered data acquisition.

**Tool Schema**:
```json
{
  "name": "research_prospect",
  "title": "Research Prospect", 
  "description": "Step 1: Compile comprehensive unstructured intelligence including company background, decision makers, and pain points",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_identifier": {
        "type": "object",
        "description": "Identifier for the prospect to research",
        "properties": {
          "domain": {
            "type": "string",
            "format": "hostname",
            "description": "Company domain name"
          },
          "company_name": {
            "type": "string",
            "description": "Company name if domain unknown"
          },
          "prospect_id": {
            "type": "string",
            "format": "uuid", 
            "description": "UUID of existing prospect record"
          }
        },
        "oneOf": [
          {"required": ["domain"]},
          {"required": ["company_name"]}, 
          {"required": ["prospect_id"]}
        ]
      },
      "research_depth": {
        "type": "string",
        "enum": ["basic", "standard", "comprehensive"],
        "default": "standard",
        "description": "Level of research detail to gather"
      },
      "focus_areas": {
        "type": "array",
        "description": "Specific research areas to prioritize",
        "items": {
          "type": "string",
          "enum": [
            "company_background",
            "decision_makers", 
            "recent_news",
            "pain_points",
            "competitive_analysis",
            "technology_stack",
            "funding_history",
            "hiring_signals",
            "public_pr_activity",
            "tender_compliance"
          ]
        },
        "uniqueItems": true,
        "maxItems": 10
      },
      "update_existing": {
        "type": "boolean",
        "default": true,
        "description": "Whether to update existing prospect data"
      }
    },
    "required": ["prospect_identifier"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
  "workflow_status": "research_complete",
  "company_profile": {
    "name": "TechCorp Inc",
    "domain": "techcorp.com", 
    "industry": "Software Development",
    "employee_count": 150,
    "founded_year": 2018,
    "headquarters": "San Francisco, CA",
    "description": "Leading provider of AI-powered analytics tools"
  },
  "research_notes_created": [
    {
      "note_id": "uuid1",
      "note_type": "company_background",
      "title": "Company Overview and History",
      "content_preview": "TechCorp was founded in 2018..."
    },
    {
      "note_id": "uuid2", 
      "note_type": "recent_news",
      "title": "Series A Funding Announcement",
      "content_preview": "TechCorp announced $10M Series A..."
    }
  ],
  "decision_makers_found": [
    {
      "name": "Jane Smith",
      "title": "Chief Technology Officer", 
      "email": "jane.smith@techcorp.com",
      "linkedin_url": "https://linkedin.com/in/janesmith",
      "decision_level": "primary"
    }
  ],
  "research_metadata": {
    "research_depth": "standard",
    "sources_used": ["firecrawl", "apollo", "linkedin"],
    "total_notes_created": 6,
    "confidence_score": 0.85,
    "research_time_ms": 3500,
    "next_step": "generate_profile"
  }
}
```

**Error Responses**:
- `ProspectNotFound`: No prospect found with given identifier
- `InsufficientData`: Not enough public information available
- `ResearchTimeout`: Research took longer than allowed time limit

### 3. get_prospect_research (Step 2 Helper)

Retrieves all unstructured research data for profile generation.

**Tool Schema**:
```json
{
  "name": "get_prospect_research",
  "title": "Get Prospect Research",
  "description": "Retrieve all unstructured research data for a prospect to enable profile generation",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of the prospect to get research for"
      },
      "note_types": {
        "type": "array",
        "description": "Filter by specific research note types",
        "items": {
          "type": "string",
          "enum": [
            "company_background", "recent_news", "pain_points",
            "competitive_analysis", "decision_makers", "technology_stack"
          ]
        }
      },
      "include_metadata": {
        "type": "boolean",
        "default": true,
        "description": "Include source metadata and confidence scores"
      }
    },
    "required": ["prospect_id"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
  "company_name": "TechCorp Inc",
  "workflow_status": "research_complete",
  "research_notes": [
    {
      "note_id": "uuid1",
      "note_type": "company_background", 
      "title": "Company Overview and History",
      "content": "TechCorp was founded in 2018 by former Google engineers...",
      "source_url": "https://techcorp.com/about",
      "source_type": "firecrawl",
      "confidence_score": 0.9,
      "created_at": "2025-09-13T09:15:00Z"
    },
    {
      "note_id": "uuid2",
      "note_type": "recent_news",
      "title": "Series A Funding Announcement", 
      "content": "TechCorp announced $10M Series A funding led by...",
      "source_url": "https://techcrunch.com/techcorp-funding",
      "source_type": "api",
      "confidence_score": 0.95,
      "created_at": "2025-09-13T09:20:00Z"
    }
  ],
  "contact_persons": [
    {
      "full_name": "Jane Smith",
      "job_title": "Chief Technology Officer",
      "email": "jane.smith@techcorp.com",
      "decision_maker_level": "primary"
    }
  ],
  "aggregated_metadata": {
    "total_notes": 6,
    "avg_confidence_score": 0.87,
    "sources_used": ["firecrawl", "api", "linkedin"],
    "research_completeness": 0.85
  }
}
```

### 4. generate_profile (Step 2: Analysis)

Transforms unstructured research into structured Mini Profile template.

**Tool Schema**:
```json
{
  "name": "generate_profile",
  "title": "Generate Profile",
  "description": "Step 2: Transform unstructured research data into structured Mini Profile template",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of prospect to generate profile for"
      },
      "analysis_focus": {
        "type": "array",
        "description": "Profile fields to prioritize during analysis",
        "items": {
          "type": "string",
          "enum": [
            "revenue_range", "hiring_signals", "tech_adoption",
            "public_pr_signals", "funding_growth", "tender_compliance",
            "decision_makers", "engagement_potential", "infostatus_pain_points"
          ]
        }
      },
      "confidence_threshold": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0,
        "default": 0.7,
        "description": "Minimum confidence required for profile field population"
      },
      "infostatus_context": {
        "type": "object",
        "description": "Infostatus company context for pain point analysis",
        "properties": {
          "services": {
            "type": "array",
            "items": {"type": "string"},
            "default": ["document_automation", "data_processing", "workflow_optimization"]
          },
          "target_pain_points": {
            "type": "array", 
            "items": {"type": "string"},
            "default": ["manual_processes", "document_handling", "compliance_automation"]
          }
        }
      }
    },
    "required": ["prospect_id"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
  "workflow_status": "profile_complete",
  "mini_profile": {
    "company_name": "TechCorp Inc",
    "employee_count": 150,
    "revenue_range": "$50M-$100M",
    "industry": "Software Development",
    "location": "San Francisco, CA",
    "hiring_signals": "Hiring Data Scientists and AI Engineers, 5 open positions in Q3 2025",
    "tech_adoption": "Migrating to AWS cloud infrastructure, implementing AI/ML pipelines",
    "public_pr_signals": "Featured in TechCrunch for AI innovation, CEO speaking at ML conferences",
    "funding_growth": "Series A $10M raised Aug 2025, 40% YoY growth reported",
    "tender_compliance": "No government contracts identified, GDPR compliant",
    "decision_makers": "Jane Smith (CTO), Mike Johnson (CEO) - both active on LinkedIn",
    "engagement_potential": "CTO posted about AI compliance challenges last week",
    "general_notes": "Fast-growing startup, strong technical team, expanding rapidly",
    "infostatus_pain_points": "Manual data processing workflows, document handling inefficiencies identified in job postings"
  },
  "profile_metadata": {
    "confidence_score": 0.83,
    "fields_populated": 13,
    "fields_missing": 0,
    "source_note_count": 6,
    "analysis_time_ms": 2100,
    "generated_by": "gpt-4-analysis-v1",
    "next_step": "create_talking_points"
  }
}
```

### 5. get_prospect_profile (Step 3 Helper)

Retrieves structured Mini Profile data for talking points generation.

**Tool Schema**:
```json
{
  "name": "get_prospect_profile", 
  "title": "Get Prospect Profile",
  "description": "Retrieve structured Mini Profile data for talking points generation",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of prospect to get profile for"
      },
      "include_source_data": {
        "type": "boolean",
        "default": false,
        "description": "Include references to source research notes"
      }
    },
    "required": ["prospect_id"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
  "workflow_status": "profile_complete",
  "mini_profile": {
    "company_name": "TechCorp Inc",
    "employee_count": 150,
    "revenue_range": "$50M-$100M",
    "industry": "Software Development",
    "location": "San Francisco, CA",
    "hiring_signals": "Hiring Data Scientists and AI Engineers",
    "tech_adoption": "Migrating to AWS cloud infrastructure",
    "public_pr_signals": "Featured in TechCrunch for AI innovation",
    "funding_growth": "Series A $10M raised Aug 2025",
    "tender_compliance": "No government contracts identified",
    "decision_makers": "Jane Smith (CTO), Mike Johnson (CEO)",
    "engagement_potential": "CTO posted about AI compliance challenges",
    "general_notes": "Fast-growing startup, strong technical team",
    "infostatus_pain_points": "Manual data processing workflows, document handling inefficiencies"
  },
  "profile_metadata": {
    "confidence_score": 0.83,
    "generated_at": "2025-09-13T11:15:00Z",
    "generated_by": "gpt-4-analysis-v1"
  }
}
```

### 6. create_talking_points (Step 3: Personalization)

Generates personalized conversation starters from Mini Profile data.

**Tool Schema**:
```json
{
  "name": "create_talking_points",
  "title": "Create Talking Points",
  "description": "Step 3: Generate personalized conversation starters and engagement opportunities from Mini Profile",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of prospect to create talking points for"
      },
      "talking_point_categories": {
        "type": "array",
        "description": "Categories of talking points to generate",
        "items": {
          "type": "string",
          "enum": [
            "personal_professional", "industry_trends", "technology_opportunities",
            "company_developments", "solution_alignment"
          ]
        },
        "default": ["industry_trends", "technology_opportunities", "solution_alignment"]
      },
      "conversation_context": {
        "type": "object",
        "description": "Context for conversation personalization",
        "properties": {
          "meeting_type": {
            "type": "string",
            "enum": ["cold_outreach", "warm_introduction", "follow_up", "conference_meeting"],
            "default": "cold_outreach"
          },
          "salesperson_background": {
            "type": "string",
            "description": "Salesperson's relevant background for personalization"
          },
          "infostatus_solutions": {
            "type": "array",
            "items": {"type": "string"},
            "default": ["document_automation", "data_processing", "compliance_tools"]
          }
        }
      },
      "max_talking_points": {
        "type": "integer",
        "minimum": 1,
        "maximum": 20,
        "default": 8,
        "description": "Maximum number of talking points to generate"
      }
    },
    "required": ["prospect_id"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
  "workflow_status": "workflow_complete",
  "talking_points": [
    {
      "talking_point_id": "uuid1",
      "category": "industry_trends",
      "title": "AI Compliance in Fintech",
      "content": "I noticed TechCorp was featured in TechCrunch for AI innovation. The fintech space is really embracing AI compliance frameworks - we've helped similar companies navigate the regulatory landscape while maintaining innovation speed.",
      "relevance_score": 0.92,
      "conversation_opener": true
    },
    {
      "talking_point_id": "uuid2", 
      "category": "technology_opportunities",
      "title": "AWS Migration Data Processing",
      "content": "Saw you're migrating to AWS infrastructure. During cloud migrations, we often see companies struggle with document processing workflows. Our AWS-native solutions have helped similar companies reduce processing time by 70%.",
      "relevance_score": 0.88,
      "conversation_opener": false
    },
    {
      "talking_point_id": "uuid3",
      "category": "company_developments",
      "title": "Series A Growth Challenges",
      "content": "Congratulations on the Series A funding! With 40% YoY growth, scaling operational processes becomes critical. We've worked with several Series A companies to automate their document workflows before they become bottlenecks.",
      "relevance_score": 0.85,
      "conversation_opener": true
    },
    {
      "talking_point_id": "uuid4",
      "category": "solution_alignment", 
      "title": "Data Scientist Hiring Pain Point",
      "content": "I see you're hiring data scientists and AI engineers. One challenge growing teams face is spending too much time on manual data preparation instead of actual modeling. Our document automation could free up your team for higher-value work.",
      "relevance_score": 0.90,
      "conversation_opener": false
    }
  ],
  "generation_metadata": {
    "total_generated": 6,
    "avg_relevance_score": 0.88,
    "conversation_openers": 2,
    "categories_covered": ["industry_trends", "technology_opportunities", "company_developments", "solution_alignment"],
    "generation_time_ms": 1800,
    "generated_by": "gpt-4-personalization-v1"
  }
}
```

### 7. save_prospect (Updated for Workflow)

Persists prospect profiles to the server's database.

**Tool Schema**:
```json
{
  "name": "save_prospect",
  "title": "Save Prospect",
  "description": "Persist prospect profile and research data to database",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_data": {
        "type": "object",
        "description": "Complete prospect information to save",
        "properties": {
          "company_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
          },
          "domain": {
            "type": "string", 
            "format": "hostname"
          },
          "industry": {
            "type": "string",
            "maxLength": 100
          },
          "employee_count": {
            "type": "integer",
            "minimum": 1
          },
          "location": {
            "type": "string",
            "maxLength": 255
          },
          "website_url": {
            "type": "string",
            "format": "uri"
          },
          "description": {
            "type": "string"
          },
          "qualification_status": {
            "type": "string",
            "enum": ["qualified", "unqualified", "pending", "contacted"]
          },
          "research_data": {
            "type": "object",
            "description": "Flexible research findings storage"
          },
          "pain_points": {
            "type": "array",
            "items": {"type": "string"}
          }
        },
        "required": ["company_name", "domain"],
        "additionalProperties": false
      },
      "contact_persons": {
        "type": "array", 
        "description": "Decision makers and contacts",
        "items": {
          "type": "object",
          "properties": {
            "full_name": {
              "type": "string",
              "minLength": 1,
              "maxLength": 255
            },
            "job_title": {
              "type": "string",
              "maxLength": 255
            },
            "email": {
              "type": "string",
              "format": "email"
            },
            "phone": {
              "type": "string",
              "maxLength": 50
            },
            "linkedin_url": {
              "type": "string", 
              "format": "uri"
            },
            "decision_maker_level": {
              "type": "string",
              "enum": ["primary", "secondary", "influencer"]
            }
          },
          "required": ["full_name"],
          "additionalProperties": false
        }
      },
      "research_notes": {
        "type": "array",
        "description": "Detailed research findings",
        "items": {
          "type": "object",
          "properties": {
            "note_type": {
              "type": "string",
              "enum": [
                "company_background", "recent_news", "pain_points",
                "competitive_analysis", "decision_makers", "technology_stack"
              ]
            },
            "title": {
              "type": "string",
              "minLength": 1,
              "maxLength": 255  
            },
            "content": {
              "type": "string",
              "minLength": 10
            },
            "source_url": {
              "type": "string",
              "format": "uri"
            },
            "source_type": {
              "type": "string",
              "enum": ["api", "firecrawl", "playwright", "manual"]
            },
            "confidence_score": {
              "type": "number",
              "minimum": 0.0,
              "maximum": 1.0
            }
          },
          "required": ["note_type", "title", "content"],
          "additionalProperties": false
        }
      },
      "icp_matches": {
        "type": "array",
        "description": "ICP criteria this prospect matches",
        "items": {
          "type": "object", 
          "properties": {
            "icp_name": {"type": "string"},
            "match_score": {
              "type": "number",
              "minimum": 0.0,
              "maximum": 100.0
            },
            "matching_criteria": {
              "type": "array",
              "items": {"type": "string"}
            }
          },
          "required": ["icp_name", "match_score"]
        }
      },
      "overwrite_existing": {
        "type": "boolean",
        "default": false,
        "description": "Whether to overwrite existing prospect with same domain"
      }
    },
    "required": ["prospect_data"],
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
  "operation": "created",
  "summary": {
    "company_name": "TechCorp Inc",
    "domain": "techcorp.com",
    "contact_persons_saved": 2,
    "research_notes_saved": 5,
    "icp_matches_linked": 1
  },
  "validation_warnings": [
    "Email format questionable for contact: john@domain"
  ],
  "save_metadata": {
    "saved_at": "2025-09-13T10:30:00Z",
    "database_id": "uuid-here",
    "save_time_ms": 150
  }
}
```

**Error Responses**:
- `DuplicateProspect`: Prospect with domain already exists (when overwrite_existing=false)
- `ValidationError`: Required fields missing or invalid format
- `DatabaseError`: Database connection or constraint violation

### 8. retrieve_prospect (Updated for Full Workflow)

Queries stored prospect data with search and filtering capabilities, including full workflow status and results.

**Tool Schema**:
```json
{
  "name": "retrieve_prospect", 
  "title": "Retrieve Prospect",
  "description": "Query stored prospect data with full 3-step workflow support and filtering capabilities",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "object",
        "description": "Search and filter criteria",
        "properties": {
          "prospect_id": {
            "type": "string",
            "format": "uuid",
            "description": "Specific prospect UUID to retrieve"
          },
          "domain": {
            "type": "string",
            "format": "hostname", 
            "description": "Company domain to search for"
          },
          "company_name": {
            "type": "string",
            "description": "Company name (supports partial matching)"
          },
          "qualification_status": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["qualified", "unqualified", "pending", "contacted"]
            },
            "description": "Filter by qualification status"
          },
          "workflow_status": {
            "type": "array",
            "items": {
              "type": "string", 
              "enum": [
                "initial", "researching", "research_complete",
                "analyzing", "profile_complete", "generating_points", "workflow_complete"
              ]
            },
            "description": "Filter by workflow completion status"
          },
          "industries": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Filter by industry"
          },
          "employee_count_range": {
            "type": "object",
            "properties": {
              "min": {"type": "integer", "minimum": 1},
              "max": {"type": "integer", "minimum": 1}
            },
            "additionalProperties": false
          },
          "icp_matches": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Filter by ICP names"
          },
          "updated_since": {
            "type": "string",
            "format": "date-time",
            "description": "Only return prospects updated after this timestamp"
          },
          "search_text": {
            "type": "string",
            "description": "Full-text search across company name, description, research notes, profile data"
          }
        },
        "additionalProperties": false
      },
      "include": {
        "type": "array",
        "description": "Related data to include in response",
        "items": {
          "type": "string", 
          "enum": ["contact_persons", "research_notes", "prospect_profile", "talking_points", "icp_matches", "all"]
        },
        "default": ["contact_persons", "prospect_profile"]
      },
      "sort": {
        "type": "object",
        "description": "Sort order for results",
        "properties": {
          "field": {
            "type": "string",
            "enum": [
              "company_name", "updated_at", "qualification_status", 
              "workflow_status", "employee_count", "profile_completed_at"
            ],
            "default": "updated_at"
          },
          "direction": {
            "type": "string", 
            "enum": ["asc", "desc"],
            "default": "desc"
          }
        },
        "additionalProperties": false
      },
      "pagination": {
        "type": "object",
        "description": "Pagination parameters",
        "properties": {
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
            "default": 20
          },
          "offset": {
            "type": "integer",
            "minimum": 0,
            "default": 0
          }
        },
        "additionalProperties": false
      }
    },
    "additionalProperties": false
  }
}
```

**Response Format**:
```json
{
  "prospects": [
    {
      "prospect_id": "123e4567-e89b-12d3-a456-426614174000",
      "company_name": "TechCorp Inc",
      "domain": "techcorp.com",
      "industry": "Software", 
      "employee_count": 150,
      "location": "San Francisco, CA",
      "qualification_status": "qualified",
      "workflow_status": "workflow_complete",
      "pain_points": ["data integration", "manual processes"],
      "created_at": "2025-09-10T14:20:00Z",
      "updated_at": "2025-09-13T10:30:00Z",
      "profile_completed_at": "2025-09-13T11:15:00Z",
      "talking_points_completed_at": "2025-09-13T11:45:00Z",
      "contact_persons": [
        {
          "full_name": "Jane Smith",
          "job_title": "CTO",
          "email": "jane@techcorp.com",
          "decision_maker_level": "primary"
        }
      ],
      "prospect_profile": {
        "revenue_range": "$50M-$100M",
        "hiring_signals": "Hiring Data Scientists & AI Engineers",
        "tech_adoption": "Migrating to AWS cloud infrastructure",
        "infostatus_pain_points": "Manual data processing workflows",
        "confidence_score": 0.83
      },
      "talking_points": [
        {
          "category": "technology_opportunities",
          "title": "AWS Migration Data Processing",
          "content": "Saw you're migrating to AWS infrastructure...",
          "relevance_score": 0.88,
          "conversation_opener": false
        }
      ],
      "research_notes": [
        {
          "note_type": "recent_news",
          "title": "Series A Funding Announcement", 
          "content": "TechCorp announced $10M Series A...",
          "source_type": "firecrawl",
          "confidence_score": 0.9,
          "created_at": "2025-09-13T09:15:00Z"
        }
      ],
      "icp_matches": [
        {
          "icp_name": "tech-startups-v1",
          "match_score": 85.5,
          "matching_criteria": ["employee_count", "industry"]
        }
      ]
    }
  ],
  "pagination": {
    "total_count": 45,
    "limit": 20,
    "offset": 0,
    "has_more": true
  },
  "query_metadata": {
    "query_time_ms": 75,
    "filters_applied": ["workflow_status", "industries"],
    "total_prospects_in_db": 1250,
    "workflow_completion_stats": {
      "workflow_complete": 12,
      "profile_complete": 8,
      "research_complete": 15,
      "initial": 10
    }
  }
}
```

**Error Responses**:
- `InvalidQuery`: Query parameters are malformed
- `DatabaseError`: Database connection issues
- `NoResults`: No prospects found matching criteria

## MCP Resource Contracts

### Prospect Resources

Resources are URI-addressable prospect data accessible to AI assistants for context.

**Resource URI Pattern**:
- `prospect://prospects/{prospect_id}` - Individual prospect with full workflow data
- `prospect://prospects/` - List of all prospects (paginated)
- `prospect://profiles/{prospect_id}` - Mini Profile data only
- `prospect://talking-points/{prospect_id}` - Talking points for prospect
- `prospect://research/{prospect_id}` - Research notes for prospect
- `prospect://icps/{icp_name}` - ICP definition resource
- `prospect://search?q={query}` - Search results resource
- `prospect://workflow-status?status={status}` - Filter by workflow status

**Resource Schema**:
```json
{
  "uri": "prospect://prospects/123e4567-e89b-12d3-a456-426614174000",
  "name": "TechCorp Inc Complete Prospect Intelligence",
  "description": "Complete 3-step workflow prospect intelligence for TechCorp Inc including research, profile, and talking points",
  "mimeType": "application/json",
  "text": "{ /* complete prospect data with workflow results */ }"
}
```

```json
{
  "uri": "prospect://profiles/123e4567-e89b-12d3-a456-426614174000", 
  "name": "TechCorp Inc Mini Profile",
  "description": "Structured Mini Profile template data for TechCorp Inc",
  "mimeType": "application/json",
  "text": "{ /* mini profile data */ }"
}
```

```json
{
  "uri": "prospect://talking-points/123e4567-e89b-12d3-a456-426614174000",
  "name": "TechCorp Inc Talking Points",
  "description": "Personalized conversation starters for TechCorp Inc engagement",
  "mimeType": "application/json", 
  "text": "{ /* talking points array */ }"
}
```

## Error Handling Standards

All tools follow JSON-RPC 2.0 error format:

```json
{
  "error": {
    "code": -32000,
    "message": "Tool execution failed",
    "data": {
      "tool_name": "find_new_prospect",
      "error_type": "RateLimitExceeded", 
      "details": "Apollo API rate limit exceeded. Retry in 3600 seconds.",
      "retry_after": 3600,
      "error_id": "uuid-for-debugging"
    }
  }
}
```

**Error Code Ranges**:
- `-32000` to `-32099`: Tool execution errors
- `-32100` to `-32199`: Validation errors  
- `-32200` to `-32299`: Database errors
- `-32300` to `-32399`: External service errors

This contract specification ensures consistent MCP protocol compliance and enables AI assistants to discover and use the complete 3-step prospect research workflow effectively. The tools support the full pipeline from unstructured research to actionable sales intelligence.
