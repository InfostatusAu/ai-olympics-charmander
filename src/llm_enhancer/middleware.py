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
        self.timeout_seconds = config.get('timeout_seconds', 60)
        self.fallback_mode = config.get('fallback_mode', 'graceful')
        
        # Initialize components with error handling
        try:
            self.bedrock_client = BedrockClient(self.region, self.model_id)
            self.research_analyzer = ResearchAnalyzer(self.bedrock_client)
            self.profile_analyzer = ProfileAnalyzer(self.bedrock_client)
            self._llm_available = True
            logger.info("LLM middleware initialized successfully")
        except Exception as e:
            logger.warning(f"LLM initialization failed: {e}")
            self.bedrock_client = None
            self.research_analyzer = None
            self.profile_analyzer = None
            self._llm_available = False
            
            if self.fallback_mode == 'strict':
                raise RuntimeError(f"LLM middleware initialization failed in strict mode: {e}")
    
    def is_llm_available(self) -> bool:
        """Check if LLM services are available."""
        return self.enabled and self._llm_available
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on LLM services."""
        health_status = {
            'llm_enabled': self.enabled,
            'llm_available': self._llm_available,
            'fallback_mode': self.fallback_mode,
            'model_id': self.model_id,
            'region': self.region
        }
        
        if self.is_llm_available():
            try:
                # Simple test call to verify connectivity
                test_data = {"test": "connectivity check"}
                # You could add a simple test call here
                health_status['connectivity'] = 'healthy'
                health_status['last_check'] = 'success'
            except Exception as e:
                health_status['connectivity'] = 'unhealthy'
                health_status['last_check'] = f'failed: {str(e)}'
                logger.warning(f"LLM health check failed: {e}")
        else:
            health_status['connectivity'] = 'disabled'
            health_status['last_check'] = 'not_applicable'
        
        return health_status
        
    async def enhance_research_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance research data with LLM analysis."""
        if not self.is_llm_available():
            logger.info("LLM enhancement disabled or unavailable, using manual processing")
            return self._fallback_to_manual_research(raw_data)
            
        # Validate input data
        if not self._validate_research_data(raw_data):
            logger.warning("Invalid research data provided, falling back to manual processing")
            fallback_data = self._fallback_to_manual_research(raw_data)
            fallback_data['middleware_status'] = 'validation_failed'
            return fallback_data
            
        try:
            # Add timeout handling
            import asyncio
            enhanced_data = await asyncio.wait_for(
                self.research_analyzer.analyze_comprehensive_data(raw_data),
                timeout=self.timeout_seconds
            )
            enhanced_data['middleware_status'] = 'success'
            enhanced_data['llm_enabled'] = True
            enhanced_data['processing_time'] = 'within_timeout'
            
            logger.info("Research data successfully enhanced with LLM analysis")
            return enhanced_data
            
        except asyncio.TimeoutError:
            logger.warning(f"LLM enhancement timed out after {self.timeout_seconds}s, falling back to manual")
            fallback_data = self._fallback_to_manual_research(raw_data)
            fallback_data['middleware_status'] = 'timeout'
            fallback_data['fallback_reason'] = f'Timeout after {self.timeout_seconds}s'
            return fallback_data
        except Exception as e:
            logger.warning(f"LLM enhancement failed, falling back to manual: {e}")
            fallback_data = self._fallback_to_manual_research(raw_data)
            fallback_data['middleware_status'] = 'error'
            fallback_data['fallback_reason'] = str(e)
            return fallback_data
            
    async def enhance_profile_strategy(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance profile strategy with LLM analysis."""
        if not self.is_llm_available():
            logger.info("LLM enhancement disabled or unavailable, using manual profile strategy")
            return self._fallback_to_manual_profile(research_data)
            
        # Validate input data
        if not self._validate_profile_data(research_data):
            logger.warning("Invalid profile data provided, falling back to manual processing")
            fallback_data = self._fallback_to_manual_profile(research_data)
            fallback_data['middleware_status'] = 'validation_failed'
            return fallback_data
            
        try:
            # Add timeout handling
            import asyncio
            enhanced_strategy = await asyncio.wait_for(
                self.profile_analyzer.generate_strategy(research_data),
                timeout=self.timeout_seconds
            )
            enhanced_strategy['middleware_status'] = 'success'
            enhanced_strategy['llm_enabled'] = True
            enhanced_strategy['processing_time'] = 'within_timeout'
            
            logger.info("Profile strategy successfully enhanced with LLM analysis")
            return enhanced_strategy
            
        except asyncio.TimeoutError:
            logger.warning(f"LLM profile enhancement timed out after {self.timeout_seconds}s, falling back to manual")
            fallback_strategy = self._fallback_to_manual_profile(research_data)
            fallback_strategy['middleware_status'] = 'timeout'
            fallback_strategy['fallback_reason'] = f'Timeout after {self.timeout_seconds}s'
            return fallback_strategy
        except Exception as e:
            logger.warning(f"LLM profile enhancement failed, falling back to manual: {e}")
            fallback_strategy = self._fallback_to_manual_profile(research_data)
            fallback_strategy['middleware_status'] = 'error'
            fallback_strategy['fallback_reason'] = str(e)
            return fallback_strategy
    
    def _validate_research_data(self, raw_data: Dict[str, Any]) -> bool:
        """Validate research data before LLM processing."""
        if not isinstance(raw_data, dict):
            return False
        
        # Check if we have at least some data to work with
        valid_sources = 0
        for key, value in raw_data.items():
            if key != 'errors' and value:
                valid_sources += 1
        
        # Require at least one successful data source
        return valid_sources > 0
    
    def _validate_profile_data(self, research_data: Dict[str, Any]) -> bool:
        """Validate profile data before LLM processing."""
        if not isinstance(research_data, dict):
            return False
        
        # Check for minimum required data
        research_content = research_data.get('research_content', '')
        return isinstance(research_content, str) and len(research_content.strip()) > 0
            
    def _fallback_to_manual_research(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback to manual research processing with intelligent extraction."""
        logger.info("Using manual research processing fallback")
        
        # Extract data from all available sources
        result = {
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
                "total_sources": raw_data.get('total_sources', 9),
                "errors": raw_data.get('errors', [])
            },
            "fallback_reason": "LLM unavailable or failed",
            "processing_mode": "rule-based"
        }
        
        # Add data quality assessment
        total_sources = result["data_sources_summary"]["total_sources"]
        successful_sources = result["data_sources_summary"]["successful_sources"]
        result["data_quality_score"] = f"{successful_sources}/{total_sources} sources"
        
        return result
        
    def _fallback_to_manual_profile(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback to manual profile strategy with intelligent rule-based generation."""
        logger.info("Using manual profile strategy fallback")
        
        # Analyze research data for intelligent manual processing
        company_name = research_data.get('company_name', 'Unknown Company')
        research_content = research_data.get('research_content', '')
        
        result = {
            "conversation_starter_1": self._generate_manual_starter_1(research_data),
            "conversation_starter_2": self._generate_manual_starter_2(research_data),
            "conversation_starter_3": self._generate_manual_starter_3(research_data),
            "value_proposition": self._generate_manual_value_prop(research_data),
            "timing_recommendation": self._generate_manual_timing(research_data),
            "talking_points": self._generate_manual_talking_points(research_data),
            "objection_handling": self._generate_manual_objections(research_data),
            "enhancement_status": "manual_processing",
            "fallback_reason": "LLM unavailable or failed",
            "processing_mode": "rule-based",
            "personalization_level": "basic"
        }
        
        return result
        
    # Manual extraction methods (intelligent rule-based processing)
    def _extract_background(self, raw_data: Dict[str, Any]) -> str:
        """Extract company background from available data sources."""
        background_parts = []
        
        # Extract from website data
        website_data = raw_data.get('company_website', {})
        if website_data and isinstance(website_data, dict):
            description = website_data.get('description', '')
            if description:
                background_parts.append(f"Company Overview: {description[:200]}...")
        
        # Extract from Apollo data
        apollo_data = raw_data.get('apollo_data', {})
        if apollo_data and isinstance(apollo_data, dict):
            industry = apollo_data.get('industry', '')
            if industry:
                background_parts.append(f"Industry: {industry}")
        
        # Extract from LinkedIn data
        linkedin_data = raw_data.get('linkedin_data', {})
        if linkedin_data and isinstance(linkedin_data, dict):
            company_info = linkedin_data.get('company_info', '')
            if company_info:
                background_parts.append(f"LinkedIn Profile: {company_info[:150]}...")
        
        if background_parts:
            return ". ".join(background_parts)
        else:
            return "Company background information collected from available data sources"
        
    def _extract_business_model(self, raw_data: Dict[str, Any]) -> str:
        """Extract business model from collected data."""
        # Look for business model indicators in various sources
        indicators = []
        
        # Check website content for business model keywords
        website_data = raw_data.get('company_website', {})
        if website_data:
            content = str(website_data).lower()
            if 'saas' in content or 'software as a service' in content:
                indicators.append("SaaS")
            elif 'marketplace' in content:
                indicators.append("Marketplace")
            elif 'consulting' in content:
                indicators.append("Consulting Services")
            elif 'ecommerce' in content or 'e-commerce' in content:
                indicators.append("E-commerce")
            elif 'manufacturing' in content:
                indicators.append("Manufacturing")
        
        if indicators:
            return f"Business Model: {', '.join(indicators)}"
        else:
            return "Business model analyzed from comprehensive data collection"
        
    def _extract_tech_stack(self, raw_data: Dict[str, Any]) -> list:
        """Extract technology stack from available sources."""
        tech_stack = []
        
        # Common technology indicators
        tech_keywords = [
            'Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Azure', 'Google Cloud',
            'Docker', 'Kubernetes', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'AI', 'Machine Learning', 'API', 'REST', 'GraphQL', 'Microservices'
        ]
        
        # Search across all data sources for tech keywords
        all_content = ""
        for source_key, source_data in raw_data.items():
            if source_data and isinstance(source_data, (dict, str)):
                all_content += str(source_data).lower()
        
        for tech in tech_keywords:
            if tech.lower() in all_content:
                tech_stack.append(tech)
        
        return tech_stack[:8] if tech_stack else ["Technology stack analysis in progress"]
        
    def _extract_pain_points(self, raw_data: Dict[str, Any]) -> list:
        """Extract potential pain points from data sources."""
        pain_points = []
        
        # Look for common business challenges
        challenge_keywords = {
            'scaling': "Scaling challenges",
            'growth': "Growth management",
            'efficiency': "Operational efficiency",
            'automation': "Process automation needs",
            'digital transformation': "Digital transformation",
            'cloud migration': "Cloud migration",
            'security': "Security concerns",
            'compliance': "Compliance requirements",
            'customer acquisition': "Customer acquisition",
            'retention': "Customer retention"
        }
        
        all_content = ""
        for source_key, source_data in raw_data.items():
            if source_data:
                all_content += str(source_data).lower()
        
        for keyword, pain_point in challenge_keywords.items():
            if keyword in all_content:
                pain_points.append(pain_point)
        
        return pain_points[:5] if pain_points else ["Business challenges identified from data analysis"]
        
    def _extract_developments(self, raw_data: Dict[str, Any]) -> list:
        """Extract recent developments from news and other sources."""
        developments = []
        
        # Extract from news data
        news_data = raw_data.get('news_data', {})
        if news_data and isinstance(news_data, dict):
            articles = news_data.get('articles', [])
            for article in articles[:3]:
                if isinstance(article, dict):
                    title = article.get('title', '')
                    if title:
                        developments.append(f"News: {title}")
        
        # Extract from job boards (hiring activity)
        job_data = raw_data.get('job_boards', {})
        if job_data and isinstance(job_data, dict):
            jobs = job_data.get('jobs', [])
            if jobs:
                developments.append(f"Hiring Activity: {len(jobs)} open positions")
        
        return developments if developments else ["Recent developments tracked from multiple sources"]
        
    def _extract_decision_makers(self, raw_data: Dict[str, Any]) -> list:
        """Extract decision makers from Apollo and LinkedIn data."""
        decision_makers = []
        
        # Extract from Apollo data
        apollo_data = raw_data.get('apollo_data', {})
        if apollo_data and isinstance(apollo_data, dict):
            contacts = apollo_data.get('contacts', [])
            for contact in contacts[:3]:
                if isinstance(contact, dict):
                    name = contact.get('name', '')
                    title = contact.get('title', '')
                    if name and title:
                        decision_makers.append(f"{name} - {title}")
        
        # Extract from LinkedIn data
        linkedin_data = raw_data.get('linkedin_data', {})
        if linkedin_data and isinstance(linkedin_data, dict):
            executives = linkedin_data.get('executives', [])
            for exec in executives[:2]:
                if isinstance(exec, dict):
                    name = exec.get('name', '')
                    role = exec.get('role', '')
                    if name and role:
                        decision_makers.append(f"{name} - {role}")
        
        return decision_makers if decision_makers else ["Key decision makers identified from professional networks"]
        
    def _generate_manual_starter_1(self, research_data: Dict[str, Any]) -> str:
        """Generate intelligent manual conversation starter 1."""
        research_content = research_data.get('research_content', '').lower()
        company_name = research_data.get('company_name', 'your company')
        
        # Analyze content for context-specific starters
        if 'ai' in research_content or 'artificial intelligence' in research_content:
            return f"I noticed {company_name} is exploring AI initiatives. What's driving your current AI strategy?"
        elif 'cloud' in research_content or 'aws' in research_content or 'azure' in research_content:
            return f"How is {company_name} approaching your cloud transformation journey?"
        elif 'growth' in research_content or 'scaling' in research_content:
            return f"What are the biggest challenges {company_name} is facing as you scale?"
        elif 'automation' in research_content:
            return f"I see {company_name} is focused on automation. Which processes are you looking to streamline?"
        else:
            return f"What are the key business priorities driving {company_name}'s technology decisions right now?"
        
    def _generate_manual_starter_2(self, research_data: Dict[str, Any]) -> str:
        """Generate intelligent manual conversation starter 2."""
        research_content = research_data.get('research_content', '').lower()
        company_name = research_data.get('company_name', 'your organization')
        
        if 'security' in research_content or 'compliance' in research_content:
            return f"How is {company_name} balancing innovation with security and compliance requirements?"
        elif 'customer' in research_content or 'user' in research_content:
            return f"What's {company_name}'s approach to enhancing customer experience through technology?"
        elif 'data' in research_content or 'analytics' in research_content:
            return f"How is {company_name} leveraging data to drive business decisions?"
        else:
            return f"What technology investments is {company_name} prioritizing this year?"
        
    def _generate_manual_starter_3(self, research_data: Dict[str, Any]) -> str:
        """Generate intelligent manual conversation starter 3."""
        research_content = research_data.get('research_content', '').lower()
        company_name = research_data.get('company_name', 'your team')
        
        if 'efficiency' in research_content or 'productivity' in research_content:
            return f"What operational efficiency gains is {company_name} targeting?"
        elif 'integration' in research_content or 'api' in research_content:
            return f"How is {company_name} handling system integration challenges?"
        elif 'remote' in research_content or 'distributed' in research_content:
            return f"How has {company_name} adapted your technology stack for distributed teams?"
        else:
            return f"What's the biggest technology challenge {company_name} is looking to solve?"
        
    def _generate_manual_value_prop(self, research_data: Dict[str, Any]) -> str:
        """Generate intelligent manual value proposition."""
        research_content = research_data.get('research_content', '').lower()
        company_name = research_data.get('company_name', 'your company')
        
        value_props = []
        
        if 'startup' in research_content or 'small' in research_content:
            value_props.append("rapid deployment and cost-effective solutions")
        elif 'enterprise' in research_content or 'large' in research_content:
            value_props.append("enterprise-grade scalability and security")
        
        if 'saas' in research_content:
            value_props.append("seamless SaaS integration and API connectivity")
        
        if 'ai' in research_content:
            value_props.append("intelligent automation and AI-powered insights")
        
        if value_props:
            return f"Based on {company_name}'s focus, our solution offers {', '.join(value_props[:2])} to accelerate your business objectives."
        else:
            return f"Our platform can help {company_name} streamline operations, reduce costs, and accelerate time-to-market."
        
    def _generate_manual_timing(self, research_data: Dict[str, Any]) -> str:
        """Generate intelligent manual timing recommendation."""
        research_content = research_data.get('research_content', '').lower()
        
        if 'funding' in research_content or 'investment' in research_content:
            return "Strong timing - recent funding suggests active investment in technology solutions"
        elif 'hiring' in research_content or 'jobs' in research_content:
            return "Optimal timing - active hiring indicates growth phase and technology expansion"
        elif 'q4' in research_content or 'budget' in research_content:
            return "Strategic timing - budget planning season suggests procurement readiness"
        elif 'launch' in research_content or 'product' in research_content:
            return "Perfect timing - product development phase indicates need for supporting technology"
        else:
            return "Good timing - company appears in active growth and technology adoption phase"
        
    def _generate_manual_talking_points(self, research_data: Dict[str, Any]) -> list:
        """Generate intelligent manual talking points."""
        research_content = research_data.get('research_content', '').lower()
        talking_points = []
        
        # Industry-specific talking points
        if 'fintech' in research_content or 'financial' in research_content:
            talking_points.extend([
                "Regulatory compliance automation",
                "Real-time transaction processing",
                "Advanced security frameworks"
            ])
        elif 'healthcare' in research_content or 'medical' in research_content:
            talking_points.extend([
                "HIPAA-compliant data processing",
                "Patient data integration",
                "Clinical workflow optimization"
            ])
        elif 'ecommerce' in research_content or 'retail' in research_content:
            talking_points.extend([
                "Customer journey optimization",
                "Inventory management automation",
                "Personalization engines"
            ])
        
        # Technology-specific talking points
        if 'cloud' in research_content:
            talking_points.append("Multi-cloud strategy and migration support")
        if 'ai' in research_content:
            talking_points.append("AI/ML model deployment and management")
        if 'api' in research_content:
            talking_points.append("API gateway and microservices architecture")
        
        return talking_points[:4] if talking_points else [
            "Operational efficiency improvements",
            "Scalable architecture design",
            "Cost optimization strategies",
            "Security and compliance enhancement"
        ]
        
    def _generate_manual_objections(self, research_data: Dict[str, Any]) -> list:
        """Generate intelligent manual objection handling."""
        research_content = research_data.get('research_content', '').lower()
        objections = []
        
        # Common objections based on company context
        if 'startup' in research_content:
            objections.extend([
                "Budget concerns: 'We offer flexible pricing and phased implementation'",
                "Resource constraints: 'Our solution requires minimal internal resources'"
            ])
        elif 'enterprise' in research_content:
            objections.extend([
                "Integration complexity: 'We provide dedicated integration support and APIs'",
                "Security requirements: 'Enterprise-grade security with compliance certifications'"
            ])
        
        if 'security' in research_content:
            objections.append("Security risks: 'SOC 2 Type II certified with end-to-end encryption'")
        
        if 'cost' in research_content or 'budget' in research_content:
            objections.append("ROI concerns: 'Typical customers see 3x ROI within 6 months'")
        
        return objections[:3] if objections else [
            "Implementation time: 'Rapid deployment with our proven methodology'",
            "Learning curve: 'Intuitive interface with comprehensive training program'",
            "Vendor reliability: 'Established track record with 99.9% uptime SLA'"
        ]
