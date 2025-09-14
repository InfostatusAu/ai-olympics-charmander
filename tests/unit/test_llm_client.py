"""
Unit tests for LLM client (AWS Bedrock wrapper).

Tests the BedrockClient class with proper mocking for AWS API calls.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock, mock_open
from typing import Dict, Any, Optional
import json
import os

# Import the LLM client
from src.llm_enhancer.client import BedrockClient


class TestBedrockClient:
    """Test cases for AWS Bedrock client wrapper."""
    
    @pytest.fixture
    def bedrock_client(self):
        """Create BedrockClient instance."""
        return BedrockClient(region="us-east-1", model_id="test-model-id")
    
    @pytest.fixture
    def bedrock_client_default(self):
        """Create BedrockClient instance with defaults."""
        return BedrockClient()
    
    @pytest.fixture
    def mock_boto3_client(self):
        """Mock boto3 bedrock-runtime client."""
        mock_client = Mock()
        mock_client.converse.return_value = {
            'output': {
                'message': {
                    'content': [{'text': 'Mock LLM response content'}]
                }
            },
            'usage': {
                'inputTokens': 100,
                'outputTokens': 50
            }
        }
        return mock_client
    
    @pytest.fixture
    def sample_raw_data(self):
        """Sample raw data for analysis."""
        return {
            'company': {
                'name': 'Test Company',
                'domain': 'testcompany.com',
                'industry': 'Technology'
            },
            'sources': ['apollo', 'serper', 'linkedin'],
            'research': {
                'apollo_data': {'employees': 100},
                'serper_search': {'results': []},
                'linkedin_data': {'company_data': {}}
            },
            'analysis': {
                'business_overview': 'Tech company focused on innovation'
            },
            'contact': {
                'name': 'John Doe',
                'title': 'CEO'
            }
        }
    
    @pytest.fixture
    def mock_prompt_files(self):
        """Mock prompt file contents."""
        return {
            'research_system_prompt.md': '# Research System Prompt\nAnalyze the research data.',
            'research_user_prompt.md': '# Research User Prompt\nCompany: {company_data}\nSources: {data_sources}\nData: {research_data}',
            'profile_system_prompt.md': '# Profile System Prompt\nGenerate a prospect profile.',
            'profile_user_prompt.md': '# Profile User Prompt\nCompany: {company_profile}\nAnalysis: {business_analysis}\nContact: {target_contact}'
        }
    
    def test_bedrock_client_init_default(self):
        """Test BedrockClient initialization with defaults."""
        client = BedrockClient()
        
        assert client.region == "ap-southeast-2"
        assert client.model_id == "apac.anthropic.claude-sonnet-4-20250514-v1:0"
        assert client.bedrock_client is None
        assert client._prompts_cache == {}
    
    def test_bedrock_client_init_custom(self, bedrock_client):
        """Test BedrockClient initialization with custom values."""
        assert bedrock_client.region == "us-east-1"
        assert bedrock_client.model_id == "test-model-id"
        assert bedrock_client.bedrock_client is None
        assert bedrock_client._prompts_cache == {}
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, bedrock_client, mock_boto3_client):
        """Test successful client initialization."""
        with patch('boto3.client', return_value=mock_boto3_client), \
             patch.object(bedrock_client, '_load_prompts', new_callable=AsyncMock) as mock_load_prompts:
            
            await bedrock_client.initialize()
            
            assert bedrock_client.bedrock_client == mock_boto3_client
            mock_load_prompts.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_initialize_boto3_import_error(self, bedrock_client):
        """Test initialization failure when boto3 is not available."""
        with patch('boto3.client', side_effect=ImportError("boto3 not available")):
            with pytest.raises(ImportError):
                await bedrock_client.initialize()
    
    @pytest.mark.asyncio
    async def test_initialize_aws_error(self, bedrock_client):
        """Test initialization failure due to AWS configuration."""
        with patch('boto3.client', side_effect=Exception("AWS credentials not configured")):
            with pytest.raises(Exception, match="AWS credentials not configured"):
                await bedrock_client.initialize()
    
    @pytest.mark.asyncio
    async def test_load_prompts_success(self, bedrock_client, mock_prompt_files):
        """Test successful prompt loading."""
        with patch('os.path.join', side_effect=lambda *args: '/'.join(args)), \
             patch('builtins.open', mock_open()) as mock_file:
            
            # Mock file reading for each prompt file
            mock_file.side_effect = [
                mock_open(read_data=content).return_value
                for content in mock_prompt_files.values()
            ]
            
            await bedrock_client._load_prompts()
            
            assert len(bedrock_client._prompts_cache) == 4
            assert 'research_system' in bedrock_client._prompts_cache
            assert 'research_user' in bedrock_client._prompts_cache
            assert 'profile_system' in bedrock_client._prompts_cache
            assert 'profile_user' in bedrock_client._prompts_cache
    
    @pytest.mark.asyncio
    async def test_load_prompts_file_not_found(self, bedrock_client):
        """Test prompt loading with missing files (fallback behavior)."""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            await bedrock_client._load_prompts()
            
            # Should have fallback prompts
            assert len(bedrock_client._prompts_cache) == 4
            for key in ['research_system', 'research_user', 'profile_system', 'profile_user']:
                assert key in bedrock_client._prompts_cache
                assert 'Please analyze the provided data' in bedrock_client._prompts_cache[key]
    
    def test_prepare_prompts_research(self, bedrock_client, sample_raw_data):
        """Test prompt preparation for research analysis."""
        # Set up mock prompts
        bedrock_client._prompts_cache = {
            'research_system': 'System prompt for research',
            'research_user': 'Company: {company_data}\nSources: {data_sources}\nData: {research_data}'
        }
        
        system_prompt, user_prompt = bedrock_client._prepare_prompts(sample_raw_data, 'research')
        
        assert system_prompt == 'System prompt for research'
        assert 'Test Company' in user_prompt
        assert 'apollo' in user_prompt
        assert 'employees' in user_prompt
    
    def test_prepare_prompts_profile(self, bedrock_client, sample_raw_data):
        """Test prompt preparation for profile analysis."""
        # Set up mock prompts
        bedrock_client._prompts_cache = {
            'profile_system': 'System prompt for profile',
            'profile_user': 'Company: {company_profile}\nAnalysis: {business_analysis}\nContact: {target_contact}'
        }
        
        system_prompt, user_prompt = bedrock_client._prepare_prompts(sample_raw_data, 'profile')
        
        assert system_prompt == 'System prompt for profile'
        assert 'Test Company' in user_prompt
        assert 'innovation' in user_prompt
        assert 'John Doe' in user_prompt
    
    def test_prepare_prompts_invalid_type(self, bedrock_client, sample_raw_data):
        """Test prompt preparation with invalid analysis type."""
        with pytest.raises(ValueError, match="Unknown analysis type"):
            bedrock_client._prepare_prompts(sample_raw_data, 'invalid_type')
    
    @pytest.mark.asyncio
    async def test_call_converse_api_success(self, bedrock_client, mock_boto3_client):
        """Test successful Bedrock Converse API call."""
        bedrock_client.bedrock_client = mock_boto3_client
        
        response = await bedrock_client._call_converse_api(
            "System prompt",
            "User prompt"
        )
        
        assert response == "Mock LLM response content"
        
        # Verify API call parameters
        mock_boto3_client.converse.assert_called_once()
        call_args = mock_boto3_client.converse.call_args
        
        assert call_args[1]['modelId'] == bedrock_client.model_id
        assert len(call_args[1]['messages']) == 1
        assert call_args[1]['messages'][0]['role'] == 'user'
        assert call_args[1]['messages'][0]['content'][0]['text'] == 'User prompt'
        assert call_args[1]['system'][0]['text'] == 'System prompt'
        assert call_args[1]['inferenceConfig']['temperature'] == 0.1
        assert call_args[1]['inferenceConfig']['maxTokens'] == 4096
        assert call_args[1]['inferenceConfig']['topP'] == 0.9
    
    @pytest.mark.asyncio
    async def test_call_converse_api_no_system_prompt(self, bedrock_client, mock_boto3_client):
        """Test Converse API call without system prompt."""
        bedrock_client.bedrock_client = mock_boto3_client
        
        response = await bedrock_client._call_converse_api("", "User prompt")
        
        assert response == "Mock LLM response content"
        
        # Verify system prompts array is empty
        call_args = mock_boto3_client.converse.call_args
        assert call_args[1]['system'] == []
    
    @pytest.mark.asyncio
    async def test_call_converse_api_error(self, bedrock_client, mock_boto3_client):
        """Test Converse API call with error."""
        bedrock_client.bedrock_client = mock_boto3_client
        mock_boto3_client.converse.side_effect = Exception("API call failed")
        
        with pytest.raises(Exception, match="API call failed"):
            await bedrock_client._call_converse_api("System prompt", "User prompt")
    
    def test_parse_llm_response_research(self, bedrock_client):
        """Test LLM response parsing for research."""
        response = "# Research Analysis\nDetailed analysis content..."
        
        result = bedrock_client._parse_llm_response(response, 'research')
        
        assert result['enhanced_content'] == response
        assert result['enhancement_status'] == 'ai_enhanced'
        assert result['source'] == 'bedrock_claude'
        assert result['format'] == 'markdown'
    
    def test_parse_llm_response_profile(self, bedrock_client):
        """Test LLM response parsing for profile."""
        response = "# Prospect Profile\nProfile content..."
        
        result = bedrock_client._parse_llm_response(response, 'profile')
        
        assert result['enhanced_content'] == response
        assert result['enhancement_status'] == 'ai_enhanced'
        assert result['source'] == 'bedrock_claude'
        assert result['format'] == 'markdown'
    
    @pytest.mark.asyncio
    async def test_analyze_research_data_success(self, bedrock_client, sample_raw_data, mock_boto3_client):
        """Test successful research data analysis."""
        # Setup mocks
        bedrock_client.bedrock_client = mock_boto3_client
        bedrock_client._prompts_cache = {
            'research_system': 'System prompt',
            'research_user': 'User prompt template: {company_data}'
        }
        
        with patch.object(bedrock_client, '_call_converse_api', return_value="Analysis result") as mock_api:
            result = await bedrock_client.analyze_research_data(sample_raw_data, 'research')
            
            assert result['enhanced_content'] == "Analysis result"
            assert result['enhancement_status'] == 'ai_enhanced'
            assert result['llm_model'] == bedrock_client.model_id
            assert result['analysis_type'] == 'research'
            mock_api.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_research_data_auto_initialize(self, bedrock_client, sample_raw_data):
        """Test research data analysis with automatic initialization."""
        with patch.object(bedrock_client, 'initialize', new_callable=AsyncMock) as mock_init, \
             patch.object(bedrock_client, '_prepare_prompts', return_value=("sys", "user")), \
             patch.object(bedrock_client, '_call_converse_api', return_value="Analysis"):
            
            result = await bedrock_client.analyze_research_data(sample_raw_data)
            
            mock_init.assert_called_once()
            assert result['enhanced_content'] == "Analysis"
    
    @pytest.mark.asyncio
    async def test_analyze_research_data_error_fallback(self, bedrock_client, sample_raw_data, mock_boto3_client):
        """Test research data analysis with error fallback."""
        bedrock_client.bedrock_client = mock_boto3_client
        
        with patch.object(bedrock_client, '_prepare_prompts', side_effect=Exception("Prompt error")):
            result = await bedrock_client.analyze_research_data(sample_raw_data)
            
            assert result['enhancement_status'] == 'error'
            assert result['fallback'] is True
            assert 'Prompt error' in result['analysis']['error']
    
    @pytest.mark.asyncio
    async def test_analyze_profile_data_success(self, bedrock_client, sample_raw_data, mock_boto3_client):
        """Test successful profile data analysis."""
        bedrock_client.bedrock_client = mock_boto3_client
        bedrock_client._prompts_cache = {
            'profile_system': 'Profile system prompt',
            'profile_user': 'Profile user prompt: {company_profile}'
        }
        
        with patch.object(bedrock_client, '_call_converse_api', return_value="Profile result") as mock_api:
            result = await bedrock_client.analyze_research_data(sample_raw_data, 'profile')
            
            assert result['enhanced_content'] == "Profile result"
            assert result['analysis_type'] == 'profile'
            mock_api.assert_called_once()


class TestBedrockClientIntegration:
    """Integration tests for BedrockClient with realistic scenarios."""
    
    @pytest.fixture
    def bedrock_client_integration(self):
        """Create BedrockClient for integration testing."""
        return BedrockClient(region="us-east-1")
    
    @pytest.fixture
    def comprehensive_raw_data(self):
        """Comprehensive raw data for integration testing."""
        return {
            'company': {
                'name': 'TechCorp Solutions',
                'domain': 'techcorp.com',
                'industry': 'Software Development',
                'employees': 150,
                'founded': 2018
            },
            'sources': ['apollo', 'serper', 'linkedin', 'news'],
            'research': {
                'apollo_data': {
                    'contacts': [
                        {'name': 'Jane Smith', 'title': 'CTO'},
                        {'name': 'Bob Wilson', 'title': 'VP Engineering'}
                    ],
                    'technologies': ['Python', 'React', 'AWS']
                },
                'serper_search': {
                    'organic_results': [
                        {'title': 'TechCorp announces new AI product', 'snippet': '...'},
                        {'title': 'TechCorp hiring 50 engineers', 'snippet': '...'}
                    ]
                },
                'linkedin_data': {
                    'company_posts': ['Recent funding round', 'Product launch'],
                    'employee_growth': '25% this year'
                },
                'news_data': {
                    'articles': [
                        {'title': 'TechCorp raises $10M Series A', 'summary': '...'}
                    ]
                }
            },
            'analysis': {
                'business_overview': 'Fast-growing software company with strong technical team',
                'key_opportunities': ['AI integration', 'Team expansion', 'Market growth']
            },
            'contact': {
                'name': 'Jane Smith',
                'title': 'CTO',
                'department': 'Engineering',
                'seniority': 'c_suite'
            }
        }
    
    @pytest.mark.asyncio
    async def test_end_to_end_research_analysis(self, bedrock_client_integration, comprehensive_raw_data):
        """Test complete end-to-end research analysis flow."""
        mock_boto3_client = Mock()
        mock_boto3_client.converse.return_value = {
            'output': {
                'message': {
                    'content': [{
                        'text': """# Business Intelligence Report

## Company Overview
TechCorp Solutions is a rapidly growing software company specializing in AI-powered solutions.

## Key Findings
- Strong technical leadership with CTO Jane Smith
- Recent Series A funding of $10M indicates growth momentum
- Expanding team (25% growth this year) suggests scaling operations
- Technology stack includes Python, React, AWS

## Opportunities
- AI integration services alignment with company focus
- Technical team expansion needs
- Cloud infrastructure optimization

## Recommended Approach
Focus on technical value proposition and growth enablement."""
                    }]
                }
            },
            'usage': {'inputTokens': 500, 'outputTokens': 200}
        }
        
        # Mock successful initialization and prompt loading
        with patch('boto3.client', return_value=mock_boto3_client), \
             patch('builtins.open', mock_open(read_data="Mock prompt content")):
            
            result = await bedrock_client_integration.analyze_research_data(
                comprehensive_raw_data, 
                'research'
            )
            
            # Verify analysis results
            assert result['enhancement_status'] == 'ai_enhanced'
            assert result['source'] == 'bedrock_claude'
            assert result['analysis_type'] == 'research'
            assert 'Business Intelligence Report' in result['enhanced_content']
            assert 'TechCorp Solutions' in result['enhanced_content']
            assert 'Jane Smith' in result['enhanced_content']
            
            # Verify API call was made correctly
            mock_boto3_client.converse.assert_called_once()
            call_args = mock_boto3_client.converse.call_args[1]
            assert call_args['modelId'] == bedrock_client_integration.model_id
            assert len(call_args['messages']) == 1
            assert call_args['inferenceConfig']['temperature'] == 0.1
    
    @pytest.mark.asyncio
    async def test_end_to_end_profile_analysis(self, bedrock_client_integration, comprehensive_raw_data):
        """Test complete end-to-end profile analysis flow."""
        mock_boto3_client = Mock()
        mock_boto3_client.converse.return_value = {
            'output': {
                'message': {
                    'content': [{
                        'text': """# Prospect Engagement Profile

## Target Contact
**Jane Smith** - Chief Technology Officer at TechCorp Solutions

## Engagement Strategy
- **Technical Focus**: Emphasize AI/ML capabilities and integration expertise
- **Growth Enablement**: Position services around scaling engineering teams
- **Infrastructure**: Discuss cloud optimization and AWS best practices

## Key Talking Points
1. Recent Series A funding creates budget for growth initiatives
2. 25% team growth indicates scaling challenges we can address
3. Technology alignment with Python/React/AWS stack

## Recommended Outreach
Lead with technical value proposition focused on AI integration and team scaling solutions."""
                    }]
                }
            },
            'usage': {'inputTokens': 400, 'outputTokens': 150}
        }
        
        with patch('boto3.client', return_value=mock_boto3_client), \
             patch('builtins.open', mock_open(read_data="Mock prompt content")):
            
            result = await bedrock_client_integration.analyze_research_data(
                comprehensive_raw_data,
                'profile'
            )
            
            # Verify profile results
            assert result['enhancement_status'] == 'ai_enhanced'
            assert result['analysis_type'] == 'profile'
            assert 'Prospect Engagement Profile' in result['enhanced_content']
            assert 'Jane Smith' in result['enhanced_content']
            assert 'Chief Technology Officer' in result['enhanced_content']
    
    @pytest.mark.asyncio
    async def test_error_handling_and_fallback(self, bedrock_client_integration, comprehensive_raw_data):
        """Test error handling and fallback behavior."""
        # Mock successful initialization but failing prompt preparation
        mock_client = Mock()
        bedrock_client_integration.bedrock_client = mock_client  # Set client to avoid initialization
        
        with patch.object(bedrock_client_integration, '_prepare_prompts', side_effect=Exception("Prompt preparation failed")):
            result = await bedrock_client_integration.analyze_research_data(
                comprehensive_raw_data,
                'research'
            )
            
            # Verify fallback response
            assert result['enhancement_status'] == 'error'
            assert result['fallback'] is True
            assert 'Prompt preparation failed' in result['analysis']['error']
    
    @pytest.mark.asyncio
    async def test_prompt_template_substitution(self, bedrock_client_integration):
        """Test that prompt templates are properly substituted with data."""
        mock_boto3_client = Mock()
        mock_boto3_client.converse.return_value = {
            'output': {'message': {'content': [{'text': 'Test response'}]}},
            'usage': {'inputTokens': 10, 'outputTokens': 5}
        }
        
        test_data = {
            'company': {'name': 'TestCorp', 'industry': 'Testing'},
            'sources': ['test_source'],
            'research': {'test_data': 'sample'}
        }
        
        # Mock prompt templates with placeholders
        mock_prompts = {
            'research_system': 'System prompt for research analysis',
            'research_user': 'Analyze company: {company_data}\nFrom sources: {data_sources}\nWith data: {research_data}'
        }
        
        with patch('boto3.client', return_value=mock_boto3_client), \
             patch('builtins.open', mock_open(read_data="Mock content")):
            
            bedrock_client_integration._prompts_cache = mock_prompts
            bedrock_client_integration.bedrock_client = mock_boto3_client
            
            await bedrock_client_integration.analyze_research_data(test_data, 'research')
            
            # Verify that user prompt was properly formatted
            call_args = mock_boto3_client.converse.call_args[1]
            user_message = call_args['messages'][0]['content'][0]['text']
            
            assert 'TestCorp' in user_message
            assert 'Testing' in user_message
            assert 'test_source' in user_message
            assert 'sample' in user_message


class TestBedrockClientEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.mark.asyncio
    async def test_empty_raw_data(self):
        """Test analysis with empty raw data."""
        client = BedrockClient()
        empty_data = {}
        
        with patch.object(client, 'initialize', new_callable=AsyncMock), \
             patch.object(client, '_prepare_prompts', return_value=("", "")), \
             patch.object(client, '_call_converse_api', return_value="Empty analysis"):
            
            result = await client.analyze_research_data(empty_data)
            assert result['enhanced_content'] == "Empty analysis"
    
    @pytest.mark.asyncio
    async def test_very_large_data(self):
        """Test analysis with very large data payload."""
        client = BedrockClient()
        large_data = {
            'company': {'large_field': 'x' * 10000},
            'research': {'massive_list': [f'item_{i}' for i in range(1000)]}
        }
        
        with patch.object(client, 'initialize', new_callable=AsyncMock), \
             patch.object(client, '_prepare_prompts', return_value=("sys", "user")), \
             patch.object(client, '_call_converse_api', return_value="Large data analysis"):
            
            result = await client.analyze_research_data(large_data)
            assert result['enhanced_content'] == "Large data analysis"
    
    def test_invalid_json_in_data(self):
        """Test handling of data that can't be JSON serialized."""
        client = BedrockClient()
        client._prompts_cache = {
            'research_system': 'System',
            'research_user': '{company_data}'
        }
        
        # Data with non-serializable object
        invalid_data = {
            'company': {'func': lambda x: x}  # Functions can't be JSON serialized
        }
        
        with pytest.raises(TypeError):
            client._prepare_prompts(invalid_data, 'research')
    
    @pytest.mark.asyncio
    async def test_partial_prompt_loading_failure(self):
        """Test behavior when some but not all prompt files fail to load."""
        client = BedrockClient()
        
        def mock_open_side_effect(filename, *args, **kwargs):
            if 'research_system' in filename:
                return mock_open(read_data="Research system prompt")()
            else:
                raise FileNotFoundError(f"File {filename} not found")
        
        with patch('builtins.open', side_effect=mock_open_side_effect):
            await client._load_prompts()
            
            # Should have one successful load and three fallbacks
            assert len(client._prompts_cache) == 4
            assert client._prompts_cache['research_system'] == "Research system prompt"
            # Others should have fallback content
            for key in ['research_user', 'profile_system', 'profile_user']:
                assert 'Please analyze the provided data' in client._prompts_cache[key]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
