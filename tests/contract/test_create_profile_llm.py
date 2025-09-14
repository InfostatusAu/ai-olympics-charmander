"""Contract tests for enhanced create_profile tool with LLM integration.

These tests MUST FAIL initially (TDD requirement) and validate the enhanced
create_profile MCP tool functionality with AI-generated conversation strategies
and personalized recommendations.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from src.mcp_server.tools import create_profile
from src.prospect_research.profile import create_profile as profile_func


class TestEnhancedCreateProfileContract:
    """Contract tests for enhanced create_profile tool."""

    @pytest.fixture
    def mock_research_data(self):
        """Mock comprehensive research data for testing."""
        return {
            'company_background': 'AI-enhanced comprehensive background analysis',
            'business_model': 'SaaS platform with enterprise focus',
            'technology_stack': ['Python', 'React', 'AWS', 'PostgreSQL'],
            'pain_points': ['Manual data processing', 'Scalability challenges', 'Integration complexity'],
            'recent_developments': ['Series B funding', 'New CTO hire', 'Product expansion'],
            'decision_makers': ['John Smith (CTO)', 'Jane Doe (VP Engineering)'],
            'enhancement_status': 'ai_enhanced',
            'data_sources_summary': {
                'successful_sources': 5,
                'failed_sources': 2,
                'total_sources': 7
            }
        }

    @pytest.mark.asyncio
    async def test_create_profile_with_ai_conversation_strategies(self, mock_research_data):
        """Test create_profile generates AI-powered conversation strategies.
        
        This test MUST FAIL initially as AI-generated conversation strategies
        are not yet implemented.
        """
        prospect_id = "ai_conversation_test"
        
        # Call the enhanced profile function
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until AI integration is implemented
        assert 'enhancement_status' in result, "Should track enhancement method"
        assert result['enhancement_status'] == 'ai_enhanced', "Should use AI enhancement"
        
        # Verify AI-generated conversation starters
        starters = [
            result['conversation_starter_1'],
            result['conversation_starter_2'], 
            result['conversation_starter_3']
        ]
        
        for starter in starters:
            assert starter != "What's driving your current business priorities?", "Should not use default manual starter"
            assert len(starter) > 20, "AI starters should be substantial"
            assert '?' in starter, "Conversation starters should be questions"
            # Should reference specific company insights
            assert any(pain in starter.lower() for pain in ['manual', 'scalability', 'integration']) or \
                   any(tech in starter.lower() for tech in ['python', 'react', 'aws']), \
                   f"Starter should reference company specifics: {starter}"

    @pytest.mark.asyncio
    async def test_create_profile_personalized_value_propositions(self, mock_research_data):
        """Test create_profile generates personalized value propositions.
        
        This test MUST FAIL initially as personalized value proposition
        generation is not yet implemented.
        """
        prospect_id = "personalized_value_test"
        
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until personalization is implemented
        assert result['value_proposition'] != "Value proposition based on manual analysis", "Should not use manual default"
        
        value_prop = result['value_proposition']
        assert len(value_prop) > 50, "Value proposition should be comprehensive"
        
        # Should reference specific company context
        company_context_found = any(keyword in value_prop.lower() for keyword in [
            'saas', 'enterprise', 'python', 'react', 'aws', 'postgresql',
            'manual data processing', 'scalability', 'integration'
        ])
        assert company_context_found, f"Value prop should reference company context: {value_prop}"

    @pytest.mark.asyncio
    async def test_create_profile_timing_recommendations(self, mock_research_data):
        """Test create_profile provides intelligent timing recommendations.
        
        This test MUST FAIL initially as intelligent timing analysis
        is not yet implemented.
        """
        prospect_id = "timing_test"
        
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until timing intelligence is implemented
        assert result['timing_recommendation'] != "Manual timing assessment", "Should not use manual default"
        
        timing = result['timing_recommendation']
        assert len(timing) > 30, "Timing recommendation should be detailed"
        
        # Should reference recent developments or business cycles
        timing_context_found = any(keyword in timing.lower() for keyword in [
            'series b', 'funding', 'new cto', 'expansion', 'growth', 'recent', 'now', 'currently'
        ])
        assert timing_context_found, f"Timing should reference business context: {timing}"

    @pytest.mark.asyncio
    async def test_create_profile_intelligent_talking_points(self, mock_research_data):
        """Test create_profile generates intelligent talking points.
        
        This test MUST FAIL initially as intelligent talking point
        generation is not yet implemented.
        """
        prospect_id = "talking_points_test"
        
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until intelligent generation is implemented
        talking_points = result['talking_points']
        assert len(talking_points) > 2, "Should have multiple talking points"
        assert talking_points != ["Manual talking point 1", "Manual talking point 2"], "Should not use manual defaults"
        
        # Each talking point should be substantial and relevant
        for point in talking_points:
            assert len(point) > 20, f"Talking point should be substantial: {point}"
            
        # Should cover different aspects of the company
        all_points = ' '.join(talking_points).lower()
        coverage_found = any(aspect in all_points for aspect in [
            'technology', 'business', 'growth', 'challenge', 'opportunity', 'solution'
        ])
        assert coverage_found, f"Talking points should cover business aspects: {talking_points}"

    @pytest.mark.asyncio
    async def test_create_profile_objection_handling_strategies(self, mock_research_data):
        """Test create_profile provides intelligent objection handling.
        
        This test MUST FAIL initially as intelligent objection handling
        generation is not yet implemented.
        """
        prospect_id = "objection_handling_test"
        
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until objection handling is implemented
        objections = result['objection_handling']
        assert len(objections) > 1, "Should have multiple objection responses"
        assert objections != ["Manual objection response 1", "Manual objection response 2"], "Should not use manual defaults"
        
        # Each objection response should be substantial
        for response in objections:
            assert len(response) > 30, f"Objection response should be detailed: {response}"
            
        # Should address common objections intelligently
        all_responses = ' '.join(objections).lower()
        objection_themes = ['cost', 'time', 'complexity', 'risk', 'integration', 'security']
        theme_addressed = any(theme in all_responses for theme in objection_themes)
        assert theme_addressed, f"Should address common objection themes: {objections}"

    @pytest.mark.asyncio
    async def test_create_profile_llm_fallback_mechanism(self, mock_research_data):
        """Test create_profile graceful fallback when LLM fails.
        
        This test MUST FAIL initially as fallback mechanism in profile
        function is not yet implemented.
        """
        prospect_id = "fallback_test"
        
        # Mock LLM failure
        with patch('src.llm_enhancer.middleware.LLMMiddleware.enhance_profile_strategy',
                  side_effect=Exception("LLM service unavailable")):
            
            result = await profile_func(prospect_id, mock_research_data)
            
            # These assertions MUST FAIL until fallback is implemented
            assert 'enhancement_status' in result, "Should track enhancement method"
            assert result['enhancement_status'] == 'manual_fallback', "Should use manual fallback"
            assert 'fallback_reason' in result, "Should explain fallback reason"
            
            # Should still produce usable content
            assert result['conversation_starter_1'] is not None, "Should have starter 1 in fallback"
            assert result['conversation_starter_2'] is not None, "Should have starter 2 in fallback"
            assert result['conversation_starter_3'] is not None, "Should have starter 3 in fallback"
            assert result['value_proposition'] is not None, "Should have value prop in fallback"

    @pytest.mark.asyncio
    async def test_create_profile_mcp_tool_integration(self, mock_research_data):
        """Test create_profile MCP tool calls enhanced profile function.
        
        This test MUST FAIL initially as MCP tool integration with enhanced
        profile logic is not yet implemented.
        """
        # Mock MCP tool arguments
        arguments = {
            "prospect_id": "mcp_integration_test",
            "research_data": mock_research_data
        }
        
        # Call MCP tool function
        result = await create_profile(arguments)
        
        # These assertions MUST FAIL until MCP integration is updated
        assert result['success'] is True, "MCP tool should succeed"
        assert 'profile_file' in result, "Should return profile file path"
        assert 'prospect_id' in result, "Should return prospect ID"
        
        # Verify enhanced content is passed through
        assert 'enhancement_metadata' in result, "Should include enhancement metadata"
        metadata = result['enhancement_metadata']
        assert 'enhancement_method' in metadata, "Should track enhancement method"
        assert 'conversation_quality_score' in metadata, "Should track conversation quality"

    @pytest.mark.asyncio
    async def test_create_profile_performance_requirements(self, mock_research_data):
        """Test create_profile meets performance requirements.
        
        This test MUST FAIL initially as performance optimization for
        LLM-enhanced profile generation is not implemented.
        """
        import time
        prospect_id = "performance_test"
        
        start_time = time.time()
        result = await profile_func(prospect_id, mock_research_data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Performance requirement: <10 seconds for profile generation
        # This WILL FAIL until optimization is implemented
        assert execution_time < 10, f"Profile creation took {execution_time}s, should be under 10s"
        
        # Verify quality wasn't sacrificed for speed
        assert result['enhancement_status'] in ['ai_enhanced', 'manual_fallback'], "Should have proper enhancement"
        assert len(result['conversation_starter_1']) > 20, "Should maintain quality despite speed requirement"

    @pytest.mark.asyncio
    async def test_create_profile_business_cycle_awareness(self, mock_research_data):
        """Test create_profile considers business cycles and timing.
        
        This test MUST FAIL initially as business cycle awareness
        in profile generation is not yet implemented.
        """
        # Add business cycle context to research data
        research_with_cycles = {
            **mock_research_data,
            'recent_developments': ['Q4 planning phase', 'Budget reviews starting', 'New fiscal year'],
            'business_context': {
                'quarterly_cycle': 'Q4',
                'budget_season': True,
                'planning_phase': True
            }
        }
        
        prospect_id = "business_cycle_test"
        result = await profile_func(prospect_id, research_with_cycles)
        
        # These assertions MUST FAIL until business cycle awareness is implemented
        assert 'business_cycle_analysis' in result, "Should include business cycle analysis"
        
        timing = result['timing_recommendation']
        cycle_awareness = any(keyword in timing.lower() for keyword in [
            'q4', 'quarter', 'budget', 'planning', 'fiscal', 'year-end'
        ])
        assert cycle_awareness, f"Timing should consider business cycles: {timing}"

    @pytest.mark.asyncio
    async def test_create_profile_decision_maker_personalization(self, mock_research_data):
        """Test create_profile personalizes for specific decision makers.
        
        This test MUST FAIL initially as decision maker personalization
        is not yet implemented.
        """
        prospect_id = "decision_maker_test"
        
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until decision maker personalization is implemented
        assert 'decision_maker_insights' in result, "Should include decision maker insights"
        
        # Should reference specific decision makers from research data
        profile_content = f"{result['conversation_starter_1']} {result['value_proposition']}".lower()
        decision_maker_referenced = any(name.lower() in profile_content for name in ['john smith', 'jane doe', 'cto', 'vp engineering'])
        assert decision_maker_referenced, "Should reference specific decision makers"

    @pytest.mark.asyncio
    async def test_create_profile_template_compatibility(self, mock_research_data):
        """Test create_profile output is compatible with existing templates.
        
        This test MUST FAIL initially as template compatibility with enhanced
        profile structure is not yet implemented.
        """
        prospect_id = "template_compatibility_test"
        
        result = await profile_func(prospect_id, mock_research_data)
        
        # These assertions MUST FAIL until template compatibility is ensured
        required_fields = [
            'conversation_starter_1',
            'conversation_starter_2',
            'conversation_starter_3',
            'value_proposition',
            'timing_recommendation',
            'talking_points',
            'objection_handling'
        ]
        
        for field in required_fields:
            assert field in result, f"Missing required template field: {field}"
            assert result[field] is not None, f"Template field {field} should not be None"
        
        # Verify field types for template compatibility
        assert isinstance(result['talking_points'], list), "Talking points should be list"
        assert isinstance(result['objection_handling'], list), "Objection handling should be list"
        
        # Verify conversation starters are strings
        for i in range(1, 4):
            starter_key = f'conversation_starter_{i}'
            assert isinstance(result[starter_key], str), f"{starter_key} should be string"
            assert len(result[starter_key]) > 0, f"{starter_key} should not be empty"
