import os
import fnmatch
from typing import List
from src.framework.actions.action import Action

def read_project_file(name: str) -> str:
    with open(name, "r") as f:
        return f.read()

def list_project_files() -> List[str]:
    all_files = os.listdir(".")
    print(f"the list of project files in the listdir is {all_files}")
    return sorted([file for file in os.listdir(".") if file.endswith(".py")])

def find_project_root(start_path: str = ".") -> str:
    """
    Find project root by looking for common project markers

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root directory
    """
    current = os.path.abspath(start_path)

    # Look for common project root indicators
    markers = ['.git', 'pyproject.toml', 'setup.py', 'requirements.txt', '.gitignore']

    while current != os.path.dirname(current):  # Not at filesystem root
        if any(os.path.exists(os.path.join(current, marker)) for marker in markers):
            return current
        current = os.path.dirname(current)

    # Fallback to current directory if no markers found
    return os.path.abspath(start_path)


def list_project_files_recursive(root_dir: str = None, pattern: str = "*.py",
                                 max_depth: int = None) -> List[str]:
    """
    Recursively search for files matching pattern throughout project structure

    Args:
        root_dir: Starting directory for search (None = auto-detect project root)
        pattern: File pattern to match (default: "*.py")
        max_depth: Maximum depth to search (None for unlimited)

    Returns:
        List of relative file paths matching the pattern

    Examples:
        - list_project_files_recursive() -> All Python files from project root
        - list_project_files_recursive("./src") -> Python files in src/ directory
        - list_project_files_recursive(None, "*.csv") -> All CSV files from project root
    """
    # Auto-detect project root if not specified
    if root_dir is None:
        root_dir = find_project_root()
        print(f"Auto-detected project root: {root_dir}")

    matches = []
    root_dir = os.path.abspath(root_dir)

    try:
        for root, dirs, files in os.walk(root_dir):
            # Calculate current depth for depth limiting
            if max_depth is not None:
                current_depth = root.replace(root_dir, '').count(os.sep)
                if current_depth >= max_depth:
                    dirs.clear()  # Don't descend further
                    continue

            # Skip common directories that shouldn't be searched
            dirs[:] = [d for d in dirs if
                       not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git',
                                                           '.venv']]

            # Find matching files in current directory
            for filename in fnmatch.filter(files, pattern):
                full_path = os.path.join(root, filename)
                # Convert to relative path for cleaner output
                relative_path = os.path.relpath(full_path, ".")
                matches.append(relative_path)

        print(f"Found {len(matches)} files matching '{pattern}' in {root_dir}")
        return sorted(matches)

    except Exception as e:
        print(f"Error during recursive search: {e}")
        return []

def create_file_explorer_actions():
    """Create and return file explorer specific actions"""
    actions = [
        Action(
            name="list_project_files",
            function=list_project_files,
            description="Lists all Python files in the project.",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            },
            terminal=False
        ),
        Action(
            name="list_project_files_recursive",
            function=list_project_files_recursive,
            description="Recursively lists files matching a pattern throughout the entire project structure. Automatically detects project root for reliable results.",
            parameters={
                "type": "object",
                "properties": {
                    "root_dir": {"type": "string",
                                 "description": "Starting directory for search (None = auto-detect project root from .git, requirements.txt, etc.)",
                                 "default": None},
                    "pattern": {"type": "string",
                                "description": "File pattern to match (e.g., '*.py', '*.csv', '*.md')",
                                "default": "*.py"},
                    "max_depth": {"type": "integer",
                                  "description": "Maximum depth to search (optional, for performance)"}
                },
                "required": []
            },
            terminal=False
        ),
        Action(
            name="read_project_file",
            function=read_project_file,
            description="Reads a file from the project.",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name of the file to read"}
                },
                "required": ["name"]
            },
            terminal=False
        ),
        Action(
            name="terminate",
            function=lambda message: f"{message}\nTerminating...",
            description="Terminates the session and prints the message to the user.",
            parameters={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "The final message to display"}
                },
                "required": ["message"]
            },
            terminal=True
        )
    ]
    return actions