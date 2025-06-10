import pytest
import tempfile
import os
from src.agents.file_explorer.actions import list_project_files_recursive


def test_project_root_detection():
    """Test that project root is detected correctly"""
    from src.agents.file_explorer.actions import find_project_root

    # Should find a directory containing .git, requirements.txt, etc.
    project_root = find_project_root()

    # Verify it found actual project markers
    assert os.path.exists(os.path.join(project_root, '.git')) or \
           os.path.exists(os.path.join(project_root, 'requirements.txt')) or \
           os.path.exists(os.path.join(project_root, '.gitignore'))

    print(f"Detected project root: {project_root}")


def test_auto_root_vs_explicit_path():
    """Test difference between auto-detection and explicit path"""
    # Auto-detect project root
    auto_results = list_project_files_recursive(None, "*.py")

    # Explicit current directory
    current_results = list_project_files_recursive(".", "*.py")

    # Auto-detection should find more files (unless already at project root)
    print(f"Auto-detected root found: {len(auto_results)} files")
    print(f"Current directory found: {len(current_results)} files")


def test_backward_compatibility():
    """Ensure existing functionality still works"""
    from src.agents.file_explorer.actions import list_project_files

    # Should still work without errors
    current_files = list_project_files()
    assert isinstance(current_files, list)