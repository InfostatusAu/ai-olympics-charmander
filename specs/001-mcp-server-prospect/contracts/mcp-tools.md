# MCP Tool Contracts

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine  
**Phase**: 1 - API Contracts and Schemas

## MCP Server Capabilities

The server implements all four MCP capabilities:
- **tools**: Exposes prospect research operations
- **resources**: Provides access to prospect database  
- **logging**: Structured operation logging
- **prompts**: Research workflow templates

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

### 2. research_prospect

Compiles comprehensive intelligence for a specific prospect.

**Tool Schema**:
```json
{
  "name": "research_prospect",
  "title": "Research Prospect", 
  "description": "Compile comprehensive intelligence including company background, decision makers, and pain points",
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
            "funding_history"
          ]
        },
        "uniqueItems": true,
        "maxItems": 7
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
  "company_profile": {
    "name": "TechCorp Inc",
    "domain": "techcorp.com", 
    "industry": "Software Development",
    "employee_count": 150,
    "founded_year": 2018,
    "headquarters": "San Francisco, CA",
    "description": "Leading provider of AI-powered analytics tools"
  },
  "decision_makers": [
    {
      "name": "Jane Smith",
      "title": "Chief Technology Officer", 
      "email": "jane.smith@techcorp.com",
      "linkedin_url": "https://linkedin.com/in/janesmith",
      "decision_level": "primary"
    }
  ],
  "research_findings": {
    "pain_points": [
      "Struggling with data integration complexity",
      "Manual reporting processes taking too long"
    ],
    "recent_news": [
      {
        "title": "TechCorp Raises $10M Series A",
        "url": "https://techcrunch.com/techcorp-funding",
        "date": "2025-08-15",
        "summary": "Funding to expand AI capabilities"
      }
    ],
    "technology_stack": ["AWS", "Python", "React", "PostgreSQL"],
    "competitive_landscape": ["DataCorp", "AnalyticsPro"]
  },
  "research_metadata": {
    "research_depth": "standard",
    "sources_used": ["firecrawl", "apollo", "linkedin"],
    "confidence_score": 0.85,
    "last_updated": "2025-09-13T10:30:00Z",
    "research_time_ms": 3500
  }
}
```

**Error Responses**:
- `ProspectNotFound`: No prospect found with given identifier
- `InsufficientData`: Not enough public information available
- `ResearchTimeout`: Research took longer than allowed time limit

### 3. save_prospect

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

### 4. retrieve_prospect

Queries stored prospect data with search and filtering capabilities.

**Tool Schema**:
```json
{
  "name": "retrieve_prospect", 
  "title": "Retrieve Prospect",
  "description": "Query stored prospect data with search and filtering capabilities",
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
            "description": "Full-text search across company name, description, research notes"
          }
        },
        "additionalProperties": false
      },
      "include": {
        "type": "array",
        "description": "Related data to include in response",
        "items": {
          "type": "string", 
          "enum": ["contact_persons", "research_notes", "icp_matches", "all"]
        },
        "default": ["contact_persons"]
      },
      "sort": {
        "type": "object",
        "description": "Sort order for results",
        "properties": {
          "field": {
            "type": "string",
            "enum": ["company_name", "updated_at", "qualification_status", "employee_count"],
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
      "pain_points": ["data integration", "manual processes"],
      "created_at": "2025-09-10T14:20:00Z",
      "updated_at": "2025-09-13T10:30:00Z",
      "contact_persons": [
        {
          "full_name": "Jane Smith",
          "job_title": "CTO",
          "email": "jane@techcorp.com",
          "decision_maker_level": "primary"
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
    "filters_applied": ["qualification_status", "industries"],
    "total_prospects_in_db": 1250
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
- `prospect://prospects/{prospect_id}` - Individual prospect resource
- `prospect://prospects/` - List of all prospects (paginated)
- `prospect://icps/{icp_name}` - ICP definition resource
- `prospect://search?q={query}` - Search results resource

**Resource Schema**:
```json
{
  "uri": "prospect://prospects/123e4567-e89b-12d3-a456-426614174000",
  "name": "TechCorp Inc Prospect Profile",
  "description": "Complete prospect research profile for TechCorp Inc",
  "mimeType": "application/json",
  "text": "{ /* prospect data */ }"
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

This contract specification ensures consistent MCP protocol compliance and enables AI assistants to discover and use prospect research tools effectively.
