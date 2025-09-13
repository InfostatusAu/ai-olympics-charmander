
import pytest
import asyncio
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.prospect_research.research import research_prospect
from src.prospect_research.profile import create_profile
from src.database.operations import init_db, create_prospect
from src.file_manager.storage import save_markdown_report, read_markdown_file

@pytest.mark.asyncio
async def test_markdown_file_generation():
    """Test that prospect research generates markdown files correctly."""
    
    # Initialize database
    await init_db()
    
    # Mock external API calls but test the file generation integration
    with patch('src.prospect_research.research.FirecrawlApp') as mock_firecrawl:
        # Mock Firecrawl response
        mock_app = MagicMock()
        mock_app.scrape.return_value = {
            'success': True,
            'data': {
                'markdown': '# TestCorp Inc\n\nA test company for integration testing.',
                'metadata': {'title': 'TestCorp Inc - Company Page'}
            }
        }
        mock_firecrawl.return_value = mock_app
        
        # Mock environment variable for API key
        with patch.dict(os.environ, {'FIRECRAWL_API_KEY': 'test_key'}):
            # Test with mocked research function
            result = await research_prospect("TestCorp Inc")
            
            # Verify response structure
            assert "prospect_id" in result
            assert "report_filename" in result
            assert "message" in result
            assert "data_sources_used" in result
            prospect_id = result["prospect_id"]
            report_filename = result["report_filename"]
            
            # Check that research markdown file was created
            research_file_path = os.path.join("data", "prospects", prospect_id, report_filename)
            assert os.path.exists(research_file_path), f"Research file not found: {research_file_path}"
            
            # Verify file content structure using file_manager
            content = read_markdown_file(research_file_path)
            assert "# Prospect Research Report" in content
            assert "TestCorp Inc" in content
            assert "## Company Background" in content
            
            # Test profile creation
            profile_result = await create_profile(prospect_id, report_filename)
            
            # Verify profile response
            assert "prospect_id" in profile_result
            assert "profile_filename" in profile_result
            assert "strategy_summary" in profile_result
            assert "message" in profile_result
            profile_filename = profile_result["profile_filename"]
            
            # Check that profile markdown file was created
            profile_file_path = os.path.join("data", "prospects", prospect_id, profile_filename)
            assert os.path.exists(profile_file_path), f"Profile file not found: {profile_file_path}"
            
            # Verify profile file content using file_manager
            profile_content = read_markdown_file(profile_file_path)
            assert "# Prospect Mini Profile" in profile_content
            assert "TestCorp Inc" in profile_content
            assert "| Field" in profile_content  # Table format header
            assert "| Value" in profile_content  # Table format header
            
            # Cleanup test files
            prospect_dir = os.path.join("data", "prospects", prospect_id)
            if os.path.exists(prospect_dir):
                shutil.rmtree(prospect_dir)

@pytest.mark.asyncio
async def test_file_manager_integration():
    """Test direct file_manager integration with prospect_research patterns."""
    
    # Test markdown report saving
    test_prospect_id = "test_prospect_12345"
    test_filename = "test_research.md"
    test_content = """# Prospect Research Report

## Company: Test Company Inc

### Executive Summary
This is a test research report for integration testing.

### Data Sources
- Manual test data
- Integration test patterns
"""
    
    # Use file_manager to save markdown report
    await save_markdown_report(test_prospect_id, test_filename, test_content)
    
    # Verify file was created
    expected_path = os.path.join("data", "prospects", test_prospect_id, test_filename)
    assert os.path.exists(expected_path)
    
    # Read back using file_manager
    retrieved_content = read_markdown_file(expected_path)
    assert retrieved_content == test_content
    
    # Cleanup
    test_dir = os.path.join("data", "prospects", test_prospect_id)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
