"""
Integration tests for LLM provider integration
"""
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.framework.llm.client import LLMClient
from src.framework.core.prompt import Prompt


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv('OPENAI_API_KEY'), reason="OpenAI API key not available")
class TestOpenAIIntegration:
    """Integration tests for OpenAI provider (requires real API key)"""

    def test_openai_basic_completion(self):
        """Test basic OpenAI completion works"""
        client = LLMClient()

        # Create simple prompt using correct interface
        prompt = Prompt()
        prompt.messages.append({"role": "user", "content": "Say 'Hello, World!' and nothing else."})

        response = client.generate_response(prompt, provider='openai', model_type='fast')
        assert "Hello" in response
        assert len(response) < 100  # Should be short response


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv('ANTHROPIC_API_KEY'), reason="Anthropic API key not available")
class TestAnthropicIntegration:
    """Integration tests for Anthropic provider (requires real API key)"""

    def test_anthropic_basic_completion(self):
        """Test basic Anthropic completion works"""
        client = LLMClient()

        # Create simple prompt using correct interface
        prompt = Prompt()
        prompt.messages.append({"role": "user", "content": "Say 'Hello, World!' and nothing else."})

        response = client.generate_response(prompt, provider='anthropic', model_type='fast')
        assert "Hello" in response
        assert len(response) < 100  # Should be short response