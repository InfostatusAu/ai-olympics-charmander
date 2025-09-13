# Data Model: Prospect Research Automation Engine

**Date**: September 13, 2025  
**Feature**: MCP Server Prospect Research  
**Phase**: 1 - Data Model and Entity Design

## Core Entities

### 1. Prospect
Primary entity representing a potential customer with comprehensive research data.

**Fields**:
- `id`: UUID (Primary Key)
- `company_name`: VARCHAR(255) (Required, Indexed)
- `domain`: VARCHAR(255) (Unique, Indexed)
- `industry`: VARCHAR(100) (Indexed)
- `employee_count`: INTEGER
- `location`: VARCHAR(255)
- `website_url`: TEXT
- `description`: TEXT
- `qualification_status`: ENUM('qualified', 'unqualified', 'pending', 'contacted')
- `research_data`: JSONB (Flexible research findings storage)
- `pain_points`: TEXT[]
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE
- `last_researched_at`: TIMESTAMP WITH TIME ZONE

**Relationships**:
- One-to-Many with ContactPerson
- One-to-Many with ResearchNote
- Many-to-Many with IdealCustomerProfile

**Validation Rules**:
- company_name: Required, 1-255 characters
- domain: Valid domain format, unique
- qualification_status: Must be one of enum values
- employee_count: Positive integer or null
- research_data: Valid JSON structure

**State Transitions**:
```
pending → qualified (via research_prospect tool)
pending → unqualified (via research_prospect tool)
qualified → contacted (via manual update)
any → pending (via re-research)
```

### 2. ContactPerson
Represents decision makers and key contacts at prospect companies.

**Fields**:
- `id`: UUID (Primary Key)
- `prospect_id`: UUID (Foreign Key to Prospect)
- `full_name`: VARCHAR(255) (Required)
- `job_title`: VARCHAR(255)
- `email`: VARCHAR(255) (Indexed)
- `phone`: VARCHAR(50)
- `linkedin_url`: TEXT
- `decision_maker_level`: ENUM('primary', 'secondary', 'influencer')
- `contact_data`: JSONB (Additional contact information)
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Relationships**:
- Many-to-One with Prospect

**Validation Rules**:
- full_name: Required, 1-255 characters
- email: Valid email format when provided
- decision_maker_level: Must be one of enum values

### 3. IdealCustomerProfile (ICP)
Defines criteria for qualifying prospects during find_new_prospect operations.

**Fields**:
- `id`: UUID (Primary Key)
- `name`: VARCHAR(255) (Required, Unique)
- `description`: TEXT
- `criteria`: JSONB (Required - ICP matching criteria)
- `min_employee_count`: INTEGER
- `max_employee_count`: INTEGER
- `target_industries`: TEXT[]
- `target_locations`: TEXT[]
- `annual_revenue_min`: DECIMAL
- `annual_revenue_max`: DECIMAL
- `technology_stack`: TEXT[]
- `company_stage`: ENUM('startup', 'growth', 'established', 'enterprise')
- `is_active`: BOOLEAN DEFAULT TRUE
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Relationships**:
- Many-to-Many with Prospect (via ProspectICP junction table)

**Validation Rules**:
- name: Required, unique, 1-255 characters
- criteria: Required, valid JSON structure
- min_employee_count: Positive integer or null
- max_employee_count: Greater than min_employee_count when both provided

### 4. ResearchNote
Stores detailed research findings and intelligence gathered for prospects.

**Fields**:
- `id`: UUID (Primary Key)
- `prospect_id`: UUID (Foreign Key to Prospect)
- `note_type`: ENUM('company_background', 'recent_news', 'pain_points', 'competitive_analysis', 'decision_makers', 'technology_stack')
- `title`: VARCHAR(255) (Required)
- `content`: TEXT (Required)
- `source_url`: TEXT
- `source_type`: ENUM('api', 'firecrawl', 'playwright', 'manual')
- `confidence_score`: DECIMAL(3,2) (0.00-1.00)
- `metadata`: JSONB (Source-specific data)
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Relationships**:
- Many-to-One with Prospect

**Validation Rules**:
- title: Required, 1-255 characters
- content: Required, minimum 10 characters
- confidence_score: Between 0.00 and 1.00
- note_type: Must be one of enum values

### 5. DataSource
Tracks external data sources and their performance for data acquisition.

**Fields**:
- `id`: UUID (Primary Key)
- `name`: VARCHAR(100) (Required, Unique)
- `source_type`: ENUM('api', 'firecrawl', 'playwright')
- `base_url`: TEXT
- `api_key_required`: BOOLEAN DEFAULT FALSE
- `rate_limit_per_hour`: INTEGER
- `success_rate`: DECIMAL(5,2) (Percentage)
- `avg_response_time_ms`: INTEGER
- `is_active`: BOOLEAN DEFAULT TRUE
- `last_used_at`: TIMESTAMP WITH TIME ZONE
- `configuration`: JSONB (Source-specific config)
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

**Validation Rules**:
- name: Required, unique, 1-100 characters
- source_type: Must be one of enum values
- success_rate: Between 0.00 and 100.00
- avg_response_time_ms: Positive integer

### 6. ProspectICP (Junction Table)
Links prospects to the ICP criteria they match.

**Fields**:
- `prospect_id`: UUID (Foreign Key to Prospect)
- `icp_id`: UUID (Foreign Key to IdealCustomerProfile)
- `match_score`: DECIMAL(5,2) (0.00-100.00)
- `matching_criteria`: JSONB (Which criteria matched)
- `created_at`: TIMESTAMP WITH TIME ZONE

**Composite Primary Key**: (prospect_id, icp_id)

## Database Schema Relationships

```
Prospect (1) ←→ (N) ContactPerson
Prospect (1) ←→ (N) ResearchNote
Prospect (N) ←→ (N) IdealCustomerProfile [via ProspectICP]
IdealCustomerProfile (1) ←→ (N) ProspectICP
DataSource (independent tracking table)
```

## Indexes for Performance

### Primary Indexes
- `idx_prospect_company_name` on Prospect(company_name)
- `idx_prospect_domain` on Prospect(domain)
- `idx_prospect_industry` on Prospect(industry)
- `idx_prospect_qualification_status` on Prospect(qualification_status)
- `idx_prospect_updated_at` on Prospect(updated_at)

### Research Indexes
- `idx_research_note_prospect_id` on ResearchNote(prospect_id)
- `idx_research_note_type` on ResearchNote(note_type)
- `idx_research_note_created_at` on ResearchNote(created_at)

### Contact Indexes
- `idx_contact_person_prospect_id` on ContactPerson(prospect_id)
- `idx_contact_person_email` on ContactPerson(email)

### ICP Indexes
- `idx_icp_name` on IdealCustomerProfile(name)
- `idx_icp_is_active` on IdealCustomerProfile(is_active)
- `idx_prospect_icp_match_score` on ProspectICP(match_score)

### Composite Indexes
- `idx_prospect_status_updated` on Prospect(qualification_status, updated_at)
- `idx_research_prospect_type` on ResearchNote(prospect_id, note_type)

## Data Migration Strategy

### Version 1.0.0 - Initial Schema
- Create all core tables with proper constraints
- Insert default ICP templates for common use cases
- Create initial data source configurations
- Set up database functions for search optimization

### Future Migrations
- Add full-text search indexes for content fields
- Implement data archival strategy for old research
- Add audit trail tables for compliance
- Create materialized views for analytics

## JSONB Field Structures

### Prospect.research_data
```json
{
  "company_overview": {
    "founded_year": 2020,
    "headquarters": "San Francisco, CA",
    "funding_rounds": [...],
    "key_metrics": {...}
  },
  "competitive_landscape": [...],
  "technology_stack": [...],
  "recent_developments": [...]
}
```

### IdealCustomerProfile.criteria
```json
{
  "required": {
    "employee_count_range": [50, 500],
    "industries": ["technology", "software"],
    "locations": ["North America", "Europe"]
  },
  "preferred": {
    "technologies": ["AWS", "Kubernetes"],
    "company_stage": ["growth", "established"]
  },
  "exclusions": {
    "industries": ["gambling", "tobacco"]
  }
}
```

### ResearchNote.metadata
```json
{
  "extraction_method": "firecrawl",
  "processing_time_ms": 1250,
  "content_length": 2048,
  "language_detected": "en",
  "sentiment_score": 0.65
}
```

## Data Validation and Constraints

### Business Rules
1. A Prospect must have at least one ContactPerson before being marked as qualified
2. ResearchNote content must be substantive (minimum length requirements)
3. ICP criteria must include at least one required field
4. DataSource performance metrics are updated asynchronously

### Referential Integrity
- Cascade delete: Prospect → ContactPerson, ResearchNote
- Restrict delete: IdealCustomerProfile (if linked to prospects)
- Soft delete: DataSource (mark inactive instead of delete)

### Performance Constraints
- Prospect.research_data JSONB size limited to 1MB
- Maximum 100 ResearchNote entries per Prospect
- ICP.criteria complexity limited to prevent query performance issues

This data model supports all MCP tool operations while maintaining data integrity and performance for multi-client access patterns.
