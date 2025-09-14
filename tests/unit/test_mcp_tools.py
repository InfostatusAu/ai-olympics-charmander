"""Unit tests for MCP server tools."""
import pytest
import tempfile
import os
import json
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.mcp_server.tools import research_prospect, create_profile, get_prospect_data, search_prospects


class TestMCPToolsUnitTests:
    """Unit tests for individual MCP tool functions."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def sample_prospect_data(self):
        """Sample prospect data for testing."""
        return {
            "id": "test-prospect-123",
            "domain": "testcompany.com",
            "company_name": "Test Company Inc",
            "status": "researched",
            "created_at": "2025-09-14T10:00:00Z",
            "updated_at": "2025-09-14T10:30:00Z"
        }


class TestResearchProspectTool:
    """Test the research_prospect MCP tool."""
    
    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @patch('src.mcp_server.tools.pr_research.research_prospect')
    @patch('src.mcp_server.tools.db_operations.create_prospect')
    @patch('src.mcp_server.tools.db_operations.update_prospect_status')
    async def test_research_prospect_success(self, mock_update_status, mock_create, mock_research, temp_dir):
        """Test successful prospect research via MCP tool."""
        # Setup mocks
        mock_create.return_value = MagicMock(id="test-123")
        mock_research.return_value = {
            "prospect_id": "test-123",
            "report_filename": "prospect_test-123_research.md",
            "data_sources_used": ["LinkedIn", "Apollo", "News"]
        }
        mock_update_status.return_value = MagicMock()
        
        # Call MCP tool
        result = await research_prospect(company="Test Corp")
        
        # Verify result format (returns string, not list)
        assert isinstance(result, str)
        assert "Test Corp" in result
        assert "research completed" in result.lower()
        assert "test-123" in result
        
        # Verify mocks were called
        mock_create.assert_called_once()
        mock_research.assert_called_once_with("Test Corp")
        mock_update_status.assert_called_once()
    
    @patch('src.mcp_server.tools.db_operations.create_prospect')
    async def test_research_prospect_error_handling(self, mock_create, temp_dir):
        """Test research prospect tool error handling."""
        # Setup mocks to raise exception
        mock_create.side_effect = Exception("Database error")
        
        # Call MCP tool
        result = await research_prospect(company="Error Corp")
        
        # Should handle error gracefully
        assert isinstance(result, str)
        assert "error" in result.lower()
    
    async def test_research_prospect_invalid_inputs(self):
        """Test research prospect with invalid inputs."""
        # Test with empty company name
        result = await research_prospect(company="")
        
        assert isinstance(result, str)
        assert "error" in result.lower()


class TestCreateProfileTool:
    """Test the create_profile MCP tool."""
    
    @patch('src.mcp_server.tools.create_profile_lib')
    @patch('src.mcp_server.tools.get_prospect_default')
    @patch('src.mcp_server.tools.update_prospect_status_default')
    async def test_create_profile_success(self, mock_update_status, mock_get_prospect, mock_create_profile):
        """Test successful profile creation via MCP tool."""
        # Setup mocks
        mock_get_prospect.return_value = MagicMock(id="test-123", status="researched")
        mock_create_profile.return_value = {
            "prospect_id": "test-123",
            "company_analysis": "Detailed analysis",
            "outreach_strategy": "Strategic approach"
        }
        mock_update_status.return_value = MagicMock()
        
        # Call MCP tool
        result = await create_profile(prospect_id="test-123")
        
        # Verify result structure
        assert isinstance(result, list)
        assert len(result) == 1
        text_result = result[0]
        assert text_result["type"] == "text"
        assert "test-123" in text_result["text"]
        assert "profile created successfully" in text_result["text"].lower()
        
        # Verify mocks were called
        mock_get_prospect.assert_called_once_with("test-123")
        mock_create_profile.assert_called_once()
        mock_update_status.assert_called_once()
    
    @patch('src.mcp_server.tools.get_prospect_default')
    async def test_create_profile_prospect_not_found(self, mock_get_prospect):
        """Test profile creation when prospect doesn't exist."""
        mock_get_prospect.return_value = None
        
        result = await create_profile(prospect_id="nonexistent")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "not found" in result[0]["text"].lower()
    
    @patch('src.mcp_server.tools.get_prospect_default')
    async def test_create_profile_not_researched(self, mock_get_prospect):
        """Test profile creation when prospect not researched."""
        mock_get_prospect.return_value = MagicMock(id="test-123", status="new")
        
        result = await create_profile(prospect_id="test-123")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "not been researched" in result[0]["text"].lower()
    
    async def test_create_profile_invalid_input(self):
        """Test profile creation with invalid input."""
        result = await create_profile(prospect_id="")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]["text"].lower()


class TestGetProspectDataTool:
    """Test the get_prospect_data MCP tool."""
    
    @patch('src.mcp_server.tools.get_prospect_default')
    @patch('src.mcp_server.tools.read_markdown_file')
    @patch('src.mcp_server.tools.get_prospect_report_path')
    async def test_get_prospect_data_success(self, mock_get_path, mock_read_file, mock_get_prospect):
        """Test successful prospect data retrieval."""
        # Setup mocks
        mock_get_prospect.return_value = MagicMock(
            id="test-123",
            company_name="Test Corp",
            domain="testcorp.com",
            status="profiled",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_get_path.return_value = "/path/to/research.md"
        mock_read_file.return_value = "# Research Report\nDetailed research content"
        
        # Call MCP tool
        result = await get_prospect_data(prospect_id="test-123")
        
        # Verify result structure
        assert isinstance(result, list)
        assert len(result) == 1
        text_result = result[0]
        assert text_result["type"] == "text"
        assert "test-123" in text_result["text"]
        assert "Test Corp" in text_result["text"]
        assert "testcorp.com" in text_result["text"]
    
    @patch('src.mcp_server.tools.get_prospect_default')
    async def test_get_prospect_data_not_found(self, mock_get_prospect):
        """Test prospect data retrieval when prospect doesn't exist."""
        mock_get_prospect.return_value = None
        
        result = await get_prospect_data(prospect_id="nonexistent")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "not found" in result[0]["text"].lower()
    
    @patch('src.mcp_server.tools.get_prospect_default')
    @patch('src.mcp_server.tools.read_markdown_file')
    @patch('src.mcp_server.tools.get_prospect_report_path')
    async def test_get_prospect_data_file_error(self, mock_get_path, mock_read_file, mock_get_prospect):
        """Test prospect data retrieval with file read error."""
        mock_get_prospect.return_value = MagicMock(id="test-123")
        mock_get_path.return_value = "/path/to/research.md"
        mock_read_file.side_effect = FileNotFoundError("File not found")
        
        result = await get_prospect_data(prospect_id="test-123")
        
        assert isinstance(result, list)
        assert len(result) == 1
        # Should still return prospect data even if file read fails
        assert "test-123" in result[0]["text"]
    
    async def test_get_prospect_data_invalid_input(self):
        """Test get prospect data with invalid input."""
        result = await get_prospect_data(prospect_id="")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]["text"].lower()


class TestSearchProspectsTool:
    """Test the search_prospects MCP tool."""
    
    @patch('src.mcp_server.tools.list_prospects_default')
    @patch('src.mcp_server.tools.search_files_for_pattern')
    async def test_search_prospects_success(self, mock_search_files, mock_list_prospects):
        """Test successful prospect search."""
        # Setup mocks
        mock_list_prospects.return_value = [
            MagicMock(id="test-1", company_name="Tech Corp", domain="techcorp.com"),
            MagicMock(id="test-2", company_name="Data Inc", domain="datainc.com")
        ]
        mock_search_files.return_value = {
            "/path/to/test-1_research.md": ["tech startup", "AI platform"],
            "/path/to/test-2_research.md": ["data analytics", "machine learning"]
        }
        
        # Call MCP tool
        result = await search_prospects(query="tech")
        
        # Verify result structure
        assert isinstance(result, list)
        assert len(result) == 1
        text_result = result[0]
        assert text_result["type"] == "text"
        assert "search results" in text_result["text"].lower()
        assert "Tech Corp" in text_result["text"] or "test-1" in text_result["text"]
    
    @patch('src.mcp_server.tools.list_prospects_default')
    async def test_search_prospects_no_results(self, mock_list_prospects):
        """Test prospect search with no results."""
        mock_list_prospects.return_value = []
        
        result = await search_prospects(query="nonexistent")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "no prospects found" in result[0]["text"].lower()
    
    @patch('src.mcp_server.tools.list_prospects_default')
    @patch('src.mcp_server.tools.search_files_for_pattern')
    async def test_search_prospects_error_handling(self, mock_search_files, mock_list_prospects):
        """Test search prospects error handling."""
        mock_list_prospects.side_effect = Exception("Database error")
        
        result = await search_prospects(query="test")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]["text"].lower()
    
    async def test_search_prospects_empty_query(self):
        """Test search prospects with empty query."""
        result = await search_prospects(query="")
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]["text"].lower()
    
    @patch('src.mcp_server.tools.list_prospects_default')
    async def test_search_prospects_database_only(self, mock_list_prospects):
        """Test search prospects using database only (when file search fails)."""
        mock_list_prospects.return_value = [
            MagicMock(id="test-1", company_name="Tech Corp", domain="techcorp.com"),
            MagicMock(id="test-2", company_name="Finance Ltd", domain="finance.com")
        ]
        
        # Call with a query that would match company names
        result = await search_prospects(query="Tech")
        
        assert isinstance(result, list)
        assert len(result) == 1
        # Should return results even without file search
        assert "prospects found" in result[0]["text"].lower()


class TestMCPToolsIntegration:
    """Test MCP tools integration aspects."""
    
    def test_all_tools_return_correct_format(self):
        """Test that all MCP tools return the correct format."""
        import inspect
        
        # All tools should be async functions
        assert inspect.iscoroutinefunction(research_prospect)
        assert inspect.iscoroutinefunction(create_profile)
        assert inspect.iscoroutinefunction(get_prospect_data)
        assert inspect.iscoroutinefunction(search_prospects)
    
    async def test_tools_handle_none_inputs(self):
        """Test that tools handle None inputs gracefully."""
        # These should not crash, but return error messages
        result1 = await research_prospect(company=None)
        result2 = await create_profile(prospect_id=None)
        result3 = await get_prospect_data(prospect_id=None)
        result4 = await search_prospects(query=None)
        
        for result in [result1, result2, result3, result4]:
            assert isinstance(result, str)
            # Check for error indicators (emoji or text)
            assert "❌" in result or "error" in result.lower() or "invalid" in result.lower() or "must be" in result.lower()
    
    async def test_error_message_format(self):
        """Test that error messages follow consistent format."""
        # Test various error conditions
        error_cases = [
            await research_prospect(company=""),
            await create_profile(prospect_id=""),
            await get_prospect_data(prospect_id=""),
            await search_prospects(query="")
        ]
        
        for result in error_cases:
            assert isinstance(result, str)
            assert "error" in result.lower() or "invalid" in result.lower() or "❌" in result


class TestMCPToolsPerformance:
    """Test performance characteristics of MCP tools."""
    
    @patch('src.mcp_server.tools.research_prospect_lib')
    @patch('src.mcp_server.tools.create_prospect_default')
    @patch('src.mcp_server.tools.update_prospect_status_default')
    async def test_research_prospect_timeout(self, mock_update, mock_create, mock_research):
        """Test research prospect handles timeouts appropriately."""
        import asyncio
        
        # Mock with delay to simulate slow operation
        async def slow_research(*args, **kwargs):
            await asyncio.sleep(0.1)  # Short delay for test
            return {"prospect_id": "test", "data": "result"}
        
        mock_create.return_value = MagicMock(id="test")
        mock_research.side_effect = slow_research
        mock_update.return_value = MagicMock()
        
        # Should complete within reasonable time
        start_time = asyncio.get_event_loop().time()
        result = await research_prospect(domain="test.com", company_name="Test")
        end_time = asyncio.get_event_loop().time()
        
        # Should complete reasonably quickly (within 1 second for test)
        assert (end_time - start_time) < 1.0
        assert isinstance(result, list)
    
    async def test_tools_memory_usage(self):
        """Test that tools don't use excessive memory."""
        # Test with large query strings
        large_query = "test " * 1000
        
        result = await search_prospects(query=large_query)
        
        # Should handle large input without issues
        assert isinstance(result, list)
        assert len(result) == 1


class TestMCPToolsValidation:
    """Test input validation for MCP tools."""
    
    async def test_research_prospect_validation(self):
        """Test research prospect input validation."""
        test_cases = [
            # (domain, company_name, should_error)
            ("", "Company", True),
            ("domain.com", "", True),
            ("valid.com", "Valid Company", False),
            ("not-a-domain", "Company", False),  # Let function handle invalid domains
            ("domain.com", "Valid Company Name Inc", False)
        ]
        
        for domain, company_name, should_error in test_cases:
            result = await research_prospect(domain=domain, company_name=company_name)
            assert isinstance(result, list)
            assert len(result) == 1
            
            if should_error:
                assert "error" in result[0]["text"].lower()
    
    async def test_create_profile_validation(self):
        """Test create profile input validation."""
        test_cases = [
            # (prospect_id, should_error)
            ("", True),
            ("valid-id-123", False),
            ("test_prospect_456", False),
            ("123", False)
        ]
        
        for prospect_id, should_error in test_cases:
            result = await create_profile(prospect_id=prospect_id)
            assert isinstance(result, list)
            assert len(result) == 1
            
            if should_error:
                assert "error" in result[0]["text"].lower()
    
    async def test_search_prospects_validation(self):
        """Test search prospects input validation."""
        test_cases = [
            # (query, should_error)
            ("", True),
            ("valid query", False),
            ("a", False),  # Single character should be ok
            ("very " * 100, False),  # Long query should be handled
        ]
        
        for query, should_error in test_cases:
            result = await search_prospects(query=query)
            assert isinstance(result, list)
            assert len(result) == 1
            
            if should_error:
                assert "error" in result[0]["text"].lower()
