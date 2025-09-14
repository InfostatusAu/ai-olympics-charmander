"""Intelligence middleware coordinator for LLM enhancement."""

import logging
from typing import Dict, Any, Optional

from .client import BedrockClient
from .analyzers import ResearchAnalyzer, ProfileAnalyzer

logger = logging.getLogger(__name__)


class LLMMiddleware:
    """Intelligence middleware coordinator for LLM enhancement."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize LLM middleware.
        
        Args:
            config: Configuration dictionary with LLM settings
        """
        config = config or {}
        
        self.enabled = config.get('llm_enabled', True)
        self.model_id = config.get('model_id', 'apac.anthropic.claude-sonnet-4-20250514-v1:0')
        self.region = config.get('aws_region', 'ap-southeast-2')
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 4000)
        
        # Initialize components
        self.bedrock_client = BedrockClient(self.region, self.model_id)
        self.research_analyzer = ResearchAnalyzer(self.bedrock_client)
        self.profile_analyzer = ProfileAnalyzer(self.bedrock_client)
        
    async def enhance_research_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance research data with LLM analysis.
        
        Args:
            raw_data: Raw data from all sources
            
        Returns:
            Dictionary containing enhanced research data
        """
        if not self.enabled:
            logger.info("LLM enhancement disabled, using manual processing")
            return self._fallback_to_manual_research(raw_data)
            
        try:
            enhanced_data = await self.research_analyzer.analyze_comprehensive_data(raw_data)
            enhanced_data['middleware_status'] = 'success'
            enhanced_data['llm_enabled'] = True
            
            logger.info("Research data successfully enhanced with LLM analysis")
            return enhanced_data
            
        except Exception as e:
            logger.warning(f"LLM enhancement failed, falling back to manual: {e}")
            fallback_data = self._fallback_to_manual_research(raw_data)
            fallback_data['middleware_status'] = 'fallback'
            fallback_data['llm_enabled'] = False
            fallback_data['fallback_reason'] = str(e)
            return fallback_data
            
    async def enhance_profile_strategy(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance profile strategy with LLM analysis.
        
        Args:
            research_data: Processed research data
            
        Returns:
            Dictionary containing enhanced profile strategy
        """
        if not self.enabled:
            logger.info("LLM enhancement disabled, using manual profile strategy")
            return self._fallback_to_manual_profile(research_data)
            
        try:
            enhanced_strategy = await self.profile_analyzer.generate_strategy(research_data)
            enhanced_strategy['middleware_status'] = 'success'
            enhanced_strategy['llm_enabled'] = True
            
            logger.info("Profile strategy successfully enhanced with LLM analysis")
            return enhanced_strategy
            
        except Exception as e:
            logger.warning(f"LLM profile enhancement failed, falling back to manual: {e}")
            fallback_strategy = self._fallback_to_manual_profile(research_data)
            fallback_strategy['middleware_status'] = 'fallback'
            fallback_strategy['llm_enabled'] = False
            fallback_strategy['fallback_reason'] = str(e)
            return fallback_strategy
            
    def _fallback_to_manual_research(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback to manual research processing."""
        logger.info("Using manual research processing fallback")
        
        # Basic manual processing of collected data
        return {
            "company_background": self._extract_background(raw_data),
            "business_model": self._extract_business_model(raw_data),
            "technology_stack": self._extract_tech_stack(raw_data),
            "pain_points": self._extract_pain_points(raw_data),
            "recent_developments": self._extract_developments(raw_data),
            "decision_makers": self._extract_decision_makers(raw_data),
            "enhancement_status": "manual_processing",
            "data_sources_summary": {
                "successful_sources": raw_data.get('successful_sources_count', 0),
                "failed_sources": raw_data.get('failed_sources_count', 0),
                "total_sources": raw_data.get('total_sources', 7),
                "errors": raw_data.get('errors', [])
            }
        }
        
    def _fallback_to_manual_profile(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback to manual profile strategy."""
        logger.info("Using manual profile strategy fallback")
        
        return {
            "conversation_starter_1": self._generate_manual_starter_1(research_data),
            "conversation_starter_2": self._generate_manual_starter_2(research_data),
            "conversation_starter_3": self._generate_manual_starter_3(research_data),
            "value_proposition": self._generate_manual_value_prop(research_data),
            "timing_recommendation": self._generate_manual_timing(research_data),
            "talking_points": self._generate_manual_talking_points(research_data),
            "objection_handling": self._generate_manual_objections(research_data),
            "enhancement_status": "manual_processing"
        }
        
    # Manual extraction methods (simplified for now)
    def _extract_background(self, raw_data: Dict[str, Any]) -> str:
        """Extract company background manually."""
        return "Company background extracted from available data sources"
        
    def _extract_business_model(self, raw_data: Dict[str, Any]) -> str:
        """Extract business model manually."""
        return "Business model analyzed from collected information"
        
    def _extract_tech_stack(self, raw_data: Dict[str, Any]) -> list:
        """Extract technology stack manually."""
        return ["Technology", "Stack", "Placeholder"]
        
    def _extract_pain_points(self, raw_data: Dict[str, Any]) -> list:
        """Extract pain points manually."""
        return ["Manual pain point 1", "Manual pain point 2"]
        
    def _extract_developments(self, raw_data: Dict[str, Any]) -> list:
        """Extract recent developments manually."""
        return ["Recent development 1", "Recent development 2"]
        
    def _extract_decision_makers(self, raw_data: Dict[str, Any]) -> list:
        """Extract decision makers manually."""
        return ["Decision maker 1", "Decision maker 2"]
        
    def _generate_manual_starter_1(self, research_data: Dict[str, Any]) -> str:
        """Generate manual conversation starter 1."""
        return "What's driving your current business priorities?"
        
    def _generate_manual_starter_2(self, research_data: Dict[str, Any]) -> str:
        """Generate manual conversation starter 2."""
        return "How are you approaching your technology roadmap?"
        
    def _generate_manual_starter_3(self, research_data: Dict[str, Any]) -> str:
        """Generate manual conversation starter 3."""
        return "What challenges are you facing in your current setup?"
        
    def _generate_manual_value_prop(self, research_data: Dict[str, Any]) -> str:
        """Generate manual value proposition."""
        return "Value proposition based on manual analysis"
        
    def _generate_manual_timing(self, research_data: Dict[str, Any]) -> str:
        """Generate manual timing recommendation."""
        return "Timing recommendation based on manual assessment"
        
    def _generate_manual_talking_points(self, research_data: Dict[str, Any]) -> list:
        """Generate manual talking points."""
        return ["Manual talking point 1", "Manual talking point 2"]
        
    def _generate_manual_objections(self, research_data: Dict[str, Any]) -> list:
        """Generate manual objection handling."""
        return ["Manual objection response 1", "Manual objection response 2"]
