# File Explorer AI Agent Framework

An enterprise-grade Python AI agent framework implementing the GAME (Goals, Actions, Memory, Environment) pattern with multi-provider LLM support, decorator-based tool registration, and automatic failover capabilities.

---

## ✅ **CURRENTLY IMPLEMENTED FEATURES**

**🌐 Multi-Provider LLM System**
- **OpenAI + Anthropic support** with unified interface
- **Model tier selection** - fast/default/advanced for cost optimization
- **Automatic failover** - seamless switching when primary provider fails
- **Environment variable configuration** for secure API key management

**🎛️ Cost-Optimized Model Selection**
- **Fast tier**: Budget-friendly models for simple tasks
- **Default tier**: Balanced performance for most use cases  
- **Advanced tier**: Premium models for complex analysis
- **Provider flexibility**: Switch between OpenAI and Anthropic based on needs

**🔧 Decorator-Based Tool System**
- `@register_tool` decorator with automatic metadata extraction
- Tag-based tool organization and filtering
- Global tool registry with automatic discovery
- JSON schema generation from Python type hints

**🤖 Specialized Agent Types**
- **File Explorer Agent**: General file system navigation and analysis
- **README Generator Agent**: Project documentation creation
- **Code Analysis Agent**: Project structure analysis and insights

**🧪 Enterprise-Grade Testing**
- Unit tests with comprehensive LLM provider coverage
- Integration tests with live API validation
- Performance tests for large directory handling
- Cross-platform compatibility validation

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd file-explorer-ai-agent-dev

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup

Configure your LLM providers (at least one required):
```bash
# Windows
set OPENAI_API_KEY=your_openai_key_here
set ANTHROPIC_API_KEY=your_anthropic_key_here

# macOS/Linux
export OPENAI_API_KEY=your_openai_key_here
export ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional: Set default provider
export DEFAULT_LLM_PROVIDER=openai  # or "anthropic"
```

### Basic Usage

```python
from src.agents.file_explorer.agent import create_file_explorer_agent

# Create and run agent (uses default provider with automatic failover)
agent = create_file_explorer_agent()
memory = agent.run("Analyze this project and create documentation")

# Get results
final_result = memory.get_memories()[-1]
print(final_result['content'])
```

### Run the Enhanced Demo

```bash
python src/examples/run_file_explorer.py
```

**Interactive Features:**
- 🔧 **Provider Selection** - Choose between OpenAI and Anthropic
- 🎛️ **Model Tier Selection** - Optimize for speed or quality
- 🤖 **Agent Type Selection** - Specialized agents for different tasks
- 📋 **Task Templates** - Pre-configured common tasks

---

## 🌐 Multi-Provider LLM Support (Currently Implemented)

### Supported Providers & Models

| Provider | Fast Tier | Default Tier | Advanced Tier |
|----------|-----------|--------------|---------------|
| **OpenAI** | GPT-3.5 Turbo | GPT-4o Mini | GPT-4o |
| **Anthropic** | Claude 3 Haiku | Claude 3.5 Sonnet | Claude 3 Opus |

### Current Implementation Usage

```python
from src.framework.llm.client import LLMClient

# Initialize client
client = LLMClient()

# Auto-select provider and model
response = client.generate_response(prompt)

# Specific provider selection
response = client.generate_response(prompt, provider='anthropic')

# Cost optimization with model tiers
response = client.generate_response(prompt, provider='openai', model_type='fast')

# Advanced model for complex tasks
response = client.generate_response(prompt, provider='anthropic', model_type='advanced')

# Custom parameters
response = client.generate_response(
    prompt, 
    provider='openai',
    model_type='default',
    temperature=0.9,
    max_tokens=2048
)
```

### Provider Status & Diagnostics (Currently Available)

```python
# Check provider availability
client = LLMClient()
status = client.get_provider_status()

for provider, info in status.items():
    emoji = "✅" if info['available'] else "❌"
    print(f"{emoji} {provider.title()}: {info['models']}")

# List available models
models = client.list_available_models()
print("Available models:", models)
```

### Automatic Failover (Currently Implemented)

The system automatically falls back to alternative providers:

```python
# If OpenAI fails, automatically tries Anthropic
# Professional logging shows failover attempts:
# 🔄 Attempting fallover: openai → anthropic
response = client.generate_response(prompt)
```

---

## 🏗️ Architecture Overview

### Project Structure
```
src/
├── agents/file_explorer/
│   ├── actions.py           # Decorated tool functions
│   └── agent.py            # Agent factory functions
├── framework/
│   ├── actions/
│   │   ├── decorators.py   # Tool registration system
│   │   ├── registry.py     # Action registries
│   │   └── action.py       # Base action class
│   ├── core/               # Core GAME components
│   ├── llm/               # Multi-provider LLM system
│   │   └── client.py      # LLMClient and LLMConfig classes
│   ├── language/          # Language processing
│   ├── memory/            # Memory management
│   └── environment/       # Action execution
├── examples/              # Usage examples with provider selection
└── scripts/
    └── diagnostics/       # Provider diagnostic tools
```

### Multi-Provider Architecture (Implemented)

```python
# LLMConfig - Provider and model management
class LLMConfig:
    def __init__(self):
        # Reads API keys from environment
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Model tier configuration
        self.models = {
            'openai': {'fast': 'gpt-3.5-turbo', 'default': 'gpt-4o-mini', ...},
            'anthropic': {'fast': 'claude-3-haiku-20240307', ...}
        }

# LLMClient - Enterprise-grade client with failover
class LLMClient:
    def generate_response(self, prompt, provider=None, model_type='default'):
        # Automatic provider selection, failover, and error handling
```

---

## 🛠️ Available Tools

| Tool | Description | Tags |
|------|-------------|------|
| `read_project_file` | Read file contents | `file_operations`, `read` |
| `list_project_files` | List Python files in current directory | `file_operations`, `list` |
| `find_project_root` | Find project root using common markers | `file_operations`, `search` |
| `list_project_files_recursive` | Recursively search for files by pattern | `file_operations`, `search`, `recursive` |
| `terminate` | End agent execution with message | `system` |

---

## 🤖 Agent Types (Currently Implemented)

### File Explorer Agent
```python
agent = create_file_explorer_agent()
```
- **Purpose**: General file exploration and documentation
- **Tools**: File operations + system tools
- **LLM Usage**: Uses current provider with automatic failover

### README Generator Agent
```python
agent = create_readme_agent()
```
- **Purpose**: Specialized README creation
- **Tools**: File operations + system tools  
- **LLM Usage**: Uses current provider configuration

### Code Analysis Agent
```python
agent = create_analysis_agent()
```
- **Purpose**: Code structure analysis
- **Tools**: File operations + search + system tools
- **LLM Usage**: Uses current provider with model tier selection

---

## 🎛️ Cost Optimization Guide (Current Implementation)

### Model Tier Selection Strategy

**Fast Tier** (`model_type='fast'`) - Use for:
- Simple file listings and basic analysis
- Quick project overviews
- Prototype development
- High-volume, low-complexity tasks

**Default Tier** (`model_type='default'`) - Use for:
- Standard documentation generation
- Balanced analysis tasks
- Most production workloads
- General-purpose agent operations

**Advanced Tier** (`model_type='advanced'`) - Use for:
- Complex architectural analysis
- High-quality documentation
- Critical business decisions
- Detailed code reviews

### Provider Selection Guide

**OpenAI** - Choose for:
- Fast response times
- Strong code understanding
- Function calling reliability
- Familiar development experience

**Anthropic** - Choose for:
- Longer context windows
- Detailed analysis capabilities
- Alternative perspective
- Claude's reasoning strengths

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run LLM-specific tests
pytest tests/unit/test_llm_client.py -v        # LLM client unit tests
pytest tests/integration/test_llm_integration.py -v  # Live provider tests

# Run with coverage
pytest --cov=src --cov-report=html
```

### Test Structure

- **Unit Tests**: Test LLM client, file operations, and components in isolation
- **Integration Tests**: Test live LLM provider integration (requires API keys)
- **Performance Tests**: Test with large directory structures
- **Cross-Platform Tests**: Ensure Windows/macOS/Linux compatibility

### Provider Testing

```bash
# Test with specific providers
export OPENAI_API_KEY="your-key"
pytest tests/integration/test_llm_integration.py::TestOpenAIIntegration -v

export ANTHROPIC_API_KEY="your-key" 
pytest tests/integration/test_llm_integration.py::TestAnthropicIntegration -v
```

---

## 📋 Requirements

- **Python 3.8+**
- **LiteLLM** for multi-provider LLM support
- **At least one LLM provider API key** (OpenAI or Anthropic)
- **Anthropic SDK** for Claude API support
- **Pytest** for testing

---

## 💡 Usage Examples (Current Implementation)

### Basic Multi-Provider Usage

```python
from src.framework.llm.client import LLMClient
from src.agents.file_explorer.agent import create_file_explorer_agent

# Check provider status
client = LLMClient()
status = client.get_provider_status()
for provider, info in status.items():
    print(f"{provider}: {'✅' if info['available'] else '❌'}")

# Use agent with current implementation
agent = create_file_explorer_agent()
memory = agent.run("Analyze this project structure")
```

### Custom LLM Configuration

```python
from src.framework.core.agent import Agent
from src.framework.llm.client import LLMClient

# Create client with specific configuration
client = LLMClient()

def cost_optimized_generate_response(prompt):
    """Use fast models for cost efficiency"""
    return client.generate_response(prompt, model_type='fast')

def premium_generate_response(prompt):
    """Use advanced models for quality"""
    return client.generate_response(prompt, model_type='advanced')

# Create agents with different strategies
# (Requires custom agent setup - see migration guide)
```

### Error Handling

```python
from src.framework.llm.client import LLMClient

try:
    client = LLMClient()
    response = client.generate_response(prompt, provider='openai')
except ValueError as e:
    if "No LLM providers configured" in str(e):
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    elif "not available" in str(e):
        print("Selected provider not configured")
except Exception as e:
    print(f"LLM error (automatic fallback attempted): {e}")
```

---

## 📋 **EXAMPLE PATTERNS YOU COULD BUILD**

*These examples show how to extend the current implementation - not currently included in the codebase.*

### Dynamic Model Selection Example

```python
# Example pattern - NOT currently implemented
def smart_model_selection(task_description, prompt):
    """Example: Select model tier based on task complexity"""
    client = LLMClient()
    
    if any(word in task_description.lower() for word in ['list', 'show', 'find']):
        return client.generate_response(prompt, model_type='fast')
    elif any(word in task_description.lower() for word in ['analyze', 'design']):
        return client.generate_response(prompt, model_type='advanced')
    else:
        return client.generate_response(prompt, model_type='default')

# How you could use it
task = "Analyze the project architecture"
response = smart_model_selection(task, prompt)
```

### Cost Monitoring Example

```python
# Example pattern - NOT currently implemented
class CostMonitor:
    """Example: Monitor LLM usage costs"""
    
    def __init__(self):
        self.client = LLMClient()
        self.usage_log = []
    
    def generate_with_monitoring(self, prompt, **kwargs):
        """Example: Add cost monitoring to LLM calls"""
        response = self.client.generate_response(prompt, **kwargs)
        
        # Log usage for cost tracking
        self.usage_log.append({
            'provider': kwargs.get('provider', 'auto'),
            'model_tier': kwargs.get('model_type', 'default'),
            'timestamp': time.time()
        })
        
        return response

# How you could use it
monitor = CostMonitor()
response = monitor.generate_with_monitoring(prompt, model_type='fast')
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
- **Automatic model downgrading** when approaching limits

### Enterprise Features
- **Load balancing** across multiple provider instances
- **Rate limiting** and throttling controls
- **Advanced monitoring** with metrics and alerting
- **Audit logging** for compliance requirements

### GUI Interface
- **Web dashboard** for provider management
- **Visual model selection** interface
- **Real-time monitoring** dashboards
- **Configuration management** UI

---

## 🔧 Configuration

### Environment Variables
```bash
# Required (at least one)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional configuration
export DEFAULT_LLM_PROVIDER="openai"  # or "anthropic"
```

### Project Structure Requirements
The framework automatically detects project roots using these markers:
- `.git/` directory
- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `.gitignore`

---

## 🛡️ Security Best Practices (Currently Implemented)

### API Key Management
- ✅ **Environment variables only** - No hardcoded keys in source code
- ✅ **Secure validation** - Keys checked without exposure
- ✅ **Professional logging** - No sensitive data in logs
- ✅ **Git exclusion** - API keys never committed to version control

### Production Deployment
```bash
# Use secure environment variable management
export OPENAI_API_KEY=$(vault kv get -field=key secret/openai)
export ANTHROPIC_API_KEY=$(vault kv get -field=key secret/anthropic)

# Set production defaults
export DEFAULT_LLM_PROVIDER="openai"
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue: "No LLM providers configured"**
```bash
# Solution: Set at least one API key
export OPENAI_API_KEY="your-key"
# or
export ANTHROPIC_API_KEY="your-key"
```

**Issue: Provider not responding**
```bash
# Solution: Check API key validity and account status
python scripts/diagnostics/check_llm_providers.py
```

**Issue: High costs**
```bash
# Solution: Use fast tier for simple tasks
# client.generate_response(prompt, model_type='fast')
```

### Diagnostic Tools

```bash
# Check provider status
python scripts/diagnostics/check_llm_providers.py

# Run comprehensive tests
pytest tests/unit/test_llm_client.py -v

# Check live API connectivity
pytest tests/integration/test_llm_integration.py -v
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass (including LLM provider tests)
5. Update documentation
6. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install test dependencies
pip install -r requirements-test.txt

# Run full test suite
pytest tests/ -v

# Check code coverage
pytest --cov=src --cov-report=html
```

---

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with the GAME framework pattern for reliable, cost-effective, enterprise-grade AI agent development.**

**🌟 Key Benefits:**
- **Vendor Independence**: Never locked into a single LLM provider
- **Cost Optimization**: Right-size models for each task
- **Enterprise Reliability**: Automatic failover and professional error handling
- **Professional Quality**: Comprehensive testing and documentation suitable for portfolio demonstration