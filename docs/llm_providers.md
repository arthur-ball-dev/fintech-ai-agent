# LLM Providers Setup

Complete setup guide for OpenAI and Anthropic providers with cost optimization strategies.

## 🎯 Provider Overview

The framework supports **OpenAI and Anthropic** with automatic failover and cost optimization through model tiers.

| Feature | OpenAI | Anthropic |
|---------|--------|-----------|
| **Models** | GPT-3.5, GPT-4o Mini, GPT-4o | Claude 3 Haiku, Sonnet, Opus |
| **Speed** | Very Fast → Moderate | Very Fast → Moderate |
| **Cost** | 1x → 10x relative | 1x → 15x relative |
| **Strengths** | Code analysis, function calling | Long context, reasoning |

---

## 🔧 Provider Configuration

### OpenAI Setup

1. **Get API Key**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Navigate to API Keys → Create new secret key
   - Copy key (starts with `sk-`)

2. **Configure Environment**
   ```bash
   # Windows
   set OPENAI_API_KEY=sk-your_actual_key_here
   
   # macOS/Linux
   export OPENAI_API_KEY="sk-your_actual_key_here"
   
   # Persist in shell profile
   echo 'export OPENAI_API_KEY="sk-your_key"' >> ~/.bashrc
   ```

3. **Verify Setup**
   ```bash
   python scripts/diagnostics/check_llm_providers.py
   ```

### Anthropic Setup

1. **Get API Key**
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Navigate to API Keys → Create new key
   - Copy key (starts with `sk-ant-`)

2. **Configure Environment**
   ```bash
   # Windows
   set ANTHROPIC_API_KEY=sk-ant-your_actual_key_here
   
   # macOS/Linux  
   export ANTHROPIC_API_KEY="sk-ant-your_actual_key_here"
   
   # Persist in shell profile
   echo 'export ANTHROPIC_API_KEY="sk-ant-your_key"' >> ~/.bashrc
   ```

3. **Verify Setup**
   ```bash
   python scripts/diagnostics/check_llm_providers.py
   ```

---

## 💰 Cost Optimization Strategy

### Model Tier System

**OpenAI Tiers:**
| Tier | Model | Use Case | Relative Cost |
|------|-------|----------|---------------|
| **Fast** | `gpt-3.5-turbo` | Quick analysis, prototyping | 1x |
| **Default** | `gpt-4o-mini` | Balanced performance | 3x |
| **Advanced** | `gpt-4o` | Complex analysis, critical decisions | 10x |

**Anthropic Tiers:**
| Tier | Model | Use Case | Relative Cost |
|------|-------|----------|---------------|
| **Fast** | `claude-3-haiku-20240307` | High volume, simple tasks | 1x |
| **Default** | `claude-3-5-sonnet-20241022` | Most production workloads | 5x |
| **Advanced** | `claude-3-opus-20240229` | Complex reasoning, critical analysis | 15x |

### Cost Optimization Examples

```python
from src.framework.llm.client import LLMClient

client = LLMClient()

# Maximum cost savings - use for simple tasks
response = client.generate_response(prompt, model_type='fast')

# Balanced performance - recommended for most tasks
response = client.generate_response(prompt, model_type='default')  

# Premium quality - use for critical decisions only
response = client.generate_response(prompt, model_type='advanced')

# Provider-specific optimization
response = client.generate_response(prompt, provider='anthropic', model_type='fast')  # Cheapest option
```

---

## 🔄 Automatic Failover

### How It Works

1. **Primary Provider Attempt** - Uses configured default or specified provider
2. **Automatic Fallback** - If primary fails, tries alternative provider
3. **Professional Logging** - Clear status messages during failover
4. **Transparent Operation** - No code changes required

### Configuration

```bash
# Set preferred default provider
export DEFAULT_LLM_PROVIDER="openai"  # or "anthropic"
```

### Failover Example

```python
# Automatic failover happens transparently
client = LLMClient()
response = client.generate_response(prompt)

# Console output during failover:
# 🔄 Attempting fallback: openai → anthropic
# ✅ Fallback successful
```

---

## 📊 Provider Status Monitoring

### Current Status Check

```python
from src.framework.llm.client import LLMClient

def check_provider_health():
    client = LLMClient()
    status = client.get_provider_status()
    
    for provider, info in status.items():
        emoji = "✅" if info['available'] else "❌"
        print(f"{emoji} {provider.title()}: {info['models']}")

check_provider_health()
```

### Diagnostic Tools

```bash
# Quick status check
python scripts/diagnostics/check_llm_providers.py

# Test specific provider
python -c "
from src.framework.llm.client import LLMClient
client = LLMClient()
print(client.get_provider_status())
"

# List all available models
python -c "
from src.framework.llm.client import LLMClient  
client = LLMClient()
print(client.list_available_models())
"
```

---

## 🏭 Production Configuration

### Environment Variable Security

```bash
# Production deployment with secrets management
# AWS Secrets Manager
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value --secret-id openai-key --query SecretString --output text)

# Azure Key Vault  
export OPENAI_API_KEY=$(az keyvault secret show --vault-name fintech-vault --name openai-key --query value -o tsv)

# HashiCorp Vault
export OPENAI_API_KEY=$(vault kv get -field=key secret/openai)
```

### Load Balancing Strategy

```python
# Example: Distribute load across providers
def intelligent_provider_selection(task_complexity):
    client = LLMClient()
    
    if task_complexity == 'simple':
        # Use cheaper provider for simple tasks
        return client.generate_response(prompt, provider='anthropic', model_type='fast')
    elif task_complexity == 'complex':
        # Use OpenAI for complex code analysis
        return client.generate_response(prompt, provider='openai', model_type='advanced')
    else:
        # Use automatic selection with failover
        return client.generate_response(prompt, model_type='default')
```

---

## 🚨 Troubleshooting

### Common Issues

**"No LLM providers configured"**
```bash
# Solution: Set at least one API key
export OPENAI_API_KEY="your-key"
# or  
export ANTHROPIC_API_KEY="your-key"
```

**Provider not responding**
```bash
# Check API key validity
python scripts/diagnostics/check_llm_providers.py

# Verify account status and billing
# Check provider console for service status
```

**High costs**
```bash
# Use cost optimization
python -c "
from src.framework.llm.client import LLMClient
client = LLMClient()
# Use fast tier for most tasks
response = client.generate_response(prompt, model_type='fast')
"
```

**Rate limiting**
```python
# Built-in retry logic handles most rate limits
# For high-volume usage, implement request throttling
import time

def throttled_analysis(items, delay=1.0):
    for item in items:
        result = client.generate_response(prompt)
        time.sleep(delay)  # Prevent rate limiting
        yield result
```

---

## 🎯 Best Practices

### Cost Management
1. **Use Fast Tier** for prototyping and simple analysis
2. **Default Tier** for most production workloads  
3. **Advanced Tier** only for critical decisions
4. **Monitor Usage** through provider dashboards

### Reliability
1. **Configure Both Providers** for maximum uptime
2. **Monitor Provider Status** in production deployments
3. **Implement Circuit Breakers** for high-volume applications
4. **Cache Results** when appropriate to reduce API calls

### Security
1. **Environment Variables Only** - never hardcode API keys
2. **Rotate Keys Regularly** - follow security best practices
3. **Monitor API Usage** - watch for unauthorized access
4. **Use Least Privilege** - restrict API key permissions

This guide provides everything needed to configure and optimize the multi-provider LLM system for both development and production environments.