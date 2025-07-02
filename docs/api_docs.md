# API Documentation

Complete reference for the File Explorer AI Agent Framework with Multi-Provider LLM Support.

## Table of Contents
1. [Multi-Provider LLM System](#multi-provider-llm-system)
2. [Decorator System](#decorator-system)
3. [Action Registry](#action-registry)
4. [Core Framework](#core-framework)
5. [Available Tools](#available-tools)
6. [Agent Factories](#agent-factories)
7. [Legacy LLM Integration](#legacy-llm-integration)

## Multi-Provider LLM System

### LLMConfig Class

```python
class LLMConfig:
    def __init__(self)
    def get_model_name(self, provider: str, model_type: str = 'default') -> str
    def validate_provider(self, provider: str) -> bool
    def get_available_providers(self) -> List[str]
```

**Configuration Management:**
- **API Keys**: Reads from system environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- **Provider Selection**: Configurable default provider via `DEFAULT_LLM_PROVIDER`
- **Model Tiers**: Cost-optimized model selection per provider

**Model Tier System:**
```python
models = {
    'openai': {
        'fast': 'gpt-3.5-turbo',        # Cheapest, fastest
        'default': 'gpt-4o-mini',       # Balanced cost/performance  
        'advanced': 'gpt-4o'            # Highest quality, most expensive
    },
    'anthropic': {
        'fast': 'claude-3-haiku-20240307',           # Cheapest, fastest
        'default': 'claude-3-5-sonnet-20241022',     # Balanced cost/performance
        'advanced': 'claude-3-opus-20240229'         # Highest quality, most expensive
    }
}
```

### LLMClient Class

```python
class LLMClient:
    def __init__(self)
    def generate_response(
        self, 
        prompt: Prompt, 
        provider: Optional[str] = None,
        model: Optional[str] = None,
        model_type: str = 'default',
        **kwargs
    ) -> str
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]
    def list_available_models(self, provider: Optional[str] = None) -> Dict[str, List[str]]
```

**Enterprise Features:**
- **Multi-Provider Support**: OpenAI and Anthropic with extensible architecture
- **Automatic Failover**: Falls back to alternative provider on failure
- **Cost Optimization**: Model tier selection for different use cases
- **Professional Logging**: Detailed error reporting with emoji indicators
- **Configuration Validation**: Validates API keys and provider availability

**Example Usage:**
```python
# Initialize client
client = LLMClient()

# Basic usage (auto-selects provider and model)
response = client.generate_response(prompt)

# Specific provider selection
response = client.generate_response(prompt, provider='anthropic')

# Model tier selection
response = client.generate_response(prompt, provider='openai', model_type='fast')

# Custom model override
response = client.generate_response(prompt, provider='anthropic', model='claude-3-opus-20240229')

# With custom parameters
response = client.generate_response(
    prompt, 
    provider='openai', 
    model_type='advanced',
    temperature=0.9,
    max_tokens=2048
)
```

**Provider Status Checking:**
```python
client = LLMClient()

# Get detailed provider status
status = client.get_provider_status()
# Returns:
# {
#     'openai': {
#         'available': True,
#         'models': {'fast': 'gpt-3.5-turbo', 'default': 'gpt-4o-mini', 'advanced': 'gpt-4o'},
#         'is_default': True
#     },
#     'anthropic': {
#         'available': True,
#         'models': {'fast': 'claude-3-haiku-20240307', ...},
#         'is_default': False
#     }
# }

# List available models
models = client.list_available_models()
# Returns: {'openai': ['gpt-3.5-turbo', 'gpt-4o-mini', 'gpt-4o'], 'anthropic': [...]}
```

**Error Handling and Fallback:**
```python
# Automatic fallback example
try:
    # Primary provider attempt
    response = client.generate_response(prompt, provider='openai')
except Exception:
    # Automatically tries fallback provider (anthropic)
    # Logs: "🔄 Attempting fallback: openai → anthropic"
    pass
```

### Environment Variable Configuration

**Required Environment Variables:**
```bash
# At least one provider required
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional configuration
export DEFAULT_LLM_PROVIDER="openai"  # or "anthropic"
```

**Validation:**
```python
config = LLMConfig()

# Check specific provider
if config.validate_provider('openai'):
    print("OpenAI configured")

# Get all available providers
available = config.get_available_providers()  # ['openai', 'anthropic']
```

## Decorator System

### Tool Registration Decorator

```python
@register_tool(
    tool_name: str = None,
    description: str = None,
    parameters_override: dict = None,
    terminal: bool = False,
    tags: List[str] = None
)
```

**Parameters:**
- `tool_name`: Tool identifier (defaults to function name)
- `description`: Tool description (defaults to function docstring)
- `parameters_override`: Custom parameter schema (defaults to auto-generated from type hints)
- `terminal`: Whether tool terminates agent execution
- `tags`: List of tags for categorization and filtering

**Example:**
```python
@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Read a file from the project"""
    with open(name, "r", encoding='utf-8', errors='ignore') as f:
        return f.read()
```

### Metadata Functions

#### `get_tool_metadata`
```python
def get_tool_metadata(
    func, 
    tool_name=None, 
    description=None, 
    parameters_override=None, 
    terminal=False, 
    tags=None
) -> dict
```

Extracts metadata from a function for tool registration. Automatically generates JSON schema from type hints.

#### `to_llm_tools`
```python
def to_llm_tools(tools_metadata: List[dict]) -> List[dict]
```

Converts tool metadata to OpenAI function calling format.

### Global Tool Registry

The decorator system maintains global dictionaries:

```python
# Global registries (from src.framework.actions.decorators)
tools = {}          # tool_name -> tool_metadata
tools_by_tag = {}   # tag -> [tool_names]
```

## Action Registry

### ActionRegistry (Base Class)

```python
class ActionRegistry:
    def __init__(self)
    def register(self, action: Action)
    def get_action(self, name: str) -> Optional[Action]
    def get_actions(self) -> List[Action]
```

### PythonActionRegistry (Enhanced)

```python
class PythonActionRegistry(ActionRegistry):
    def __init__(self, tags: List[str] = None, tool_names: List[str] = None)
```

**Parameters:**
- `tags`: Only include tools with ANY of these tags
- `tool_names`: Only include these specific tool names

**How it works:**
1. Reads from global `tools` dictionary populated by decorators
2. Filters tools based on tags or tool_names in constructor
3. Creates `Action` objects and registers them with base class

**Example:**
```python
# Include only file operation tools
file_registry = PythonActionRegistry(tags=["file_operations"])

# Include file operations AND system tools
complete_registry = PythonActionRegistry(tags=["file_operations", "system"])

# Include specific tools only
custom_registry = PythonActionRegistry(tool_names=["read_project_file", "terminate"])
```

## Core Framework

### Agent Class

```python
class Agent:
    def __init__(self,
                 goals: List[Goal],
                 agent_language: AgentLanguage,
                 action_registry: ActionRegistry,
                 generate_response: Callable[[Prompt], str],
                 environment: Environment)
    
    def run(self, user_input: str, memory: Optional[Memory] = None, max_iterations: int = 50) -> Memory
```

**Key Methods:**
- `run()`: Main execution loop with goal-driven iteration
- `construct_prompt()`: Builds LLM prompt from goals, memory, and actions
- `get_action()`: Parses LLM response and retrieves corresponding action
- `should_terminate()`: Checks if agent should stop execution

### Goal Class

```python
@dataclass(frozen=True)
class Goal:
    priority: int
    name: str
    description: str
```

### Memory Class

```python
class Memory:
    def add_memory(self, memory: dict)
    def get_memories(self, limit: Optional[int] = None) -> List[Dict]
    def copy_without_system_memories(self) -> Memory
```

**Memory Types:**
- `"user"`: User input/requests
- `"assistant"`: Agent responses/decisions
- `"environment"`: Tool execution results
- `"system"`: System messages

### Environment Class

```python
class Environment:
    def execute_action(self, action: Action, args: dict) -> dict
    def format_result(self, result: Any) -> dict
```

**Returns formatted result:**
```python
{
    "tool_executed": True,
    "result": "actual_result",
    "timestamp": "2024-01-01T12:00:00+0000"
}
```

## Available Tools

These are the actual tools implemented in `src/agents/file_explorer/actions.py`:

### File Operations

#### `read_project_file`
```python
@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str
```
**Description:** Read a file from the project  
**Parameters:** `name` - File path to read  
**Returns:** File contents as string  

#### `list_project_files`
```python
@register_tool(tags=["file_operations", "list"])
def list_project_files() -> List[str]
```
**Description:** Lists Python files in current directory only  
**Returns:** Sorted list of .py files in current directory  

#### `find_project_root`
```python
@register_tool(tags=["file_operations", "search"])
def find_project_root(start_path: str = ".") -> str
```
**Description:** Find project root by looking for common markers  
**Parameters:** `start_path` - Directory to start searching from  
**Returns:** Path to project root directory  
**Markers:** `.git`, `pyproject.toml`, `setup.py`, `requirements.txt`, `.gitignore`

#### `list_project_files_recursive`
```python
@register_tool(tags=["file_operations", "search", "recursive"])
def list_project_files_recursive(
    root_dir: str = None, 
    pattern: str = "*.py",
    max_depth: int = None
) -> List[str]
```
**Description:** Recursively search for files matching pattern  
**Parameters:**
- `root_dir`: Starting directory (None = auto-detect project root)
- `pattern`: File pattern to match (default: "*.py")
- `max_depth`: Maximum search depth (None = unlimited)

**Returns:** List of relative file paths matching pattern  
**Excludes:** `.git`, `__pycache__`, `.venv`, `node_modules`, hidden directories

### System Tools

#### `terminate`
```python
@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str
```
**Description:** Terminates agent execution with final message  
**Parameters:** `message` - Final message to return  
**Returns:** Message with termination note  

## Agent Factories

All located in `src/agents/file_explorer/agent.py`:

### `create_file_explorer_agent()`
```python
def create_file_explorer_agent() -> Agent
```

**Purpose:** General file exploration and documentation  
**Tools:** `["file_operations", "system"]` tags  
**Goals:**
1. Gather Information - Read project files
2. Generate Documentation - Create documentation
3. Terminate - Complete with results

### `create_readme_agent()`
```python
def create_readme_agent() -> Agent
```

**Purpose:** Specialized README generation  
**Tools:** `["file_operations", "system"]` tags  
**Goals:**
1. Gather Information - Deep project understanding
2. Terminate - Provide complete README

### `create_analysis_agent()`
```python
def create_analysis_agent() -> Agent
```

**Purpose:** Code analysis and architecture insights  
**Tools:** `["file_operations", "search", "system"]` tags  
**Goals:**
1. Code Analysis - Analyze structure
2. Generate Analysis - Provide insights and recommendations

## Legacy LLM Integration

### Backward Compatibility Function

```python
def generate_response(prompt: Prompt, model: str = "gpt-4o") -> str
```

**Implementation:** Maintains original function signature while providing enhanced capabilities
**Smart Provider Detection:** Automatically detects provider based on model name
- Models containing `"claude"` → Anthropic provider
- Models containing `"gpt"` → OpenAI provider
- Other models → Default provider

**Example:**
```python
# Legacy usage still works
response = generate_response(prompt, model="gpt-4o")
response = generate_response(prompt, model="claude-3-5-sonnet-20241022")

# Automatically routes to correct provider
```

### Prompt Class

```python
@dataclass
class Prompt:
    messages: List[Dict] = field(default_factory=list)
    tools: List[Dict] = field(default_factory=list)
```

### Language Processing

```python
class AgentFunctionCallingActionLanguage(AgentLanguage):
    def construct_prompt(self, actions, environment, goals, memory) -> Prompt
    def parse_response(self, response: str) -> dict
```

**Response Format:**
```python
{
    "tool": "tool_name",
    "args": {"param1": "value1", "param2": "value2"}
}
```

## Usage Examples

### Multi-Provider Agent Creation

```python
from src.framework.llm.client import LLMClient
from src.agents.file_explorer.agent import create_file_explorer_agent

# Create client with specific provider
client = LLMClient()

# Use with existing agent factories (uses default provider)
agent = create_file_explorer_agent()
memory = agent.run("Analyze this project structure")

# Check which providers are available
status = client.get_provider_status()
for provider, info in status.items():
    print(f"{provider}: {'✅' if info['available'] else '❌'}")
```

### Custom Agent with Specific Provider

```python
from src.framework.core.agent import Agent
from src.framework.core.goals import Goal
from src.framework.actions.registry import PythonActionRegistry
from src.framework.language.function_calling import AgentFunctionCallingActionLanguage
from src.framework.environment.environment import Environment
from src.framework.llm.client import LLMClient

# Create LLM client with specific configuration
client = LLMClient()

# Custom generate_response function with provider selection
def custom_generate_response(prompt):
    return client.generate_response(
        prompt, 
        provider='anthropic',  # Force Anthropic
        model_type='advanced'  # Use best model
    )

# Create custom agent
custom_goals = [Goal(priority=1, name="Task", description="Complete analysis")]
registry = PythonActionRegistry(tags=["file_operations", "system"])

agent = Agent(
    goals=custom_goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=registry,
    generate_response=custom_generate_response,
    environment=Environment()
)
```

### Cost Optimization Examples

```python
client = LLMClient()

# Fast, cheap responses for simple tasks
quick_response = client.generate_response(
    prompt, 
    provider='openai', 
    model_type='fast'  # gpt-3.5-turbo
)

# Balanced performance for most tasks
normal_response = client.generate_response(
    prompt, 
    provider='anthropic', 
    model_type='default'  # claude-3-5-sonnet
)

# High-quality responses for complex tasks
advanced_response = client.generate_response(
    prompt, 
    provider='openai', 
    model_type='advanced'  # gpt-4o
)
```

## Error Handling

### Provider Availability Errors

```python
try:
    client = LLMClient()
except ValueError as e:
    print(f"No LLM providers configured: {e}")
    # Handle missing API keys
```

### Provider-Specific Errors

```python
try:
    response = client.generate_response(prompt, provider='anthropic')
except ValueError as e:
    print(f"Provider not available: {e}")
    # Handle invalid provider selection
```

### Automatic Fallback Handling

```python
# Fallback is automatic - no special handling needed
response = client.generate_response(prompt)
# If primary provider fails, automatically tries fallback
# Logs fallback attempts with professional formatting
```

## Diagnostic Tools

### Provider Status Checking

```python
# Use the diagnostic script
# python scripts/diagnostics/check_llm_providers.py

# Or check programmatically
client = LLMClient()
status = client.get_provider_status()

for provider, info in status.items():
    print(f"{provider}: {info}")
```

### Model Listing

```python
client = LLMClient()

# List all available models
all_models = client.list_available_models()

# List models for specific provider
openai_models = client.list_available_models('openai')
```

## Configuration

### Environment Variables

```bash
# Required (at least one)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional
export DEFAULT_LLM_PROVIDER="openai"  # or "anthropic"
```

### Provider Priority Configuration

```python
# Set default provider via environment
os.environ['DEFAULT_LLM_PROVIDER'] = 'anthropic'

# Or programmatically
config = LLMConfig()
config.default_provider = 'anthropic'
```

This enhanced API documentation reflects the complete multi-provider LLM system implementation with enterprise-grade features for professional AI agent development.