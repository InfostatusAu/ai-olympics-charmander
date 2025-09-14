"""AWS Bedrock client wrapper for LLM integration."""

import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class BedrockClient:
    """AWS Bedrock client wrapper for Claude Sonnet integration using Converse API."""
    
    def __init__(self, region: str = "ap-southeast-2", model_id: Optional[str] = None):
        """Initialize Bedrock client.
        
        Args:
            region: AWS region for Bedrock service
            model_id: Model ID to use (default: Claude Sonnet)
        """
        self.region = region
        self.model_id = model_id or "apac.anthropic.claude-sonnet-4-20250514-v1:0"
        self.bedrock_client = None
        self._prompts_cache = {}
        
    async def initialize(self):
        """Initialize the AWS Bedrock client."""
        try:
            import boto3
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=self.region)
            logger.info(f"Bedrock client initialized with model {self.model_id}")
            
            # Load prompts into cache
            await self._load_prompts()
            
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
            
    async def _load_prompts(self):
        """Load prompt templates from files."""
        import os
        
        prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")
        prompt_files = {
            "research_system": "research_system_prompt.md",
            "research_user": "research_user_prompt.md", 
            "profile_system": "profile_system_prompt.md",
            "profile_user": "profile_user_prompt.md"
        }
        
        for key, filename in prompt_files.items():
            try:
                filepath = os.path.join(prompts_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    self._prompts_cache[key] = f.read()
                logger.debug(f"Loaded prompt template: {key}")
            except Exception as e:
                logger.error(f"Failed to load prompt {key}: {e}")
                # Fallback to basic prompts if files not available
                self._prompts_cache[key] = f"# {key.replace('_', ' ').title()}\nPlease analyze the provided data."
            
    async def analyze_research_data(self, raw_data: Dict[str, Any], analysis_type: str = "research") -> Dict[str, Any]:
        """Analyze research data using Claude Converse API.
        
        Args:
            raw_data: Raw data from all sources
            analysis_type: Type of analysis (research, profile)
            
        Returns:
            Dictionary containing LLM analysis results
        """
        if not self.bedrock_client:
            await self.initialize()
            
        try:
            # Prepare system and user prompts
            system_prompt, user_prompt = self._prepare_prompts(raw_data, analysis_type)
            
            # Call Bedrock Converse API
            response = await self._call_converse_api(system_prompt, user_prompt)
            
            # Parse and structure response
            structured_response = self._parse_llm_response(response, analysis_type)
            structured_response['llm_model'] = self.model_id
            structured_response['analysis_type'] = analysis_type
            
            logger.info(f"LLM analysis completed for {analysis_type}")
            return structured_response
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            # Return fallback response structure
            return {
                "analysis": {"error": str(e)},
                "enhancement_status": "error",
                "source": "bedrock_claude",
                "fallback": True
            }
            
    def _prepare_prompts(self, raw_data: Dict[str, Any], analysis_type: str) -> tuple[str, str]:
        """Prepare system and user prompts for analysis."""
        if analysis_type == "research":
            system_prompt = self._prompts_cache.get("research_system", "")
            user_template = self._prompts_cache.get("research_user", "")
            
            # Format user prompt with data
            user_prompt = user_template.format(
                company_data=json.dumps(raw_data.get("company", {}), indent=2),
                data_sources=json.dumps(raw_data.get("sources", []), indent=2), 
                research_data=json.dumps(raw_data.get("research", {}), indent=2)
            )
            
        elif analysis_type == "profile":
            system_prompt = self._prompts_cache.get("profile_system", "")
            user_template = self._prompts_cache.get("profile_user", "")
            
            # Format user prompt with data
            user_prompt = user_template.format(
                company_profile=json.dumps(raw_data.get("company", {}), indent=2),
                business_analysis=json.dumps(raw_data.get("analysis", {}), indent=2),
                target_contact=json.dumps(raw_data.get("contact", {}), indent=2)
            )
            
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
            
        return system_prompt, user_prompt
        
    async def _call_converse_api(self, system_prompt: str, user_prompt: str) -> str:
        """Make API call to Bedrock Converse API following best practices."""
        try:
            # Prepare inference configuration following best practices
            inference_config = {
                "temperature": 0.1,  # Low temperature for consistent analysis
                "maxTokens": 4096,   # Sufficient for detailed analysis
                "topP": 0.9          # Focused but not too restrictive
            }
            
            # Prepare system prompts (array format for Converse API)
            system_prompts = [{"text": system_prompt}] if system_prompt else []
            
            # Prepare messages (must start with user role and alternate)
            messages = [
                {
                    "role": "user",
                    "content": [{"text": user_prompt}]
                }
            ]
            
            # Make the API call using Converse API
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                system=system_prompts,
                inferenceConfig=inference_config
            )
            
            # Extract the response text
            output_message = response['output']['message']
            response_text = output_message['content'][0]['text']
            
            # Log token usage for monitoring
            usage = response.get('usage', {})
            logger.info(f"Bedrock API call completed. Tokens - Input: {usage.get('inputTokens', 0)}, Output: {usage.get('outputTokens', 0)}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Bedrock Converse API call failed: {e}")
            raise
            
    def _parse_llm_response(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """Parse and structure LLM response for markdown output."""
        # For research and profile, we expect markdown output following templates
        return {
            "enhanced_content": response,
            "enhancement_status": "ai_enhanced",
            "source": "bedrock_claude",
            "format": "markdown"
        }
