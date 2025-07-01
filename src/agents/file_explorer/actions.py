"""
File Explorer Actions using the decorator system.
"""
import os
import fnmatch
from typing import List
from src.framework.actions.decorators import register_tool

@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Read a file from the project"""
    with open(name, "r", encoding='utf-8', errors='ignore') as f:
        return f.read()

@register_tool(tags=["file_operations", "list"])
def list_project_files() -> List[str]:
    all_files = os.listdir(".")
    print(f"the list of project files in the listdir is {all_files}")
    return sorted([file for file in os.listdir(".") if file.endswith(".py")])

@register_tool(tags=["file_operations", "search"])
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

@register_tool(tags=["file_operations", "search", "recursive"])
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
                # Use relative path from the search root, not current directory
                relative_path = os.path.relpath(full_path, root_dir)
                matches.append(relative_path)

        print(f"Found {len(matches)} files matching '{pattern}' in {root_dir}")
        return sorted(matches)

    except Exception as e:
        print(f"Error during recursive search: {e}")
        return []

@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."