"""Unit tests for LLM analyzers module."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any

from src.llm_enhancer.analyzers import ResearchAnalyzer, ProfileAnalyzer


class TestResearchAnalyzer:
    """Test cases for ResearchAnalyzer class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        client = Mock()
        client.analyze_research_data = AsyncMock()
        return client
    
    @pytest.fixture
    def analyzer(self, mock_llm_client):
        """Create ResearchAnalyzer instance with mock client."""
        return ResearchAnalyzer(mock_llm_client)
    
    @pytest.fixture
    def sample_raw_data(self):
        """Sample raw data for testing."""
        return {
            'apollo_data': {'company': 'Test Company', 'employees': 100},
            'serper_data': {'news': ['Article 1', 'Article 2']},
            'linkedin_data': {'posts': ['Post 1', 'Post 2']},
            'successful_sources_count': 3,
            'failed_sources_count': 1,
            'total_sources': 7,
            'errors': ['Error in government source']
        }
    
    @pytest.fixture
    def sample_llm_analysis(self):
        """Sample LLM analysis response."""
        return {
            'analysis': {
                'background': 'AI-enhanced company background',
                'business_model': 'B2B SaaS platform',
                'tech_stack': ['Python', 'AWS', 'React'],
                'pain_points': ['Scaling issues', 'Data integration'],
                'developments': ['New product launch', 'Series B funding'],
                'decision_makers': ['CTO', 'VP Engineering']
            },
            'enhancement_status': 'ai_enhanced'
        }
    
    def test_init(self, mock_llm_client):
        """Test ResearchAnalyzer initialization."""
        analyzer = ResearchAnalyzer(mock_llm_client)
        assert analyzer.llm_client == mock_llm_client
    
    @pytest.mark.asyncio
    async def test_analyze_comprehensive_data_success(
        self, analyzer, sample_raw_data, sample_llm_analysis
    ):
        """Test successful comprehensive data analysis."""
        # Setup
        analyzer.llm_client.analyze_research_data.return_value = sample_llm_analysis
        
        # Execute
        result = await analyzer.analyze_comprehensive_data(sample_raw_data)
        
        # Verify
        assert result['company_background'] == 'AI-enhanced company background'
        assert result['business_model'] == 'B2B SaaS platform'
        assert result['technology_stack'] == ['Python', 'AWS', 'React']
        assert result['pain_points'] == ['Scaling issues', 'Data integration']
        assert result['recent_developments'] == ['New product launch', 'Series B funding']
        assert result['decision_makers'] == ['CTO', 'VP Engineering']
        assert result['enhancement_status'] == 'ai_enhanced'
        assert result['data_sources_summary']['successful_sources'] == 3
        assert result['data_sources_summary']['failed_sources'] == 1
        
        # Verify LLM client was called correctly
        analyzer.llm_client.analyze_research_data.assert_called_once_with(
            sample_raw_data, "research"
        )
    
    @pytest.mark.asyncio
    async def test_analyze_comprehensive_data_llm_failure(
        self, analyzer, sample_raw_data
    ):
        """Test analysis with LLM failure falling back to manual processing."""
        # Setup
        analyzer.llm_client.analyze_research_data.side_effect = Exception("LLM error")
        
        # Execute
        with patch('src.llm_enhancer.analyzers.logger') as mock_logger:
            result = await analyzer.analyze_comprehensive_data(sample_raw_data)
        
        # Verify fallback behavior
        assert result['company_background'] == 'Manual analysis of collected data'
        assert result['business_model'] == 'Extracted from available sources'
        assert result['enhancement_status'] == 'manual_fallback'
        assert result['data_sources_summary']['successful_sources'] == 3
        
        # Verify error was logged
        mock_logger.error.assert_called_once()
        mock_logger.info.assert_called_once_with('Using fallback manual research analysis')
    
    def test_structure_research_analysis_complete_data(self, analyzer, sample_llm_analysis, sample_raw_data):
        """Test structuring with complete LLM analysis data."""
        result = analyzer._structure_research_analysis(sample_llm_analysis, sample_raw_data)
        
        assert result['company_background'] == 'AI-enhanced company background'
        assert result['business_model'] == 'B2B SaaS platform'
        assert result['technology_stack'] == ['Python', 'AWS', 'React']
        assert result['pain_points'] == ['Scaling issues', 'Data integration']
        assert result['recent_developments'] == ['New product launch', 'Series B funding']
        assert result['decision_makers'] == ['CTO', 'VP Engineering']
        assert result['enhancement_status'] == 'ai_enhanced'
    
    def test_structure_research_analysis_partial_data(self, analyzer, sample_raw_data):
        """Test structuring with partial LLM analysis data."""
        partial_analysis = {
            'analysis': {
                'background': 'Partial background',
                'business_model': 'Partial model'
                # Missing other fields
            },
            'enhancement_status': 'partial_ai_enhanced'
        }
        
        result = analyzer._structure_research_analysis(partial_analysis, sample_raw_data)
        
        assert result['company_background'] == 'Partial background'
        assert result['business_model'] == 'Partial model'
        assert result['technology_stack'] == []  # Default empty list
        assert result['pain_points'] == []  # Default empty list
        assert result['recent_developments'] == []  # Default empty list
        assert result['decision_makers'] == []  # Default empty list
        assert result['enhancement_status'] == 'partial_ai_enhanced'
    
    def test_structure_research_analysis_empty_data(self, analyzer, sample_raw_data):
        """Test structuring with empty LLM analysis data."""
        empty_analysis = {}
        
        result = analyzer._structure_research_analysis(empty_analysis, sample_raw_data)
        
        assert result['company_background'] == 'AI-enhanced background'  # Default
        assert result['business_model'] == 'AI-analyzed business model'  # Default
        assert result['technology_stack'] == []
        assert result['pain_points'] == []
        assert result['recent_developments'] == []
        assert result['decision_makers'] == []
        assert result['enhancement_status'] == 'ai_enhanced'  # Default
    
    def test_fallback_research_analysis(self, analyzer, sample_raw_data):
        """Test fallback research analysis."""
        with patch('src.llm_enhancer.analyzers.logger') as mock_logger:
            result = analyzer._fallback_research_analysis(sample_raw_data)
        
        assert result['company_background'] == 'Manual analysis of collected data'
        assert result['business_model'] == 'Extracted from available sources'
        assert result['technology_stack'] == []
        assert result['pain_points'] == []
        assert result['recent_developments'] == []
        assert result['decision_makers'] == []
        assert result['enhancement_status'] == 'manual_fallback'
        assert result['data_sources_summary']['successful_sources'] == 3
        
        mock_logger.info.assert_called_once_with('Using fallback manual research analysis')
    
    def test_summarize_sources_complete_data(self, analyzer):
        """Test data sources summary with complete data."""
        raw_data = {
            'successful_sources_count': 5,
            'failed_sources_count': 2,
            'total_sources': 7,
            'errors': ['Error 1', 'Error 2']
        }
        
        result = analyzer._summarize_sources(raw_data)
        
        assert result['successful_sources'] == 5
        assert result['failed_sources'] == 2
        assert result['total_sources'] == 7
        assert result['errors'] == ['Error 1', 'Error 2']
    
    def test_summarize_sources_missing_data(self, analyzer):
        """Test data sources summary with missing data."""
        raw_data = {}
        
        result = analyzer._summarize_sources(raw_data)
        
        assert result['successful_sources'] == 0  # Default
        assert result['failed_sources'] == 0  # Default
        assert result['total_sources'] == 7  # Default
        assert result['errors'] == []  # Default


class TestProfileAnalyzer:
    """Test cases for ProfileAnalyzer class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        client = Mock()
        client.analyze_research_data = AsyncMock()
        return client
    
    @pytest.fixture
    def analyzer(self, mock_llm_client):
        """Create ProfileAnalyzer instance with mock client."""
        return ProfileAnalyzer(mock_llm_client)
    
    @pytest.fixture
    def sample_research_data(self):
        """Sample research data for testing."""
        return {
            'company_background': 'Technology company',
            'business_model': 'B2B SaaS',
            'technology_stack': ['Python', 'AWS'],
            'pain_points': ['Scaling issues'],
            'recent_developments': ['Product launch'],
            'decision_makers': ['CTO'],
            'enhancement_status': 'ai_enhanced'
        }
    
    @pytest.fixture
    def sample_llm_strategy(self):
        """Sample LLM strategy response."""
        return {
            'analysis': {
                'conversation_starters': [
                    'How is your team handling scaling challenges?',
                    'What\'s your current approach to cloud infrastructure?',
                    'How are you evaluating new technology solutions?'
                ],
                'value_proposition': 'Streamlined scaling solutions for growing tech teams',
                'timing': 'Best to reach out during Q1 planning cycles',
                'talking_points': [
                    'Cost optimization opportunities',
                    'Team productivity improvements',
                    'Security compliance benefits'
                ],
                'objection_handling': [
                    'Address budget concerns with ROI metrics',
                    'Provide case studies for technical doubts'
                ]
            },
            'enhancement_status': 'ai_enhanced'
        }
    
    def test_init(self, mock_llm_client):
        """Test ProfileAnalyzer initialization."""
        analyzer = ProfileAnalyzer(mock_llm_client)
        assert analyzer.llm_client == mock_llm_client
    
    @pytest.mark.asyncio
    async def test_generate_strategy_success(
        self, analyzer, sample_research_data, sample_llm_strategy
    ):
        """Test successful strategy generation."""
        # Setup
        analyzer.llm_client.analyze_research_data.return_value = sample_llm_strategy
        
        # Execute
        result = await analyzer.generate_strategy(sample_research_data)
        
        # Verify
        assert result['conversation_starter_1'] == 'How is your team handling scaling challenges?'
        assert result['conversation_starter_2'] == 'What\'s your current approach to cloud infrastructure?'
        assert result['conversation_starter_3'] == 'How are you evaluating new technology solutions?'
        assert result['value_proposition'] == 'Streamlined scaling solutions for growing tech teams'
        assert result['timing_recommendation'] == 'Best to reach out during Q1 planning cycles'
        assert len(result['talking_points']) == 3
        assert len(result['objection_handling']) == 2
        assert result['enhancement_status'] == 'ai_enhanced'
        
        # Verify LLM client was called correctly
        analyzer.llm_client.analyze_research_data.assert_called_once_with(
            sample_research_data, "profile"
        )
    
    @pytest.mark.asyncio
    async def test_generate_strategy_llm_failure(
        self, analyzer, sample_research_data
    ):
        """Test strategy generation with LLM failure falling back to manual."""
        # Setup
        analyzer.llm_client.analyze_research_data.side_effect = Exception("LLM error")
        
        # Execute
        with patch('src.llm_enhancer.analyzers.logger') as mock_logger:
            result = await analyzer.generate_strategy(sample_research_data)
        
        # Verify fallback behavior
        assert result['conversation_starter_1'] == 'What\'s driving your current business priorities?'
        assert result['conversation_starter_2'] == 'How are you approaching your technology roadmap?'
        assert result['conversation_starter_3'] == 'What challenges are you facing in your current setup?'
        assert result['value_proposition'] == 'Manual value proposition based on research'
        assert result['timing_recommendation'] == 'Manual timing assessment'
        assert result['enhancement_status'] == 'manual_fallback'
        
        # Verify error was logged
        mock_logger.error.assert_called_once()
        mock_logger.info.assert_called_once_with('Using fallback manual profile strategy')
    
    def test_structure_profile_strategy_complete_data(self, analyzer, sample_llm_strategy, sample_research_data):
        """Test structuring with complete LLM strategy data."""
        result = analyzer._structure_profile_strategy(sample_llm_strategy, sample_research_data)
        
        assert result['conversation_starter_1'] == 'How is your team handling scaling challenges?'
        assert result['conversation_starter_2'] == 'What\'s your current approach to cloud infrastructure?'
        assert result['conversation_starter_3'] == 'How are you evaluating new technology solutions?'
        assert result['value_proposition'] == 'Streamlined scaling solutions for growing tech teams'
        assert result['timing_recommendation'] == 'Best to reach out during Q1 planning cycles'
        assert result['talking_points'] == [
            'Cost optimization opportunities',
            'Team productivity improvements', 
            'Security compliance benefits'
        ]
        assert result['objection_handling'] == [
            'Address budget concerns with ROI metrics',
            'Provide case studies for technical doubts'
        ]
        assert result['enhancement_status'] == 'ai_enhanced'
    
    def test_structure_profile_strategy_partial_data(self, analyzer, sample_research_data):
        """Test structuring with partial LLM strategy data."""
        partial_strategy = {
            'analysis': {
                'conversation_starters': ['Single starter'],
                'value_proposition': 'Partial value prop'
                # Missing other fields
            },
            'enhancement_status': 'partial_ai_enhanced'
        }
        
        result = analyzer._structure_profile_strategy(partial_strategy, sample_research_data)
        
        assert result['conversation_starter_1'] == 'Single starter'
        assert result['conversation_starter_2'] == 'AI-generated fallback'  # Fallback for missing
        assert result['conversation_starter_3'] == 'AI-generated fallback'  # Fallback for missing
        assert result['value_proposition'] == 'Partial value prop'
        assert result['timing_recommendation'] == 'AI-recommended timing'  # Default
        assert result['talking_points'] == []  # Default empty list
        assert result['objection_handling'] == []  # Default empty list
        assert result['enhancement_status'] == 'partial_ai_enhanced'
    
    def test_structure_profile_strategy_empty_data(self, analyzer, sample_research_data):
        """Test structuring with empty LLM strategy data."""
        empty_strategy = {}
        
        result = analyzer._structure_profile_strategy(empty_strategy, sample_research_data)
        
        assert result['conversation_starter_1'] == 'AI-generated starter'  # Default
        assert result['conversation_starter_2'] == 'AI-generated fallback'  # Default
        assert result['conversation_starter_3'] == 'AI-generated fallback'  # Default
        assert result['value_proposition'] == 'AI-aligned value proposition'  # Default
        assert result['timing_recommendation'] == 'AI-recommended timing'  # Default
        assert result['talking_points'] == []
        assert result['objection_handling'] == []
        assert result['enhancement_status'] == 'ai_enhanced'  # Default
    
    def test_structure_profile_strategy_no_conversation_starters(self, analyzer, sample_research_data):
        """Test structuring with no conversation starters."""
        strategy_no_starters = {
            'analysis': {
                'conversation_starters': [],
                'value_proposition': 'Test value prop'
            }
        }
        
        result = analyzer._structure_profile_strategy(strategy_no_starters, sample_research_data)
        
        assert result['conversation_starter_1'] == 'AI-generated starter'  # Default fallback
        assert result['conversation_starter_2'] == 'AI-generated fallback'
        assert result['conversation_starter_3'] == 'AI-generated fallback'
    
    def test_fallback_profile_strategy(self, analyzer, sample_research_data):
        """Test fallback profile strategy."""
        with patch('src.llm_enhancer.analyzers.logger') as mock_logger:
            result = analyzer._fallback_profile_strategy(sample_research_data)
        
        assert result['conversation_starter_1'] == 'What\'s driving your current business priorities?'
        assert result['conversation_starter_2'] == 'How are you approaching your technology roadmap?'
        assert result['conversation_starter_3'] == 'What challenges are you facing in your current setup?'
        assert result['value_proposition'] == 'Manual value proposition based on research'
        assert result['timing_recommendation'] == 'Manual timing assessment'
        assert result['talking_points'] == ['Manual talking point 1', 'Manual talking point 2']
        assert result['objection_handling'] == ['Manual objection response']
        assert result['enhancement_status'] == 'manual_fallback'
        
        mock_logger.info.assert_called_once_with('Using fallback manual profile strategy')


class TestAnalyzersIntegration:
    """Integration tests for analyzer components."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client for integration tests."""
        client = Mock()
        client.analyze_research_data = AsyncMock()
        return client
    
    @pytest.fixture
    def research_analyzer(self, mock_llm_client):
        """Create ResearchAnalyzer for integration tests."""
        return ResearchAnalyzer(mock_llm_client)
    
    @pytest.fixture
    def profile_analyzer(self, mock_llm_client):
        """Create ProfileAnalyzer for integration tests."""
        return ProfileAnalyzer(mock_llm_client)
    
    @pytest.mark.asyncio
    async def test_full_analysis_pipeline(
        self, research_analyzer, profile_analyzer, mock_llm_client
    ):
        """Test full analysis pipeline from raw data to profile strategy."""
        # Setup raw data
        raw_data = {
            'apollo_data': {'company': 'TechCorp', 'employees': 500},
            'serper_data': {'news': ['Funding announcement', 'Product launch']},
            'successful_sources_count': 2,
            'failed_sources_count': 0,
            'total_sources': 7
        }
        
        # Setup LLM responses
        research_response = {
            'analysis': {
                'background': 'Growing tech company',
                'business_model': 'Enterprise software',
                'tech_stack': ['Java', 'AWS'],
                'pain_points': ['Legacy system migration'],
                'developments': ['Series C funding'],
                'decision_makers': ['CTO', 'Head of Engineering']
            },
            'enhancement_status': 'ai_enhanced'
        }
        
        profile_response = {
            'analysis': {
                'conversation_starters': [
                    'How is your legacy migration progressing?',
                    'What are your priorities for the new funding?'
                ],
                'value_proposition': 'Accelerated migration with minimal downtime',
                'timing': 'Post-funding implementation phase',
                'talking_points': ['Migration expertise', 'Proven track record'],
                'objection_handling': ['Address timeline concerns']
            },
            'enhancement_status': 'ai_enhanced'
        }
        
        # Configure mock to return different responses for different calls
        mock_llm_client.analyze_research_data.side_effect = [research_response, profile_response]
        
        # Execute pipeline
        research_analysis = await research_analyzer.analyze_comprehensive_data(raw_data)
        profile_strategy = await profile_analyzer.generate_strategy(research_analysis)
        
        # Verify research analysis
        assert research_analysis['company_background'] == 'Growing tech company'
        assert research_analysis['business_model'] == 'Enterprise software'
        assert research_analysis['enhancement_status'] == 'ai_enhanced'
        
        # Verify profile strategy
        assert profile_strategy['conversation_starter_1'] == 'How is your legacy migration progressing?'
        assert profile_strategy['value_proposition'] == 'Accelerated migration with minimal downtime'
        assert profile_strategy['enhancement_status'] == 'ai_enhanced'
        
        # Verify LLM client called correctly for both phases
        assert mock_llm_client.analyze_research_data.call_count == 2
        calls = mock_llm_client.analyze_research_data.call_args_list
        
        # First call for research analysis
        assert calls[0][0][0] == raw_data
        assert calls[0][0][1] == "research"
        
        # Second call for profile strategy
        assert calls[1][0][0] == research_analysis
        assert calls[1][0][1] == "profile"
    
    @pytest.mark.asyncio
    async def test_pipeline_with_research_failure_profile_success(
        self, research_analyzer, profile_analyzer, mock_llm_client
    ):
        """Test pipeline where research analysis fails but profile generation succeeds."""
        raw_data = {'test': 'data'}
        
        # Research analysis fails, profile generation succeeds
        mock_llm_client.analyze_research_data.side_effect = [
            Exception("Research LLM error"),
            {
                'analysis': {
                    'conversation_starters': ['Fallback starter'],
                    'value_proposition': 'Fallback value prop'
                },
                'enhancement_status': 'ai_enhanced'
            }
        ]
        
        # Execute pipeline
        with patch('src.llm_enhancer.analyzers.logger'):
            research_analysis = await research_analyzer.analyze_comprehensive_data(raw_data)
            profile_strategy = await profile_analyzer.generate_strategy(research_analysis)
        
        # Verify research fell back to manual
        assert research_analysis['enhancement_status'] == 'manual_fallback'
        
        # Verify profile still used LLM
        assert profile_strategy['enhancement_status'] == 'ai_enhanced'
        assert profile_strategy['conversation_starter_1'] == 'Fallback starter'
    
    @pytest.mark.asyncio
    async def test_pipeline_complete_fallback(
        self, research_analyzer, profile_analyzer, mock_llm_client
    ):
        """Test pipeline where both research and profile analysis fail."""
        raw_data = {'test': 'data'}
        
        # Both LLM calls fail
        mock_llm_client.analyze_research_data.side_effect = [
            Exception("Research LLM error"),
            Exception("Profile LLM error")
        ]
        
        # Execute pipeline
        with patch('src.llm_enhancer.analyzers.logger'):
            research_analysis = await research_analyzer.analyze_comprehensive_data(raw_data)
            profile_strategy = await profile_analyzer.generate_strategy(research_analysis)
        
        # Verify both fell back to manual
        assert research_analysis['enhancement_status'] == 'manual_fallback'
        assert profile_strategy['enhancement_status'] == 'manual_fallback'
        
        # Verify manual fallback content
        assert research_analysis['company_background'] == 'Manual analysis of collected data'
        assert profile_strategy['conversation_starter_1'] == 'What\'s driving your current business priorities?'
