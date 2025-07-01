# File Explorer AI Agent Framework

A Python-based AI agent framework implementing the GAME (Goals, Actions, Memory, Environment) pattern with decorator-based tool registration and LLM-agnostic design using LiteLLM.

## 🎯 Key Features

**🔧 Decorator-Based Tool System**
- `@register_tool` decorator with automatic metadata extraction
- Tag-based tool organization and filtering
- Global tool registry with automatic discovery
- JSON schema generation from Python type hints

**🤖 Specialized Agent Types**
- **File Explorer Agent**: General file system navigation and analysis
- **README Generator Agent**: Project documentation creation
- **Code Analysis Agent**: Project structure analysis and insights

**🌐 LLM-Agnostic Architecture**
- Multi-provider support via LiteLLM (OpenAI, Anthropic, Google, etc.)
- Simple model switching with parameter support
- Unified interface across different LLM providers

**🧪 Comprehensive Testing**
- Unit tests for individual components
- Integration tests for framework interaction
- Performance tests for large directory handling
- Cross-platform compatibility validation

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

Set your API key:
```bash
# Windows
set OPENAI_API_KEY=your_openai_key_here

# macOS/Linux
export OPENAI_API_KEY=your_openai_key_here
```

### Basic Usage

```python
from src.agents.file_explorer.agent import create_file_explorer_agent

# Create and run agent
agent = create_file_explorer_agent()
memory = agent.run("Analyze this project and create documentation")

# Get results
final_result = memory.get_memories()[-1]
print(final_result['content'])
```

### Run the Demo

```bash
python src/examples/run_file_explorer.py
```

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
│   ├── llm/               # LLM integration (LiteLLM)
│   ├── language/          # Language processing
│   ├── memory/            # Memory management
│   └── environment/       # Action execution
└── examples/              # Usage examples
```

### Decorator System Example

```python
@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Read a file from the project"""
    with open(name, "r", encoding='utf-8', errors='ignore') as f:
        return f.read()
```

### Tag-Based Registry Filtering

```python
from src.framework.actions.registry import PythonActionRegistry

# Create registry with specific tools
file_registry = PythonActionRegistry(tags=["file_operations"])
search_registry = PythonActionRegistry(tags=["search"])
complete_registry = PythonActionRegistry(tags=["file_operations", "system"])
```

## 🛠️ Available Tools

| Tool | Description | Tags |
|------|-------------|------|
| `read_project_file` | Read file contents | `file_operations`, `read` |
| `list_project_files` | List Python files in current directory | `file_operations`, `list` |
| `find_project_root` | Find project root using common markers | `file_operations`, `search` |
| `list_project_files_recursive` | Recursively search for files by pattern | `file_operations`, `search`, `recursive` |
| `terminate` | End agent execution with message | `system` |

## 🤖 Agent Types

### File Explorer Agent
```python
agent = create_file_explorer_agent()
```
- **Purpose**: General file exploration and documentation
- **Tools**: File operations + system tools
- **Use Cases**: Project analysis, documentation generation

### README Generator Agent
```python
agent = create_readme_agent()
```
- **Purpose**: Specialized README creation
- **Tools**: File operations + system tools  
- **Use Cases**: Automated project documentation

### Code Analysis Agent
```python
agent = create_analysis_agent()
```
- **Purpose**: Code structure analysis
- **Tools**: File operations + search + system tools
- **Use Cases**: Architecture review, improvement suggestions

## 🌐 LLM Provider Support

The framework uses LiteLLM for multi-provider support:

```python
from src.framework.llm.client import generate_response

# Different models/providers
response = generate_response(prompt, model="gpt-4o")           # OpenAI
response = generate_response(prompt, model="gpt-4o-mini")     # OpenAI (cheaper)
response = generate_response(prompt, model="claude-3-5-sonnet-20241022")  # Anthropic
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests

# Run with coverage
pytest --cov=src
```

### Test Structure

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test framework component interaction
- **Performance Tests**: Test with large directory structures
- **Edge Case Tests**: Test error handling and unusual scenarios

## 📋 Requirements

- **Python 3.8+**
- **LiteLLM** for multi-provider LLM support
- **OpenAI API key** (or other LLM provider key)
- **Pytest** for testing

## 💡 Usage Examples

### Creating Custom Tools

```python
from src.framework.actions.decorators import register_tool

@register_tool(tags=["analysis"])
def count_lines(file_path: str) -> int:
    """Count lines in a file."""
    with open(file_path, 'r') as f:
        return len(f.readlines())

# Tool automatically available to agents with "analysis" tag
```

### Custom Agent Creation

```python
from src.framework.core.agent import Agent
from src.framework.core.goals import Goal
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import generate_response

# Define goals
goals = [
    Goal(priority=1, name="Task", description="Complete the analysis task"),
    Goal(priority=2, name="Report", description="Provide results")
]

# Create registry with specific tools
registry = PythonActionRegistry(tags=["file_operations", "analysis"])

# Create custom agent
agent = Agent(
    goals=goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=registry,
    generate_response=generate_response,
    environment=Environment()
)
```

### Different Model Usage

```python
# Create agents with different models
openai_agent = create_file_explorer_agent()  # Uses default gpt-4o
# Custom model usage requires modifying agent creation

# For custom models, create agent manually:
custom_agent = Agent(
    goals=goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=registry,
    generate_response=lambda p: generate_response(p, model="gpt-4o-mini"),
    environment=Environment()
)
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
export OPENAI_API_KEY="your-openai-key"

# Optional (for other providers)
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### Project Structure Requirements
The framework automatically detects project roots using these markers:
- `.git/` directory
- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `.gitignore`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests before committing
pytest tests/
```

## 📄 License

MIT License - see LICENSE file for details.

## 🚀 Future Enhancements

- Additional LLM provider integrations
- More specialized agent types
- Enhanced tool categorization
- Performance optimizations
- GUI interface for agent interaction

---

**Built with the GAME framework pattern for reliable, extensible AI agent development.**