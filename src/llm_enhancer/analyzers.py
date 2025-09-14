"""Research data analyzers for LLM processing."""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ResearchAnalyzer:
    """Analyzer for research data using LLM insights."""
    
    def __init__(self, llm_client):
        """Initialize analyzer with LLM client."""
        self.llm_client = llm_client
        
    async def analyze_comprehensive_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze comprehensive research data.
        
        Args:
            raw_data: Raw data from all sources
            
        Returns:
            Dictionary containing structured analysis
        """
        try:
            # Use LLM to analyze all collected data
            analysis = await self.llm_client.analyze_research_data(raw_data, "research")
            
            # Structure for template compatibility
            return self._structure_research_analysis(analysis, raw_data)
            
        except Exception as e:
            logger.error(f"Research analysis failed: {e}")
            # Fallback to manual processing
            return self._fallback_research_analysis(raw_data)
            
    def _structure_research_analysis(self, llm_analysis: Dict[str, Any], raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Structure LLM analysis for template compatibility."""
        # TODO: Implement sophisticated structuring
        return {
            "company_background": llm_analysis.get("analysis", {}).get("background", "AI-enhanced background"),
            "business_model": llm_analysis.get("analysis", {}).get("business_model", "AI-analyzed business model"),
            "technology_stack": llm_analysis.get("analysis", {}).get("tech_stack", []),
            "pain_points": llm_analysis.get("analysis", {}).get("pain_points", []),
            "recent_developments": llm_analysis.get("analysis", {}).get("developments", []),
            "decision_makers": llm_analysis.get("analysis", {}).get("decision_makers", []),
            "enhancement_status": llm_analysis.get("enhancement_status", "ai_enhanced"),
            "data_sources_summary": self._summarize_sources(raw_data)
        }
        
    def _fallback_research_analysis(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback manual analysis when LLM fails."""
        logger.info("Using fallback manual research analysis")
        
        # Basic manual processing of whatever data was collected
        return {
            "company_background": "Manual analysis of collected data",
            "business_model": "Extracted from available sources",
            "technology_stack": [],
            "pain_points": [],
            "recent_developments": [],
            "decision_makers": [],
            "enhancement_status": "manual_fallback",
            "data_sources_summary": self._summarize_sources(raw_data)
        }
        
    def _summarize_sources(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize data source collection results."""
        return {
            "successful_sources": raw_data.get('successful_sources_count', 0),
            "failed_sources": raw_data.get('failed_sources_count', 0),
            "total_sources": raw_data.get('total_sources', 7),
            "errors": raw_data.get('errors', [])
        }


class ProfileAnalyzer:
    """Analyzer for profile strategy generation using LLM."""
    
    def __init__(self, llm_client):
        """Initialize analyzer with LLM client."""
        self.llm_client = llm_client
        
    async def generate_strategy(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate conversation strategy from research data.
        
        Args:
            research_data: Processed research data
            
        Returns:
            Dictionary containing profile strategy
        """
        try:
            # Use LLM to generate strategy
            strategy = await self.llm_client.analyze_research_data(research_data, "profile")
            
            # Structure for template compatibility
            return self._structure_profile_strategy(strategy, research_data)
            
        except Exception as e:
            logger.error(f"Profile strategy generation failed: {e}")
            # Fallback to manual strategy
            return self._fallback_profile_strategy(research_data)
            
    def _structure_profile_strategy(self, llm_strategy: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Structure LLM strategy for template compatibility."""
        # TODO: Implement sophisticated strategy structuring
        strategy_data = llm_strategy.get("analysis", {})
        conversation_starters = strategy_data.get("conversation_starters", [])
        
        return {
            "conversation_starter_1": conversation_starters[0] if len(conversation_starters) > 0 else "AI-generated starter",
            "conversation_starter_2": conversation_starters[1] if len(conversation_starters) > 1 else "AI-generated fallback",
            "conversation_starter_3": conversation_starters[2] if len(conversation_starters) > 2 else "AI-generated fallback",
            "value_proposition": strategy_data.get("value_proposition", "AI-aligned value proposition"),
            "timing_recommendation": strategy_data.get("timing", "AI-recommended timing"),
            "talking_points": strategy_data.get("talking_points", []),
            "objection_handling": strategy_data.get("objection_handling", []),
            "enhancement_status": llm_strategy.get("enhancement_status", "ai_enhanced")
        }
        
    def _fallback_profile_strategy(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback manual strategy when LLM fails."""
        logger.info("Using fallback manual profile strategy")
        
        return {
            "conversation_starter_1": "What's driving your current business priorities?",
            "conversation_starter_2": "How are you approaching your technology roadmap?", 
            "conversation_starter_3": "What challenges are you facing in your current setup?",
            "value_proposition": "Manual value proposition based on research",
            "timing_recommendation": "Manual timing assessment",
            "talking_points": ["Manual talking point 1", "Manual talking point 2"],
            "objection_handling": ["Manual objection response"],
            "enhancement_status": "manual_fallback"
        }
