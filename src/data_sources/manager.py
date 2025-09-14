"""Data source manager for orchestrating all research data sources."""

import logging
import time
from typing import Dict, Any, Optional, List
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
    """Orchestrates all research data sources with advanced error handling and coordination."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize data source manager with configuration.
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        config = config or {}
        
        # Initialize all enhanced data sources
        self.apollo_source = ApolloSource(config.get('apollo_api_key'))
        self.serper_source = SerperSource(config.get('serper_api_key'))
        self.playwright_source = PlaywrightSource(
            config.get('linkedin_email'),
            config.get('linkedin_password')
        )
        self.linkedin_source = LinkedInSource(
            email=config.get('linkedin_email'),
            password=config.get('linkedin_password'),
            firecrawl_api_key=config.get('firecrawl_api_key')
        )
        self.job_boards_source = JobBoardsSource(
            credentials={
                "seek": {"username": config.get('seek_username'), "password": config.get('seek_password')},
                "indeed": {"username": config.get('indeed_username'), "password": config.get('indeed_password')},
                "glassdoor": {"username": config.get('glassdoor_username'), "password": config.get('glassdoor_password')}
            }
        )
        self.news_source = NewsSource(
            news_api_key=config.get('news_api_key'),
            serper_api_key=config.get('serper_api_key')
        )
        self.government_source = GovernmentSource(
            api_keys={
                "sec": config.get('sec_api_key'),
                "companies_house": config.get('companies_house_api_key'),
                "asic": config.get('asic_api_key')
            }
        )
        
        # Configuration for different research modes
        self.config = config
        self.parallel_execution = config.get('parallel_execution', True)
        self.timeout_per_source = config.get('timeout_per_source', 30)
        self.retry_failed_sources = config.get('retry_failed_sources', True)
        self.max_retries = config.get('max_retries', 2)
        
    async def collect_all_prospect_data(self, company: str, research_mode: str = "comprehensive") -> Dict[str, Any]:
        """Collect data from all sources with advanced error handling and coordination.
        
        Args:
            company: Company name to research
            research_mode: Research mode ("quick", "comprehensive", "deep")
            
        Returns:
            Dictionary containing all collected data and detailed error information
        """
        logger.info(f"Starting {research_mode} data collection for {company}")
        
        # Initialize results structure
        results = {
            'company': company,
            'research_mode': research_mode,
            'timestamp': self._get_timestamp(),
            'apollo_data': None,
            'serper_search': None,
            'playwright_data': None,
            'linkedin_data': None,
            'job_boards': None,
            'news_data': None,
            'government_data': None,
            'errors': [],
            'successful_sources': [],
            'failed_sources': [],
            'source_metadata': {},
            'performance_metrics': {}
        }
        
        # Define source configurations based on research mode
        source_configs = self._get_source_configs(research_mode)
        
        if self.parallel_execution:
            results = await self._collect_parallel(company, source_configs, results)
        else:
            results = await self._collect_sequential(company, source_configs, results)
        
        # Add final summary and insights
        results = self._add_summary_insights(results)
        
        logger.info(f"Data collection complete for {company}: "
                   f"{results['successful_sources_count']}/{results['total_sources']} sources successful")
        
        return results
        
    def _get_source_configs(self, research_mode: str) -> Dict[str, Dict[str, Any]]:
        """Get source configurations based on research mode."""
        base_configs = {
            'apollo': {
                'method': self.apollo_source.enrich_company,
                'params': {},
                'priority': 1,
                'critical': True
            },
            'serper': {
                'method': self.serper_source.search_company,
                'params': {},
                'priority': 2,
                'critical': True
            },
            'linkedin': {
                'method': self.linkedin_source.research_company,
                'params': {},
                'priority': 3,
                'critical': True
            },
            'playwright': {
                'method': self.playwright_source.browse_linkedin,
                'params': {},
                'priority': 4,
                'critical': False
            },
            'job_boards': {
                'method': self.job_boards_source.research_jobs,
                'params': {},
                'priority': 5,
                'critical': False
            },
            'news': {
                'method': self.news_source.research_news,
                'params': {},
                'priority': 6,
                'critical': False
            },
            'government': {
                'method': self.government_source.research_company,
                'params': {},
                'priority': 7,
                'critical': False
            }
        }
        
        # Adjust configurations based on research mode
        if research_mode == "quick":
            # Only run critical sources for quick mode
            return {k: v for k, v in base_configs.items() if v['critical']}
        elif research_mode == "deep":
            # Enhanced parameters for deep research
            base_configs['news']['params'] = {'days_back': 90}
            base_configs['job_boards']['params'] = {'platforms': ['seek', 'indeed', 'glassdoor', 'linkedin_jobs']}
            base_configs['government']['params'] = {'include_filings': True}
            
        return base_configs
        
    async def _collect_parallel(self, company: str, source_configs: Dict[str, Dict[str, Any]], results: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data from sources in parallel."""
        start_time = time.time()
        
        # Create tasks for parallel execution
        tasks = []
        for source_name, config in source_configs.items():
            task = self._safe_collect_with_timeout(
                source_name, 
                config['method'], 
                company, 
                config.get('params', {}),
                self.timeout_per_source
            )
            tasks.append(task)
        
        # Execute all tasks concurrently
        task_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        results = self._process_task_results(task_results, source_configs, results)
        
        # Record performance metrics
        results['performance_metrics']['parallel_execution_time'] = time.time() - start_time
        results['performance_metrics']['execution_mode'] = 'parallel'
        
        return results
        
    async def _collect_sequential(self, company: str, source_configs: Dict[str, Dict[str, Any]], results: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data from sources sequentially."""
        start_time = time.time()
        
        # Sort sources by priority
        sorted_sources = sorted(source_configs.items(), key=lambda x: x[1]['priority'])
        
        for source_name, config in sorted_sources:
            source_start = time.time()
            
            try:
                source_name, result_data, error = await self._safe_collect_with_timeout(
                    source_name, 
                    config['method'], 
                    company, 
                    config.get('params', {}),
                    self.timeout_per_source
                )
                
                results = self._process_single_result(source_name, result_data, error, results)
                
                # Record individual source performance
                results['source_metadata'][source_name] = {
                    'execution_time': time.time() - source_start,
                    'priority': config['priority'],
                    'critical': config['critical']
                }
                
            except Exception as e:
                error_msg = f"{source_name} sequential execution failed: {e}"
                results['errors'].append(error_msg)
                results['failed_sources'].append(source_name)
                logger.error(error_msg)
        
        # Record performance metrics
        results['performance_metrics']['sequential_execution_time'] = time.time() - start_time
        results['performance_metrics']['execution_mode'] = 'sequential'
        
        return results
        
    async def _safe_collect_with_timeout(self, source_name: str, method, company: str, params: Dict[str, Any], timeout: int) -> tuple:
        """Safely collect data from a source with timeout and retry logic.
        
        Args:
            source_name: Name of the data source
            method: Async method to call
            company: Company name parameter
            params: Additional parameters for the method
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (source_name, result_data, error_message)
        """
        attempt = 0
        last_error = None
        
        while attempt <= self.max_retries:
            try:
                # Apply timeout wrapper
                async with asyncio.timeout(timeout):
                    if params:
                        result = await method(company, **params)
                    else:
                        result = await method(company)
                    
                    # Validate result
                    if result and isinstance(result, dict) and result.get('status') not in ['error', 'failed']:
                        return (source_name, result, None)
                    else:
                        error_msg = f"Invalid or error result from {source_name}: {result.get('error', 'Unknown error')}"
                        if attempt < self.max_retries and self.retry_failed_sources:
                            logger.warning(f"{error_msg} - Retrying (attempt {attempt + 1}/{self.max_retries})")
                            attempt += 1
                            await asyncio.sleep(1 * attempt)  # Exponential backoff
                            continue
                        else:
                            return (source_name, result, error_msg)
                    
            except asyncio.TimeoutError:
                error_msg = f"{source_name} timed out after {timeout} seconds"
                last_error = error_msg
            except Exception as e:
                error_msg = f"{source_name} failed: {str(e)}"
                last_error = error_msg
                
            if attempt < self.max_retries and self.retry_failed_sources:
                logger.warning(f"{last_error} - Retrying (attempt {attempt + 1}/{self.max_retries})")
                attempt += 1
                await asyncio.sleep(1 * attempt)  # Exponential backoff
            else:
                break
                
        return (source_name, None, last_error)
        
    def _process_task_results(self, task_results: List, source_configs: Dict[str, Dict[str, Any]], results: Dict[str, Any]) -> Dict[str, Any]:
        """Process results from parallel task execution."""
        source_names = list(source_configs.keys())
        
        for i, task_result in enumerate(task_results):
            if isinstance(task_result, Exception):
                # Task itself failed
                source_name = source_names[i] if i < len(source_names) else f"unknown_source_{i}"
                error_msg = f"{source_name} task failed: {task_result}"
                results['errors'].append(error_msg)
                results['failed_sources'].append(source_name)
                logger.error(error_msg)
            else:
                # Task completed (may have source-level error)
                source_name, result_data, error = task_result
                results = self._process_single_result(source_name, result_data, error, results)
                
        return results
        
    def _process_single_result(self, source_name: str, result_data: Any, error: Optional[str], results: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single source result."""
        # Map source names to result keys
        source_map = {
            'apollo': 'apollo_data',
            'serper': 'serper_search', 
            'playwright': 'playwright_data',
            'linkedin': 'linkedin_data',
            'job_boards': 'job_boards',
            'news': 'news_data',
            'government': 'government_data'
        }
        
        if error:
            # Source returned error
            results['errors'].append(f"{source_name}: {error}")
            results['failed_sources'].append(source_name)
            logger.warning(f"{source_name} source failed: {error}")
        else:
            # Success
            result_key = source_map.get(source_name, f"{source_name}_data")
            results[result_key] = result_data
            results['successful_sources'].append(source_name)
            logger.info(f"{source_name} source succeeded")
            
        return results
        
    def _add_summary_insights(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Add summary insights and metrics to results."""
        # Add summary metrics
        results['successful_sources_count'] = len(results['successful_sources'])
        results['failed_sources_count'] = len(results['failed_sources'])
        results['total_sources'] = len(results['successful_sources']) + len(results['failed_sources'])
        results['success_rate'] = results['successful_sources_count'] / results['total_sources'] if results['total_sources'] > 0 else 0
        
        # Generate data quality insights
        results['data_quality'] = self._assess_data_quality(results)
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
        
    def _assess_data_quality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of collected data."""
        quality_score = 0
        quality_factors = []
        
        # Check for critical data sources
        critical_sources = ['apollo', 'serper', 'linkedin']
        critical_success = sum(1 for source in critical_sources if source in results['successful_sources'])
        
        if critical_success == len(critical_sources):
            quality_score += 40
            quality_factors.append("All critical sources successful")
        elif critical_success >= 2:
            quality_score += 25
            quality_factors.append("Most critical sources successful")
        else:
            quality_factors.append("Some critical sources failed")
            
        # Check for data richness
        if results['job_boards'] and results['job_boards'].get('jobs'):
            quality_score += 15
            quality_factors.append("Job market data available")
            
        if results['news_data'] and results['news_data'].get('articles'):
            quality_score += 15
            quality_factors.append("Recent news data available")
            
        if results['government_data'] and results['government_data'].get('primary_company_data'):
            quality_score += 15
            quality_factors.append("Official government data available")
            
        # Check for comprehensive coverage
        if results['success_rate'] >= 0.8:
            quality_score += 15
            quality_factors.append("High source coverage")
        elif results['success_rate'] >= 0.6:
            quality_score += 10
            quality_factors.append("Good source coverage")
            
        return {
            "score": quality_score,
            "grade": "Excellent" if quality_score >= 80 else "Good" if quality_score >= 60 else "Fair" if quality_score >= 40 else "Poor",
            "factors": quality_factors,
            "critical_sources_success": f"{critical_success}/{len(critical_sources)}"
        }
        
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on results."""
        recommendations = []
        
        # Check for missing critical data
        if 'apollo' in results['failed_sources']:
            recommendations.append("Consider verifying Apollo.io API key for enhanced contact data")
            
        if 'linkedin' in results['failed_sources']:
            recommendations.append("LinkedIn data collection failed - consider reviewing authentication")
            
        if results['success_rate'] < 0.5:
            recommendations.append("Low success rate - review API configurations and network connectivity")
            
        # Suggest improvements based on available data
        if not results.get('job_boards') or not results['job_boards'].get('jobs'):
            recommendations.append("Job market intelligence could be enhanced with proper job board credentials")
            
        if not results.get('news_data') or not results['news_data'].get('articles'):
            recommendations.append("News monitoring could be improved with NewsAPI or other news service keys")
            
        if len(recommendations) == 0:
            recommendations.append("Data collection appears comprehensive - no immediate improvements needed")
            
        return recommendations
        
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
        
    async def close_all_sources(self):
        """Close all data source connections."""
        try:
            await asyncio.gather(
                self.apollo_source.close(),
                self.serper_source.close(),
                self.playwright_source.close(),
                self.linkedin_source.close(),
                self.job_boards_source.close(),
                self.news_source.close(),
                self.government_source.close(),
                return_exceptions=True
            )
            logger.info("All data source connections closed")
        except Exception as e:
            logger.error(f"Error closing data sources: {e}")
            
    async def test_all_sources(self, test_company: str = "TestCorp") -> Dict[str, Any]:
        """Test all data sources with a test company."""
        logger.info(f"Testing all data sources with {test_company}")
        
        test_results = await self.collect_all_prospect_data(test_company, research_mode="quick")
        
        # Add test-specific analysis
        test_results['test_summary'] = {
            'test_company': test_company,
            'sources_tested': test_results['total_sources'],
            'sources_working': test_results['successful_sources_count'],
            'test_passed': test_results['success_rate'] >= 0.6,
            'configuration_issues': [error for error in test_results['errors'] if 'api' in error.lower() or 'key' in error.lower()]
        }
        
        return test_results
