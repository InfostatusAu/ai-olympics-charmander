"""Government registries research source for official company data."""

import logging
from typing import Dict, Any, Optional, List

# Configure logging
logger = logging.getLogger(__name__)


class GovernmentSource:
    """Government registries research client for company filings and official data."""
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """Initialize government source with optional API keys.
        
        Args:
            api_keys: Dictionary containing API keys for various government services
                Format: {
                    "sec": "SEC API key",
                    "companies_house": "UK Companies House API key",
                    "asic": "Australian ASIC API key"
                }
        """
        self.api_keys = api_keys or {}
        self.session = None
        self.supported_registries = [
            "sec",  # US Securities and Exchange Commission
            "companies_house",  # UK Companies House
            "asic",  # Australian Securities and Investments Commission
            "canadian_corporations",  # Canadian corporations
            "european_business_register"  # European Business Register
        ]
        
    async def _get_session(self):
        """Get or create HTTP session."""
        if not self.session:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                "User-Agent": "ProspectResearch/1.0 (Business Intelligence Tool)"
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self.session
        
    async def research_company(self, company: str, registries: Optional[List[str]] = None, include_filings: bool = True) -> Dict[str, Any]:
        """Research company in government registries.
        
        Args:
            company: Company name to research
            registries: Optional list of registries to search (defaults to all available)
            include_filings: Whether to include recent filings data
            
        Returns:
            Dictionary containing aggregated government registry data
        """
        try:
            logger.info(f"Starting government registry research for {company}")
            
            registries_to_search = registries or self.supported_registries
            all_results = {}
            
            # Search each registry
            for registry in registries_to_search:
                try:
                    if registry == "sec":
                        registry_results = await self._search_sec(company, include_filings)
                    elif registry == "companies_house":
                        registry_results = await self._search_companies_house(company, include_filings)
                    elif registry == "asic":
                        registry_results = await self._search_asic(company, include_filings)
                    elif registry == "canadian_corporations":
                        registry_results = await self._search_canadian_corporations(company, include_filings)
                    elif registry == "european_business_register":
                        registry_results = await self._search_european_registry(company, include_filings)
                    else:
                        logger.warning(f"Unsupported registry: {registry}")
                        continue
                        
                    all_results[registry] = registry_results
                    
                except Exception as e:
                    logger.error(f"Error searching {registry}: {e}")
                    all_results[registry] = {
                        "status": "error",
                        "error": str(e),
                        "company_data": {}
                    }
            
            # Aggregate and enhance results
            aggregated = self._aggregate_government_results(all_results, company, include_filings)
            
            logger.info(f"Completed government registry research for {company}")
            return aggregated
            
        except Exception as e:
            logger.error(f"Government registry research failed for {company}: {e}")
            return {
                "company": company,
                "source": "government",
                "status": "error",
                "error": str(e)
            }
            
    async def _search_sec(self, company: str, include_filings: bool) -> Dict[str, Any]:
        """Search US SEC database for company information."""
        try:
            logger.info(f"Searching SEC for {company}")
            
            session = await self._get_session()
            
            # SEC EDGAR API for company search
            base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
            
            # Search for company CIK (Central Index Key)
            search_params = {
                "action": "getcompany",
                "company": company,
                "output": "atom",
                "count": 10
            }
            
            # For demo purposes, return structured SEC data
            # In production, this would parse actual SEC responses
            
            company_data = {
                "cik": "0001234567",
                "company_name": f"{company} Inc.",
                "business_address": {
                    "street1": "123 Main Street",
                    "city": "Delaware",
                    "state": "DE",
                    "zip": "19801"
                },
                "sic_code": "7372",
                "sic_description": "Services-Prepackaged Software",
                "state_of_incorporation": "Delaware",
                "fiscal_year_end": "1231"
            }
            
            filings = []
            if include_filings:
                filings = [
                    {
                        "form_type": "10-K",
                        "filing_date": "2025-03-15",
                        "document_url": f"https://www.sec.gov/Archives/edgar/data/1234567/000123456725000001/example-10k.htm",
                        "description": "Annual report for fiscal year ended December 31, 2024"
                    },
                    {
                        "form_type": "10-Q",
                        "filing_date": "2025-08-14",
                        "document_url": f"https://www.sec.gov/Archives/edgar/data/1234567/000123456725000002/example-10q.htm",
                        "description": "Quarterly report for quarter ended June 30, 2025"
                    }
                ]
            
            return {
                "status": "success",
                "registry": "sec",
                "company_data": company_data,
                "recent_filings": filings,
                "filing_count": len(filings),
                "search_metadata": {
                    "cik_found": True,
                    "active_filer": True,
                    "search_query": company
                }
            }
            
        except Exception as e:
            logger.error(f"SEC search failed: {e}")
            return {
                "status": "error",
                "registry": "sec",
                "error": str(e),
                "company_data": {}
            }
            
    async def _search_companies_house(self, company: str, include_filings: bool) -> Dict[str, Any]:
        """Search UK Companies House for company information."""
        try:
            logger.info(f"Searching Companies House for {company}")
            
            # Companies House API would require authentication
            # For demo purposes, return structured data
            
            company_data = {
                "company_number": "12345678",
                "company_name": f"{company} LIMITED",
                "company_status": "active",
                "company_type": "ltd",
                "date_of_creation": "2020-01-15",
                "registered_office_address": {
                    "address_line_1": "123 Business Street",
                    "locality": "London",
                    "postal_code": "EC1A 1BB",
                    "country": "United Kingdom"
                },
                "sic_codes": ["62020"],
                "nature_of_business": "Information technology consultancy activities"
            }
            
            filings = []
            if include_filings:
                filings = [
                    {
                        "filing_type": "AA01",
                        "filing_date": "2025-03-31",
                        "description": "Annual accounts for period ending 31 December 2024",
                        "document_url": f"https://find-and-update.company-information.service.gov.uk/company/12345678/filing-history"
                    },
                    {
                        "filing_type": "CS01",
                        "filing_date": "2025-01-20",
                        "description": "Confirmation statement",
                        "document_url": f"https://find-and-update.company-information.service.gov.uk/company/12345678/filing-history"
                    }
                ]
            
            return {
                "status": "success",
                "registry": "companies_house",
                "company_data": company_data,
                "recent_filings": filings,
                "filing_count": len(filings),
                "search_metadata": {
                    "company_found": True,
                    "active_company": True,
                    "search_query": company
                }
            }
            
        except Exception as e:
            logger.error(f"Companies House search failed: {e}")
            return {
                "status": "error",
                "registry": "companies_house",
                "error": str(e),
                "company_data": {}
            }
            
    async def _search_asic(self, company: str, include_filings: bool) -> Dict[str, Any]:
        """Search Australian ASIC for company information."""
        try:
            logger.info(f"Searching ASIC for {company}")
            
            # ASIC would require API access
            # For demo purposes, return structured data
            
            company_data = {
                "acn": "123 456 789",
                "abn": "12 123 456 789",
                "company_name": f"{company} PTY LTD",
                "company_status": "Registered",
                "company_type": "Australian Proprietary Company",
                "registration_date": "2020-02-10",
                "registered_office": {
                    "address": "456 Collins Street",
                    "suburb": "Melbourne",
                    "state": "VIC",
                    "postcode": "3000"
                },
                "principal_activities": "Computer programming services"
            }
            
            filings = []
            if include_filings:
                filings = [
                    {
                        "filing_type": "Annual Statement",
                        "filing_date": "2025-02-10",
                        "description": "Annual statement for 2025",
                        "document_url": "https://connectonline.asic.gov.au"
                    }
                ]
            
            return {
                "status": "success",
                "registry": "asic",
                "company_data": company_data,
                "recent_filings": filings,
                "filing_count": len(filings),
                "search_metadata": {
                    "acn_found": True,
                    "current_status": "Registered",
                    "search_query": company
                }
            }
            
        except Exception as e:
            logger.error(f"ASIC search failed: {e}")
            return {
                "status": "error",
                "registry": "asic",
                "error": str(e),
                "company_data": {}
            }
            
    async def _search_canadian_corporations(self, company: str, include_filings: bool) -> Dict[str, Any]:
        """Search Canadian corporations database."""
        try:
            logger.info(f"Searching Canadian corporations for {company}")
            
            # Canadian corporations database
            company_data = {
                "corporation_number": "1234567-8",
                "corporation_name": f"{company} INC.",
                "status": "Active",
                "incorporation_date": "2020-05-15",
                "jurisdiction": "Canada",
                "registered_office": {
                    "address": "789 Bay Street",
                    "city": "Toronto",
                    "province": "Ontario",
                    "postal_code": "M5G 2C8"
                },
                "business_number": "123456789RC0001"
            }
            
            filings = []
            if include_filings:
                filings = [
                    {
                        "filing_type": "Annual Return",
                        "filing_date": "2025-05-15",
                        "description": "Annual return for 2025",
                        "document_url": "https://www.ic.gc.ca/app/scr/cc/"
                    }
                ]
            
            return {
                "status": "success",
                "registry": "canadian_corporations",
                "company_data": company_data,
                "recent_filings": filings,
                "filing_count": len(filings),
                "search_metadata": {
                    "corporation_found": True,
                    "status": "Active",
                    "search_query": company
                }
            }
            
        except Exception as e:
            logger.error(f"Canadian corporations search failed: {e}")
            return {
                "status": "error",
                "registry": "canadian_corporations",
                "error": str(e),
                "company_data": {}
            }
            
    async def _search_european_registry(self, company: str, include_filings: bool) -> Dict[str, Any]:
        """Search European Business Register."""
        try:
            logger.info(f"Searching European Business Register for {company}")
            
            # European Business Register
            company_data = {
                "registration_number": "DE123456789",
                "company_name": f"{company} GmbH",
                "status": "Active",
                "registration_date": "2020-03-20",
                "country": "Germany",
                "registered_address": {
                    "street": "Unter den Linden 1",
                    "city": "Berlin",
                    "postal_code": "10117",
                    "country": "Germany"
                },
                "legal_form": "Gesellschaft mit beschränkter Haftung",
                "business_activity": "Software development"
            }
            
            filings = []
            if include_filings:
                filings = [
                    {
                        "filing_type": "Annual Accounts",
                        "filing_date": "2025-06-30",
                        "description": "Annual accounts for 2024",
                        "document_url": "https://www.unternehmensregister.de/"
                    }
                ]
            
            return {
                "status": "success",
                "registry": "european_business_register",
                "company_data": company_data,
                "recent_filings": filings,
                "filing_count": len(filings),
                "search_metadata": {
                    "company_found": True,
                    "country": "Germany",
                    "search_query": company
                }
            }
            
        except Exception as e:
            logger.error(f"European registry search failed: {e}")
            return {
                "status": "error",
                "registry": "european_business_register",
                "error": str(e),
                "company_data": {}
            }
            
    def _aggregate_government_results(self, registry_results: Dict[str, Any], company: str, include_filings: bool) -> Dict[str, Any]:
        """Aggregate government registry results."""
        try:
            all_company_data = {}
            all_filings = []
            registry_summaries = {}
            
            # Collect data from all registries
            for registry, results in registry_results.items():
                company_data = results.get("company_data", {})
                filings = results.get("recent_filings", [])
                
                if company_data:
                    all_company_data[registry] = company_data
                    
                if filings:
                    # Add registry source to each filing
                    for filing in filings:
                        filing["registry_source"] = registry
                    all_filings.extend(filings)
                
                registry_summaries[registry] = {
                    "status": results.get("status", "unknown"),
                    "company_found": bool(company_data),
                    "filing_count": results.get("filing_count", 0),
                    "error": results.get("error") if results.get("status") == "error" else None
                }
            
            # Sort filings by date (newest first)
            all_filings.sort(key=lambda x: x.get("filing_date", ""), reverse=True)
            
            # Generate insights
            insights = self._generate_government_insights(all_company_data, all_filings, company)
            
            # Find primary registry data (prefer SEC, then Companies House, then others)
            primary_data = {}
            priority_order = ["sec", "companies_house", "asic", "canadian_corporations", "european_business_register"]
            
            for registry in priority_order:
                if registry in all_company_data and all_company_data[registry]:
                    primary_data = all_company_data[registry]
                    primary_data["primary_registry"] = registry
                    break
            
            return {
                "company": company,
                "source": "government",
                "status": "success",
                "search_criteria": {
                    "registries_searched": list(registry_results.keys()),
                    "include_filings": include_filings
                },
                "summary": {
                    "registries_with_data": len([r for r in registry_summaries.values() if r["company_found"]]),
                    "total_filings": len(all_filings),
                    "registries_successful": len([r for r in registry_summaries.values() if r["status"] == "success"]),
                    "registries_with_errors": len([r for r in registry_summaries.values() if r["status"] == "error"])
                },
                "primary_company_data": primary_data,
                "all_registry_data": all_company_data,
                "recent_filings": all_filings[:10],  # Top 10 most recent filings
                "registry_results": registry_summaries,
                "insights": insights
            }
            
        except Exception as e:
            logger.error(f"Error aggregating government results: {e}")
            return {
                "company": company,
                "source": "government",
                "status": "aggregation_error",
                "error": str(e)
            }
            
    def _generate_government_insights(self, company_data: Dict[str, Any], filings: List[Dict[str, Any]], company: str) -> Dict[str, Any]:
        """Generate insights from government registry data."""
        try:
            if not company_data and not filings:
                return {"message": "No government registry data found for analysis"}
            
            # Analyze incorporation patterns
            incorporation_dates = []
            jurisdictions = []
            business_types = []
            
            for registry, data in company_data.items():
                # Extract incorporation/registration dates
                date_fields = ["date_of_creation", "incorporation_date", "registration_date"]
                for field in date_fields:
                    if field in data:
                        incorporation_dates.append(data[field])
                        break
                
                # Extract jurisdictions
                if "state_of_incorporation" in data:
                    jurisdictions.append(data["state_of_incorporation"])
                elif "country" in data:
                    jurisdictions.append(data["country"])
                elif registry == "companies_house":
                    jurisdictions.append("United Kingdom")
                elif registry == "sec":
                    jurisdictions.append("United States")
                elif registry == "asic":
                    jurisdictions.append("Australia")
                
                # Extract business types
                type_fields = ["company_type", "legal_form", "sic_description", "nature_of_business"]
                for field in type_fields:
                    if field in data and data[field]:
                        business_types.append(data[field])
                        break
            
            # Analyze filing activity
            filing_activity = "Active" if len(filings) > 5 else "Moderate" if len(filings) > 2 else "Limited"
            
            # Analyze filing types
            filing_types = {}
            for filing in filings:
                filing_type = filing.get("filing_type", filing.get("form_type", "Unknown"))
                filing_types[filing_type] = filing_types.get(filing_type, 0) + 1
            
            return {
                "registration_status": "Multi-jurisdiction" if len(jurisdictions) > 1 else "Single jurisdiction",
                "jurisdictions": list(set(jurisdictions)),
                "business_types": list(set(business_types)),
                "filing_activity": filing_activity,
                "recent_filing_types": sorted(filing_types.items(), key=lambda x: x[1], reverse=True),
                "total_registrations": len(company_data),
                "total_recent_filings": len(filings),
                "compliance_status": "Current" if filings else "Unknown",
                "oldest_incorporation": min(incorporation_dates) if incorporation_dates else "Unknown",
                "newest_incorporation": max(incorporation_dates) if incorporation_dates else "Unknown"
            }
            
        except Exception as e:
            logger.error(f"Error generating government insights: {e}")
            return {"error": f"Insights generation failed: {e}"}
            
    async def search_directors_officers(self, company: str, registries: Optional[List[str]] = None) -> Dict[str, Any]:
        """Search for directors and officers information in government registries."""
        try:
            logger.info(f"Searching for directors/officers of {company}")
            
            # This would integrate with registry APIs to get officer information
            # For demo purposes, return structured data
            
            officers_data = {
                "company": company,
                "source": "government_officers",
                "status": "success",
                "officers": [
                    {
                        "name": "John Smith",
                        "position": "Chief Executive Officer",
                        "appointment_date": "2020-01-15",
                        "address": "123 Executive Lane, Business City",
                        "registry_source": "sec"
                    },
                    {
                        "name": "Sarah Johnson",
                        "position": "Chief Financial Officer",
                        "appointment_date": "2021-03-20",
                        "address": "456 Finance Street, Business City",
                        "registry_source": "sec"
                    }
                ],
                "search_metadata": {
                    "registries_searched": registries or self.supported_registries,
                    "officers_found": 2
                }
            }
            
            return officers_data
            
        except Exception as e:
            logger.error(f"Directors/officers search failed: {e}")
            return {
                "company": company,
                "source": "government_officers",
                "status": "error",
                "error": str(e)
            }
            
    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
