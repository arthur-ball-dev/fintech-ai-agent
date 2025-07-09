# Contributing to FinTech AI Agent Framework

Thank you for your interest in contributing to the FinTech AI Agent Framework! This document provides guidelines for contributing to the project.

## 🤝 Code of Conduct

This project adheres to professional standards expected in financial technology:
- **Respectful Communication**: Professional and constructive feedback
- **Quality First**: Security and reliability over speed
- **Domain Expertise**: Value FinTech knowledge and best practices
- **Collaborative Spirit**: Share knowledge and help others learn

## 🚀 Getting Started

### Prerequisites
1. Python 3.8+ installed
2. Understanding of the GAME framework pattern
3. Familiarity with financial technology concepts
4. Experience with AI/LLM integration (preferred)

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd fintech-ai-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -r requirements-test.txt

# Run tests to verify setup
pytest
```

## 📝 How to Contribute

### 1. Reporting Issues
- Check existing issues first
- Use clear, descriptive titles
- Include reproduction steps
- Specify environment details
- Attach relevant logs or screenshots

### 2. Suggesting Enhancements
- Explain the use case
- Describe expected behavior
- Consider FinTech implications
- Discuss security impacts

### 3. Code Contributions

#### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Create bugfix branch
git checkout -b fix/issue-description
```

#### Commit Messages
Follow conventional commits:
```
feat: Add portfolio risk calculation patterns
fix: Correct HFT latency detection regex
docs: Update API documentation for compliance tools
test: Add unit tests for risk scoring
refactor: Simplify agent registry logic
```

#### Code Standards
- **Type Hints**: All functions must have type hints
- **Docstrings**: Comprehensive docstrings required
- **Testing**: Minimum 90% coverage for new code
- **Security**: Follow security best practices
- **Performance**: Consider large-scale implications

## 🧪 Testing Requirements

### Unit Tests
```python
def test_new_pattern_detection():
    """Test description following naming convention"""
    # Arrange
    test_data = create_test_fixture()
    
    # Act
    result = analyze_pattern(test_data)
    
    # Assert
    assert result.score >= expected_score
```

### Integration Tests
- Test with multiple file types
- Validate cross-platform compatibility
- Test error handling scenarios
- Verify LLM integration

### FinTech Domain Tests
- Validate financial patterns
- Test compliance mappings
- Verify risk calculations
- Check performance metrics

## 📋 Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add/update API documentation
   - Update CHANGELOG.md

2. **Pass All Checks**
   ```bash
   # Format code
   black src/ tests/
   
   # Sort imports
   isort src/ tests/
   
   # Run linting
   flake8 src/ tests/
   
   # Type checking
   mypy src/
   
   # Run all tests
   pytest --cov=src
   ```

3. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   
   ## FinTech Impact
   - [ ] Risk patterns updated
   - [ ] Compliance mappings verified
   - [ ] Performance impact assessed
   - [ ] Security review completed
   ```

## 🏗️ Architecture Guidelines

### Adding New Analysis Tools
1. Create pattern definitions
2. Implement scoring algorithm
3. Add @register_tool decorator
4. Write comprehensive tests
5. Update documentation

### Creating New Agents
1. Define agent in registry
2. Set appropriate category
3. Specify analysis capabilities
4. Add factory function
5. Create usage examples

### Pattern Library Extensions
- Research industry standards
- Validate with real examples
- Consider false positives
- Document pattern rationale

## 🔒 Security Considerations

All contributions must:
- Avoid hardcoded secrets
- Validate all inputs
- Handle errors gracefully
- Follow secure coding practices
- Consider compliance implications

## 📚 Resources

### FinTech References
- Financial Risk Management standards
- Regulatory compliance guidelines
- HFT best practices
- Security frameworks

### Technical Resources
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [GAME Framework Pattern](https://www.coursera.org/learn/ai-agents-python/)

## 🎯 Focus Areas for Contribution

Current areas where contributions are especially welcome:
- Additional financial risk patterns
- Market data integration tools
- Real-time monitoring capabilities
- Cloud deployment configurations
- Performance optimizations
- Additional compliance frameworks

Thank you for helping make the FinTech AI Agent Framework better!