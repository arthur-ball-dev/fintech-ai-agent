# API Documentation

## File Explorer Actions Reference

### Enhanced Actions (v0.2.0)

#### `list_project_files_recursive`

**Purpose**: Recursively discover files throughout entire project structure with intelligent project root detection.

**Function Signature**:
```python
def list_project_files_recursive(
    root_dir: str = None, 
    pattern: str = "*.py", 
    max_depth: int = None
) -> List[str]
```

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `root_dir` | `str` | `None` | Starting directory for search. When `None`, automatically detects project root using common markers (`.git`, `requirements.txt`, etc.) |
| `pattern` | `str` | `"*.py"` | File pattern to match using glob syntax (e.g., `"*.csv"`, `"*.md"`, `"*"`) |
| `max_depth` | `int` | `None` | Maximum directory depth to search. `None` for unlimited depth |

**Returns**: 
- `List[str]`: Sorted list of relative file paths matching the specified pattern

**Examples**:
```python
# Find all Python files from project root
files = list_project_files_recursive()

# Find all CSV files with explicit root directory  
data_files = list_project_files_recursive("./data", "*.csv")

# Find all files with depth limit for performance
limited_search = list_project_files_recursive(None, "*", max_depth=2)
```

**Project Root Detection Logic**:
The function searches upward from the starting location for these markers:
1. `.git` directory (version control root)
2. `requirements.txt` (Python project dependencies)
3. `pyproject.toml` (modern Python project)
4. `setup.py` (traditional Python package)
5. `.gitignore` (project boundary indicator)

**Directory Filtering**:
Automatically excludes these directories from search:
- `.git` (version control)
- `__pycache__` (Python bytecode)
- `.venv`, `venv`, `ENV` (virtual environments)
- `node_modules` (Node.js dependencies)
- Any directory starting with `.` (hidden directories)

**Error Handling**:
- Returns empty list on permission errors
- Logs warnings for inaccessible directories
- Gracefully handles broken symlinks
- Continues search despite individual directory failures

**Performance Considerations**:
- Use `max_depth` parameter for large projects
- Pattern specificity improves performance (`"*.py"` vs `"*"`)
- Automatic exclusion of common non-relevant directories

---

### Core Actions (v0.1.0)

#### `list_project_files`

**Purpose**: Lists Python files in current working directory only (backward compatibility).

**Function Signature**:
```python
def list_project_files() -> List[str]
```

**Parameters**: None

**Returns**: 
- `List[str]`: Sorted list of Python files (*.py) in current directory only

**Use Case**: Quick local file discovery when you know you're in the target directory.

#### `read_project_file`

**Purpose**: Read and return complete contents of a specified file.

**Function Signature**:
```python
def read_project_file(name: str) -> str
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Relative or absolute path to file to read |

**Returns**: 
- `str`: Complete file contents as string

**Error Handling**:
- Raises `FileNotFoundError` if file doesn't exist
- Raises `PermissionError` if file not readable
- Raises `UnicodeDecodeError` for non-text files

**Examples**:
```python
# Read specific file
content = read_project_file("src/agents/file_explorer/agent.py")

# Read configuration file
config = read_project_file("requirements.txt")
```

#### `terminate`

**Purpose**: End agent session with final message to user.

**Function Signature**:
```python
def terminate(message: str) -> str
```

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Final message to display to user |

**Returns**: 
- `str`: Formatted termination message

**Use Case**: Proper session completion with results summary.

---

## Action Registry Integration

### Registering Actions

```python
from src.framework.actions.registry import ActionRegistry
from src.agents.file_explorer.actions import create_file_explorer_actions

# Initialize registry
registry = ActionRegistry()

# Register all file explorer actions
for action in create_file_explorer_actions():
    registry.register(action)

# Access specific action
recursive_action = registry.get_action("list_project_files_recursive")
```

### Action Metadata

Each action includes comprehensive metadata for LLM function calling:

```python
{
    "name": "list_project_files_recursive",
    "description": "Recursively lists files matching a pattern...",
    "parameters": {
        "type": "object",
        "properties": {
            "root_dir": {"type": "string", "description": "...", "default": None},
            "pattern": {"type": "string", "description": "...", "default": "*.py"},
            "max_depth": {"type": "integer", "description": "..."}
        },
        "required": []
    },
    "terminal": False
}
```

---

## Error Handling Patterns

### Graceful Degradation
```python
try:
    files = list_project_files_recursive(root_dir, pattern)
except PermissionError:
    # Fallback to current directory search
    files = list_project_files()
except Exception as e:
    # Log error and return empty result
    print(f"Search failed: {e}")
    files = []
```

### Validation Best Practices
```python
# Validate inputs before processing
if root_dir and not os.path.exists(root_dir):
    raise ValueError(f"Directory not found: {root_dir}")

if max_depth is not None and max_depth < 0:
    raise ValueError("max_depth must be non-negative")
```

---

## Integration Examples

### FinTech Use Cases

```python
# Discover all data files for analysis
data_files = list_project_files_recursive("./data", "*.csv")
for file in data_files:
    content = read_project_file(file)
    # Process trading data, portfolio information, etc.

# Find all configuration files
config_files = list_project_files_recursive(None, "*.json")
# Analyze system configurations, API settings, etc.

# Locate all documentation
docs = list_project_files_recursive("./docs", "*.md") 
# Generate documentation summaries, compliance reports, etc.
```

### Enterprise Workflow Integration

```python
# CI/CD Pipeline Integration
def analyze_project_structure():
    """Analyze entire project for CI/CD reporting"""
    python_files = list_project_files_recursive(None, "*.py")
    test_files = list_project_files_recursive("./tests", "test_*.py")
    
    return {
        "source_files": len(python_files),
        "test_files": len(test_files),
        "test_coverage": len(test_files) / len(python_files) * 100
    }
```