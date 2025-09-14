"""Apollo.io API integration for contact enrichment and lead data."""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ApolloSource:
    """Apollo.io API client for contact and company enrichment."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Apollo source with API key."""
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/api/v1"
        self.session = None
        
    async def _get_session(self):
        """Get or create HTTP session."""
        if not self.session:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
        
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Apollo API."""
        if not self.api_key:
            raise ValueError("Apollo API key not configured")
            
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": self.api_key
        }
        
        kwargs.setdefault("headers", {}).update(headers)
        
        try:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Apollo API request failed: {e}")
            raise
    
    async def enrich_company(self, company: str) -> Dict[str, Any]:
        """Enrich company data using Apollo.io API.
        
        Args:
            company: Company name or domain to research
            
        Returns:
            Dictionary containing enriched company data
        """
        if not self.api_key:
            logger.warning("Apollo API key not configured, returning placeholder")
            return {
                "company": company,
                "source": "apollo",
                "status": "no_api_key",
                "error": "API key not configured"
            }
            
        try:
            # Clean domain for API call
            domain = company.lower()
            if domain.startswith("http"):
                from urllib.parse import urlparse
                domain = urlparse(domain).netloc
            domain = domain.replace("www.", "")
            
            logger.info(f"Enriching company data for {domain} via Apollo")
            
            # Use Organization Enrichment endpoint
            params = {"domain": domain}
            data = await self._make_request("GET", "/organizations/enrich", params=params)
            
            # Extract key company information
            org = data.get("organization", {})
            result = {
                "company": company,
                "source": "apollo", 
                "status": "success",
                "apollo_id": org.get("id"),
                "name": org.get("name"),
                "domain": org.get("website_url"),
                "description": org.get("short_description"),
                "industry": org.get("industry"),
                "employees": org.get("estimated_num_employees"),
                "revenue": org.get("annual_revenue_printed"),
                "funding": org.get("total_funding_printed"),
                "founded_year": org.get("founded_year"),
                "location": org.get("primary_location"),
                "linkedin_url": org.get("linkedin_url"),
                "phone": org.get("phone"),
                "technologies": org.get("technologies", []),
                "keywords": org.get("keywords", [])
            }
            
            logger.info(f"Successfully enriched company {domain}")
            return result
            
        except Exception as e:
            logger.error(f"Apollo company enrichment failed for {company}: {e}")
            return {
                "company": company,
                "source": "apollo",
                "status": "error",
                "error": str(e)
            }
        
    async def search_people(self, company: str, job_titles: Optional[List[str]] = None, 
                          seniorities: Optional[List[str]] = None) -> Dict[str, Any]:
        """Search for people at a company using Apollo.io.
        
        Args:
            company: Company name to search for contacts
            job_titles: List of job titles to filter by
            seniorities: List of seniority levels to filter by
            
        Returns:
            Dictionary containing contact search results
        """
        if not self.api_key:
            logger.warning("Apollo API key not configured, returning placeholder")
            return {
                "company": company,
                "contacts": [],
                "source": "apollo",
                "status": "no_api_key",
                "error": "API key not configured"
            }
            
        try:
            # Clean domain for API call
            domain = company.lower()
            if domain.startswith("http"):
                from urllib.parse import urlparse
                domain = urlparse(domain).netloc
            domain = domain.replace("www.", "")
            
            logger.info(f"Searching people at {domain} via Apollo")
            
            # Build search payload
            payload = {
                "q_organization_domains_list": [domain],
                "page": 1,
                "per_page": 25  # Reasonable limit for initial search
            }
            
            # Add filters if provided
            if job_titles:
                payload["person_titles"] = job_titles
            if seniorities:
                payload["person_seniorities"] = seniorities
                
            data = await self._make_request("POST", "/mixed_people/search", json=payload)
            
            # Extract contact information
            contacts = []
            for contact in data.get("contacts", []):
                contacts.append({
                    "apollo_id": contact.get("id"),
                    "name": contact.get("name"),
                    "first_name": contact.get("first_name"),
                    "last_name": contact.get("last_name"),
                    "title": contact.get("title"),
                    "seniority": contact.get("seniority"),
                    "email": contact.get("email"),
                    "phone": contact.get("phone_numbers", [{}])[0].get("raw_number") if contact.get("phone_numbers") else None,
                    "linkedin_url": contact.get("linkedin_url"),
                    "location": contact.get("present_raw_address"),
                    "departments": contact.get("departments", []),
                    "email_status": contact.get("email_status")
                })
                
            result = {
                "company": company,
                "domain": domain,
                "contacts": contacts,
                "total_found": data.get("pagination", {}).get("total_entries", 0),
                "page_info": data.get("pagination", {}),
                "source": "apollo",
                "status": "success"
            }
            
            logger.info(f"Found {len(contacts)} contacts at {domain}")
            return result
            
        except Exception as e:
            logger.error(f"Apollo people search failed for {company}: {e}")
            return {
                "company": company,
                "contacts": [],
                "source": "apollo",
                "status": "error",
                "error": str(e)
            }
            
    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
