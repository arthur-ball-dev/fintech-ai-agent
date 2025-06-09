# GAME Framework - File Explorer Agent

A flexible framework for building AI agents using the GAME (Goals, Actions, Memory, Environment) pattern.

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key set as system environment variable

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/game-framework.git
   cd game-framework-file-explorer

Create a virtual environment:
bashpython -m venv .venv
.venv\Scripts\activate  # On Windows

Install dependencies:
bashpip install -r requirements.txt

Set your OpenAI API key as a system environment variable:

Windows: Set OPENAI_API_KEY in System Environment Variables
Mac/Linux: Add to .bashrc or .zshrc: export OPENAI_API_KEY="your-key"



Usage
bashpython -m src.examples.run_file_explorer
Project Structure
├── src/
│   ├── framework/         # Core framework components
│   ├── agents/           # Agent implementations
│   └── examples/         # Example scripts
├── tests/                # Test files
└── docs/                 # Documentation

### 2.5 `pyproject.toml`
```toml
[project]
name = "game-framework"
version = "0.1.0"
description = "GAME Framework for building AI Agents"
readme = "README.md"
requires-python = ">=3.8"

[tool.black]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]