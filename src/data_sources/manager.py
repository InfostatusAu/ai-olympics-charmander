"""Data source manager for orchestrating all research data sources."""

import logging
from typing import Dict, Any, Optional
import asyncio

from .apollo_source import ApolloSource
from .serper_source import SerperSource 
from .playwright_source import PlaywrightSource
from .linkedin_source import LinkedInSource
from .job_boards_source import JobBoardsSource
from .news_source import NewsSource
from .government_source import GovernmentSource

logger = logging.getLogger(__name__)


class DataSourceManager:
    """Orchestrates all research data sources with graceful error handling."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize data source manager with configuration.
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        config = config or {}
        
        # Initialize all data sources
        self.apollo_source = ApolloSource(config.get('apollo_api_key'))
        self.serper_source = SerperSource(config.get('serper_api_key'))
        self.playwright_source = PlaywrightSource(
            config.get('linkedin_email'),
            config.get('linkedin_password')
        )
        self.linkedin_source = LinkedInSource()
        self.job_boards_source = JobBoardsSource()
        self.news_source = NewsSource()
        self.government_source = GovernmentSource()
        
    async def collect_all_prospect_data(self, company: str) -> Dict[str, Any]:
        """Collect data from all sources with graceful error handling.
        
        Args:
            company: Company name to research
            
        Returns:
            Dictionary containing all collected data and error information
        """
        results = {
            'company_website': None,
            'apollo_data': None,
            'linkedin_data': None,
            'serper_search': None,
            'playwright_data': None,
            'job_boards': None,
            'news_data': None,
            'government_data': None,
            'errors': [],
            'successful_sources': [],
            'failed_sources': []
        }
        
        # Define all data source collection tasks
        tasks = [
            self._safe_collect('apollo', self.apollo_source.enrich_company, company),
            self._safe_collect('serper', self.serper_source.search_company, company),
            self._safe_collect('playwright', self.playwright_source.browse_linkedin, company),
            self._safe_collect('linkedin', self.linkedin_source.research_company, company),
            self._safe_collect('job_boards', self.job_boards_source.research_jobs, company),
            self._safe_collect('news', self.news_source.research_news, company),
            self._safe_collect('government', self.government_source.research_company, company),
        ]
        
        # Execute all tasks concurrently
        task_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        source_map = {
            'apollo': 'apollo_data',
            'serper': 'serper_search', 
            'playwright': 'playwright_data',
            'linkedin': 'linkedin_data',
            'job_boards': 'job_boards',
            'news': 'news_data',
            'government': 'government_data'
        }
        
        for i, (source_name, result_data, error) in enumerate(task_results):
            if isinstance(task_results[i], Exception):
                # Task itself failed
                error_msg = f"{source_name} task failed: {task_results[i]}"
                results['errors'].append(error_msg)
                results['failed_sources'].append(source_name)
                logger.warning(error_msg)
            elif error:
                # Source returned error
                results['errors'].append(f"{source_name}: {error}")
                results['failed_sources'].append(source_name)
                logger.warning(f"{source_name} source failed: {error}")
            else:
                # Success
                results[source_map[source_name]] = result_data
                results['successful_sources'].append(source_name)
                logger.info(f"{source_name} source succeeded")
                
        # Add summary metrics
        results['successful_sources_count'] = len(results['successful_sources'])
        results['failed_sources_count'] = len(results['failed_sources'])
        results['total_sources'] = 7  # Total number of sources
        
        logger.info(f"Data collection complete for {company}: "
                   f"{results['successful_sources_count']}/{results['total_sources']} sources successful")
        
        return results
        
    async def _safe_collect(self, source_name: str, method, company: str) -> tuple:
        """Safely collect data from a source with error handling.
        
        Args:
            source_name: Name of the data source
            method: Async method to call
            company: Company name parameter
            
        Returns:
            Tuple of (source_name, result_data, error_message)
        """
        try:
            result = await method(company)
            return (source_name, result, None)
        except Exception as e:
            return (source_name, None, str(e))
