# Data Sources for Identifying ICP Companies (with API / MCP Info)

## Professional & Company Databases

- **LinkedIn** – [linkedin.com](https://www.linkedin.com/)  
  - General use: confirm employment, search people, roles, company data  
  - **API / MCP / Server Info:**  
    - LinkedIn offers a set of APIs under its Developer Solutions: Sales, Talent, Marketing, Ads, Learning etc. :contentReference[oaicite:0]{index=0}  
    - Authentication via OAuth 2.0. :contentReference[oaicite:1]{index=1}  
    - Base API endpoint is `api.linkedin.com/v2` for many REST endpoints. :contentReference[oaicite:2]{index=2}  

- **ZoomInfo** – [zoominfo.com](https://www.zoominfo.com/)  
  - General use: backup verification of contact and company details  
  - **API / MCP / Server Info:**  
    - ZoomInfo provides a hosted API for contact, company, and intent/enrichment data. :contentReference[oaicite:3]{index=3}  
    - Enables integration with CRMs, data enrichment workflows. :contentReference[oaicite:4]{index=4}  

- **Apollo** – [apollo.io](https://app.apollo.io/)  
  - General use: contact details, phone & email, company-level details  
  - **API / MCP / Server Info:**  
    - Apollo has a REST API allowing access to people, organizations, enrichment endpoints, sequences, etc. :contentReference[oaicite:5]{index=5}  
    - You need an API key scoped by endpoint; pricing and plan determine how many calls and features are accessible. :contentReference[oaicite:6]{index=6}  

- **Other Databases** (e.g., Crunchbase, Gartner/Forrester Peer Insights)  
  - General use: funding info, reviews, growth signals  
  - **API / MCP / Server Info:**  
    - *Crunchbase* has APIs that give company, financial, funding, and organizational data (though usage may require subscription)  
    - *Gartner / Forrester Peer Insights* are more content / review-based; API access may be limited or not public.

## Public Job Boards & Hiring Platforms

- **Seek** – [seek.com.au](https://www.seek.com.au/)  
  - General use: job listings by company, keywords  
  - **API / MCP / Server Info:**  
    - As of current public documentation, Seek has limited public API access for job listing data. Some partner or premium access may allow more. (No strong publicly documented full-MCP for contact data.)  

- **Other boards** (Indeed, LinkedIn Jobs, Glassdoor)  
  - Similar: job listing info, hiring signals  
  - **API / MCP / Server Info:**  
    - LinkedIn Jobs is integrated via LinkedIn’s APIs (Jobs endpoints) under LinkedIn’s developer suite. :contentReference[oaicite:7]{index=7}  
    - Indeed and Glassdoor may have APIs or feed access (requires checking their developer/partner documentation).

## Search & News

- **Google Search / News** – [google.com](https://www.google.com/)  
  - General use: recent news, announcements, POV for outreach  
  - **API / MCP / Server Info:**  
    - Google offers some API products (e.g. News API) but many searches are manual.  
    - For custom / automated monitoring, one might use Google News RSS feeds, or paid API access via Google Cloud or third party providers.

## Company Websites & Social Channels

- **Company Websites, Blogs, Employee Bios etc.**  
  - General use: info-gathering, talking points, verifying roles / technologies  
  - **API / MCP / Server Info:**  
    - Usually no formal API; manual crawling/scraping may be used (subject to legal / terms considerations).  

- **Twitter/X & LinkedIn Updates**  
  - For LinkedIn, various APIs (Profile, Posts) exist, but often via restricted endpoints. :contentReference[oaicite:8]{index=8}  
  - For Twitter/X, subject to their API access rules (often paid / restricted).  

## Government & Business Registries

- **ASIC, ABN Lookup, NSW Government Open Data Portal**  
  - General use: company registration, legal status, size, official contract engagement  
  - **API / MCP / Server Info:**  
    - ABN Lookup offers an API for ABN, entity names, registration details.  
    - NSW Government Open Data Portal often has downloadable datasets or APIs (depending on dataset).  

## Industry Associations & Membership Lists

- **AIIA, AI Group, Healthcare IT, Construction Councils**  
  - General use: membership directories, events, published reports  
  - **API / MCP / Server Info:**  
    - Usually manual or via membership access; APIs are rare unless they publish open data.

---




# Data Sources API / MCP Summary Table

| Source                        | API Availability | Access Type            | Endpoint / Notes                                                                 |
|-------------------------------|------------------|------------------------|---------------------------------------------------------------------------------|
| **LinkedIn**                  | Yes              | Partner / Premium      | `https://api.linkedin.com/v2` (OAuth 2.0). Limited access for Sales/Talent APIs.|
| **ZoomInfo**                  | Yes              | Partner / Paid         | REST API for contacts, companies, intent data. Subscription required.           |
| **Apollo**                    | Yes              | Paid (API key)         | REST API. Docs: [docs.apollo.io](https://docs.apollo.io). Requires API key.     |
| **Crunchbase**                | Yes              | Paid / Premium         | REST API for org, funding, people, and acquisitions data.                       |
| **Gartner / Forrester PI**    | Limited          | Partner / Enterprise   | Not public. Enterprise clients may access APIs or export feeds.                 |
| **Seek (Australia)**          | Limited          | Partner / Enterprise   | Some API feeds for job postings. Requires business agreement.                   |
| **Indeed**                    | Yes (restricted) | Partner / Enterprise   | Job Search API (deprecated publicly). Paid partners may access job feeds.       |
| **Glassdoor**                 | Limited          | Partner / Enterprise   | APIs for job/salary data exist but require business contracts.                  |
| **Google Search / News**      | Yes              | Paid / Public          | Google Custom Search API (`https://developers.google.com/custom-search`). News API via Google Cloud. |
| **Company Websites**           | No (manual)      | —                      | No official APIs. Scraping/manual collection only (check ToS).                  |
| **Twitter / X**               | Yes              | Paid (tiered access)   | REST API v2 + Streaming API. Paid subscriptions required.                        |
| **ASIC (Australia)**          | Limited          | Paid / Subscription    | No broad public API. Data extracts available for partners.                      |
| **ABN Lookup**                | Yes              | Public / Free          | API: `https://abr.business.gov.au/abrxmlsearch` (requires free GUID key).       |
| **NSW Gov Open Data Portal**  | Yes              | Public / Free          | Dataset APIs via `https://data.nsw.gov.au`. Each dataset has unique endpoint.   |
| **Industry Associations**     | No (manual)      | Membership access      | Typically member directories or reports. APIs rarely available.                 |
