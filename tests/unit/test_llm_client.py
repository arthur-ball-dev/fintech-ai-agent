"""
Unit tests for enhanced LLM client functionality
"""
import pytest
import os
from unittest.mock import patch, MagicMock
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.framework.llm.client import LLMConfig, LLMClient
from src.framework.core.prompt import Prompt


class TestLLMConfig:
    """Test LLM configuration management"""

    def test_config_initialization(self):
        """Test that config initializes with proper defaults"""
        config = LLMConfig()
        assert config.default_provider in ['openai', 'anthropic']
        assert 'openai' in config.models
        assert 'anthropic' in config.models

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_openai_validation_with_key(self):
        """Test OpenAI validation when API key is present"""
        config = LLMConfig()
        assert config.validate_provider('openai') is True

    @patch.dict(os.environ, {}, clear=True)
    def test_openai_validation_without_key(self):
        """Test OpenAI validation when API key is missing"""
        config = LLMConfig()
        assert config.validate_provider('openai') is False

    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    def test_anthropic_validation_with_key(self):
        """Test Anthropic validation when API key is present"""
        config = LLMConfig()
        assert config.validate_provider('anthropic') is True

    def test_model_selection(self):
        """Test model selection for different tiers"""
        config = LLMConfig()

        # Test OpenAI models
        assert 'gpt' in config.get_model_name('openai', 'fast').lower()
        assert 'gpt' in config.get_model_name('openai', 'default').lower()
        assert 'gpt' in config.get_model_name('openai', 'advanced').lower()

        # Test Anthropic models  
        assert 'claude' in config.get_model_name('anthropic', 'fast').lower()
        assert 'claude' in config.get_model_name('anthropic', 'default').lower()
        assert 'claude' in config.get_model_name('anthropic', 'advanced').lower()

    def test_available_providers(self):
        """Test available providers detection"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test', 'ANTHROPIC_API_KEY': 'test'}):
            config = LLMConfig()
            available = config.get_available_providers()
            assert 'openai' in available
            assert 'anthropic' in available


class TestLLMClient:
    """Test LLM client functionality"""

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_client_initialization_success(self):
        """Test client initializes successfully with valid config"""
        client = LLMClient()
        assert client.config is not None

    @patch.dict(os.environ, {}, clear=True)
    def test_client_initialization_failure(self):
        """Test client fails initialization without API keys"""
        with pytest.raises(ValueError, match="No LLM providers configured"):
            LLMClient()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test'})
    @patch('src.framework.llm.client.completion')
    def test_generate_response_success(self, mock_completion):
        """Test successful response generation"""
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_response.choices[0].message.tool_calls = None
        mock_completion.return_value = mock_response

        # Test
        client = LLMClient()
        prompt = MagicMock()
        prompt.messages = [{"role": "user", "content": "test"}]
        prompt.tools = None

        response = client.generate_response(prompt)
        assert response == "Test response"
        mock_completion.assert_called_once()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test', 'ANTHROPIC_API_KEY': 'test'})
    def test_provider_status(self):
        """Test provider status reporting"""
        client = LLMClient()
        status = client.get_provider_status()

        assert 'openai' in status
        assert 'anthropic' in status
        assert status['openai']['available'] is True
        assert status['anthropic']['available'] is True


class TestLegacyCompatibility:
    """Test backward compatibility"""

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test'})
    @patch('src.framework.llm.client.completion')
    def test_legacy_function_compatibility(self, mock_completion):
        """Test that legacy generate_response function still works"""
        from src.framework.llm.client import generate_response

        # Mock response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Legacy response"
        mock_response.choices[0].message.tool_calls = None
        mock_completion.return_value = mock_response

        # Test
        prompt = MagicMock()
        prompt.messages = [{"role": "user", "content": "test"}]
        prompt.tools = None

        response = generate_response(prompt)
        assert response == "Legacy response"