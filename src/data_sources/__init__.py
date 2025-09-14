"""Data sources module for comprehensive prospect research.

This module provides data source integrations for:
- Apollo.io API (contact enrichment)
- Serper API (search enhancement) 
- Playwright MCP (authenticated browsing)
- Enhanced LinkedIn research
- Job boards (Seek, Indeed, Glassdoor)
- News and government data
"""

from .manager import DataSourceManager

__all__ = ["DataSourceManager"]
