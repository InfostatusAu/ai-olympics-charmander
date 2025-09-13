# MCP Tool Contracts: Simplified Markdown-First Architecture

**Date**: September 13, 2025  
**Feature**: Prospect Research Automation Engine  
**Phase**: 1 - Simplified API Contracts  
**Update**: Refactored for markdown-first, minimal database approach

## MCP Server Capabilities

The server implements simplified MCP capabilities focused on AI-generated markdown outputs:
- **tools**: 5 streamlined prospect research tools
- **resources**: File-based prospect data access
- **logging**: Essential operation logging
- **prompts**: Research workflow templates

## Simplified Tool Overview

The MCP server provides 5 focused tools supporting markdown-first prospect research:

### Core Workflow Tools
- `research_prospect` - Step 1: Gather research, output markdown
- `generate_profile` - Step 2: Create structured profile markdown  
- `create_talking_points` - Step 3: Generate conversation starters markdown

### Data Access Tools
- `get_prospect_data` - Retrieve prospect with all markdown files
- `search_prospects` - Find prospects with metadata search

## Tool Contracts

### 1. research_prospect (Step 1: Research)

Compiles comprehensive research and generates markdown research report.

**Tool Schema**:
```json
{
  "name": "research_prospect",
  "title": "Research Prospect", 
  "description": "Step 1: Compile comprehensive research and generate markdown research report",
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
          }
        },
        "oneOf": [
          {"required": ["domain"]},
          {"required": ["company_name"]}
        ]
      },
      "research_depth": {
        "type": "string",
        "enum": ["basic", "standard", "comprehensive"],
        "default": "standard",
        "description": "Level of research detail to gather"
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
  "company_name": "TechCorp Inc",
  "domain": "techcorp.com",
  "research_status": "researched",
  "files_created": {
    "research_file": "/data/prospects/123e4567_research.md",
    "file_size_kb": 15.2
  },
  "research_summary": {
    "sections_found": ["company_overview", "recent_developments", "technology_stack", "decision_makers", "pain_points"],
    "sources_used": ["website", "recent_news", "job_postings"],
    "confidence_score": 0.85,
    "research_time_ms": 3500
  }
}
```

### 2. generate_profile (Step 2: Analysis)

Transforms research markdown into structured Mini Profile markdown.

**Tool Schema**:
```json
{
  "name": "generate_profile",
  "title": "Generate Profile",
  "description": "Step 2: Transform research markdown into structured Mini Profile template",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of prospect to generate profile for"
      },
      "focus_areas": {
        "type": "array",
        "description": "Profile fields to emphasize",
        "items": {
          "type": "string",
          "enum": [
            "revenue_estimation", "hiring_signals", "tech_adoption",
            "funding_status", "decision_makers", "pain_points"
          ]
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
  "files_processed": {
    "input_file": "/data/prospects/123e4567_research.md",
    "output_file": "/data/prospects/123e4567_profile.md",
    "file_size_kb": 8.5
  },
  "profile_summary": {
    "fields_populated": 13,
    "confidence_score": 0.83,
    "key_findings": ["Series A funding", "AWS migration", "AI hiring"],
    "infostatus_fit_score": 0.88,
    "generation_time_ms": 2100
  }
}
```

### 3. create_talking_points (Step 3: Personalization)

Generates personalized conversation starters from Mini Profile markdown.

**Tool Schema**:
```json
{
  "name": "create_talking_points",
  "title": "Create Talking Points",
  "description": "Step 3: Generate personalized conversation starters from Mini Profile",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of prospect to create talking points for"
      },
      "categories": {
        "type": "array",
        "description": "Categories of talking points to generate",
        "items": {
          "type": "string",
          "enum": [
            "business_challenges", "technology_opportunities", "recent_news",
            "personal_connections", "solution_alignment"
          ]
        },
        "default": ["business_challenges", "technology_opportunities", "solution_alignment"]
      },
      "max_points": {
        "type": "integer",
        "minimum": 3,
        "maximum": 15,
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
  "files_processed": {
    "input_file": "/data/prospects/123e4567_profile.md",
    "output_file": "/data/prospects/123e4567_talking_points.md",
    "file_size_kb": 12.3
  },
  "talking_points_summary": {
    "total_generated": 8,
    "categories_covered": ["business_challenges", "technology_opportunities", "solution_alignment"],
    "conversation_openers": 3,
    "avg_relevance_score": 0.88,
    "generation_time_ms": 1800
  }
}
```

### 4. get_prospect_data

Retrieves prospect metadata with all generated markdown files.

**Tool Schema**:
```json
{
  "name": "get_prospect_data",
  "title": "Get Prospect Data",
  "description": "Retrieve prospect metadata with all generated markdown files",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prospect_id": {
        "type": "string",
        "format": "uuid",
        "description": "UUID of prospect to retrieve"
      },
      "include_content": {
        "type": "boolean",
        "default": true,
        "description": "Include markdown file contents in response"
      },
      "file_types": {
        "type": "array",
        "description": "Specific file types to retrieve",
        "items": {
          "type": "string",
          "enum": ["research", "profile", "talking_points"]
        },
        "default": ["research", "profile", "talking_points"]
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
  "domain": "techcorp.com",
  "research_status": "researched",
  "created_at": "2025-09-13T09:15:00Z",
  "updated_at": "2025-09-13T11:45:00Z",
  "files": {
    "research": {
      "path": "/data/prospects/123e4567_research.md",
      "exists": true,
      "size_kb": 15.2,
      "created_at": "2025-09-13T10:30:00Z",
      "content": "# Company Research: TechCorp Inc\n\n## Company Overview...",
      "sections": ["company_overview", "recent_developments", "decision_makers"]
    },
    "profile": {
      "path": "/data/prospects/123e4567_profile.md",
      "exists": true,
      "size_kb": 8.5,
      "created_at": "2025-09-13T11:15:00Z",
      "content": "# Mini Profile: TechCorp Inc\n\n| Field | Value |\n...",
      "confidence_score": 0.83
    },
    "talking_points": {
      "path": "/data/prospects/123e4567_talking_points.md",
      "exists": true,
      "size_kb": 12.3,
      "created_at": "2025-09-13T11:45:00Z",
      "content": "# Conversation Starters: TechCorp Inc\n\n## 🎯 Business Challenges...",
      "total_points": 8
    }
  }
}
```

### 5. search_prospects

Searches prospects by metadata and optionally file content.

**Tool Schema**:
```json
{
  "name": "search_prospects",
  "title": "Search Prospects",
  "description": "Search prospects by metadata and optionally markdown file content",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "object",
        "description": "Search criteria",
        "properties": {
          "company_name": {
            "type": "string",
            "description": "Company name (partial matching)"
          },
          "domain": {
            "type": "string",
            "description": "Company domain"
          },
          "research_status": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["pending", "researched", "failed"]
            }
          },
          "content_search": {
            "type": "string",
            "description": "Search within markdown file content"
          },
          "created_after": {
            "type": "string",
            "format": "date-time"
          }
        }
      },
      "include_files": {
        "type": "boolean",
        "default": false,
        "description": "Include file paths and metadata in results"
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20
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
      "research_status": "researched",
      "created_at": "2025-09-13T09:15:00Z",
      "files": {
        "research_exists": true,
        "profile_exists": true,
        "talking_points_exists": true,
        "research_path": "/data/prospects/123e4567_research.md",
        "profile_path": "/data/prospects/123e4567_profile.md",
        "talking_points_path": "/data/prospects/123e4567_talking_points.md"
      }
    }
  ],
  "total_found": 1,
  "search_metadata": {
    "query_time_ms": 45,
    "content_search_performed": false,
    "total_prospects_in_db": 25
  }
}
```

## MCP Resource Contracts

### Prospect Resources

Resources are URI-addressable prospect data accessible to AI assistants for context.

**Resource URI Pattern**:
- `prospect://prospects/{prospect_id}` - Individual prospect with all files
- `prospect://prospects/` - List of all prospects (paginated)
- `prospect://files/{prospect_id}/research` - Research markdown file
- `prospect://files/{prospect_id}/profile` - Profile markdown file  
- `prospect://files/{prospect_id}/talking_points` - Talking points markdown file
- `prospect://search?q={query}` - Search results resource
- `prospect://icp` - ICP definition from /data/icp.md

**Resource Schema**:
```json
{
  "uri": "prospect://prospects/123e4567-e89b-12d3-a456-426614174000",
  "name": "TechCorp Inc Complete Prospect Data",
  "description": "Complete prospect data including database metadata and all generated markdown files",
  "mimeType": "application/json",
  "text": "{ /* complete prospect data with file contents */ }"
}
```

```json
{
  "uri": "prospect://files/123e4567-e89b-12d3-a456-426614174000/profile", 
  "name": "TechCorp Inc Mini Profile",
  "description": "Structured Mini Profile markdown file",
  "mimeType": "text/markdown",
  "text": "# Mini Profile: TechCorp Inc\n\n| Field | Value |\n..."
}
```

```json
{
  "uri": "prospect://icp",
  "name": "Infostatus Ideal Customer Profile",
  "description": "Current ICP criteria for prospect qualification",
  "mimeType": "text/markdown", 
  "text": "# Infostatus Ideal Candidate Profile (ICP)\n\n## Company Details..."
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
      "tool_name": "research_prospect",
      "error_type": "FileNotFound", 
      "details": "Research file does not exist for prospect ID: 123e4567",
      "file_path": "/data/prospects/123e4567_research.md",
      "error_id": "uuid-for-debugging"
    }
  }
}
```

**Error Code Ranges**:
- `-32000` to `-32099`: Tool execution errors
- `-32100` to `-32199`: Validation errors  
- `-32200` to `-32299`: Database errors
- `-32300` to `-32399`: File system errors

**Common Error Types**:
- `FileNotFound`: Markdown file doesn't exist
- `DatabaseError`: SQLite connection or query issues
- `ValidationError`: Invalid input parameters
- `ResearchTimeout`: External API timeout
- `InsufficientData`: Not enough research data found

This simplified contract specification focuses on markdown-first outputs while maintaining MCP protocol compliance, enabling AI assistants to work with rich, human-readable prospect intelligence.
