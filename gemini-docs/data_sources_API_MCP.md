# Infostatus Data Sources for Identifying ICP Companies

This document lists all data sources Infostatus can use to identify, verify, and engage with Ideal Candidate Profile (ICP) companies.  
For each source, the **API/MCP availability**, **fallback method** (if API not available), and **use case in prospecting** are described.

---

## Professional & Company Databases

### LinkedIn – [linkedin.com](https://www.linkedin.com/)
- **API/MCP:** Yes – REST API (`https://api.linkedin.com/v2`) via OAuth 2.0. Access requires LinkedIn Partner or premium programs (Sales Navigator, Talent, Marketing).  
- **Fallback if API not available:** Manual search (prospect name + company) or role search (company name + CIO/CTO/IT Manager). Sales Navigator advanced filters.  
- **Prospecting Use Case:**  
  - Identify decision-makers by title and confirm current employment.  
  - Track hiring signals (AI, ML, Cloud, Automation roles).  
  - Research company growth and technology adoption indicators.

---

### ZoomInfo – [zoominfo.com](https://www.zoominfo.com/)
- **API/MCP:** Yes – paid REST API for contacts, company profiles, and intent data.  
- **Fallback if API not available:** Manual browsing via ZoomInfo web portal.  
- **Prospecting Use Case:**  
  - Verify target decision-makers’ employment status.  
  - Enrich leads with verified emails and phone numbers.  
  - Surface intent signals (companies actively researching cloud/AI).

---

### Apollo – [apollo.io](https://app.apollo.io/)
- **API/MCP:** Yes – REST API (requires API key). Docs: [docs.apollo.io](https://docs.apollo.io).  
- **Fallback if API not available:** Web search within Apollo platform.  
- **Prospecting Use Case:**  
  - Find verified contact information (email, phone).  
  - Discover companies by industry, size, and tech signals.  
  - Automate enrichment into CRM for outreach campaigns.

---

### Crunchbase – [crunchbase.com](https://www.crunchbase.com/)
- **API/MCP:** Yes – REST API (subscription required). Provides company, funding, and people data.  
- **Fallback if API not available:** Manual lookups on Crunchbase website.  
- **Prospecting Use Case:**  
  - Identify mid-market companies with funding or growth momentum.  
  - Cross-check revenue and size against ICP criteria.  
  - Spot potential buyers investing in AI/cloud infrastructure.

---

### Gartner / Forrester Peer Insights
- **API/MCP:** Limited – enterprise/partner access only.  
- **Fallback if API not available:** Manual review of published reports and buyer reviews.  
- **Prospecting Use Case:**  
  - Identify companies reviewing or purchasing AI/Cloud solutions.  
  - Use reviews as a talking point in outreach.  
  - Target organizations in active technology evaluation cycles.

---

## Public Job Boards & Hiring Platforms

### Seek – [seek.com.au](https://www.seek.com.au/)
- **API/MCP:** Limited – partner APIs exist but not public.  
- **Fallback if API not available:** Manual job search by company name + keywords (AI, ML, Cloud, AWS, Automation).  
- **Prospecting Use Case:**  
  - Detect companies actively hiring for AI/Cloud/automation roles.  
  - Use job ads as evidence of digital transformation initiatives.  
  - Identify emerging needs for Infostatus services.

---

### Indeed / Glassdoor / LinkedIn Jobs
- **API/MCP:**  
  - **Indeed** – API (deprecated publicly, now partner-only).  
  - **Glassdoor** – limited partner feeds.  
  - **LinkedIn Jobs** – accessible through LinkedIn’s developer suite.  
- **Fallback if API not available:** Manual search by keyword + company.  
- **Prospecting Use Case:**  
  - Surface technology adoption signals.  
  - Map hiring demand to Infostatus services.  
  - Identify decision-making teams (job listings often show department owners).

---

## Search & News

### Google Search / Google News – [google.com](https://www.google.com/)
- **API/MCP:** Yes – Google Custom Search API & Google News API (via Google Cloud).  
- **Fallback if API not available:** Manual search queries (“company name” + “AI” / “Cloud” / “Data breach”).  
- **Prospecting Use Case:**  
  - Find recent news or press releases related to AI/Cloud adoption.  
  - Surface relevant talking points for outreach.  
  - Monitor competitors and industry trends.

---

## Company Websites & Social Channels

### Company Websites
- **API/MCP:** None (manual only).  
- **Fallback:** Manual browsing of sites for employee bios, blogs, reports, and job postings.  
- **Prospecting Use Case:**  
  - Confirm decision-makers and their roles.  
  - Extract thought-leadership talking points from blogs.  
  - Spot transformation initiatives in reports or case studies.

---

### Twitter/X & LinkedIn Company Pages
- **API/MCP:**  
  - **Twitter/X** – Paid REST API v2 and Streaming API.  
  - **LinkedIn Company Pages** – limited via LinkedIn APIs (requires partner access).  
- **Fallback if API not available:** Manual monitoring of updates.  
- **Prospecting Use Case:**  
  - Identify announcements about partnerships, AI/cloud adoption.  
  - Leverage social updates as engagement hooks in outreach.  

---

## Government & Business Registries

### ASIC – [asic.gov.au](https://asic.gov.au/)
- **API/MCP:** Limited – no broad public API, data extracts available for partners.  
- **Fallback if API not available:** Manual search of company registration info.  
- **Prospecting Use Case:**  
  - Verify official company details.  
  - Confirm legal status and directors.  
  - Filter legitimate businesses from low-quality leads.

---

### ABN Lookup – [abr.business.gov.au](https://abr.business.gov.au/)
- **API/MCP:** Yes – ABN Lookup API (`https://abr.business.gov.au/abrxmlsearch`). Requires free GUID key.  
- **Fallback if API not available:** Manual searches on ABN Lookup portal.  
- **Prospecting Use Case:**  
  - Confirm company registration, ABN, and location in NSW.  
  - Validate prospect before outreach.  
  - Useful for compliance and record accuracy.

---

### NSW Government Open Data Portal – [data.nsw.gov.au](https://data.nsw.gov.au/)
- **API/MCP:** Yes – dataset-specific APIs available via portal.  
- **Fallback if API not available:** Download CSV/Excel datasets.  
- **Prospecting Use Case:**  
  - Identify companies with government contracts (healthcare, construction, etc.).  
  - Use contract wins as indicators of funding and growth.  
  - Prioritize firms investing in infrastructure and digital capabilities.

---

## Industry Associations & Membership Lists

### AIIA, AI Group, HISA, NSW Construction & Manufacturing Councils
- **API/MCP:** None (manual).  
- **Fallback:** Membership directories, published reports, event attendee lists.  
- **Prospecting Use Case:**  
  - Identify active industry participants and members.  
  - Leverage association membership as a trust-building hook.  
  - Spot prospects attending conferences and industry events.

---
# Data Source Prospecting Matrix

This matrix shows the strength of each source for three stages of prospecting:  
- **Lead Discovery** – finding new companies/leads  
- **Lead Verification** – confirming company and decision-maker details  
- **Lead Enrichment** – adding contact info, news, insights, or talking points  

| Source                         | Lead Discovery | Lead Verification | Lead Enrichment | Notes                                                                 |
|--------------------------------|----------------|-------------------|-----------------|----------------------------------------------------------------------|
| **LinkedIn**                   | ✅✅✅ Strong   | ✅✅✅ Strong      | ✅ Moderate     | Best for identifying roles, job titles, hiring signals. Limited enrichment beyond profiles. |
| **ZoomInfo**                   | ✅ Moderate    | ✅✅✅ Strong      | ✅✅✅ Strong   | Excellent for verified contact info, emails, phone, and intent signals. |
| **Apollo**                     | ✅✅ Strong    | ✅✅✅ Strong      | ✅✅✅ Strong   | Combines discovery, verification, and enrichment in one platform.     |
| **Crunchbase**                 | ✅✅ Strong    | ✅ Moderate       | ✅ Moderate     | Great for growth signals and funding insights, less useful for individual contacts. |
| **Gartner / Forrester PI**     | ✅ Moderate    | ✅ Moderate       | ✅✅ Strong     | Good for enrichment via reviews and buyer signals. Limited direct lead data. |
| **Seek / Job Boards**          | ✅✅ Strong    | ✅ Moderate       | ✅ Moderate     | Detects hiring signals. Useful for discovery but limited for contacts. |
| **Google Search / News**       | ✅ Moderate    | ✅ Moderate       | ✅✅✅ Strong   | Best for enrichment via news/talking points. Manual verification needed. |
| **Company Websites**            | ✅ Moderate    | ✅✅ Strong       | ✅✅ Strong     | Good for confirming decision-makers and pulling blogs/reports for talking points. |
| **Twitter/X & LinkedIn Pages** | ✅ Moderate    | ✅ Moderate       | ✅✅ Strong     | Useful for enrichment via announcements. Limited for discovery/verification. |
| **ASIC**                       | ❌ Weak        | ✅✅ Strong       | ❌ Weak        | Useful only for legal verification of companies. Not for discovery or enrichment. |
| **ABN Lookup**                 | ❌ Weak        | ✅✅ Strong       | ❌ Weak        | Similar to ASIC. Compliance tool, not for discovery. |
| **NSW Open Data Portal**       | ✅✅ Strong    | ✅ Moderate       | ✅ Moderate     | Useful for discovering contract winners. Limited enrichment data. |
| **Industry Associations**      | ✅✅ Strong    | ✅ Moderate       | ✅ Strong       | Excellent for discovery and warm leads. Some enrichment via reports/events. |

---

## Key:
- ✅✅✅ Strong = High reliability and usefulness
- ✅✅ Strong = Moderate / situationally useful
- ✅ Weak = Limited or niche application
- ❌ = Not suitable for that stage

---

## Insights
- **Best for Lead Discovery:** LinkedIn, Apollo, Seek, Crunchbase, NSW Open Data, Industry Associations.  
- **Best for Lead Verification:** LinkedIn, Apollo, ZoomInfo, ABN Lookup/ASIC.  
- **Best for Lead Enrichment:** ZoomInfo, Apollo, Google News, Company Websites, Industry Associations.  

---
