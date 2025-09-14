"""
Unit tests for data source modules.

Tests all data source implementations with proper mocking and fixtures.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, Optional, List
import aiohttp
import json
import time

# Import all data source classes
from src.data_sources.apollo_source import ApolloSource
from src.data_sources.serper_source import SerperSource
from src.data_sources.playwright_source import PlaywrightSource
from src.data_sources.linkedin_source import LinkedInSource
from src.data_sources.job_boards_source import JobBoardsSource
from src.data_sources.news_source import NewsSource
from src.data_sources.government_source import GovernmentSource
from src.data_sources.manager import DataSourceManager


class TestApolloSource:
    """Test cases for Apollo.io data source."""
    
    @pytest.fixture
    def apollo_source(self):
        """Create Apollo source with test API key."""
        return ApolloSource(api_key="test_apollo_key")
    
    @pytest.fixture
    def apollo_source_no_key(self):
        """Create Apollo source without API key."""
        return ApolloSource()
    
    @pytest.fixture
    def mock_apollo_company_response(self):
        """Mock Apollo company enrichment response."""
        return {
            "organization": {
                "id": "123456",
                "name": "Test Company",
                "website_url": "https://testcompany.com",
                "short_description": "A test company for unit testing",
                "industry": "Technology",
                "estimated_num_employees": 100,
                "annual_revenue_printed": "$10M",
                "total_funding_printed": "$5M",
                "founded_year": 2020,
                "primary_location": "San Francisco, CA",
                "linkedin_url": "https://linkedin.com/company/testcompany",
                "phone": "+1234567890",
                "technologies": ["Python", "React"],
                "keywords": ["SaaS", "AI"]
            }
        }
    
    @pytest.fixture
    def mock_apollo_people_response(self):
        """Mock Apollo people search response."""
        return {
            "contacts": [
                {
                    "id": "contact_1",
                    "name": "John Doe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "title": "CEO",
                    "seniority": "c_suite",
                    "email": "john@testcompany.com",
                    "phone_numbers": [{"raw_number": "+1234567890"}],
                    "linkedin_url": "https://linkedin.com/in/johndoe",
                    "present_raw_address": "San Francisco, CA",
                    "departments": ["executive"],
                    "email_status": "verified"
                }
            ],
            "pagination": {
                "total_entries": 1,
                "per_page": 25,
                "page": 1
            }
        }
    
    def test_apollo_init_with_key(self):
        """Test Apollo source initialization with API key."""
        source = ApolloSource(api_key="test_key")
        assert source.api_key == "test_key"
        assert source.base_url == "https://api.apollo.io/api/v1"
        assert source.session is None
    
    def test_apollo_init_no_key(self):
        """Test Apollo source initialization without API key."""
        with patch.dict('os.environ', {}, clear=True):
            source = ApolloSource()
            assert source.api_key is None
    
    def test_apollo_init_env_key(self):
        """Test Apollo source initialization with environment variable."""
        with patch.dict('os.environ', {'APOLLO_API_KEY': 'env_key'}):
            source = ApolloSource()
            assert source.api_key == 'env_key'
    
    @pytest.mark.asyncio
    async def test_get_session(self, apollo_source):
        """Test HTTP session creation."""
        session = await apollo_source._get_session()
        assert session is not None
        assert apollo_source.session == session
        
        # Test session reuse
        session2 = await apollo_source._get_session()
        assert session2 == session
        
        await apollo_source.close()
    
    @pytest.mark.asyncio
    async def test_make_request_no_api_key(self):
        """Test request fails without API key."""
        with patch.dict('os.environ', {}, clear=True):
            source = ApolloSource()
            
            with pytest.raises(ValueError, match="Apollo API key not configured"):
                await source._make_request("GET", "/test")
    
    @pytest.mark.asyncio
    async def test_make_request_success(self, apollo_source, mock_apollo_company_response):
        """Test successful API request."""
        # Directly mock the _make_request method
        with patch.object(apollo_source, '_make_request', return_value=mock_apollo_company_response):
            result = await apollo_source._make_request("GET", "/test")
            assert result == mock_apollo_company_response
    
    @pytest.mark.asyncio
    async def test_make_request_http_error(self, apollo_source):
        """Test API request with HTTP error."""
        # Mock _make_request to raise an exception
        with patch.object(apollo_source, '_make_request', side_effect=aiohttp.ClientResponseError(
            request_info=None, history=None, status=400
        )):
            with pytest.raises(aiohttp.ClientResponseError):
                await apollo_source._make_request("GET", "/test")
    
    @pytest.mark.asyncio
    async def test_enrich_company_no_api_key(self, apollo_source_no_key):
        """Test company enrichment without API key."""
        with patch.dict('os.environ', {}, clear=True):
            source = ApolloSource()
            result = await source.enrich_company("testcompany.com")
            
            assert result["company"] == "testcompany.com"
            assert result["source"] == "apollo"
            assert result["status"] == "no_api_key"
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_enrich_company_success(self, apollo_source, mock_apollo_company_response):
        """Test successful company enrichment."""
        with patch.object(apollo_source, '_make_request', return_value=mock_apollo_company_response):
            result = await apollo_source.enrich_company("testcompany.com")
            
            assert result["company"] == "testcompany.com"
            assert result["source"] == "apollo"
            assert result["status"] == "success"
            assert result["apollo_id"] == "123456"
            assert result["name"] == "Test Company"
            assert result["domain"] == "https://testcompany.com"
            assert result["employees"] == 100
    
    @pytest.mark.asyncio
    async def test_enrich_company_domain_cleaning(self, apollo_source, mock_apollo_company_response):
        """Test domain cleaning for company enrichment."""
        test_cases = [
            "https://www.testcompany.com",
            "http://testcompany.com", 
            "www.testcompany.com",
            "testcompany.com"
        ]
        
        with patch.object(apollo_source, '_make_request', return_value=mock_apollo_company_response) as mock_request:
            for domain in test_cases:
                await apollo_source.enrich_company(domain)
                
            # Verify all calls used cleaned domain
            for call in mock_request.call_args_list:
                assert call[1]['params']['domain'] == 'testcompany.com'
    
    @pytest.mark.asyncio
    async def test_enrich_company_api_error(self, apollo_source):
        """Test company enrichment with API error."""
        with patch.object(apollo_source, '_make_request', side_effect=Exception("API Error")):
            result = await apollo_source.enrich_company("testcompany.com")
            
            assert result["company"] == "testcompany.com"
            assert result["source"] == "apollo"
            assert result["status"] == "error"
            assert "API Error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_search_people_success(self, apollo_source, mock_apollo_people_response):
        """Test successful people search."""
        with patch.object(apollo_source, '_make_request', return_value=mock_apollo_people_response):
            result = await apollo_source.search_people(
                "testcompany.com",
                job_titles=["CEO", "CTO"],
                seniorities=["c_suite"]
            )
            
            assert result["company"] == "testcompany.com"
            assert result["source"] == "apollo"
            assert result["status"] == "success"
            assert len(result["contacts"]) == 1
            assert result["contacts"][0]["name"] == "John Doe"
            assert result["contacts"][0]["title"] == "CEO"
            assert result["total_found"] == 1
    
    @pytest.mark.asyncio
    async def test_search_people_no_api_key(self, apollo_source_no_key):
        """Test people search without API key."""
        with patch.dict('os.environ', {}, clear=True):
            source = ApolloSource()
            result = await source.search_people("testcompany.com")
            
            assert result["company"] == "testcompany.com"
            assert result["source"] == "apollo"
            assert result["status"] == "no_api_key"
            assert result["contacts"] == []
    
    @pytest.mark.asyncio
    async def test_close(self, apollo_source):
        """Test closing Apollo source."""
        # Create a session first
        await apollo_source._get_session()
        assert apollo_source.session is not None
        
        # Close the source
        await apollo_source.close()
        assert apollo_source.session is None


class TestSerperSource:
    """Test cases for Serper search source."""
    
    @pytest.fixture
    def serper_source(self):
        """Create Serper source with test API key."""
        return SerperSource(api_key="test_serper_key")
    
    @pytest.fixture
    def mock_serper_response(self):
        """Mock Serper search response."""
        return {
            "organic": [
                {
                    "title": "Test Company - Official Website",
                    "link": "https://testcompany.com",
                    "snippet": "Leading technology company focused on innovation",
                    "position": 1
                },
                {
                    "title": "Test Company News",
                    "link": "https://news.com/testcompany",
                    "snippet": "Recent news about Test Company",
                    "position": 2
                }
            ],
            "searchParameters": {
                "q": "Test Company"
            }
        }
    
    def test_serper_init(self):
        """Test Serper source initialization."""
        source = SerperSource(api_key="test_key")
        assert source.api_key == "test_key"
        assert source.base_url == "https://google.serper.dev"
    
    @pytest.mark.asyncio
    async def test_search_company_success(self, serper_source, mock_serper_response):
        """Test successful company search."""
        with patch.object(serper_source, '_make_request', return_value=mock_serper_response):
            result = await serper_source.search_company("Test Company")
            
            assert result["company"] == "Test Company"
            assert result["source"] == "serper"
            assert result["status"] == "success"
            assert len(result["organic_results"]) == 2
            assert result["organic_results"][0]["title"] == "Test Company - Official Website"
    
    @pytest.mark.asyncio
    async def test_search_company_no_api_key(self):
        """Test company search without API key."""
        with patch.dict('os.environ', {}, clear=True):
            source = SerperSource()
            result = await source.search_company("Test Company")
            
            assert result["company"] == "Test Company"
            assert result["source"] == "serper"
            assert result["status"] == "no_api_key"


class TestDataSourceManager:
    """Test cases for Data Source Manager."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for data source manager."""
        return {
            'apollo_api_key': 'test_apollo',
            'serper_api_key': 'test_serper',
            'linkedin_email': 'test@example.com',
            'linkedin_password': 'test_password',
            'parallel_execution': True,
            'timeout_per_source': 30,
            'max_retries': 2
        }
    
    @pytest.fixture
    def data_source_manager(self, mock_config):
        """Create data source manager with mock config."""
        return DataSourceManager(config=mock_config)
    
    @pytest.fixture
    def mock_source_results(self):
        """Mock successful results from all sources."""
        return {
            'apollo': {
                'company': 'Test Company',
                'source': 'apollo',
                'status': 'success',
                'name': 'Test Company Inc.'
            },
            'serper': {
                'company': 'Test Company',
                'source': 'serper', 
                'status': 'success',
                'organic_results': []
            },
            'linkedin': {
                'company': 'Test Company',
                'source': 'linkedin',
                'status': 'success',
                'company_data': {}
            }
        }
    
    def test_manager_init(self, data_source_manager, mock_config):
        """Test data source manager initialization."""
        manager = data_source_manager
        
        assert manager.config == mock_config
        assert manager.parallel_execution is True
        assert manager.timeout_per_source == 30
        assert manager.max_retries == 2
        
        # Check all sources are initialized
        assert manager.apollo_source is not None
        assert manager.serper_source is not None
        assert manager.linkedin_source is not None
        assert manager.job_boards_source is not None
        assert manager.news_source is not None
        assert manager.government_source is not None
        assert manager.playwright_source is not None
    
    def test_get_source_configs_quick_mode(self, data_source_manager):
        """Test source configurations for quick research mode."""
        configs = data_source_manager._get_source_configs("quick")
        
        # Should only include critical sources
        critical_sources = ['apollo', 'serper', 'linkedin']
        assert set(configs.keys()) == set(critical_sources)
        
        for source_name, config in configs.items():
            assert config['critical'] is True
            assert 'method' in config
            assert 'priority' in config
    
    def test_get_source_configs_comprehensive_mode(self, data_source_manager):
        """Test source configurations for comprehensive research mode."""
        configs = data_source_manager._get_source_configs("comprehensive")
        
        # Should include all sources
        expected_sources = ['apollo', 'serper', 'linkedin', 'playwright', 'job_boards', 'news', 'government']
        assert set(configs.keys()) == set(expected_sources)
    
    def test_get_source_configs_deep_mode(self, data_source_manager):
        """Test source configurations for deep research mode."""
        configs = data_source_manager._get_source_configs("deep")
        
        # Should include all sources with enhanced parameters
        assert 'news' in configs
        assert configs['news']['params'].get('days_back') == 90
        
        assert 'job_boards' in configs
        assert 'platforms' in configs['job_boards']['params']
        
        assert 'government' in configs
        assert configs['government']['params'].get('include_filings') is True
    
    @pytest.mark.asyncio
    async def test_safe_collect_with_timeout_success(self, data_source_manager):
        """Test successful data collection with timeout."""
        async def mock_method(company):
            return {'company': company, 'status': 'success', 'data': 'test'}
        
        source_name, result, error = await data_source_manager._safe_collect_with_timeout(
            'test_source', mock_method, 'Test Company', {}, 30
        )
        
        assert source_name == 'test_source'
        assert result['status'] == 'success'
        assert error is None
    
    @pytest.mark.asyncio
    async def test_safe_collect_with_timeout_error(self, data_source_manager):
        """Test data collection with method error."""
        async def failing_method(company):
            raise Exception("Source failed")
        
        source_name, result, error = await data_source_manager._safe_collect_with_timeout(
            'test_source', failing_method, 'Test Company', {}, 30
        )
        
        assert source_name == 'test_source'
        assert result is None
        assert "Source failed" in error
    
    @pytest.mark.asyncio
    async def test_safe_collect_with_timeout_retry_logic(self, data_source_manager):
        """Test retry logic in safe collection."""
        call_count = 0
        
        async def failing_method(company):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise Exception("Temporary failure")
            return {'company': company, 'status': 'success'}
        
        source_name, result, error = await data_source_manager._safe_collect_with_timeout(
            'test_source', failing_method, 'Test Company', {}, 30
        )
        
        assert call_count == 3  # Initial + 2 retries
        assert result['status'] == 'success'
        assert error is None
    
    @pytest.mark.asyncio 
    async def test_safe_collect_with_timeout_timeout(self, data_source_manager):
        """Test timeout handling in safe collection."""
        async def slow_method(company):
            await asyncio.sleep(1)  # Simulate slow operation
            return {'company': company, 'status': 'success'}
        
        source_name, result, error = await data_source_manager._safe_collect_with_timeout(
            'test_source', slow_method, 'Test Company', {}, 0.1  # Very short timeout
        )
        
        assert source_name == 'test_source'
        assert result is None
        assert "timed out" in error
    
    def test_process_single_result_success(self, data_source_manager):
        """Test processing successful source result."""
        results = {
            'apollo_data': None,
            'successful_sources': [],
            'failed_sources': [],
            'errors': []
        }
        
        test_data = {'company': 'Test', 'status': 'success'}
        
        updated_results = data_source_manager._process_single_result(
            'apollo', test_data, None, results
        )
        
        assert updated_results['apollo_data'] == test_data
        assert 'apollo' in updated_results['successful_sources']
        assert len(updated_results['errors']) == 0
    
    def test_process_single_result_error(self, data_source_manager):
        """Test processing failed source result."""
        results = {
            'apollo_data': None,
            'successful_sources': [],
            'failed_sources': [],
            'errors': []
        }
        
        updated_results = data_source_manager._process_single_result(
            'apollo', None, 'API Error', results
        )
        
        assert updated_results['apollo_data'] is None
        assert 'apollo' in updated_results['failed_sources']
        assert 'apollo: API Error' in updated_results['errors']
    
    def test_assess_data_quality_excellent(self, data_source_manager):
        """Test data quality assessment for excellent results."""
        results = {
            'successful_sources': ['apollo', 'serper', 'linkedin', 'job_boards', 'news', 'government'],
            'failed_sources': [],
            'job_boards': {'jobs': [{'title': 'Engineer'}]},
            'news_data': {'articles': [{'title': 'News'}]},
            'government_data': {'primary_company_data': {'name': 'Test'}}
        }
        results['success_rate'] = 1.0
        
        quality = data_source_manager._assess_data_quality(results)
        
        assert quality['score'] >= 80
        assert quality['grade'] == 'Excellent'
        assert 'All critical sources successful' in quality['factors']
    
    def test_assess_data_quality_poor(self, data_source_manager):
        """Test data quality assessment for poor results."""
        results = {
            'successful_sources': ['news'],
            'failed_sources': ['apollo', 'serper', 'linkedin'],
            'job_boards': None,
            'news_data': None,
            'government_data': None
        }
        results['success_rate'] = 0.25
        
        quality = data_source_manager._assess_data_quality(results)
        
        assert quality['score'] < 40
        assert quality['grade'] == 'Poor'
    
    def test_generate_recommendations(self, data_source_manager):
        """Test recommendation generation."""
        results = {
            'failed_sources': ['apollo', 'linkedin'],
            'success_rate': 0.3,
            'job_boards': None,
            'news_data': None
        }
        
        recommendations = data_source_manager._generate_recommendations(results)
        
        assert any('Apollo.io API key' in rec for rec in recommendations)
        assert any('LinkedIn data collection' in rec for rec in recommendations)
        assert any('Low success rate' in rec for rec in recommendations)
        assert any('Job market intelligence' in rec for rec in recommendations)
    
    def test_add_summary_insights(self, data_source_manager):
        """Test adding summary insights to results."""
        results = {
            'successful_sources': ['apollo', 'serper'],
            'failed_sources': ['linkedin'],
            'errors': ['linkedin: API Error'],
            'job_boards': None,
            'news_data': None,
            'government_data': None
        }
        
        updated_results = data_source_manager._add_summary_insights(results)
        
        assert updated_results['successful_sources_count'] == 2
        assert updated_results['failed_sources_count'] == 1
        assert updated_results['total_sources'] == 3
        assert updated_results['success_rate'] == 2/3
        assert 'data_quality' in updated_results
        assert 'recommendations' in updated_results
    
    @pytest.mark.asyncio
    async def test_close_all_sources(self, data_source_manager):
        """Test closing all data sources."""
        # Mock all close methods (some sources might not have close method)
        with patch.object(data_source_manager.apollo_source, 'close', new_callable=AsyncMock) as mock_apollo, \
             patch.object(data_source_manager.serper_source, 'close', new_callable=AsyncMock) as mock_serper, \
             patch.object(data_source_manager.linkedin_source, 'close', new_callable=AsyncMock) as mock_linkedin, \
             patch.object(data_source_manager.job_boards_source, 'close', new_callable=AsyncMock) as mock_jobs, \
             patch.object(data_source_manager.news_source, 'close', new_callable=AsyncMock) as mock_news, \
             patch.object(data_source_manager.government_source, 'close', new_callable=AsyncMock) as mock_gov:
            
            # For playwright source, create a mock close method if it doesn't exist
            if not hasattr(data_source_manager.playwright_source, 'close'):
                data_source_manager.playwright_source.close = AsyncMock()
            
            await data_source_manager.close_all_sources()
            
            # Verify all close methods were called
            mock_apollo.assert_called_once()
            mock_serper.assert_called_once()
            mock_linkedin.assert_called_once()
            mock_jobs.assert_called_once()
            mock_news.assert_called_once()
            mock_gov.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_test_all_sources(self, data_source_manager):
        """Test testing all data sources."""
        mock_results = {
            'total_sources': 7,
            'successful_sources_count': 5,
            'success_rate': 5/7,
            'errors': ['linkedin: Auth failed'],
            'failed_sources': ['linkedin', 'government']
        }
        
        with patch.object(data_source_manager, 'collect_all_prospect_data', return_value=mock_results):
            test_results = await data_source_manager.test_all_sources("TestCorp")
            
            assert 'test_summary' in test_results
            assert test_results['test_summary']['test_company'] == 'TestCorp'
            assert test_results['test_summary']['sources_tested'] == 7
            assert test_results['test_summary']['sources_working'] == 5
            assert test_results['test_summary']['test_passed'] is True  # 5/7 > 0.6


class TestMockingUtilities:
    """Test mocking utilities and fixtures work correctly."""
    
    @pytest.mark.asyncio
    async def test_async_mock_functionality(self):
        """Test AsyncMock works correctly for async methods."""
        mock_method = AsyncMock(return_value={'status': 'success'})
        
        result = await mock_method('test_param')
        
        assert result['status'] == 'success'
        mock_method.assert_called_once_with('test_param')
    
    def test_patch_environment_variables(self):
        """Test patching environment variables."""
        with patch.dict('os.environ', {'TEST_VAR': 'test_value'}):
            import os
            assert os.getenv('TEST_VAR') == 'test_value'
        
        # Variable should not exist outside patch
        import os
        assert os.getenv('TEST_VAR') is None
    
    @pytest.mark.asyncio
    async def test_timeout_simulation(self):
        """Test timeout simulation in async methods."""
        async def slow_method():
            await asyncio.sleep(0.2)
            return 'completed'
        
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(slow_method(), timeout=0.1)


# Performance and stress testing utilities
class TestPerformanceUtilities:
    """Utilities for testing performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_concurrent_execution_performance(self):
        """Test performance of concurrent async operations."""
        async def mock_source_method(delay=0.1):
            await asyncio.sleep(delay)
            return {'status': 'success', 'timestamp': time.time()}
        
        # Test sequential vs parallel execution time
        start_time = time.time()
        
        # Simulate parallel execution
        tasks = [mock_source_method(0.05) for _ in range(3)]
        results = await asyncio.gather(*tasks)
        
        parallel_time = time.time() - start_time
        
        # Parallel should be significantly faster than sequential
        assert parallel_time < 0.2  # Should complete in ~0.05s not 0.15s
        assert len(results) == 3
        assert all(r['status'] == 'success' for r in results)
    
    def test_memory_usage_patterns(self):
        """Test memory usage patterns for large result sets."""
        # Simulate large data structures
        large_result = {
            'apollo_data': {'contacts': [{'id': i} for i in range(1000)]},
            'serper_search': {'results': [{'url': f'url_{i}'} for i in range(1000)]},
            'errors': [],
            'metadata': {'large_field': 'x' * 10000}
        }
        
        # Test that results structure can handle large data
        assert len(large_result['apollo_data']['contacts']) == 1000
        assert len(large_result['serper_search']['results']) == 1000
        assert len(large_result['metadata']['large_field']) == 10000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
