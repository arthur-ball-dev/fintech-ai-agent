#!/usr/bin/env python3
"""
Quick test to verify LLM provider setup and API key detection
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.framework.llm.client import LLMClient


def test_provider_setup():
    """Test LLM provider configuration and availability"""
    print("🔍 Testing LLM Provider Setup")
    print("=" * 50)

    try:
        # Initialize client
        client = LLMClient()

        # Get provider status
        status = client.get_provider_status()

        print("Provider Status:")
        for provider, info in status.items():
            emoji = "✅" if info['available'] else "❌"
            default = " (DEFAULT)" if info['is_default'] else ""
            print(f"{emoji} {provider.title()}{default}")

            if info['available']:
                models = list(info['models'].values())
                print(f"   Available models: {models}")
            else:
                print(f"   Missing API key: {provider.upper()}_API_KEY")

        # Test available providers list
        available = client.config.get_available_providers()
        print(f"\nReady providers: {available}")

        if available:
            print(f"\n🎯 Setup successful! {len(available)} provider(s) ready.")
            return True
        else:
            print("\n⚠️  No providers available. Check your API keys.")
            return False

    except Exception as e:
        print(f"\n❌ Setup error: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_provider_setup()
    exit(0 if success else 1)