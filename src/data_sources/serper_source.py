"""Serper API integration for Google search alternative."""

import logging
import os
from typing import Dict, Any, Optional, List

# Import config to trigger dotenv loading  
from .. import config

logger = logging.getLogger(__name__)


class SerperSource:
    """Serper API client for search and news data."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Serper source with API key."""
        # Load from environment if not provided
        self.api_key = api_key or os.getenv('SERPER_API_KEY')
        self.base_url = "https://google.serper.dev"
        self.session = None
        
    async def _get_session(self):
        """Get or create HTTP session."""
        if not self.session:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
        
    async def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make authenticated request to Serper API."""
        if not self.api_key:
            raise ValueError("Serper API key not configured")
            
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Serper API request failed: {e}")
            raise
    
    async def search_company(self, company: str, num_results: int = 10) -> Dict[str, Any]:
        """Search for company information using Serper API.
        
        Args:
            company: Company name to search for
            num_results: Number of results to return (max 100)
            
        Returns:
            Dictionary containing search results
        """
        if not self.api_key:
            logger.warning("Serper API key not configured, returning placeholder")
            return {
                "company": company,
                "source": "serper",
                "status": "no_api_key",
                "error": "API key not configured"
            }
            
        try:
            logger.info(f"Searching for company {company} via Serper")
            
            # Build search query focused on company information
            query = f"{company} company information headquarters contact"
            
            payload = {
                "q": query,
                "num": min(num_results, 100),  # Respect API limits
                "gl": "us",  # Geo location
                "hl": "en",  # Language
                "autocorrect": True,
                "type": "search"
            }
            
            data = await self._make_request("/search", payload)
            
            # Extract structured information
            result = {
                "company": company,
                "query": query,
                "source": "serper",
                "status": "success",
                "search_parameters": data.get("searchParameters", {}),
                "knowledge_graph": data.get("knowledgeGraph", {}),
                "organic_results": data.get("organic", []),
                "people_also_ask": data.get("peopleAlsoAsk", []),
                "related_searches": data.get("relatedSearches", []),
                "total_results": len(data.get("organic", []))
            }
            
            logger.info(f"Found {result['total_results']} organic results for {company}")
            return result
            
        except Exception as e:
            logger.error(f"Serper company search failed for {company}: {e}")
            return {
                "company": company,
                "source": "serper",
                "status": "error",
                "error": str(e)
            }
        
    async def news_search(self, company: str, num_results: int = 10) -> Dict[str, Any]:
        """Search for news about a company using Serper.
        
        Args:
            company: Company name to search news for
            num_results: Number of news results to return
            
        Returns:
            Dictionary containing news search results
        """
        if not self.api_key:
            logger.warning("Serper API key not configured, returning placeholder")
            return {
                "company": company,
                "news": [],
                "source": "serper",
                "status": "no_api_key",
                "error": "API key not configured"
            }
            
        try:
            logger.info(f"Searching news for {company} via Serper")
            
            # Build news-focused search query
            query = f"{company} news updates announcements"
            
            payload = {
                "q": query,
                "num": min(num_results, 100),
                "gl": "us",
                "hl": "en",
                "autocorrect": True,
                "type": "news"  # Use news search type
            }
            
            data = await self._make_request("/news", payload)
            
            # Extract news articles
            news_articles = []
            for article in data.get("news", []):
                news_articles.append({
                    "title": article.get("title"),
                    "link": article.get("link"),
                    "snippet": article.get("snippet"),
                    "source": article.get("source"),
                    "date": article.get("date"),
                    "position": article.get("position")
                })
            
            result = {
                "company": company,
                "query": query,
                "news": news_articles,
                "source": "serper",
                "status": "success",
                "search_parameters": data.get("searchParameters", {}),
                "total_articles": len(news_articles)
            }
            
            logger.info(f"Found {len(news_articles)} news articles for {company}")
            return result
            
        except Exception as e:
            logger.error(f"Serper news search failed for {company}: {e}")
            return {
                "company": company,
                "news": [],
                "source": "serper",
                "status": "error",
                "error": str(e)
            }
            
    async def general_search(self, query: str, search_type: str = "search", 
                           num_results: int = 10) -> Dict[str, Any]:
        """Perform general search using Serper API.
        
        Args:
            query: Search query
            search_type: Type of search (search, news, images, etc.)
            num_results: Number of results to return
            
        Returns:
            Dictionary containing search results
        """
        if not self.api_key:
            logger.warning("Serper API key not configured, returning placeholder")
            return {
                "query": query,
                "results": [],
                "source": "serper",
                "status": "no_api_key",
                "error": "API key not configured"
            }
            
        try:
            logger.info(f"Performing {search_type} search for: {query}")
            
            payload = {
                "q": query,
                "num": min(num_results, 100),
                "gl": "us",
                "hl": "en",
                "autocorrect": True,
                "type": search_type
            }
            
            endpoint = f"/{search_type}" if search_type != "search" else "/search"
            data = await self._make_request(endpoint, payload)
            
            result = {
                "query": query,
                "search_type": search_type,
                "source": "serper",
                "status": "success",
                "search_parameters": data.get("searchParameters", {}),
                "results": data,
                "total_results": len(data.get("organic", [])) if search_type == "search" else len(data.get(search_type, []))
            }
            
            logger.info(f"Search completed: {result['total_results']} results")
            return result
            
        except Exception as e:
            logger.error(f"Serper {search_type} search failed for {query}: {e}")
            return {
                "query": query,
                "search_type": search_type,
                "source": "serper",
                "status": "error",
                "error": str(e)
            }
            
    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
