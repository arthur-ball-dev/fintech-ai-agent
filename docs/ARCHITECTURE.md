# Technical Architecture

Complete technical reference for the FinTech AI Agent Framework's multi-agent system and financial analysis capabilities.

## 🏗️ System Architecture

### Multi-Agent Framework Design

```
FinTech AI Agent Framework
│
├── Agent Registry (13+ Specialized Agents)
│   ├── FinTech Specialized (5) - Pattern-based financial analysis
│   ├── Hybrid Analysis (5) - Pattern + AI combined insights  
│   └── Basic Utilities (3) - General file operations
│
├── Analysis Engine
│   ├── Risk Management Scanner
│   ├── HFT Performance Analyzer
│   ├── Regulatory Compliance Engine
│   └── Architecture Evaluator
│
├── Multi-Provider LLM System
│   ├── LLMConfig - Provider & model management
│   ├── LLMClient - Unified interface with failover
│   └── Cost Optimization - 3-tier model selection
│
├── GAME Framework Core
│   ├── Goals - Agent objectives and priorities
│   ├── Actions - Tool registry with decorators
│   ├── Memory - Conversation and analysis history
│   └── Environment - Secure execution context
│
└── Security & Compliance Layer
    ├── Environment Variable Configuration
    ├── Audit Trail Support
    └── Pattern-Based Security Scanning
```

---

## 🏦 Financial Analysis Capabilities

### Risk Management Analysis Engine

**Pattern Detection:**
- Position limit controls: `MAX_POSITION`, `position_size_limit`
- Stop-loss mechanisms: `stop_price`, `risk_per_trade`, `trailing_stop`
- Portfolio risk assessment: VaR calculations, correlation matrices
- Operational controls: circuit breakers, kill switches, audit trails

**Risk Scoring Algorithm:**
```python
Risk Score = (Position Controls × 25) + 
             (Stop Loss × 25) + 
             (Portfolio Risk × 25) + 
             (Operational Controls × 25)
# Range: 0-100 (higher = better risk management)
```

### HFT Performance Optimization

**Performance Patterns:**
- Latency optimization: async operations, threading patterns
- Memory efficiency: numpy usage, `__slots__`, struct operations  
- Network optimization: WebSocket usage, connection pooling
- Anti-pattern detection: blocking operations, inefficient loops

**HFT Readiness Score:**
```python
HFT Score = (Async Operations × 25) +
            (Memory Optimization × 25) +
            (Network Efficiency × 25) +
            (No Anti-Patterns × 25)
# Range: 0-100 (higher = better HFT readiness)
```

### Regulatory Compliance Engine

**Compliance Domains:**
- **SOX Compliance**: Audit logging, access controls, data integrity
- **GDPR Compliance**: PII handling, encryption, data protection
- **PCI-DSS Compliance**: Payment security, encryption standards

**Security Pattern Detection:**
- Encryption implementation: SSL/TLS, data-at-rest encryption
- Authentication patterns: JWT/OAuth, multi-factor authentication
- Access control: RBAC patterns, authorization frameworks
- Vulnerability scanning: hardcoded secrets, weak cryptography

**Compliance Scoring:**
```python
Compliance Score = Base Score (100) - 
                   (Security Risks × 15) -
                   (Missing Controls × 10)
# Range: 0-100 (higher = better compliance)
```

### Architecture Evaluation

**System Design Patterns:**
- Microservices architecture assessment
- API design and security evaluation
- Scalability pattern detection
- Monitoring and observability readiness

---

## 🤖 Multi-Agent System API

### Agent Registry Management

```python
from src.agents.file_explorer import create_agent_by_key, get_agents_by_category

# Available agent categories
categories = get_agents_by_category()
# Returns:
# {
#     'FinTech Specialized': [...],
#     'Hybrid Analysis': [...], 
#     'Basic Utilities': [...]
# }

# Create specific agent
agent = create_agent_by_key('fintech_risk_analyst')
memory = agent.run("Analyze financial risk patterns")
```

### Agent Factory Functions

**FinTech Specialized Agents:**
```python
# Pattern-based financial analysis
fintech_risk_analyst         # Risk management pattern detection
fintech_performance_analyst  # HFT performance optimization  
fintech_compliance_analyst   # Regulatory compliance scanning
fintech_architect           # System architecture evaluation
fintech_comprehensive       # Multi-domain orchestrator
```

**Hybrid Analysis Agents:**
```python
# Pattern detection + AI insights
fintech_risk_hybrid         # Risk analysis with AI context
fintech_performance_hybrid  # Performance + strategic analysis
fintech_compliance_hybrid   # Compliance with AI interpretation
fintech_architect_hybrid    # Architecture with recommendations
fintech_comprehensive_hybrid # Complete multi-domain analysis
```

**Basic Utility Agents:**
```python
# General-purpose tools
file_explorer_agent         # File system navigation
readme_generator_agent      # Documentation creation
code_analysis_agent        # Code structure analysis
```

---

## 🌐 Multi-Provider LLM System

### LLMConfig Class

```python
class LLMConfig:
    def __init__(self)
    def get_model_name(self, provider: str, model_type: str = 'default') -> str
    def validate_provider(self, provider: str) -> bool
    def get_available_providers(self) -> List[str]
```

**Model Tier Configuration:**
```python
models = {
    'openai': {
        'fast': 'gpt-3.5-turbo',      # Cost: 1x
        'default': 'gpt-4o-mini',     # Cost: 3x  
        'advanced': 'gpt-4o'          # Cost: 10x
    },
    'anthropic': {
        'fast': 'claude-3-haiku-20240307',       # Cost: 1x
        'default': 'claude-3-5-sonnet-20241022', # Cost: 5x
        'advanced': 'claude-3-opus-20240229'     # Cost: 15x
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

**Usage Examples:**
```python
client = LLMClient()

# Automatic provider selection
response = client.generate_response(prompt)

# Cost optimization
response = client.generate_response(prompt, model_type='fast')      # Cheapest
response = client.generate_response(prompt, model_type='advanced')  # Best quality

# Provider-specific
response = client.generate_response(prompt, provider='anthropic')

# Custom parameters
response = client.generate_response(
    prompt, 
    provider='openai',
    model_type='default',
    temperature=0.9,
    max_tokens=2048
)
```

---

## 🔧 Tool Registration System

### Decorator-Based Registration

```python
@register_tool(
    tool_name: str = None,
    description: str = None, 
    parameters_override: dict = None,
    terminal: bool = False,
    tags: List[str] = None
)
```

**Available Financial Analysis Tools:**

| Tool | Purpose | Tags | Used By |
|------|---------|------|---------|
| `analyze_financial_risk_patterns` | Risk management assessment | `fintech`, `risk` | Risk analysts |
| `analyze_hft_performance_patterns` | Trading optimization | `fintech`, `performance` | Performance analysts |
| `analyze_regulatory_compliance` | Compliance validation | `fintech`, `compliance` | Compliance agents |
| `analyze_fintech_architecture_patterns` | System design evaluation | `fintech`, `architecture` | Architecture agents |
| `analyze_fintech_project_comprehensive` | Multi-domain analysis | `fintech`, `comprehensive` | Comprehensive agents |

### Action Registry

```python
class PythonActionRegistry(ActionRegistry):
    def __init__(self, tags: List[str] = None, tool_names: List[str] = None)
    def get_actions(self) -> List[Action]
```

**Registry Filtering Examples:**
```python
# Risk-focused agent
risk_registry = PythonActionRegistry(tags=["fintech", "risk", "system"])

# Comprehensive analysis
full_registry = PythonActionRegistry(tags=["fintech", "system"])

# Specific tools only
custom_registry = PythonActionRegistry(tool_names=["analyze_financial_risk_patterns", "terminate"])
```

---

## 🎯 Analysis Modes & Workflows

### Pattern-Based Analysis (Deterministic)

**Characteristics:**
- Fast execution (no LLM costs)
- Consistent, reproducible results
- Audit-friendly with traceable logic
- Ideal for compliance and reporting

**Usage:**
```python
agent = create_agent_by_key('fintech_risk_analyst')
memory = agent.run("Perform deterministic risk pattern analysis")
```

### LLM-Enhanced Analysis (AI-Powered)

**Characteristics:**
- Contextual business insights
- Strategic recommendations
- Natural language explanations
- Requires LLM provider configuration

**Usage:**
```python
agent = create_agent_by_key('file_explorer_agent')  # Uses LLM
memory = agent.run("Analyze project with business context and recommendations")
```

### Hybrid Analysis (Combined)

**Characteristics:**
- Pattern detection feeds AI analysis
- Best of both approaches
- Comprehensive coverage with insights
- Flexible cost management

**Usage:**
```python
agent = create_agent_by_key('fintech_risk_hybrid')
memory = agent.run("Combine pattern detection with AI-powered business insights")
```

---

## 🏗️ GAME Framework Implementation

### Goals System

```python
@dataclass(frozen=True)
class Goal:
    priority: int
    name: str
    description: str
```

### Actions System

```python
class Action:
    def __init__(self, name: str, function: Callable, description: str, 
                 parameters: Dict, terminal: bool = False)
    def execute(self, **args) -> Any
```

### Memory Management

```python
class Memory:
    def add_memory(self, memory: dict)
    def get_memories(self, limit: Optional[int] = None) -> List[Dict]
    def copy_without_system_memories(self) -> Memory
```

**Memory Types:**
- `"user"` - User requests and inputs
- `"assistant"` - Agent responses and decisions  
- `"environment"` - Tool execution results
- `"system"` - System messages and metadata

### Environment Execution

```python
class Environment:
    def execute_action(self, action: Action, args: dict) -> dict
    def format_result(self, result: Any) -> dict
```

**Execution Result Format:**
```python
{
    "tool_executed": True,
    "result": "actual_result", 
    "timestamp": "2024-01-01T12:00:00+0000"
}
```

---

## 🔒 Security Architecture

### Environment Variable Configuration

```python
# Required environment variables
OPENAI_API_KEY      # OpenAI provider access
ANTHROPIC_API_KEY   # Anthropic provider access

# Optional configuration  
DEFAULT_LLM_PROVIDER  # Provider preference (openai|anthropic)
```

### Security Features

- **Zero Hardcoded Secrets** - All credentials via environment variables
- **Secure Validation** - API key verification without exposure
- **Audit Trail Support** - Comprehensive logging for compliance
- **Input Validation** - All file paths and inputs validated
- **Error Sanitization** - No sensitive data in error messages

---

## 📊 Performance Characteristics

### Benchmarks

**Analysis Performance:**
- Pattern detection: ~100ms for typical projects
- LLM analysis: 1-5 seconds (provider dependent)
- Hybrid analysis: 2-8 seconds (pattern + LLM)
- Large projects (1000+ files): <30 seconds

**Cost Optimization:**
- Fast tier: Up to 10x cost reduction
- Default tier: 3-5x cost reduction vs premium
- Advanced tier: Highest quality for critical decisions

**Memory Efficiency:**
- Streaming file processing
- Configurable depth limits
- Cross-platform path handling
- Optimized for large codebases

---

## 🧪 Testing Architecture

### Test Categories

- **Unit Tests** (98% coverage) - Individual component validation
- **Integration Tests** - Multi-component workflows and live LLM validation
- **Performance Tests** - Large-scale directory handling
- **Security Tests** - Vulnerability scanning and compliance validation

### Test Execution

```bash
# Complete test suite
pytest

# Category-specific testing
pytest tests/unit/test_fintech_agents.py      # Financial analysis validation
pytest tests/integration/test_llm_integration.py  # Live LLM provider testing
pytest tests/performance/                    # Performance benchmarks

# Coverage analysis
pytest --cov=src --cov-report=html
```

This architecture demonstrates production-ready design suitable for enterprise financial technology environments with comprehensive security, testing, and compliance considerations.