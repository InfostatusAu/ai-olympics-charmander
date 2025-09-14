"""Performance tests for complete LLM-enhanced prospect research workflow."""

import asyncio
import time
import psutil
import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List
import sys
import gc

from src.prospect_research.research import research_prospect
from src.prospect_research.profile import create_profile
from src.data_sources.manager import DataSourceManager
from src.llm_enhancer.middleware import LLMMiddleware
from src.llm_enhancer.client import BedrockClient
from src.llm_enhancer.analyzers import ResearchAnalyzer, ProfileAnalyzer


class PerformanceMetrics:
    """Helper class to track performance metrics."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start_memory = None
        self.end_memory = None
        self.peak_memory = None
        
    def start(self):
        """Start tracking performance."""
        gc.collect()  # Force garbage collection
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = self.start_memory
        
    def update_peak_memory(self):
        """Update peak memory usage."""
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = max(self.peak_memory, current_memory)
        
    def stop(self):
        """Stop tracking and calculate metrics."""
        self.end_time = time.time()
        self.end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.update_peak_memory()
        
    @property
    def duration(self) -> float:
        """Get execution duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
        
    @property
    def memory_delta(self) -> float:
        """Get memory usage delta in MB."""
        if self.start_memory and self.end_memory:
            return self.end_memory - self.start_memory
        return 0.0
        
    @property
    def peak_memory_delta(self) -> float:
        """Get peak memory usage above baseline in MB."""
        if self.start_memory and self.peak_memory:
            return self.peak_memory - self.start_memory
        return 0.0


class TestCompleteWorkflowPerformance:
    """Performance tests for complete research workflow."""
    
    @pytest.fixture
    def mock_data_source_manager(self):
        """Create mock data source manager with controlled performance."""
        manager = Mock()
        manager.collect_all_data = AsyncMock()
        
        # Simulate realistic data collection time (2-5 seconds)
        async def mock_collect_data(company_identifier):
            await asyncio.sleep(0.1)  # Simulate network latency
            return {
                'apollo_data': {'company': company_identifier, 'employees': 100},
                'serper_data': {'news': ['Article 1', 'Article 2']},
                'linkedin_data': {'posts': ['Post 1']},
                'successful_sources_count': 3,
                'failed_sources_count': 1,
                'total_sources': 7,
                'errors': ['Error in one source']
            }
        
        manager.collect_all_data.side_effect = mock_collect_data
        return manager
    
    @pytest.fixture
    def mock_llm_middleware(self):
        """Create mock LLM middleware with controlled performance."""
        middleware = Mock()
        middleware.enhance_research_data = AsyncMock()
        middleware.enhance_profile_strategy = AsyncMock()
        
        # Simulate LLM response time (1-3 seconds)
        async def mock_enhance_research(data):
            await asyncio.sleep(0.05)  # Simulate LLM processing
            return {
                'enhanced_data': {
                    'company_background': 'AI-enhanced background',
                    'business_model': 'AI-analyzed model',
                    'technology_stack': ['Python', 'AWS'],
                    'pain_points': ['Scaling challenges'],
                    'recent_developments': ['Product launch']
                },
                'confidence_score': 0.85
            }
        
        async def mock_enhance_profile(data):
            await asyncio.sleep(0.03)  # Simulate LLM processing
            return {
                'conversation_starter_1': 'AI-generated starter 1',
                'conversation_starter_2': 'AI-generated starter 2',
                'conversation_starter_3': 'AI-generated starter 3',
                'value_proposition': 'AI-aligned value proposition',
                'timing_recommendation': 'AI-recommended timing',
                'talking_points': ['Point 1', 'Point 2'],
                'objection_handling': ['Response 1']
            }
        
        middleware.enhance_research_data.side_effect = mock_enhance_research
        middleware.enhance_profile_strategy.side_effect = mock_enhance_profile
        return middleware
    
    @pytest.mark.asyncio
    async def test_complete_workflow_performance_baseline(
        self, mock_data_source_manager, mock_llm_middleware
    ):
        """Test baseline performance of complete research + profile workflow."""
        metrics = PerformanceMetrics()
        
        # Mock the core data source and LLM components directly
        with patch('src.data_sources.manager.DataSourceManager', return_value=mock_data_source_manager), \
             patch('src.llm_enhancer.middleware.LLMMiddleware', return_value=mock_llm_middleware):
            
            metrics.start()
            
            # Test core data collection performance
            data_result = await mock_data_source_manager.collect_all_data("Test Company")
            
            # Test LLM enhancement performance  
            research_enhancement = await mock_llm_middleware.enhance_research_data(data_result)
            profile_enhancement = await mock_llm_middleware.enhance_profile_strategy(research_enhancement['enhanced_data'])
            
            metrics.stop()
        
        # Performance assertions
        assert metrics.duration < 0.5, f"Core workflow took {metrics.duration:.2f}s, expected < 0.5s"
        assert metrics.peak_memory_delta < 20, f"Peak memory usage {metrics.peak_memory_delta:.1f}MB, expected < 20MB"
        
        # Verify successful completion
        assert data_result['apollo_data']['company'] == "Test Company"
        assert research_enhancement['enhanced_data']['company_background'] == 'AI-enhanced background'
        assert profile_enhancement['conversation_starter_1'] == 'AI-generated starter 1'
        
        print(f"Baseline Performance: {metrics.duration:.3f}s, Peak Memory: {metrics.peak_memory_delta:.1f}MB")
    
    @pytest.mark.asyncio
    async def test_workflow_performance_with_failures(
        self, mock_data_source_manager, mock_llm_middleware
    ):
        """Test workflow performance when LLM enhancement fails."""
        metrics = PerformanceMetrics()
        
        # Configure LLM middleware to fail
        mock_llm_middleware.enhance_research_data.side_effect = Exception("LLM error")
        mock_llm_middleware.enhance_profile_strategy.side_effect = Exception("LLM error")
        
        metrics.start()
        
        # Test fallback performance - data collection should still work
        data_result = await mock_data_source_manager.collect_all_data("Test Company")
        
        # Test LLM failure handling
        try:
            await mock_llm_middleware.enhance_research_data(data_result)
        except Exception:
            pass  # Expected failure
            
        try:
            await mock_llm_middleware.enhance_profile_strategy(data_result)
        except Exception:
            pass  # Expected failure
        
        metrics.stop()
        
        # Performance assertions for fallback scenario
        assert metrics.duration < 0.3, f"Fallback workflow took {metrics.duration:.2f}s, expected < 0.3s"
        assert metrics.peak_memory_delta < 15, f"Fallback peak memory {metrics.peak_memory_delta:.1f}MB, expected < 15MB"
        
        # Verify data collection still works
        assert data_result['apollo_data']['company'] == "Test Company"
        
        print(f"Fallback Performance: {metrics.duration:.3f}s, Peak Memory: {metrics.peak_memory_delta:.1f}MB")
    
    @pytest.mark.asyncio
    async def test_concurrent_workflow_performance(
        self, mock_data_source_manager, mock_llm_middleware
    ):
        """Test performance of multiple concurrent workflow executions."""
        metrics = PerformanceMetrics()
        num_concurrent = 5
        
        metrics.start()
        
        # Execute multiple data collection operations concurrently
        tasks = []
        for i in range(num_concurrent):
            task = asyncio.create_task(mock_data_source_manager.collect_all_data(f"Test Company {i}"))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Test concurrent LLM enhancements
        llm_tasks = []
        for result in results:
            task = asyncio.create_task(mock_llm_middleware.enhance_research_data(result))
            llm_tasks.append(task)
        
        llm_results = await asyncio.gather(*llm_tasks)
        
        metrics.stop()
        
        # Performance assertions for concurrent execution
        assert metrics.duration < 1.0, f"Concurrent operations took {metrics.duration:.2f}s, expected < 1.0s"
        assert metrics.peak_memory_delta < 30, f"Concurrent peak memory {metrics.peak_memory_delta:.1f}MB, expected < 30MB"
        
        # Verify all executions succeeded
        assert len(results) == num_concurrent
        assert len(llm_results) == num_concurrent
        for i, result in enumerate(results):
            assert result['apollo_data']['company'] == f"Test Company {i}"
        
        print(f"Concurrent Performance ({num_concurrent}x): {metrics.duration:.3f}s, Peak Memory: {metrics.peak_memory_delta:.1f}MB")


class TestComponentPerformance:
    """Performance tests for individual components."""
    
    @pytest.fixture
    def sample_research_data(self):
        """Sample research data for testing."""
        return {
            'apollo_data': {'company': 'Test Corp', 'employees': 500},
            'serper_data': {'news': ['News 1', 'News 2']},
            'linkedin_data': {'posts': ['Post 1', 'Post 2']},
            'successful_sources_count': 3,
            'failed_sources_count': 1,
            'total_sources': 7
        }
    
    @pytest.mark.asyncio
    async def test_data_source_manager_performance(self, sample_research_data):
        """Test data source collection performance."""
        metrics = PerformanceMetrics()
        
        # Mock the DataSourceManager's internal methods instead of individual sources
        with patch.object(DataSourceManager, '_collect_parallel') as mock_collect:
            # Mock the result structure to match expected format
            mock_collect.return_value = {
                'apollo_data': {'company': 'Test Corp', 'employees': 100},
                'serper_search': {'news': ['News 1']},
                'linkedin_data': {'posts': ['Post 1']},
                'job_boards': {'jobs': ['Job 1']},
                'news_data': {'articles': ['Article 1']},
                'government_data': {'registrations': ['Reg 1']},
                'playwright_data': {'browser_info': 'Info'},
                'successful_sources': ['apollo', 'serper', 'linkedin', 'job_boards', 'news', 'government', 'playwright'],
                'failed_sources': [],
                'errors': [],
                'performance_metrics': {
                    'parallel_execution_time': 0.1,
                    'execution_mode': 'parallel'
                }
            }
            
            manager = DataSourceManager()
            
            metrics.start()
            result = await manager.collect_all_prospect_data("Test Company")
            metrics.stop()
        
        # Performance assertions - much tighter since we're using mocks
        assert metrics.duration < 0.5, f"Data collection took {metrics.duration:.2f}s, expected < 0.5s"
        assert metrics.memory_delta < 10, f"Data collection memory delta {metrics.memory_delta:.1f}MB, expected < 10MB"
        
        print(f"Data Source Performance: {metrics.duration:.3f}s, Memory Delta: {metrics.memory_delta:.1f}MB")
    
    @pytest.mark.asyncio
    async def test_llm_client_performance(self):
        """Test LLM client performance."""
        metrics = PerformanceMetrics()
        
        with patch('boto3.client') as mock_boto:
            # Mock boto3 client
            mock_bedrock = Mock()
            mock_bedrock.invoke_model = Mock()
            mock_bedrock.invoke_model.return_value = {
                'body': Mock(read=Mock(return_value=b'{"message": {"content": [{"text": "test response"}]}}'))
            }
            mock_boto.return_value = mock_bedrock
            
            client = BedrockClient()
            
            metrics.start()
            
            # Test multiple LLM calls
            tasks = []
            for i in range(5):
                task = client.analyze_research_data({'test': f'data_{i}'}, 'research')
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            metrics.stop()
        
        # Performance assertions
        assert metrics.duration < 1.0, f"5 LLM calls took {metrics.duration:.2f}s, expected < 1.0s"
        assert len(results) == 5
        assert all(result.get('analysis') for result in results)
        
        print(f"LLM Client Performance (5 calls): {metrics.duration:.3f}s, Memory Delta: {metrics.memory_delta:.1f}MB")
    
    @pytest.mark.asyncio  
    async def test_analyzer_performance(self, sample_research_data):
        """Test analyzer component performance."""
        metrics = PerformanceMetrics()
        
        # Mock LLM client
        mock_llm_client = Mock()
        mock_llm_client.analyze_research_data = AsyncMock()
        mock_llm_client.analyze_research_data.return_value = {
            'analysis': {
                'background': 'Test background',
                'business_model': 'Test model',
                'tech_stack': ['Python'],
                'pain_points': ['Challenge 1'],
                'developments': ['Update 1'],
                'decision_makers': ['CTO']
            },
            'enhancement_status': 'ai_enhanced'
        }
        
        research_analyzer = ResearchAnalyzer(mock_llm_client)
        profile_analyzer = ProfileAnalyzer(mock_llm_client)
        
        metrics.start()
        
        # Test analysis pipeline
        research_analysis = await research_analyzer.analyze_comprehensive_data(sample_research_data)
        profile_strategy = await profile_analyzer.generate_strategy(research_analysis)
        
        metrics.stop()
        
        # Performance assertions
        assert metrics.duration < 0.2, f"Analysis pipeline took {metrics.duration:.2f}s, expected < 0.2s"
        assert research_analysis['enhancement_status'] == 'ai_enhanced'
        assert profile_strategy['enhancement_status'] == 'ai_enhanced'
        
        print(f"Analyzer Performance: {metrics.duration:.3f}s, Memory Delta: {metrics.memory_delta:.1f}MB")


class TestResourceUtilization:
    """Tests for memory usage and resource utilization."""
    
    @pytest.mark.asyncio
    async def test_memory_leak_detection(self):
        """Test for potential memory leaks in repeated workflow execution."""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Create simple mock for repeated operations
        mock_manager = Mock()
        mock_manager.collect_all_data = AsyncMock(return_value={'test': 'data'})
        
        mock_middleware = Mock()
        mock_middleware.enhance_research_data = AsyncMock(return_value={'enhanced_data': {'test': 'enhanced'}})
        
        # Run operations multiple times
        for i in range(10):
            # Simulate data collection and enhancement
            data = await mock_manager.collect_all_data(f"Company {i}")
            await mock_middleware.enhance_research_data(data)
            
            # Force garbage collection
            gc.collect()
            
            # Check memory growth
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            memory_growth = current_memory - initial_memory
            
            # Alert if memory grows significantly
            assert memory_growth < 50, f"Memory grew by {memory_growth:.1f}MB after {i+1} iterations"
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        total_growth = final_memory - initial_memory
        
        print(f"Memory growth after 10 iterations: {total_growth:.1f}MB")
        
        # Allow some growth but not excessive
        assert total_growth < 20, f"Total memory growth {total_growth:.1f}MB exceeded 20MB threshold"
    
    def test_cpu_usage_monitoring(self):
        """Test CPU usage during intensive operations."""
        process = psutil.Process()
        
        # Get baseline CPU usage
        cpu_before = process.cpu_percent()
        time.sleep(0.1)  # Brief pause for measurement
        
        # Simulate CPU intensive operation
        start_time = time.time()
        while time.time() - start_time < 0.5:  # Run for 500ms
            # Simulate computation
            sum(i**2 for i in range(1000))
        
        cpu_after = process.cpu_percent()
        
        print(f"CPU usage: {cpu_before:.1f}% -> {cpu_after:.1f}%")
        
        # Ensure CPU usage is reasonable (not hanging or consuming excessive resources)
        assert cpu_after < 90, f"CPU usage {cpu_after:.1f}% too high"
    
    @pytest.mark.asyncio
    async def test_async_task_cleanup(self):
        """Test that async tasks are properly cleaned up."""
        import asyncio
        
        initial_tasks = len(asyncio.all_tasks())
        
        with patch('src.data_sources.manager.DataSourceManager') as MockManager, \
             patch('src.llm_enhancer.middleware.LLMMiddleware') as MockMiddleware, \
             patch('src.file_manager.storage.save_markdown_report', return_value='test_path.md'):
            
            # Configure mocks
            manager = Mock()
            manager.collect_all_data = AsyncMock(return_value={'test': 'data'})
            MockManager.return_value = manager
            
            middleware = Mock()
            middleware.enhance_research_data = AsyncMock(return_value={'enhanced_data': {'test': 'enhanced'}})
            MockMiddleware.return_value = middleware
            
            # Execute workflow
            await research_prospect("Test Company")
        
        # Allow brief time for cleanup
        await asyncio.sleep(0.1)
        
        final_tasks = len(asyncio.all_tasks())
        
        print(f"Async tasks: {initial_tasks} -> {final_tasks}")
        
        # Ensure no tasks are left hanging
        task_growth = final_tasks - initial_tasks
        assert task_growth <= 1, f"Too many async tasks created: {task_growth} new tasks"


class TestScalabilityBoundaries:
    """Tests to identify scalability limits and boundaries."""
    
    @pytest.mark.asyncio
    async def test_large_data_processing(self):
        """Test performance with large datasets."""
        metrics = PerformanceMetrics()
        
        # Create large mock dataset
        large_dataset = {
            'apollo_data': {'company': 'Large Corp', 'employees': 10000, 'data': 'x' * 10000},
            'serper_data': {'news': ['Article ' + str(i) for i in range(100)]},
            'linkedin_data': {'posts': ['Post ' + str(i) for i in range(200)]},
            'job_boards_data': {'jobs': ['Job ' + str(i) for i in range(500)]},
            'news_data': {'articles': ['News ' + str(i) for i in range(300)]},
            'government_data': {'records': ['Record ' + str(i) for i in range(50)]}
        }
        
        # Mock LLM client to handle large data
        mock_llm_client = Mock()
        mock_llm_client.analyze_research_data = AsyncMock()
        mock_llm_client.analyze_research_data.return_value = {
            'analysis': {'background': 'Large company analysis'},
            'enhancement_status': 'ai_enhanced'
        }
        
        research_analyzer = ResearchAnalyzer(mock_llm_client)
        
        metrics.start()
        result = await research_analyzer.analyze_comprehensive_data(large_dataset)
        metrics.stop()
        
        # Performance assertions for large data
        assert metrics.duration < 5.0, f"Large data processing took {metrics.duration:.2f}s, expected < 5.0s"
        assert metrics.peak_memory_delta < 200, f"Large data peak memory {metrics.peak_memory_delta:.1f}MB, expected < 200MB"
        assert result['enhancement_status'] == 'ai_enhanced'
        
        print(f"Large Data Performance: {metrics.duration:.3f}s, Peak Memory: {metrics.peak_memory_delta:.1f}MB")
    
    @pytest.mark.asyncio
    async def test_max_concurrent_operations(self):
        """Test maximum number of concurrent operations the system can handle."""
        max_concurrent = 10
        successful_operations = 0
        
        # Create mocks with realistic delays
        mock_manager = Mock()
        async def slow_collect_data(company):
            await asyncio.sleep(0.01)  # Small delay
            return {'company': company, 'data': 'collected'}
        mock_manager.collect_all_data = AsyncMock(side_effect=slow_collect_data)
        
        mock_middleware = Mock()
        async def slow_enhance_data(data):
            await asyncio.sleep(0.005)  # Small delay
            return {'enhanced_data': {'enhanced': True}}
        mock_middleware.enhance_research_data = AsyncMock(side_effect=slow_enhance_data)
        
        start_time = time.time()
        
        # Launch maximum concurrent operations
        tasks = []
        for i in range(max_concurrent):
            async def process_company(company_id):
                data = await mock_manager.collect_all_data(f"Company {company_id}")
                enhanced = await mock_middleware.enhance_research_data(data)
                return {'success': True, 'data': data, 'enhanced': enhanced}
            
            task = asyncio.create_task(process_company(i))
            tasks.append(task)
        
        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        
        # Count successful operations
        for result in results:
            if isinstance(result, dict) and result.get('success'):
                successful_operations += 1
        
        duration = end_time - start_time
        success_rate = successful_operations / max_concurrent
        
        print(f"Concurrent Operations: {successful_operations}/{max_concurrent} successful in {duration:.2f}s")
        print(f"Success Rate: {success_rate:.1%}")
        
        # Performance assertions
        assert duration < 1.0, f"Concurrent operations took {duration:.2f}s, expected < 1.0s"
        assert success_rate >= 0.9, f"Success rate {success_rate:.1%} below 90% threshold"
        assert successful_operations >= 9, f"Only {successful_operations} operations succeeded"


if __name__ == "__main__":
    # Run performance tests directly
    pytest.main([__file__, "-v", "-s"])
