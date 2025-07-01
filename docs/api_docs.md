# API Documentation

Complete reference for the File Explorer AI Agent Framework based on actual implementation.

## Table of Contents
1. [Decorator System](#decorator-system)
2. [Action Registry](#action-registry)
3. [Core Framework](#core-framework)
4. [Available Tools](#available-tools)
5. [Agent Factories](#agent-factories)
6. [LLM Integration](#llm-integration)

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

## LLM Integration

### LLM Client

```python
def generate_response(prompt: Prompt, model: str = "gpt-4o") -> str
```

**Implementation:** Uses LiteLLM for multi-provider support  
**Parameters:**
- `prompt`: Prompt object with messages and tools
- `model`: Model identifier

**Supported Models (via LiteLLM):**
- OpenAI: `"gpt-4o"`, `"gpt-4o-mini"`
- Anthropic: `"claude-3-5-sonnet-20241022"`
- And others supported by LiteLLM

**Response Handling:**
- With tools: Returns JSON string with tool call
- Without tools: Returns text response

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

### Basic Agent Creation and Execution

```python
from src.agents.file_explorer.agent import create_file_explorer_agent

# Create agent
agent = create_file_explorer_agent()

# Execute task
memory = agent.run("Analyze this project structure")

# Get results
results = memory.get_memories()
final_result = results[-1] if results else None
```

### Custom Registry Creation

```python
from src.framework.actions.registry import PythonActionRegistry

# File operations only
file_registry = PythonActionRegistry(tags=["file_operations"])

# Search-focused tools
search_registry = PythonActionRegistry(tags=["search"])

# Specific tools
custom_registry = PythonActionRegistry(
    tool_names=["read_project_file", "list_project_files_recursive"]
)
```

### Creating Custom Tools

```python
from src.framework.actions.decorators import register_tool

@register_tool(tags=["analysis", "custom"])
def count_lines_of_code(file_path: str) -> int:
    """Count lines of code in a file."""
    with open(file_path, 'r') as f:
        return len(f.readlines())

# Tool is automatically available to agents with "analysis" or "custom" tags
```

## Error Handling

### Common Error Patterns

**File Not Found:**
```python
try:
    content = read_project_file("nonexistent.py")
except FileNotFoundError:
    # Handle missing file
```

**Tool Not Found:**
```python
action, invocation = agent.get_action(response)
if not action:
    print(f"Unknown action: {invocation['tool']}")
```

**LLM Response Parsing:**
```python
# AgentFunctionCallingActionLanguage.parse_response() handles this
try:
    return json.loads(response)
except Exception:
    return {"tool": "terminate", "args": {"message": response}}
```

## Configuration

### Environment Variables

```bash
# Required for LLM functionality
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"  # Optional
```

### Agent Configuration

```python
# Custom goals
custom_goals = [
    Goal(priority=1, name="Task", description="Complete the task"),
    Goal(priority=2, name="Report", description="Report results")
]

# Custom registry
registry = PythonActionRegistry(tags=["file_operations", "system"])

# Custom agent
agent = Agent(
    goals=custom_goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=registry,
    generate_response=lambda p: generate_response(p, model="gpt-4o-mini"),
    environment=Environment()
)
```

This API documentation accurately reflects your current implementation and can serve as a reference for understanding and extending the framework.