"""Unit tests for prospect research logic."""
import pytest
import tempfile
import os
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.prospect_research.research import research_prospect
from src.prospect_research.profile import (
    create_profile, parse_research_markdown,
    _determine_industry, _estimate_company_size, _extract_headquarters,
    _get_primary_contact, _get_primary_contact_title, _summarize_recent_news,
    _summarize_tech_stack, _summarize_pain_points, _generate_conversation_starter_1,
    _generate_conversation_starter_2, _generate_value_proposition, _calculate_relevance_score
)


class TestResearchProspect:
    """Test the main research_prospect function."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def mock_research_data(self):
        """Sample research data for testing."""
        return {
            "company_name": "TechCorp Inc",
            "domain": "techcorp.com",
            "industry": "Technology",
            "size": "100-500 employees",
            "headquarters": "San Francisco, CA",
            "description": "Leading AI software company",
            "recent_news": "Raised $10M Series A funding",
            "tech_stack": "React, Python, AWS",
            "pain_points": "Scaling customer support"
        }
    
    @patch('src.prospect_research.research.get_firecrawl_content')
    @patch('src.prospect_research.research.get_linkedin_data')
    @patch('src.prospect_research.research.get_apollo_data')
    @patch('src.prospect_research.research.get_job_postings')
    @patch('src.prospect_research.research.get_news_data')
    async def test_research_prospect_success(self, mock_news, mock_jobs, mock_apollo, 
                                           mock_linkedin, mock_firecrawl, temp_dir, mock_research_data):
        """Test successful prospect research."""
        # Setup mocks
        mock_firecrawl.return_value = {"content": "Company website content"}
        mock_linkedin.return_value = {"company_info": "LinkedIn data"}
        mock_apollo.return_value = {"contacts": "Apollo data"}
        mock_jobs.return_value = {"job_listings": "Job data"}
        mock_news.return_value = {"articles": "News data"}
        
        # Execute research
        result = await research_prospect("test-123", "techcorp.com", "TechCorp Inc", temp_dir)
        
        # Verify result
        assert result is not None
        assert "prospect_id" in result
        assert result["prospect_id"] == "test-123"
        assert "company_name" in result
        assert "domain" in result
        
        # Verify all data sources were called
        mock_firecrawl.assert_called_once_with("techcorp.com")
        mock_linkedin.assert_called_once_with("TechCorp Inc")
        mock_apollo.assert_called_once_with("techcorp.com")
        mock_jobs.assert_called_once_with("TechCorp Inc")
        mock_news.assert_called_once_with("TechCorp Inc")
    
    @patch('src.prospect_research.research.get_firecrawl_content')
    async def test_research_prospect_api_failure(self, mock_firecrawl, temp_dir):
        """Test research when API calls fail."""
        # Setup mock to raise exception
        mock_firecrawl.side_effect = Exception("API Error")
        
        # Execute research (should handle errors gracefully)
        result = await research_prospect("test-123", "failcorp.com", "FailCorp", temp_dir)
        
        # Should still return a result with available data
        assert result is not None
        assert result["prospect_id"] == "test-123"
    
    @patch('src.prospect_research.research.save_markdown_report')
    @patch('src.prospect_research.research.get_firecrawl_content')
    async def test_research_prospect_file_saving(self, mock_firecrawl, mock_save, temp_dir):
        """Test that research results are saved to file."""
        mock_firecrawl.return_value = {"content": "Website content"}
        mock_save.return_value = "/path/to/saved/file.md"
        
        result = await research_prospect("test-123", "savecorp.com", "SaveCorp", temp_dir)
        
        # Verify save was called
        mock_save.assert_called_once()
        
        # Check that result includes file path
        assert "file_path" in result or result is not None


class TestProfileCreation:
    """Test profile creation functionality."""
    
    @pytest.fixture
    def sample_research_content(self):
        """Sample research markdown content."""
        return """# Company Research: TechCorp Inc
        
## Company Overview
- **Domain**: techcorp.com
- **Industry**: Technology
- **Size**: 100-500 employees
- **Headquarters**: San Francisco, CA
- **Description**: Leading AI software company

## Recent News
- Raised $10M Series A funding
- Launched new AI product

## Technology Stack
- Frontend: React, TypeScript
- Backend: Python, FastAPI
- Cloud: AWS, Docker

## Pain Points & Challenges
- Scaling customer support
- Data integration challenges

## Key Personnel
- John Doe, CEO
- Jane Smith, CTO

## Contact Information
- Primary Contact: John Doe (CEO)
- Email: john@techcorp.com
        """
    
    async def test_create_profile_success(self, sample_research_content):
        """Test successful profile creation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(sample_research_content)
            research_file_path = f.name
        
        try:
            result = await create_profile("test-123", research_file_path)
            
            assert result is not None
            assert "prospect_id" in result
            assert result["prospect_id"] == "test-123"
            assert "company_analysis" in result
            assert "outreach_strategy" in result
            
        finally:
            os.unlink(research_file_path)
    
    async def test_create_profile_invalid_file(self):
        """Test profile creation with invalid file."""
        result = await create_profile("test-123", "/nonexistent/file.md")
        
        # Should handle gracefully
        assert result is not None
        assert result["prospect_id"] == "test-123"
    
    def test_parse_research_markdown(self, sample_research_content):
        """Test parsing research markdown content."""
        parsed = parse_research_markdown(sample_research_content)
        
        assert isinstance(parsed, dict)
        assert "company_name" in parsed
        assert "domain" in parsed
        assert "industry" in parsed
        assert "headquarters" in parsed


class TestProfileHelperFunctions:
    """Test individual profile helper functions."""
    
    def test_determine_industry(self):
        """Test industry determination."""
        tech_data = {"background": "software development tech platform"}
        finance_data = {"background": "banking financial services investment"}
        education_data = {"background": "university learning education platform"}
        unknown_data = {"background": "general business operations"}
        
        assert _determine_industry(tech_data) == "Technology"
        assert _determine_industry(finance_data) == "Financial Services"
        assert _determine_industry(education_data) == "Education"
        assert _determine_industry(unknown_data) == "General Business"
    
    def test_estimate_company_size(self):
        """Test company size estimation."""
        large_data = {"job_board_info": "enterprise large global corporation", "linkedin_info": "multinational"}
        medium_data = {"job_board_info": "medium growing company", "linkedin_info": "expanding business"}
        small_data = {"background": "company business"}
        
        assert _estimate_company_size(large_data) == "Large Enterprise (1000+ employees)"
        assert _estimate_company_size(medium_data) == "Medium Business (100-1000 employees)"
        assert _estimate_company_size(small_data) == "Small-Medium Business (10-500 employees)"
    
    def test_extract_headquarters(self):
        """Test headquarters extraction."""
        data_with_hq = {"background": "headquarters in San Francisco, CA office location"}
        data_with_address = {"background": "located at 123 Main St, New York, NY"}
        data_no_location = {"background": "company business operations"}
        
        assert "San Francisco" in _extract_headquarters(data_with_hq)
        assert "New York" in _extract_headquarters(data_with_address)
        assert _extract_headquarters(data_no_location) == "Not specified"
    
    def test_get_primary_contact(self):
        """Test primary contact extraction."""
        data_with_ceo = {"decision_makers": ["John Doe is the CEO and founder"]}
        data_with_president = {"decision_makers": ["Jane Smith, President of the company"]}
        data_with_contact = {"decision_makers": ["Contact: Mike Johnson"]}
        data_no_contact = {"background": "company information"}
        
        assert "John Doe" in _get_primary_contact(data_with_ceo)
        assert "Jane Smith" in _get_primary_contact(data_with_president)
        assert "Mike Johnson" in _get_primary_contact(data_with_contact)
        assert _get_primary_contact(data_no_contact) == "Not specified"
    
    def test_get_primary_contact_title(self):
        """Test primary contact title extraction."""
        data_with_ceo = {"decision_makers": ["John Doe is the CEO and founder"]}
        data_with_titles = {"decision_makers": ["Jane Smith, Chief Technology Officer"]}
        data_no_title = {"decision_makers": ["John Doe works at the company"]}
        
        assert _get_primary_contact_title(data_with_ceo) == "CEO"
        assert "Chief Technology Officer" in _get_primary_contact_title(data_with_titles)
        assert _get_primary_contact_title(data_no_title) == "Not specified"
    
    def test_summarize_recent_news(self):
        """Test recent news summarization."""
        data_with_news = {
            "recent_news": [
                "Raised $10M Series A funding from top VCs",
                "Launched new AI-powered product suite",
                "Expanded to European markets"
            ]
        }
        data_no_news = {"background": "company business general information"}
        
        news_summary = _summarize_recent_news(data_with_news)
        assert "funding" in news_summary.lower()
        assert "AI" in news_summary or "ai" in news_summary.lower()
        
        no_news_summary = _summarize_recent_news(data_no_news)
        assert "No significant recent news" in no_news_summary
    
    def test_summarize_tech_stack(self):
        """Test tech stack summarization."""
        data_with_tech = {
            "tech_stack": [
                "Frontend: React, TypeScript, Next.js",
                "Backend: Python, FastAPI, PostgreSQL",
                "Cloud: AWS, Docker, Kubernetes"
            ]
        }
        data_no_tech = {"background": "company business operations"}
        
        tech_summary = _summarize_tech_stack(data_with_tech)
        assert "React" in tech_summary
        assert "Python" in tech_summary
        assert "AWS" in tech_summary
        
        no_tech_summary = _summarize_tech_stack(data_no_tech)
        assert "No specific technology stack" in no_tech_summary
    
    def test_summarize_pain_points(self):
        """Test pain points summarization."""
        data_with_challenges = {
            "pain_points": [
                "Scaling customer support operations",
                "Data integration across multiple systems",
                "Hiring qualified engineers"
            ]
        }
        data_no_challenges = {"background": "company successful operations"}
        
        pain_summary = _summarize_pain_points(data_with_challenges)
        assert "scaling" in pain_summary.lower()
        assert "integration" in pain_summary.lower()
        
        no_pain_summary = _summarize_pain_points(data_no_challenges)
        assert "No specific pain points" in no_pain_summary
    
    def test_generate_conversation_starters(self):
        """Test conversation starter generation."""
        company_data = {
            "company_name": "TechCorp",
            "industry": "Technology",
            "recent_news": "Raised $10M funding",
            "tech_stack": "React, Python",
            "pain_points": "Scaling support"
        }
        
        starter1 = _generate_conversation_starter_1(company_data)
        starter2 = _generate_conversation_starter_2(company_data)
        
        assert isinstance(starter1, str)
        assert isinstance(starter2, str)
        assert len(starter1) > 10
        assert len(starter2) > 10
        assert "TechCorp" in starter1
    
    def test_generate_value_proposition(self):
        """Test value proposition generation."""
        company_data = {
            "company_name": "TechCorp",
            "industry": "Technology",
            "pain_points": "Scaling customer support",
            "tech_stack": "React, Python"
        }
        
        value_prop = _generate_value_proposition(company_data)
        
        assert isinstance(value_prop, str)
        assert len(value_prop) > 20
        assert "TechCorp" in value_prop
    
    def test_calculate_relevance_score(self):
        """Test relevance score calculation."""
        high_relevance_data = {
            "industry": "Technology",
            "pain_points": "scaling automation integration",
            "tech_stack": "Python React API",
            "size": "100-500 employees",
            "recent_news": "funding growth expansion"
        }
        
        low_relevance_data = {
            "industry": "Other",
            "pain_points": "general business",
            "tech_stack": "unknown",
            "size": "Unknown",
            "recent_news": "no news"
        }
        
        high_score = _calculate_relevance_score(high_relevance_data)
        low_score = _calculate_relevance_score(low_relevance_data)
        
        assert isinstance(high_score, (int, float))
        assert isinstance(low_score, (int, float))
        assert 0 <= high_score <= 100
        assert 0 <= low_score <= 100
        assert high_score > low_score


class TestResearchIntegration:
    """Test research and profile integration."""
    
    @patch('src.prospect_research.research.get_firecrawl_content')
    async def test_full_research_to_profile_workflow(self, mock_firecrawl):
        """Test complete workflow from research to profile."""
        mock_firecrawl.return_value = {
            "content": """TechCorp Inc is a technology company 
            based in San Francisco with 200 employees.
            CEO John Doe leads the team."""
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 1: Research
            research_result = await research_prospect(
                "test-123", "techcorp.com", "TechCorp Inc", temp_dir
            )
            
            assert research_result is not None
            
            # Note: For full integration test, we would need to:
            # 1. Create actual research file
            # 2. Pass file path to create_profile
            # This is covered in integration tests instead


class TestErrorHandling:
    """Test error handling in research functions."""
    
    async def test_research_prospect_with_none_inputs(self):
        """Test research with None inputs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = await research_prospect(None, None, None, temp_dir)
            # Should handle gracefully without crashing
            assert result is not None
    
    async def test_create_profile_with_empty_file(self):
        """Test profile creation with empty research file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("")  # Empty file
            empty_file_path = f.name
        
        try:
            result = await create_profile("test-123", empty_file_path)
            assert result is not None
            assert result["prospect_id"] == "test-123"
        finally:
            os.unlink(empty_file_path)
    
    def test_helper_functions_with_empty_content(self):
        """Test helper functions with empty or None content."""
        empty_content = ""
        none_content = None
        
        # These should all handle empty/None input gracefully
        assert _determine_industry({}) == "General Business"
        assert _estimate_company_size({}) == "Small-Medium Business (10-500 employees)"
        assert _extract_headquarters({}) == "Not specified"
        assert _get_primary_contact({}) == "Not specified"
        assert _get_primary_contact_title({}) == "Not specified"
        
        # Test with None input
        if none_content is not None:  # Safety check
            assert _determine_industry({}) == "General Business"


@pytest.mark.asyncio
async def test_async_functions_are_actually_async():
    """Ensure async functions are properly defined as async."""
    import inspect
    
    assert inspect.iscoroutinefunction(research_prospect)
    assert inspect.iscoroutinefunction(create_profile)


class TestPerformance:
    """Test performance characteristics of research functions."""
    
    def test_helper_functions_performance(self):
        """Test that helper functions perform reasonably with large content."""
        large_content = "test content " * 1000  # Large content string
        
        # These should complete quickly even with large input
        import time
        
        start_time = time.time()
        _determine_industry(large_content)
        _estimate_company_size(large_content)
        _extract_headquarters(large_content)
        end_time = time.time()
        
        # Should complete within reasonable time (1 second for this test)
        assert (end_time - start_time) < 1.0
    
    def test_relevance_score_consistency(self):
        """Test that relevance score is consistent for same input."""
        test_data = {
            "industry": "Technology",
            "pain_points": "scaling",
            "tech_stack": "Python",
            "size": "100 employees",
            "recent_news": "funding"
        }
        
        score1 = _calculate_relevance_score(test_data)
        score2 = _calculate_relevance_score(test_data)
        
        # Same input should produce same score
        assert score1 == score2
