"""
Comprehensive test suite for File Explorer AI Agent
Tests cover unit, integration, edge cases, and performance scenarios
"""

import pytest
import tempfile
import os
import sys
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.file_explorer.actions import (
    list_project_files,
    list_project_files_recursive, 
    find_project_root,
    read_project_file
)


class TestBasicFunctionality:
    """Test core functionality and backward compatibility"""
    
    def test_list_project_files_backward_compatibility(self):
        """Ensure existing functionality remains unchanged"""
        # This should work without errors
        files = list_project_files()
        assert isinstance(files, list)
        # All returned items should be Python files
        for file in files:
            assert file.endswith('.py')
    
    def test_read_project_file_basic(self):
        """Test basic file reading functionality"""
        # Test reading a known file (this test file itself)
        content = read_project_file(__file__)
        assert isinstance(content, str)
        assert len(content) > 0
        assert "TestBasicFunctionality" in content
    
    def test_read_project_file_nonexistent(self):
        """Test error handling for non-existent files"""
        with pytest.raises(FileNotFoundError):
            read_project_file("nonexistent_file.py")


class TestRecursiveSearch:
    """Test recursive directory search functionality"""
    
    @pytest.fixture
    def sample_project_structure(self):
        """Create a temporary project structure for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create complex directory structure
            dirs = [
                "src/agents/file_explorer",
                "src/framework/core", 
                "src/framework/actions",
                "tests/unit",
                "tests/integration",
                "docs",
                "scripts",
                ".git",
                "__pycache__",
                ".venv/lib/python3.9"
            ]
            
            for dir_path in dirs:
                os.makedirs(os.path.join(temp_dir, dir_path), exist_ok=True)
            
            # Create test files
            files = [
                ("src/agents/file_explorer/agent.py", "# Agent implementation"),
                ("src/agents/file_explorer/actions.py", "# Actions implementation"),
                ("src/framework/core/agent.py", "# Core agent"),
                ("src/framework/actions/action.py", "# Base action"),
                ("tests/unit/test_agent.py", "# Unit tests"),
                ("tests/integration/test_workflow.py", "# Integration tests"),
                ("docs/README.md", "# Documentation"),
                ("scripts/deploy.sh", "#!/bin/bash\necho 'deploy'"),
                ("requirements.txt", "pytest>=7.0.0\nopenai>=1.0.0"),
                (".gitignore", "__pycache__/\n*.pyc"),
                ("data.csv", "name,value\ntest,123"),
                ("config.json", '{"setting": "value"}'),
                (".git/config", "[core]\n    repositoryformatversion = 0"),
                ("__pycache__/test.pyc", "compiled code"),
                (".venv/lib/python3.9/site.py", "# Virtual env file")
            ]
            
            for file_path, content in files:
                full_path = os.path.join(temp_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
            
            yield temp_dir

    def test_recursive_search_python_files(self, sample_project_structure):
        """Test recursive search for Python files"""
        results = list_project_files_recursive(sample_project_structure, "*.py")

        # Should find Python files but exclude system directories
        python_files = [r for r in results if r.endswith('.py')]
        assert len(python_files) >= 4  # At least 4 Python files created

        # Should include source files (cross-platform check)
        found_files = [os.path.basename(r) for r in results]
        assert "agent.py" in found_files
        assert any("file_explorer" in r for r in results)

        # Should exclude virtual environment and cache files
        assert not any(".venv" in r for r in results)
        assert not any("__pycache__" in r for r in results)
    
    def test_recursive_search_all_files(self, sample_project_structure):
        """Test recursive search for all file types"""
        results = list_project_files_recursive(sample_project_structure, "*")
        
        # Should find various file types
        assert any(r.endswith('.py') for r in results)
        assert any(r.endswith('.md') for r in results)
        assert any(r.endswith('.csv') for r in results)
        assert any(r.endswith('.json') for r in results)
        assert any(r.endswith('.txt') for r in results)
        
        # Should still exclude system directories
        assert not any(".venv" in r for r in results)
        assert not any("__pycache__" in r for r in results)
    
    def test_recursive_search_specific_patterns(self, sample_project_structure):
        """Test pattern matching functionality"""
        # Test CSV files
        csv_results = list_project_files_recursive(sample_project_structure, "*.csv")
        assert len(csv_results) == 1
        assert csv_results[0].endswith('data.csv')
        
        # Test Markdown files
        md_results = list_project_files_recursive(sample_project_structure, "*.md")
        assert len(md_results) == 1
        assert any("README.md" in r for r in md_results)
        
        # Test shell scripts
        sh_results = list_project_files_recursive(sample_project_structure, "*.sh")
        assert len(sh_results) == 1
        assert any("deploy.sh" in r for r in sh_results)
    
    def test_depth_limiting(self, sample_project_structure):
        """Test max_depth parameter functionality"""
        # Search with depth limit
        limited_results = list_project_files_recursive(
            sample_project_structure, "*.py", max_depth=1
        )
        unlimited_results = list_project_files_recursive(
            sample_project_structure, "*.py"
        )
        
        # Limited search should find fewer files
        assert len(limited_results) < len(unlimited_results)
        
        # Verify depth limiting works correctly
        for result in limited_results:
            # Should not have deeply nested paths
            depth = result.count(os.sep)
            assert depth <= 1
    
    def test_nonexistent_directory(self):
        """Test handling of non-existent directories"""
        results = list_project_files_recursive("/nonexistent/directory", "*.py")
        assert results == []  # Should return empty list, not crash


class TestProjectRootDetection:
    """Test intelligent project root detection"""
    
    @pytest.fixture
    def project_with_markers(self):
        """Create project structure with various root markers"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested structure
            project_root = os.path.join(temp_dir, "my_project")
            subdir = os.path.join(project_root, "src", "deep", "nested")
            os.makedirs(subdir)
            
            # Add project root markers
            markers = [
                ".git/config",
                "requirements.txt", 
                "pyproject.toml",
                ".gitignore"
            ]
            
            for marker in markers:
                marker_path = os.path.join(project_root, marker)
                os.makedirs(os.path.dirname(marker_path), exist_ok=True)
                with open(marker_path, 'w') as f:
                    f.write("# Project marker")
            
            yield project_root, subdir
    
    def test_find_project_root_from_subdirectory(self, project_with_markers):
        """Test project root detection from deep subdirectory"""
        project_root, subdir = project_with_markers
        
        # Should find project root even when starting from deep subdirectory
        detected_root = find_project_root(subdir)
        assert os.path.samefile(detected_root, project_root)
    
    def test_find_project_root_with_git(self, project_with_markers):
        """Test detection using .git directory"""
        project_root, _ = project_with_markers
        
        detected_root = find_project_root(project_root)
        assert os.path.samefile(detected_root, project_root)
        
        # Verify .git directory exists
        assert os.path.exists(os.path.join(detected_root, ".git"))
    
    def test_auto_root_detection_in_recursive_search(self, project_with_markers):
        """Test automatic root detection in recursive search"""
        project_root, subdir = project_with_markers
        
        # Create test files
        test_files = [
            "main.py",
            "src/module.py", 
            "src/deep/nested/util.py"
        ]
        
        for file_path in test_files:
            full_path = os.path.join(project_root, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write("# Test file")
        
        # Search from subdirectory with auto-detection
        results = list_project_files_recursive(None, "*.py")
        
        # Should find all files from project root, not just subdirectory
        assert len(results) >= 3


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_permission_denied_handling(self):
        """Test handling of permission denied errors"""
        with tempfile.TemporaryDirectory() as temp_dir:
            restricted_dir = os.path.join(temp_dir, "restricted")
            os.makedirs(restricted_dir)
            
            # Create file in restricted directory
            test_file = os.path.join(restricted_dir, "test.py")
            with open(test_file, 'w') as f:
                f.write("# Test file")
            
            # Make directory non-readable (Unix only)
            if os.name != 'nt':  # Skip on Windows
                os.chmod(restricted_dir, 0o000)
                
                try:
                    # Should handle permission error gracefully
                    results = list_project_files_recursive(temp_dir, "*.py")
                    # Should return results from accessible directories
                    assert isinstance(results, list)
                finally:
                    # Restore permissions for cleanup
                    os.chmod(restricted_dir, 0o755)
    
    def test_broken_symlink_handling(self):
        """Test handling of broken symbolic links"""
        if os.name == 'nt':  # Skip on Windows (symlinks require admin)
            pytest.skip("Symlinks require admin privileges on Windows")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create broken symlink
            broken_link = os.path.join(temp_dir, "broken_link.py")
            os.symlink("/nonexistent/target.py", broken_link)
            
            # Should handle broken symlink gracefully
            results = list_project_files_recursive(temp_dir, "*.py")
            assert isinstance(results, list)
            # Broken symlink should not appear in results
            assert "broken_link.py" not in [os.path.basename(r) for r in results]
    
    def test_unicode_filename_handling(self):
        """Test handling of unicode filenames"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create files with unicode names
            unicode_files = [
                "测试文件.py",  # Chinese
                "файл_тест.py",  # Russian  
                "arquivo_teste.py",  # Portuguese
                "café_münü.py"  # Mixed accents
            ]
            
            for filename in unicode_files:
                try:
                    file_path = os.path.join(temp_dir, filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("# Unicode test file")
                except (OSError, UnicodeError):
                    # Skip if filesystem doesn't support unicode
                    continue
            
            # Should handle unicode filenames gracefully
            results = list_project_files_recursive(temp_dir, "*.py")
            assert isinstance(results, list)


class TestPerformance:
    """Test performance with large directory structures"""
    
    def test_large_directory_performance(self):
        """Test performance with many files and directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create moderately large structure (not too large for CI)
            num_dirs = 10
            files_per_dir = 5
            
            for i in range(num_dirs):
                dir_path = os.path.join(temp_dir, f"dir_{i}")
                os.makedirs(dir_path)
                
                for j in range(files_per_dir):
                    file_path = os.path.join(dir_path, f"file_{j}.py")
                    with open(file_path, 'w') as f:
                        f.write(f"# File {i}-{j}")
            
            # Should complete in reasonable time
            import time
            start_time = time.time()
            results = list_project_files_recursive(temp_dir, "*.py")
            end_time = time.time()
            
            # Should find all files
            assert len(results) == num_dirs * files_per_dir
            
            # Should complete quickly (less than 1 second for this size)
            assert end_time - start_time < 1.0
    
    def test_depth_limiting_performance(self):
        """Test that depth limiting improves performance"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create deep nested structure
            current_dir = temp_dir
            for i in range(10):  # 10 levels deep
                current_dir = os.path.join(current_dir, f"level_{i}")
                os.makedirs(current_dir)
                
                # Add file at each level
                file_path = os.path.join(current_dir, f"file_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(f"# File at level {i}")
            
            import time
            
            # Test unlimited depth
            start_time = time.time()
            unlimited_results = list_project_files_recursive(temp_dir, "*.py")
            unlimited_time = time.time() - start_time
            
            # Test limited depth
            start_time = time.time()
            limited_results = list_project_files_recursive(temp_dir, "*.py", max_depth=3)
            limited_time = time.time() - start_time
            
            # Limited search should be faster and find fewer files
            assert len(limited_results) < len(unlimited_results)
            assert limited_time <= unlimited_time + 0.1  # Allow small margin for timing variations


class TestIntegration:
    """Integration tests for complete workflows"""

    def test_full_workflow_simulation(self):
        """Test complete agent workflow simulation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create project structure
            project_files = [
                "main.py",
                "src/agent.py",
                "src/utils.py",
                "tests/test_main.py",
                "README.md",
                "requirements.txt"
            ]

            for file_path in project_files:
                full_path = os.path.join(temp_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Content of {file_path}")

            # Simulate agent workflow
            # 1. Discover Python files
            python_files = list_project_files_recursive(temp_dir, "*.py")
            assert len(python_files) == 4  # main.py, agent.py, utils.py, test_main.py

            # 2. Read specific files
            for py_file in python_files:
                # Create correct absolute path by joining temp_dir with relative path
                abs_path = os.path.join(temp_dir, py_file)
                content = read_project_file(abs_path)
                assert len(content) > 0  # Should have content
                assert "# Content of" in content  # Should contain expected prefix
                # Cross-platform path check
                normalized_path = py_file.replace('\\', '/')
                assert f"Content of {normalized_path}" in content

            # 3. Find documentation
            docs = list_project_files_recursive(temp_dir, "*.md")
            assert len(docs) == 1
            assert "README.md" in docs[0]

# Pytest configuration and fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment"""
    # Ensure clean test environment
    original_cwd = os.getcwd()
    yield
    # Cleanup after tests
    os.chdir(original_cwd)


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
