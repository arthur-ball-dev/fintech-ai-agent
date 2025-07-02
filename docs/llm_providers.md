# LLM Providers Setup Guide

Comprehensive guide for configuring and using the multi-provider LLM system in the File Explorer AI Agent Framework.

## 🎯 Overview

The framework currently supports **OpenAI and Anthropic** providers with automatic failover, cost optimization through model tiers, and enterprise-grade reliability.

---

## ✅ **CURRENTLY IMPLEMENTED FEATURES**

### Multi-Provider Support

Your framework **currently includes**:
- **OpenAI integration** with GPT models
- **Anthropic integration** with Claude models  
- **Automatic failover** between providers when primary fails
- **Model tier system** (fast/default/advanced per provider)
- **Environment variable configuration** for secure API key management
- **Provider status diagnostics** for monitoring

## 🔧 Provider Configuration (Implemented)

### OpenAI Setup

#### 1. Get API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-`)

#### 2. Configure Environment
```bash
# Windows
set OPENAI_API_KEY=sk-your_actual_key_here

# macOS/Linux
export OPENAI_API_KEY="sk-your_actual_key_here"

# Add to .bashrc/.zshrc for persistence
echo 'export OPENAI_API_KEY="sk-your_actual_key_here"' >> ~/.bashrc
```

#### 3. Verify Setup
```python
from src.framework.llm.client import LLMClient

client = LLMClient()
status = client.get_provider_status()
print("OpenAI Available:", status['openai']['available'])
```

### Anthropic Setup

#### 1. Get API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create account or log in
3. Navigate to API Keys section
4. Create new key
5. Copy the key (starts with `sk-ant-`)

#### 2. Configure Environment
```bash
# Windows
set ANTHROPIC_API_KEY=sk-ant-your_actual_key_here

# macOS/Linux
export ANTHROPIC_API_KEY="sk-ant-your_actual_key_here"

# Add to .bashrc/.zshrc for persistence
echo 'export ANTHROPIC_API_KEY="sk-ant-your_actual_key_here"' >> ~/.bashrc
```

#### 3. Verify Setup
```python
from src.framework.llm.client import LLMClient

client = LLMClient()
status = client.get_provider_status()
print("Anthropic Available:", status['anthropic']['available'])
```

## 🎛️ Model Tiers & Cost Optimization (Implemented)

### Current Model Configuration

**OpenAI Model Tiers:**
| Tier | Model | Use Case | Relative Cost | Speed |
|------|-------|----------|---------------|-------|
| **Fast** | `gpt-3.5-turbo` | Simple tasks, prototyping | 1x | Very Fast |
| **Default** | `gpt-4o-mini` | Balanced performance | 3x | Fast |
| **Advanced** | `gpt-4o` | Complex analysis, production | 10x | Moderate |

**Anthropic Model Tiers:**
| Tier | Model | Use Case | Relative Cost | Speed |
|------|-------|----------|---------------|-------|
| **Fast** | `claude-3-haiku-20240307` | Quick tasks, high volume | 1x | Very Fast |
| **Default** | `claude-3-5-sonnet-20241022` | Balanced performance | 5x | Fast |
| **Advanced** | `claude-3-opus-20240229` | Complex reasoning, critical tasks | 15x | Moderate |

### Using Model Tiers (Current Implementation)

```python
from src.framework.llm.client import LLMClient

client = LLMClient()

# Use fast tier for simple tasks
response = client.generate_response(prompt, model_type='fast')

# Use default tier for balanced performance  
response = client.generate_response(prompt, model_type='default')

# Use advanced tier for complex tasks
response = client.generate_response(prompt, model_type='advanced')

# Specify provider + tier
response = client.generate_response(prompt, provider='anthropic', model_type='fast')
```

## 🔄 Automatic Failover (Implemented)

### How Failover Works

Your current implementation **automatically** attempts failover when the primary provider fails:

```python
# This happens automatically - no special code needed
client = LLMClient()

# If OpenAI (default) fails, automatically tries Anthropic
# Console shows: "🔄 Attempting fallback: openai → anthropic"
response = client.generate_response(prompt)
```

### Failover Configuration

```bash
# Set default provider preference
export DEFAULT_LLM_PROVIDER="anthropic"  # or "openai"
```

### Testing Failover

```python
def test_current_failover():
    """Test the implemented failover mechanism"""
    client = LLMClient()
    
    # Check which providers are available
    status = client.get_provider_status()
    available = [p for p, info in status.items() if info['available']]
    
    print(f"Available providers: {available}")
    
    if len(available) > 1:
        print("✅ Failover capability available")
    else:
        print("⚠️  Only one provider - no failover possible")
```

## 📊 Provider Status Monitoring (Implemented)

### Current Monitoring Capabilities

```python
from src.framework.llm.client import LLMClient

def check_provider_health():
    """Use current implementation to check provider status"""
    client = LLMClient()
    status = client.get_provider_status()
    
    for provider, info in status.items():
        emoji = "✅" if info['available'] else "❌"
        default = " (DEFAULT)" if info['is_default'] else ""
        print(f"{emoji} {provider.title()}{default}")
        
        if info['available']:
            models = list(info['models'].values())
            print(f"   Available models: {models}")
        else:
            print(f"   Missing API key: {provider.upper()}_API_KEY")

# Run the check
check_provider_health()
```

### Available Diagnostics

```python
# List available models per provider
client = LLMClient()
models = client.list_available_models()
print("All available models:", models)

# Check specific provider
openai_models = client.list_available_models('openai')
print("OpenAI models:", openai_models)
```

## 🔧 Production Configuration (Implemented)

### Environment Variables
```bash
# Required (at least one)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional configuration
export DEFAULT_LLM_PROVIDER="openai"  # or "anthropic"
```

### Security Best Practices (Implemented)
- ✅ **Environment variables only** - No hardcoded keys in source code
- ✅ **Secure validation** - Keys checked without exposure
- ✅ **Professional logging** - No sensitive data in logs
- ✅ **Git exclusion** - API keys never committed to version control

---

## 📋 **EXAMPLE PATTERNS YOU COULD BUILD**

*These are examples showing how to extend the current implementation - not currently included in the codebase.*

### Dynamic Model Selection Example

```python
# Example pattern - NOT currently implemented
def smart_model_selection(task_description, prompt):
    """Example: Select model tier based on task complexity"""
    client = LLMClient()
    
    simple_keywords = ['list', 'show', 'find', 'count']
    complex_keywords = ['analyze', 'design', 'architect', 'optimize']
    
    if any(keyword in task_description.lower() for keyword in simple_keywords):
        return client.generate_response(prompt, model_type='fast')
    elif any(keyword in task_description.lower() for keyword in complex_keywords):
        return client.generate_response(prompt, model_type='advanced')
    else:
        return client.generate_response(prompt, model_type='default')

# Usage example
task = "Analyze the project architecture"
response = smart_model_selection(task, prompt)
```

### Usage Tracking Example

```python
# Example pattern - NOT currently implemented
class UsageTracker:
    """Example: Track LLM usage for cost monitoring"""
    
    def __init__(self):
        self.client = LLMClient()
        self.usage_stats = {
            'requests': 0,
            'by_provider': {},
            'by_model_tier': {}
        }
    
    def generate_response_with_tracking(self, prompt, **kwargs):
        """Example: Add usage tracking to LLM calls"""
        self.usage_stats['requests'] += 1
        
        # Use existing LLMClient
        response = self.client.generate_response(prompt, **kwargs)
        
        # Track usage (would need to extract provider/model from response)
        return response
    
    def get_usage_report(self):
        """Example: Get usage statistics"""
        return self.usage_stats

# Usage example
tracker = UsageTracker()
response = tracker.generate_response_with_tracking(prompt, model_type='fast')
report = tracker.get_usage_report()
```

### Cost Optimization Example

```python
# Example pattern - NOT currently implemented
class CostOptimizer:
    """Example: Optimize costs by choosing cheapest provider for each tier"""
    
    def __init__(self):
        self.client = LLMClient()
        # Approximate costs per 1K tokens
        self.provider_costs = {
            'openai': {'fast': 0.0015, 'default': 0.015, 'advanced': 0.03},
            'anthropic': {'fast': 0.00025, 'default': 0.003, 'advanced': 0.015}
        }
    
    def get_cheapest_provider(self, model_type='default'):
        """Example: Select cheapest provider for given model tier"""
        available = self.client.config.get_available_providers()
        if not available:
            raise ValueError("No providers available")
        
        cheapest = min(available, key=lambda p: self.provider_costs.get(p, {}).get(model_type, float('inf')))
        return cheapest
    
    def generate_cost_optimized_response(self, prompt, model_type='default'):
        """Example: Use cheapest provider for given tier"""
        provider = self.get_cheapest_provider(model_type)
        return self.client.generate_response(prompt, provider=provider, model_type=model_type)

# Usage example
optimizer = CostOptimizer()
response = optimizer.generate_cost_optimized_response(prompt, model_type='fast')
```

---

## 🚀 **FUTURE ENHANCEMENT IDEAS**

*These are potential future features that could be added to the framework.*

### Additional Provider Support
- **Google Gemini** integration
- **Cohere** model support  
- **Azure OpenAI** endpoints
- **Local model** support (Ollama, etc.)

### Advanced Cost Management
- **Real-time usage tracking** with billing integration
- **Budget alerts** and spending limits
- **Cost analytics dashboard** with usage reports
- **Automatic model downgrading** when approaching budget limits

### Enterprise Features
- **Load balancing** across multiple provider instances
- **Rate limiting** and throttling controls
- **Advanced monitoring** with metrics and alerting
- **Audit logging** for compliance requirements

### Container Deployment
- **Docker containerization** with multi-provider support
- **Kubernetes deployment** manifests
- **Helm charts** for enterprise deployments
- **CI/CD pipeline** integration examples

### GUI Interface
- **Web dashboard** for provider management
- **Visual model selection** interface
- **Real-time monitoring** dashboards
- **Configuration management** UI

---

## 🚨 Troubleshooting (Current Implementation)

### Common Issues & Solutions

#### Issue: "No LLM providers configured"
```python
# Diagnostic using current implementation
from src.framework.llm.client import LLMConfig

config = LLMConfig()
print("OpenAI Key:", "✅" if config.openai_api_key else "❌")
print("Anthropic Key:", "✅" if config.anthropic_api_key else "❌")

# Solution: Set at least one API key in environment variables
```

#### Issue: Provider not responding
```bash
# Use current diagnostic script
python scripts/diagnostics/check_llm_providers.py
```

#### Issue: Want to test specific provider
```python
# Using current implementation
client = LLMClient()

# Test specific provider
try:
    response = client.generate_response(prompt, provider='openai')
    print("✅ OpenAI working")
except Exception as e:
    print(f"❌ OpenAI failed: {e}")

try:
    response = client.generate_response(prompt, provider='anthropic')
    print("✅ Anthropic working")
except Exception as e:
    print(f"❌ Anthropic failed: {e}")
```

This guide focuses on what's actually implemented in your current codebase while providing clear examples of patterns that could be built on top of your foundation.