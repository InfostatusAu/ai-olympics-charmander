# Research Approach to Gather Prospect Information

This document outlines the step-by-step approach for gathering prospect information, leveraging various data sources and tools.

## 1. LinkedIn
- **Tools**: Firecrawl, Serper, Playwright MCP browser tools.
- **Process**:
  1. Attempt to fetch/crawl all possible information from LinkedIn using Firecrawl or Serper SDK/API.
  2. If necessary, use Playwright MCP browser tools to browse and capture screens for information. **User will be asked to log in to LinkedIn before proceeding with Playwright.**
- **Purpose**: Confirm prospect's employment, search by prospect name + company, identify decision-makers (company name + job title), track hiring signals for AI, ML, Cloud, or Automation roles.

## 2. Apollo (apollo.io)
- **Tools**: Apollo API.
- **Process**: Utilize the Apollo API to gather additional information.
- **Purpose**: Source verified contact details (emails, phone numbers), lead enrichment, and intent data.

## 3. Public Job Boards and Hiring Platforms
- **Platforms**: Seek, Indeed, Glassdoor.
- **Tools**: Firecrawl API, Playwright MCP browser tools.
- **Process**:
  1. Attempt to fetch information using Firecrawl APIs.
  2. **Fallback**: Use Playwright MCP browser tools. **User will be asked to enter credentials for sites required.**
- **Purpose**: Search for active listings by company name, identify roles mentioning AI, ML, Generative AI, Cloud, AWS, Automation.

## 4. General Search and News
- **Sources**: Google, company's website, other social channels like X.
- **Purpose**: Identify recent news for relevant outreach talking points, track company announcements about AI, Cloud, or transformation projects, find employee bios, job postings, blog posts, company reports, case studies, tech announcements, partnerships, and hiring drives.

## 5. Government & Business Registries
- **Registries**: ASIC (asic.gov.au), ABN Lookup (abr.business.gov.au), NSW Government Open Data Portal (data.nsw.gov.au).
- **Purpose**: Identify company size, registration, and contract activity.

## Data Sources for Identifying ICP Companies (Purpose Summary)

### Professional & Company Databases
- **LinkedIn**: Confirm employment, search by prospect/company, track hiring signals.
- **Apollo**: Verified contact details, lead enrichment, intent data.

### Public Job Boards & Hiring Platforms
- **Seek, Indeed, LinkedIn Jobs, Glassdoor**: Identify companies hiring for tech/AI/cloud roles.

### Search & News
- **Google Search, Google News Alerts, Industry Media**: Identify recent news, track announcements, find thought-leadership talking points.

### Company Websites & Social Channels
- **Company Websites, Twitter/X & LinkedIn Updates**: Employee bios, job postings, blog posts, company reports, tech announcements, partnerships, hiring drives.

### Government & Business Registries
- **ASIC, ABN Lookup, NSW Government Open Data Portal**: Identify company size, registration, contract activity.

### Industry Associations & Memberships
- **AIIA, AI Group, Healthcare IT associations, NSW Construction and Manufacturing Councils**: (Implicitly for identifying relevant industry context and potential leads, though not explicitly used for direct data fetching in the above steps).