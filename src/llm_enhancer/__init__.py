"""LLM enhancer module for intelligence middleware.

This module provides LLM integration for:
- AWS Bedrock client wrapper
- Research data analyzers
- Intelligence middleware coordination
- Profile strategy generation
"""

from .middleware import LLMMiddleware
from .client import BedrockClient

__all__ = ["LLMMiddleware", "BedrockClient"]
