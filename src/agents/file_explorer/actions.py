"""
File Explorer Actions with FinTech Analysis capabilities.
Enhanced with domain-specific analysis tools for financial technology applications.
Includes hybrid pattern-based + LLM analysis capabilities.
"""
import os
import re
import ast
import fnmatch
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.framework.actions.decorators import register_tool

# === Core File Operations ===

@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Read a file from the project"""
    with open(name, "r", encoding='utf-8', errors='ignore') as f:
        return f.read()

@register_tool(tags=["file_operations", "list"])
def list_project_files() -> List[str]:
    """List Python files in current directory"""
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

# === LLM Analysis Helper Functions ===

def _generate_llm_analysis_prompt(analysis_type: str, pattern_results: Dict[str, Any], 
                                 code_snippets: List[str]) -> str:
    """Generate LLM prompt for contextual analysis"""
    
    base_prompt = f"""
You are a senior FinTech engineer analyzing code for {analysis_type}.

PATTERN-BASED ANALYSIS SUMMARY:
{pattern_results.get('summary', 'No pattern analysis available')}

KEY FINDINGS:
{pattern_results.get('key_findings', 'No key findings')}

CODE SNIPPETS FOR REVIEW:
"""
    
    for i, snippet in enumerate(code_snippets[:3], 1):  # Limit to 3 snippets
        base_prompt += f"\n--- Snippet {i} ---\n{snippet[:500]}...\n"
    
    if analysis_type == "regulatory compliance":
        base_prompt += """
ANALYSIS REQUIRED:
1. Identify additional security risks not caught by pattern matching
2. Assess the business impact of compliance gaps
3. Prioritize remediation efforts for a financial services environment
4. Flag any industry-specific compliance concerns (SOX, PCI-DSS, GDPR)

Provide your analysis in structured format with specific, actionable recommendations.
"""
    elif analysis_type == "risk management":
        base_prompt += """
ANALYSIS REQUIRED:
1. Identify missing risk controls not detected by patterns
2. Assess operational risk exposure in trading scenarios
3. Evaluate the effectiveness of existing risk controls
4. Recommend additional safeguards for financial trading systems

Focus on practical risk management for live trading environments.
"""
    elif analysis_type == "performance optimization":
        base_prompt += """
ANALYSIS REQUIRED:
1. Identify performance bottlenecks not caught by pattern analysis
2. Assess latency-critical code paths for trading systems
3. Recommend specific optimizations for high-frequency trading
4. Evaluate scalability concerns for enterprise deployment

Prioritize recommendations that impact trading system performance.
"""
    elif analysis_type == "architecture":
        base_prompt += """
ANALYSIS REQUIRED:
1. Assess architectural patterns for FinTech scalability
2. Identify potential single points of failure
3. Evaluate API design for financial services requirements
4. Recommend improvements for enterprise deployment

Focus on production-ready financial system architecture.
"""
    
    return base_prompt

def _extract_code_snippets_for_llm(python_files: List[str], max_snippets: int = 3) -> List[str]:
    """Extract representative code snippets for LLM analysis"""
    
    snippets = []
    files_processed = 0
    
    for file_path in python_files:
        if files_processed >= max_snippets:
            break
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Skip very small files
            if len(content) < 200:
                continue
                
            # Take first 1000 characters as representative snippet
            snippet = f"File: {file_path}\n{content[:1000]}"
            snippets.append(snippet)
            files_processed += 1
            
        except Exception:
            continue
    
    return snippets

def _run_llm_analysis(analysis_type: str, pattern_results: Dict[str, Any], 
                     python_files: List[str]) -> str:
    """Run LLM analysis on code for additional insights"""
    
    try:
        # Extract code snippets for LLM review
        code_snippets = _extract_code_snippets_for_llm(python_files)
        
        if not code_snippets:
            return "No suitable code snippets found for LLM analysis."
        
        # Generate analysis prompt
        prompt = _generate_llm_analysis_prompt(analysis_type, pattern_results, code_snippets)
        
        # For now, return a placeholder - in real implementation, this would call the LLM
        # from src.framework.llm.client import generate_response
        # llm_response = generate_response(prompt)
        
        return f"""
🤖 LLM CONTEXTUAL ANALYSIS:

Based on pattern analysis and code review, the AI identified:

• Additional considerations beyond pattern matching
• Context-specific insights for {analysis_type}
• Business impact assessment for financial services
• Prioritized recommendations for remediation

[Note: This is a placeholder for LLM integration. In production, this would contain
actual AI-generated insights based on the code analysis and business context.]

INTEGRATION POINTS:
• Cross-reference with pattern analysis findings
• Consider business risk tolerance
• Align with regulatory requirements
• Factor in operational constraints
"""
        
    except Exception as e:
        return f"LLM analysis failed: {str(e)}"

# === Enhanced FinTech Risk Management Analysis ===

@register_tool(tags=["fintech", "risk_management", "analysis"])
def analyze_financial_risk_patterns(project_path: str = ".", include_llm_analysis: bool = False) -> str:
    """
    Analyze codebase for financial risk management patterns.
    Examines position limits, stop losses, and operational controls.
    
    Args:
        project_path: Path to analyze (default: current directory)
        include_llm_analysis: Whether to include LLM contextual analysis
    
    Returns:
        Risk analysis report with optional LLM insights
    """
    # Risk control patterns to detect
    risk_patterns = {
        'position_limits': [
            r'position_limit|max_position|position_size_limit',
            r'check_position_limit|validate_position',
            r'MAX_POSITION|POSITION_LIMIT'
        ],
        'stop_loss': [
            r'stop_loss|stop_price|exit_price',
            r'risk_per_trade|max_loss',
            r'trailing_stop|protective_stop'
        ],
        'portfolio_risk': [
            r'portfolio_var|value_at_risk|var_calculation',
            r'correlation_matrix|diversification',
            r'risk_allocation|exposure_limit'
        ],
        'operational_risk': [
            r'circuit_breaker|kill_switch|emergency_stop',
            r'audit_trail|compliance_check',
            r'rate_limit|throttle|timeout'
        ]
    }
    
    # Use existing recursive search function
    python_files = list_project_files_recursive(project_path, "*.py")
    
    # Analyze each file for risk patterns
    risk_controls_found = {}
    flagged_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            file_has_patterns = False
            for risk_type, patterns in risk_patterns.items():
                matches = []
                for pattern in patterns:
                    found = re.finditer(pattern, content, re.IGNORECASE)
                    matches.extend([match.group() for match in found])
                
                if matches:
                    if risk_type not in risk_controls_found:
                        risk_controls_found[risk_type] = 0
                    risk_controls_found[risk_type] += len(matches)
                    file_has_patterns = True
            
            # Track files with risk patterns for LLM analysis
            if file_has_patterns:
                flagged_files.append(file_path)
        
        except Exception:
            continue
    
    # Generate pattern analysis results
    total_controls = sum(risk_controls_found.values())
    risk_score = min(100, (total_controls / len(python_files)) * 10) if python_files else 0
    
    # Pattern-based analysis summary
    pattern_results = {
        'summary': f"Found {total_controls} risk control patterns across {len(python_files)} files",
        'key_findings': f"Risk Score: {risk_score:.1f}/100, Controls: {list(risk_controls_found.keys())}",
        'flagged_files': flagged_files
    }
    
    # Build report starting with pattern analysis
    report = f"""
🏦 FINANCIAL RISK MANAGEMENT ANALYSIS
=====================================

Project: {project_path}
Files Analyzed: {len(python_files)}
Risk Controls Score: {risk_score:.1f}/100

📊 PATTERN-BASED ANALYSIS (Deterministic):
"""
    
    if risk_controls_found:
        for risk_type, count in risk_controls_found.items():
            emoji = "✅" if count > 0 else "❌"
            report += f"{emoji} {risk_type.replace('_', ' ').title()}: {count} instances\n"
    else:
        report += "❌ No risk management patterns detected\n"
    
    report += f"""
🎯 PATTERN-BASED RECOMMENDATIONS:
• Position Management: {'✅ Implemented' if 'position_limits' in risk_controls_found else '❌ Add position size limits'}
• Stop Loss Controls: {'✅ Implemented' if 'stop_loss' in risk_controls_found else '❌ Implement stop loss mechanisms'}
• Portfolio Risk: {'✅ Implemented' if 'portfolio_risk' in risk_controls_found else '❌ Add VaR calculations'}
• Operational Safety: {'✅ Implemented' if 'operational_risk' in risk_controls_found else '❌ Add circuit breakers'}
"""
    
    # Add LLM analysis if requested
    if include_llm_analysis:
        llm_analysis = _run_llm_analysis("risk management", pattern_results, flagged_files or python_files[:3])
        report += f"\n{llm_analysis}"
        
        report += f"""
🔗 INTEGRATED RISK ASSESSMENT:
The combination of pattern analysis and contextual review provides a comprehensive
view of risk management maturity. Cross-reference deterministic findings with
AI insights for complete risk assessment.
"""
    
    return report

# === Enhanced FinTech Performance Analysis ===

@register_tool(tags=["fintech", "performance", "analysis"])
def analyze_hft_performance_patterns(project_path: str = ".", include_llm_analysis: bool = False) -> str:
    """
    Analyze code for high-frequency trading performance optimization.
    Identifies latency-critical patterns and performance bottlenecks.
    
    Args:
        project_path: Path to analyze
        include_llm_analysis: Whether to include LLM contextual analysis
    
    Returns:
        Performance analysis report with optional LLM insights
    """
    # Performance optimization patterns
    performance_patterns = {
        'latency_critical': [
            r'time\.time\(\)|datetime\.now\(\)|perf_counter',
            r'asyncio|async\s|await\s',
            r'threading|multiprocessing',
            r'queue\.Queue|collections\.deque'
        ],
        'memory_efficiency': [
            r'numpy|pandas',
            r'\_\_slots\_\_',
            r'array\.array|bytearray',
            r'struct\.pack|struct\.unpack'
        ],
        'network_optimization': [
            r'socket\.|websocket',
            r'connection_pool|session\.',
            r'timeout=|connect_timeout',
            r'keep_alive|persistent'
        ]
    }
    
    # Performance anti-patterns that hurt latency
    anti_patterns = {
        'blocking_operations': [
            r'time\.sleep\(',
            r'requests\.get\(|requests\.post\(',
            r'input\(\)|raw_input\('
        ],
        'inefficient_loops': [
            r'for.*in.*range\(len\(',
            r'while.*True:.*(?!break)'
        ]
    }
    
    # Use existing recursive search function
    python_files = list_project_files_recursive(project_path, "*.py")
    
    performance_score = 100
    pattern_counts = {}
    anti_pattern_counts = {}
    flagged_files = []
    
    # Analyze each file for performance patterns
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            file_has_issues = False
            
            # Count performance patterns (good)
            for pattern_type, patterns in performance_patterns.items():
                for pattern in patterns:
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + matches
            
            # Count anti-patterns (bad)
            for anti_type, patterns in anti_patterns.items():
                for pattern in patterns:
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    if matches > 0:
                        anti_pattern_counts[anti_type] = anti_pattern_counts.get(anti_type, 0) + matches
                        performance_score -= (matches * 10)
                        file_has_issues = True
            
            # Track problematic files for LLM analysis
            if file_has_issues:
                flagged_files.append(file_path)
        
        except Exception:
            continue
    
    performance_score = max(0, performance_score)
    
    # Calculate readiness for high-frequency trading
    hft_score = 0
    if pattern_counts.get('latency_critical', 0) > 0:
        hft_score += 25
    if pattern_counts.get('memory_efficiency', 0) > 0:
        hft_score += 25
    if pattern_counts.get('network_optimization', 0) > 0:
        hft_score += 25
    if performance_score > 70:
        hft_score += 25
    
    # Pattern analysis results
    pattern_results = {
        'summary': f"Performance Score: {performance_score}/100, HFT Readiness: {hft_score}/100",
        'key_findings': f"Optimizations: {list(pattern_counts.keys())}, Issues: {list(anti_pattern_counts.keys())}",
        'flagged_files': flagged_files
    }
    
    report = f"""
⚡ HIGH-FREQUENCY TRADING PERFORMANCE ANALYSIS
===========================================

Project: {project_path}
Files Analyzed: {len(python_files)}
Performance Score: {performance_score}/100
HFT Readiness: {hft_score}/100

📊 PATTERN-BASED ANALYSIS (Deterministic):

🚀 PERFORMANCE OPTIMIZATIONS DETECTED:
"""
    
    for pattern_type, count in pattern_counts.items():
        emoji = "✅" if count > 0 else "❌"
        report += f"{emoji} {pattern_type.replace('_', ' ').title()}: {count} instances\n"
    
    if anti_pattern_counts:
        report += f"\n⚠️ PERFORMANCE ISSUES DETECTED:\n"
        for anti_type, count in anti_pattern_counts.items():
            report += f"❌ {anti_type.replace('_', ' ').title()}: {count} instances\n"
    
    report += f"""
🎯 PATTERN-BASED ASSESSMENT:
• Async Operations: {'✅ Implemented' if pattern_counts.get('latency_critical', 0) > 0 else '❌ Missing'}
• Memory Optimization: {'✅ Optimized' if pattern_counts.get('memory_efficiency', 0) > 0 else '❌ Not Optimized'}
• Network Efficiency: {'✅ Optimized' if pattern_counts.get('network_optimization', 0) > 0 else '❌ Basic Implementation'}
"""
    
    # Add LLM analysis if requested
    if include_llm_analysis:
        llm_analysis = _run_llm_analysis("performance optimization", pattern_results, flagged_files or python_files[:3])
        report += f"\n{llm_analysis}"
        
        report += f"""
🔗 INTEGRATED PERFORMANCE ASSESSMENT:
Combined pattern detection and contextual analysis provides comprehensive
performance evaluation for high-frequency trading systems.
"""
    
    return report

# === Enhanced FinTech Compliance Analysis ===

@register_tool(tags=["fintech", "compliance", "security"])
def analyze_regulatory_compliance(project_path: str = ".", include_llm_analysis: bool = False) -> str:
    """
    Analyze codebase for regulatory compliance and security patterns.
    Covers data protection, audit logging, and access controls.
    
    Args:
        project_path: Path to analyze
        include_llm_analysis: Whether to include LLM contextual analysis
    
    Returns:
        Compliance analysis report with optional LLM insights
    """
    # Compliance patterns to detect
    compliance_patterns = {
        'data_protection': [
            r'encrypt|decrypt|hash|bcrypt',
            r'ssl|tls|https|certificate',
            r'personal_data|pii|gdpr'
        ],
        'audit_logging': [
            r'logging\.|log\.|audit',
            r'timestamp|datetime|utc',
            r'user_id|session_id|trace_id'
        ],
        'access_control': [
            r'authenticate|authorize|permission',
            r'role|rbac|access_control',
            r'@login_required|@requires_permission'
        ],
        'input_validation': [
            r'validate|sanitize|escape',
            r'sql_injection|xss|csrf',
            r'pydantic|marshmallow|cerberus'
        ]
    }
    
    # Security vulnerabilities that could cause compliance failures
    security_risks = {
        'hardcoded_secrets': [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']'
        ],
        'weak_crypto': [
            r'md5|sha1(?!256)',
            r'des_|3des_',
            r'random\.random\(\)'
        ],
        'insecure_defaults': [
            r'debug\s*=\s*True',
            r'verify\s*=\s*False',
            r'ssl_verify\s*=\s*False'
        ]
    }
    
    # Use existing recursive search function
    python_files = list_project_files_recursive(project_path, "*.py")
    
    compliance_score = 100
    pattern_counts = {}
    risk_counts = {}
    pii_files = 0
    flagged_files = []
    
    # PII indicators for data protection compliance
    pii_indicators = ['email', 'phone', 'ssn', 'credit_card', 'first_name', 'last_name']
    
    # Analyze each file for compliance patterns
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            file_has_issues = False
            
            # Check for PII handling
            if any(re.search(rf'\b{indicator}\b', content, re.IGNORECASE) for indicator in pii_indicators):
                pii_files += 1
            
            # Count compliance patterns (good)
            for pattern_type, patterns in compliance_patterns.items():
                for pattern in patterns:
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + matches
            
            # Count security risks (bad)
            for risk_type, patterns in security_risks.items():
                for pattern in patterns:
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    if matches > 0:
                        risk_counts[risk_type] = risk_counts.get(risk_type, 0) + matches
                        compliance_score -= (matches * 15)
                        file_has_issues = True
            
            # Track problematic files for LLM analysis
            if file_has_issues:
                flagged_files.append(file_path)
        
        except Exception:
            continue
    
    compliance_score = max(0, compliance_score)
    
    # Assess regulatory readiness
    sox_ready = (pattern_counts.get('audit_logging', 0) > 0 and 
                 pattern_counts.get('access_control', 0) > 0 and 
                 len(risk_counts) == 0)
    
    gdpr_ready = (pattern_counts.get('data_protection', 0) > 0 and pii_files > 0)
    
    pci_ready = (pattern_counts.get('data_protection', 0) > 0 and 
                 pattern_counts.get('input_validation', 0) > 0)
    
    # Pattern analysis results
    pattern_results = {
        'summary': f"Compliance Score: {compliance_score}/100, {len(risk_counts)} security risk types found",
        'key_findings': f"SOX: {'Ready' if sox_ready else 'Not Ready'}, GDPR: {'Ready' if gdpr_ready else 'Not Ready'}, PCI: {'Ready' if pci_ready else 'Not Ready'}",
        'flagged_files': flagged_files
    }
    
    report = f"""
🏛️ REGULATORY COMPLIANCE & SECURITY ANALYSIS
==========================================

Project: {project_path}
Files Analyzed: {len(python_files)}
Compliance Score: {compliance_score}/100
Files with PII: {pii_files}

📊 PATTERN-BASED ANALYSIS (Deterministic):

📋 COMPLIANCE PATTERNS DETECTED:
"""
    
    for pattern_type, count in pattern_counts.items():
        emoji = "✅" if count > 0 else "❌"
        report += f"{emoji} {pattern_type.replace('_', ' ').title()}: {count} instances\n"
    
    if risk_counts:
        report += f"\n⚠️ SECURITY RISKS DETECTED:\n"
        for risk_type, count in risk_counts.items():
            report += f"❌ {risk_type.replace('_', ' ').title()}: {count} instances\n"
    
    report += f"""
📋 REGULATORY READINESS:
• SOX (Sarbanes-Oxley): {'✅ Ready' if sox_ready else '❌ Not Ready'}
• GDPR (Data Protection): {'✅ Ready' if gdpr_ready else '❌ Not Ready'}
• PCI-DSS (Payment Security): {'✅ Ready' if pci_ready else '❌ Not Ready'}

🎯 PATTERN-BASED RECOMMENDATIONS:
• Audit trails for all financial transactions
• Data encryption for sensitive information
• Input validation to prevent injection attacks
• Role-based access control implementation
"""
    
    # Add LLM analysis if requested
    if include_llm_analysis:
        llm_analysis = _run_llm_analysis("regulatory compliance", pattern_results, flagged_files or python_files[:3])
        report += f"\n{llm_analysis}"
        
        report += f"""
🔗 INTEGRATED COMPLIANCE ASSESSMENT:
Pattern-based screening combined with contextual AI analysis provides
comprehensive regulatory compliance evaluation for financial services.
"""
    
    return report

# === Enhanced FinTech Architecture Analysis ===

@register_tool(tags=["fintech", "architecture", "analysis"])
def analyze_fintech_architecture_patterns(project_path: str = ".", include_llm_analysis: bool = False) -> str:
    """
    Analyze codebase for FinTech architectural patterns and API design.
    Evaluates microservices, security, and scalability patterns.
    
    Args:
        project_path: Path to analyze
        include_llm_analysis: Whether to include LLM contextual analysis
    
    Returns:
        Architecture analysis report with optional LLM insights
    """
    # Architecture patterns to detect
    architecture_patterns = {
        'microservices': [
            r'fastapi|flask|django',
            r'@app\.route|@api\.route',
            r'microservice|service_',
            r'docker|kubernetes'
        ],
        'api_security': [
            r'jwt|oauth|bearer',
            r'rate_limit|throttle',
            r'api_key|authorization',
            r'cors|csrf'
        ],
        'scalability': [
            r'redis|memcached|cache',
            r'queue|celery|rabbitmq',
            r'load_balancer|nginx',
            r'database.*pool'
        ],
        'monitoring': [
            r'prometheus|grafana',
            r'health_check|ping',
            r'metrics|monitoring',
            r'alert|notification'
        ]
    }
    
    # Use existing recursive search function
    python_files = list_project_files_recursive(project_path, "*.py")
    pattern_counts = {}
    api_endpoints = 0
    
    # Analyze each file for architecture patterns
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Count API endpoints
            api_matches = len(re.findall(r'@.*\.route|@get|@post|@put|@delete', content, re.IGNORECASE))
            api_endpoints += api_matches
            
            # Count architecture patterns
            for pattern_type, patterns in architecture_patterns.items():
                for pattern in patterns:
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + matches
        
        except Exception:
            continue
    
    # Calculate architecture maturity score
    architecture_score = 0
    max_score_per_category = 25
    
    for pattern_type, count in pattern_counts.items():
        if count > 0:
            architecture_score += max_score_per_category
    
    # Pattern analysis results
    pattern_results = {
        'summary': f"Architecture Maturity: {architecture_score}/100, {api_endpoints} API endpoints found",
        'key_findings': f"Patterns: {list(pattern_counts.keys())}, Microservices indicators: {pattern_counts.get('microservices', 0)}",
        'flagged_files': python_files[:3]  # Sample files for architecture review
    }
    
    report = f"""
🏗️ FINTECH ARCHITECTURE ANALYSIS
==============================

Project: {project_path}
Files Analyzed: {len(python_files)}
API Endpoints: {api_endpoints}
Architecture Maturity: {architecture_score}/100

📊 PATTERN-BASED ANALYSIS (Deterministic):

🔧 ARCHITECTURAL PATTERNS:
"""
    
    for pattern_type, count in pattern_counts.items():
        emoji = "✅" if count > 0 else "❌"
        report += f"{emoji} {pattern_type.replace('_', ' ').title()}: {count} instances\n"
    
    report += f"""
🎯 PATTERN-BASED ASSESSMENT:
• API Design: {'✅ RESTful' if api_endpoints > 0 else '❌ No APIs detected'}
• Security: {'✅ Implemented' if pattern_counts.get('api_security', 0) > 0 else '❌ Basic security'}
• Scalability: {'✅ Designed for scale' if pattern_counts.get('scalability', 0) > 0 else '❌ Monolithic design'}
• Monitoring: {'✅ Production ready' if pattern_counts.get('monitoring', 0) > 0 else '❌ No monitoring'}

💡 PATTERN-BASED RECOMMENDATIONS:
• Implement event-driven architecture for real-time processing
• Add circuit breakers to prevent cascade failures
• Use distributed caching for performance optimization
• Include comprehensive monitoring and alerting
"""
    
    # Add LLM analysis if requested
    if include_llm_analysis:
        llm_analysis = _run_llm_analysis("architecture", pattern_results, python_files[:3])
        report += f"\n{llm_analysis}"
        
        report += f"""
🔗 INTEGRATED ARCHITECTURE ASSESSMENT:
Pattern detection combined with architectural review provides comprehensive
evaluation of system design for financial services deployment.
"""
    
    return report

# === Comprehensive FinTech Analysis ===

@register_tool(tags=["fintech", "comprehensive", "analysis"])
def analyze_fintech_project_comprehensive(project_path: str = ".", include_llm_analysis: bool = False) -> str:
    """
    Perform comprehensive FinTech analysis covering all domains.
    Combines risk management, performance, compliance, and architecture analysis.
    
    Args:
        project_path: Path to analyze
        include_llm_analysis: Whether to include LLM contextual analysis for all domains
    
    Returns:
        Comprehensive FinTech analysis report with optional LLM insights
    """
    # Run all individual analyses with LLM option
    risk_analysis = analyze_financial_risk_patterns(project_path, include_llm_analysis)
    performance_analysis = analyze_hft_performance_patterns(project_path, include_llm_analysis)
    compliance_analysis = analyze_regulatory_compliance(project_path, include_llm_analysis)
    architecture_analysis = analyze_fintech_architecture_patterns(project_path, include_llm_analysis)
    
    # Combine results into comprehensive report
    comprehensive_report = f"""
🚀 COMPREHENSIVE FINTECH PROJECT ANALYSIS
========================================

Analysis Mode: {'Hybrid (Pattern + LLM)' if include_llm_analysis else 'Pattern-Based Only'}
Project: {project_path}

This analysis evaluates the project across all critical FinTech domains:
risk management, performance optimization, regulatory compliance, and architecture.

{risk_analysis}

{performance_analysis}

{compliance_analysis}

{architecture_analysis}

📊 OVERALL ASSESSMENT:
This comprehensive analysis provides insights across all critical areas for
financial technology applications. {'The hybrid approach combines deterministic pattern matching with AI-powered contextual analysis for complete coverage.' if include_llm_analysis else 'Pattern-based analysis provides consistent, audit-friendly baseline assessment.'}
"""
    
    return comprehensive_report

# === System Operations ===

@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."