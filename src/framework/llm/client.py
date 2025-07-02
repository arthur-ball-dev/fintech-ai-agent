import os
import json
from typing import Optional, Dict, Any, List
from litellm import completion
from ..core.prompt import Prompt


class LLMConfig:
    """
    Configuration management for multiple LLM providers

    Reads API keys from system environment variables and manages
    model configurations for enterprise-grade flexibility.
    """

    def __init__(self):
        # API Keys from system environment variables
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        # Default provider selection
        self.default_provider = os.getenv('DEFAULT_LLM_PROVIDER', 'openai')

        # Model configurations per provider
        self.models = {
            'openai': {
                'fast': 'gpt-3.5-turbo',  # Cheapest, fastest
                'default': 'gpt-4o-mini',  # Balanced cost/performance
                'advanced': 'gpt-4o'  # Highest quality, most expensive
            },
            'anthropic': {
                'fast': 'claude-3-haiku-20240307',  # Cheapest, fastest
                'default': 'claude-3-5-sonnet-20241022',  # Balanced cost/performance
                'advanced': 'claude-3-opus-20240229'  # Highest quality, most expensive
            }
        }

        # Default parameters for cost and performance control
        self.default_params = {
            'max_tokens': 1024,
            'temperature': 0.7
        }

    def get_model_name(self, provider: str, model_type: str = 'default') -> str:
        """
        Get the appropriate model name for specified provider and type

        Args:
            provider: 'openai' or 'anthropic'
            model_type: 'default', 'fast', or 'advanced'
        """
        if provider in self.models and model_type in self.models[provider]:
            return self.models[provider][model_type]
        return self.models.get(provider, {}).get('default', 'gpt-4o')

    def validate_provider(self, provider: str) -> bool:
        """Validate that the specified provider has required API key"""
        if provider == 'openai':
            return bool(self.openai_api_key)
        elif provider == 'anthropic':
            return bool(self.anthropic_api_key)
        return False

    def get_available_providers(self) -> List[str]:
        """Get list of providers with valid API keys"""
        available = []
        for provider in ['openai', 'anthropic']:
            if self.validate_provider(provider):
                available.append(provider)
        return available


class LLMClient:
    """
    Enterprise-grade LLM client with multi-provider support

    Features:
    - Multiple LLM provider support (OpenAI, Anthropic)
    - Automatic fallback on provider failure
    - Cost optimization through model selection
    - Professional error handling and logging
    """

    def __init__(self):
        self.config = LLMConfig()
        self._validate_setup()

    def _validate_setup(self):
        """Validate that at least one provider is configured"""
        available = self.config.get_available_providers()
        if not available:
            raise ValueError(
                "No LLM providers configured. Please set OPENAI_API_KEY "
                "and/or ANTHROPIC_API_KEY in your system environment variables."
            )

    def generate_response(
            self,
            prompt: Prompt,
            provider: Optional[str] = None,
            model: Optional[str] = None,
            model_type: str = 'default',
            **kwargs
    ) -> str:
        """
        Generate LLM response with flexible provider selection

        Args:
            prompt: Prompt object containing messages and tools
            provider: Specific provider ('openai', 'anthropic'). Auto-selects if None
            model: Specific model name. Overrides provider's default model
            model_type: Model performance tier ('default', 'fast', 'advanced')
            **kwargs: Additional LLM parameters (temperature, max_tokens, etc.)

        Returns:
            Generated response string or JSON for tool calls

        Raises:
            ValueError: If no providers are available
            Exception: If all providers fail
        """

        # Provider selection logic
        if provider is None:
            provider = self._select_best_provider()
        elif not self.config.validate_provider(provider):
            raise ValueError(f"Provider '{provider}' not available. Check API key.")

        # Model selection
        if model is None:
            model = self.config.get_model_name(provider, model_type)

        # Prepare LLM parameters
        params = self._prepare_llm_params(prompt, model, **kwargs)

        try:
            # Primary attempt
            return self._call_llm_with_retry(params, provider, model)

        except Exception as primary_error:
            # Attempt fallback to alternative provider
            return self._attempt_fallback(prompt, provider, primary_error, **kwargs)

    def _select_best_provider(self) -> str:
        """
        Select the best available provider based on configuration and availability

        Business logic: Prefer configured default, fall back to any available
        """
        available = self.config.get_available_providers()

        if self.config.default_provider in available:
            return self.config.default_provider
        elif available:
            return available[0]  # Use first available
        else:
            raise ValueError("No LLM providers available")

    def _prepare_llm_params(self, prompt: Prompt, model: str, **kwargs) -> Dict[str, Any]:
        """Prepare parameters for LLM API call"""
        params = {
            'model': model,
            'messages': prompt.messages,
            'max_tokens': kwargs.get('max_tokens', self.config.default_params['max_tokens']),
            'temperature': kwargs.get('temperature', self.config.default_params['temperature'])
        }

        # Add tools if available
        if prompt.tools:
            params['tools'] = prompt.tools

        return params

    def _call_llm_with_retry(self, params: Dict[str, Any], provider: str, model: str) -> str:
        """Execute LLM call with error context"""
        try:
            response = completion(**params)
            return self._process_response(response)
        except Exception as e:
            error_msg = f"LLM call failed - Provider: {provider}, Model: {model}, Error: {str(e)}"
            print(f"⚠️  {error_msg}")  # Professional logging
            raise e

    def _attempt_fallback(
            self,
            prompt: Prompt,
            failed_provider: str,
            primary_error: Exception,
            **kwargs
    ) -> str:
        """Attempt fallback to alternative provider"""
        available = self.config.get_available_providers()
        fallback_providers = [p for p in available if p != failed_provider]

        if not fallback_providers:
            raise primary_error  # No fallback available

        fallback_provider = fallback_providers[0]
        print(f"🔄 Attempting fallback: {failed_provider} → {fallback_provider}")

        try:
            return self.generate_response(
                prompt,
                provider=fallback_provider,
                **kwargs
            )
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {str(fallback_error)}")
            # Return both errors for debugging
            raise Exception(
                f"Primary provider ({failed_provider}) failed: {str(primary_error)}. "
                f"Fallback provider ({fallback_provider}) also failed: {str(fallback_error)}"
            )

    def _process_response(self, response) -> str:
        """Process LLM response and extract content or tool calls"""
        if hasattr(response.choices[0].message, 'tool_calls') and response.choices[
            0].message.tool_calls:
            # Handle tool calls
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            return json.dumps(result)
        else:
            # Handle regular text response
            return response.choices[0].message.content

    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed status of all providers for diagnostics

        Returns:
            Dictionary with provider status, models, and configuration
        """
        status = {}

        for provider in ['openai', 'anthropic']:
            available = self.config.validate_provider(provider)
            status[provider] = {
                'available': available,
                'models': self.config.models.get(provider, {}),
                'is_default': provider == self.config.default_provider
            }

        return status

    def list_available_models(self, provider: Optional[str] = None) -> Dict[str, List[str]]:
        """List all available models by provider"""
        if provider:
            if provider in self.config.models:
                return {provider: list(self.config.models[provider].values())}
            return {}

        result = {}
        for p in self.config.get_available_providers():
            result[p] = list(self.config.models[p].values())
        return result


# Backward compatibility wrapper - maintains existing function signature
def generate_response(prompt: Prompt, model: str = "gpt-4o") -> str:
    """
    Legacy wrapper function for backward compatibility

    This maintains the original function signature while providing
    enhanced multi-provider capabilities under the hood.

    Args:
        prompt: Prompt object with messages and tools
        model: Model name (can be OpenAI or Anthropic model)

    Returns:
        Generated response string
    """
    client = LLMClient()

    # Smart provider detection based on model name
    if 'claude' in model.lower():
        return client.generate_response(prompt, provider='anthropic', model=model)
    elif 'gpt' in model.lower():
        return client.generate_response(prompt, provider='openai', model=model)
    else:
        # Use default provider
        return client.generate_response(prompt, model=model)