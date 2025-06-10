# File Explorer AI Agent

**[Under Development]** AI-powered file exploration agent for comprehensive project analysis and document discovery.

A flexible framework for building AI agents using the **GAME (Goals, Actions, Memory, Environment)** pattern, specifically designed for intelligent file system navigation and analysis.

## 🚀 Features

### Core Capabilities
- **Intelligent File Discovery**: Recursive search across entire project structures
- **Smart Project Root Detection**: Automatically identifies project boundaries using common markers
- **Pattern-Based Filtering**: Support for multiple file types (*.py, *.csv, *.pdf, *.md, etc.)
- **Conversational Interface**: Natural language commands for file operations
- **Enterprise-Ready**: Robust error handling and performance optimizations

### Enhanced File Operations
- **Recursive Directory Search**: Discovers files throughout complete project hierarchies
- **Content Analysis**: LLM-powered intelligent file content processing
- **Metadata Extraction**: File size, modification dates, and structural information
- **Depth-Limited Search**: Configurable search depth for performance control

## 📋 Requirements

- Python 3.8+
- OpenAI API key (set as environment variable)
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arthur-ball-dev/file-explorer-ai-agent.git
   cd file-explorer-ai-agent
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Mac/Linux  
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenAI API key:**
   ```bash
   # Windows
   set OPENAI_API_KEY=your-api-key-here
   
   # Mac/Linux
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🚀 Usage

### Basic Usage
```bash
python -m src.examples.run_file_explorer
```

### Example Commands

#### File Discovery
- *"List all Python files in the entire project"*
- *"Find all CSV files that might contain data"*
- *"Show me all markdown documentation files"*

#### Project Analysis  
- *"Analyze the code structure and suggest improvements"*
- *"Create a summary of all Python files in the project"*
- *"Find all files related to testing"*

#### Content Analysis
- *"Read the main agent file and explain how it works"*
- *"Analyze the requirements.txt and list all dependencies"*
- *"Examine the test files and describe the testing strategy"*

## 🏗️ Architecture

### GAME Framework Components

```
├── src/
│   ├── framework/           # Core GAME framework
│   │   ├── core/           # Agent orchestration & goals
│   │   ├── actions/        # Action registry & definitions  
│   │   ├── memory/         # Conversation & context memory
│   │   ├── environment/    # Execution environment
│   │   ├── language/       # LLM integration & prompting
│   │   └── llm/           # Language model client
│   ├── agents/            # Agent implementations
│   │   └── file_explorer/ # File exploration specialist
│   └── examples/          # Usage demonstrations
├── tests/                 # Comprehensive test suite
└── docs/                  # Documentation
```

### Enhanced Actions Available

| Action | Description | Use Case |
|--------|-------------|----------|
| `list_project_files` | Lists Python files in current directory | Quick local file discovery |
| `list_project_files_recursive` | **[NEW]** Recursively searches entire project | Enterprise-scale file discovery |
| `read_project_file` | Reads and analyzes file contents | Content analysis and processing |
| `terminate` | Completes session with results | Task completion |

## 🔧 Configuration

### Project Root Detection
The agent automatically detects project root using these markers:
- `.git` (version control root)
- `requirements.txt` (Python project dependencies)
- `pyproject.toml` (modern Python project configuration)
- `setup.py` (traditional Python package)
- `.gitignore` (project boundary indicator)

### Search Patterns
Supports standard glob patterns:
- `*.py` - Python source files
- `*.csv` - Comma-separated values data
- `*.json` - JSON configuration/data files
- `*.md` - Markdown documentation
- `*.txt` - Text files
- `*` - All files

## 🧪 Testing

### Run Test Suite
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test module
python -m pytest tests/test_recursive_search.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage
- ✅ Recursive file discovery
- ✅ Pattern matching functionality  
- ✅ Project root auto-detection
- ✅ Error handling and edge cases
- ✅ Backward compatibility

## 📚 Development

### Contributing
1. Create feature branch: `git checkout -b feature/your-enhancement`
2. Implement changes with tests
3. Update documentation
4. Submit pull request with detailed description

### Roadmap
- [ ] Advanced content search capabilities
- [ ] File type intelligence and metadata extraction
- [ ] Integration with external document management systems
- [ ] Multi-agent collaboration for complex analysis tasks
- [ ] Financial document-specific processing (CSV, PDF, Excel)

## 🔐 Security

- **No sensitive data storage**: All processing in memory
- **API key protection**: Environment variable configuration only
- **Safe file operations**: Read-only access with comprehensive error handling
- **Path traversal protection**: Automatic filtering of system directories

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact: arthur-ball-dev on GitHub

---

**Note**: This project demonstrates enterprise-level AI agent development practices suitable for financial technology and document analysis applications.