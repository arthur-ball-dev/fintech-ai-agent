"""
Progressive Task Selection System
Better UX through step-by-step decision making for FinTech AI agents
"""

def step3_select_analysis_focus():
    """
    Step 3: High-level analysis focus selection
    Choose between FinTech analysis or basic utilities
    """
    print("\n🎯 Analysis Focus Selection")
    print("=" * 50)
    print("Choose your analysis approach:")
    print()
    
    print("1. 🏛️ FINTECH SPECIALIZED ANALYSIS (Pattern-Based)")
    print("   Advanced financial domain analysis with:")
    print("   • Trading system risk management")
    print("   • High-frequency trading optimization") 
    print("   • Regulatory compliance assessment")
    print("   • Enterprise architecture evaluation")
    print()
    
    print("2. 🛠️ BASIC FINTECH UTILITIES")
    print("   General-purpose operations with FinTech awareness:")
    print("   • Professional documentation generation")
    print("   • Code structure analysis")
    print("   • Project utility functions")
    print()
    
    choice = input("Select focus area (1=FinTech Analysis, 2=Basic Utilities): ").strip()
    
    if choice == "2":
        return step3b_select_utility_agent()
    else:
        return step3a_select_fintech_agent()


def step3a_select_fintech_agent():
    """
    Step 3a: FinTech Specialized Agent Selection
    6 specific financial analysis agents
    """
    print("\n🏦 FinTech Specialized Analysis Agents")
    print("=" * 50)
    print("Select your financial analysis focus:")
    print()
    
    agents = {
        1: {
            "name": "TRADING RISK MANAGEMENT AGENT",
            "description": "Position limits, stop losses, operational safeguards",
            "key": "risk_management"
        },
        2: {
            "name": "HIGH FREQUENCY TRADING PERFORMANCE OPTIMIZATION",
            "description": "Latency analysis, bottleneck identification, HFT readiness",
            "key": "performance"
        },
        3: {
            "name": "REGULATORY COMPLIANCE AGENT", 
            "description": "SOX, GDPR, PCI-DSS compliance and security assessment",
            "key": "compliance"
        },
        4: {
            "name": "ARCHITECTURE EVALUATION AGENT",
            "description": "Microservices, API security, enterprise scalability",
            "key": "architecture"
        },
        5: {
            "name": "COMPREHENSIVE ANALYSIS AGENT",
            "description": "Complete analysis across all FinTech domains",
            "key": "comprehensive"
        },
        6: {
            "name": "CUSTOM ANALYSIS",
            "description": "Specify your custom FinTech analysis requirements",
            "key": "custom"
        }
    }
    
    for num, agent in agents.items():
        print(f"{num}. 🔹 {agent['name']}")
        print(f"   {agent['description']}")
        print()
    
    choice = input("Select agent (1-6): ").strip()
    
    try:
        selected = int(choice)
        if 1 <= selected <= 6:
            agent_info = agents[selected]
            if selected == 6:  # Custom analysis
                custom_task = input("Describe your custom FinTech analysis needs: ").strip()
                return step5_hybrid_analysis_option(agent_info, custom_task)
            else:
                return step4_select_specific_tasks(agent_info)
        else:
            print("Invalid selection. Using Comprehensive Analysis.")
            return step4_select_specific_tasks(agents[5])
    except ValueError:
        print("Invalid input. Using Comprehensive Analysis.")
        return step4_select_specific_tasks(agents[5])


def step3b_select_utility_agent():
    """
    Step 3b: Basic Utility Agent Selection  
    4 utility-focused agents
    """
    print("\n🛠️ Basic FinTech Utilities")
    print("=" * 40)
    print("Select your utility focus:")
    print()
    
    utilities = {
        1: {
            "name": "DOCUMENTATION AGENT",
            "description": "Professional README, technical docs, compliance templates",
            "key": "readme"
        },
        2: {
            "name": "GENERAL CODE ANALYSIS AGENT",
            "description": "Code structure analysis with FinTech pattern recognition",
            "key": "code_analysis"
        },
        3: {
            "name": "PROJECT UTILITIES AGENT", 
            "description": "GitHub structure, metrics, executive briefings",
            "key": "file_explorer"
        },
        4: {
            "name": "CUSTOM UTILITY AGENT",
            "description": "Custom documentation or analysis task",
            "key": "custom_utility"
        }
    }
    
    for num, utility in utilities.items():
        print(f"{num}. 📋 {utility['name']}")
        print(f"   {utility['description']}")
        print()
    
    choice = input("Select utility (1-4): ").strip()
    
    try:
        selected = int(choice)
        if 1 <= selected <= 4:
            utility_info = utilities[selected]
            if selected == 4:  # Custom utility
                custom_task = input("Describe your custom utility needs: ").strip()
                return {
                    'agent_key': utility_info['key'],
                    'agent_name': utility_info['name'], 
                    'task': custom_task,
                    'use_hybrid': False,
                    'category': 'Basic Utilities'
                }
            else:
                return step4_select_utility_tasks(utility_info)
        else:
            print("Invalid selection. Using Documentation Agent.")
            return step4_select_utility_tasks(utilities[1])
    except ValueError:
        print("Invalid input. Using Documentation Agent.")
        return step4_select_utility_tasks(utilities[1])


def step4_select_specific_tasks(agent_info):
    """
    Step 4: Select specific tasks for chosen FinTech agent
    Different task sets based on agent type
    """
    print(f"\n📋 {agent_info['name']} - Task Selection")
    print("=" * 60)
    
    # Define tasks for each agent type
    task_sets = {
        "risk_management": [
            "Trading system risk controls assessment (position limits, stop losses, circuit breakers)",
            "Operational risk pattern analysis with control gap identification", 
            "Portfolio risk management evaluation with VaR considerations",
            "Risk control maturity assessment for trading environments"
        ],
        "performance": [
            "High-frequency trading latency analysis and bottleneck identification",
            "Trading system performance patterns with optimization recommendations",
            "Memory efficiency and network optimization assessment",
            "HFT readiness evaluation with specific performance metrics"
        ],
        "compliance": [
            "Financial services compliance analysis (SOX, GDPR, PCI-DSS)",
            "Security vulnerability assessment with regulatory context", 
            "Data protection and audit logging compliance review",
            "Regulatory readiness evaluation for financial services"
        ],
        "architecture": [
            "FinTech system architecture patterns and scalability assessment",
            "Microservices and API security analysis for financial services",
            "Enterprise deployment readiness evaluation",
            "Technology stack assessment for financial applications"
        ],
        "comprehensive": [
            "Complete FinTech assessment across all domains (risk, performance, compliance, architecture)",
            "Cross-domain integration analysis with strategic recommendations",
            "Enterprise-grade system evaluation for financial services",
            "Comprehensive technical capability demonstration"
        ]
    }
    
    tasks = task_sets.get(agent_info['key'], task_sets['comprehensive'])
    
    print("Available tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print(f"{len(tasks) + 1}. 💭 Custom task for this agent")
    print()
    
    choice = input(f"Select task (1-{len(tasks) + 1}): ").strip()
    
    try:
        task_num = int(choice)
        if 1 <= task_num <= len(tasks):
            selected_task = tasks[task_num - 1]
        else:
            selected_task = input("Describe your custom task: ").strip()
    except ValueError:
        if choice:
            selected_task = choice
        else:
            selected_task = tasks[0]  # Default to first task
    
    return step5_hybrid_analysis_option(agent_info, selected_task)


def step4_select_utility_tasks(utility_info):
    """
    Step 4: Select tasks for utility agents (simpler, no hybrid option)
    """
    print(f"\n📋 {utility_info['name']} - Task Selection")
    print("=" * 50)
    
    # Define tasks for utility agents
    utility_tasks = {
        "readme": [
            "Generate professional README highlighting FinTech capabilities",
            "Create technical documentation for financial services deployment",
            "Generate compliance documentation templates",
            "Create executive summary of technical capabilities"
        ],
        "code_analysis": [
            "Basic code structure analysis with FinTech pattern recognition",
            "File exploration with financial technology awareness", 
            "Project summary with emphasis on enterprise-grade features",
            "Technical debt assessment with FinTech focus"
        ],
        "file_explorer": [
            "Create GitHub repository structure for FinTech portfolios",
            "Generate project metrics and technical capabilities summary",
            "Prepare executive briefing materials",
            "Create professional project presentation structure"
        ]
    }
    
    tasks = utility_tasks.get(utility_info['key'], utility_tasks['readme'])
    
    print("Available tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print(f"{len(tasks) + 1}. 💭 Custom task")
    print()
    
    choice = input(f"Select task (1-{len(tasks) + 1}): ").strip()
    
    try:
        task_num = int(choice)
        if 1 <= task_num <= len(tasks):
            selected_task = tasks[task_num - 1]
        else:
            selected_task = input("Describe your custom task: ").strip()
    except ValueError:
        if choice:
            selected_task = choice
        else:
            selected_task = tasks[0]
    
    return {
        'agent_key': utility_info['key'],
        'agent_name': utility_info['name'],
        'task': selected_task, 
        'use_hybrid': False,
        'category': 'Basic Utilities'
    }


def step5_hybrid_analysis_option(agent_info, selected_task):
    """
    Step 5: Ask if user wants hybrid analysis (Pattern + AI)
    Only for FinTech analysis agents
    """
    print(f"\n🤖 Analysis Mode Selection")
    print("=" * 40)
    print(f"Agent: {agent_info['name']}")
    print(f"Task: {selected_task}")
    print()
    
    print("Choose your analysis approach:")
    print()
    print("1. 📊 PATTERN-BASED ANALYSIS (Default)")
    print("   • Fast, consistent, audit-friendly")
    print("   • Deterministic pattern matching") 
    print("   • No additional LLM costs")
    print("   • Professional baseline assessment")
    print()
    
    print("2. 🧠 HYBRID ANALYSIS (Pattern + AI-Powered)")
    print("   • Deep insights with business context")
    print("   • AI-powered strategic recommendations")
    print("   • Comprehensive contextual analysis")
    print("   • Maximum insight depth")
    print()
    
    choice = input("Select analysis mode (1=Pattern-Based, 2=Hybrid): ").strip()
    
    use_hybrid = (choice == "2")
    
    if use_hybrid:
        print("✅ Selected: Hybrid Analysis (Pattern + AI-Powered)")
        agent_key = f"hybrid_{agent_info['key']}" if agent_info['key'] != 'custom' else 'hybrid_comprehensive'
        category = 'Hybrid Analysis'
    else:
        print("✅ Selected: Pattern-Based Analysis")
        agent_key = agent_info['key'] if agent_info['key'] != 'custom' else 'comprehensive'
        category = 'FinTech Specialized'
    
    return {
        'agent_key': agent_key,
        'agent_name': agent_info['name'],
        'task': selected_task,
        'use_hybrid': use_hybrid,
        'category': category
    }


def run_progressive_task_selection():
    """
    Main function to run the complete progressive task selection
    Steps 1-2 (LLM provider/tier) would be called before this
    """
    print("\n🎯 Progressive Task Selection")
    print("=" * 50)
    
    # Step 3: Analysis focus
    result = step3_select_analysis_focus()
    
    print(f"\n✅ Task Selection Complete!")
    print("=" * 50)
    print(f"Agent: {result['agent_name']}")
    print(f"Category: {result['category']}")
    print(f"Task: {result['task']}")
    if result.get('use_hybrid'):
        print(f"Analysis Mode: Hybrid (Pattern + AI-Powered)")
    else:
        print(f"Analysis Mode: Pattern-Based")
    
    return result


def display_selection_summary(result):
    """
    Display a professional summary of the user's selections
    """
    print(f"\n📊 Selection Summary")
    print("=" * 50)
    print(f"🤖 Agent: {result['agent_name']}")
    print(f"📂 Category: {result['category']}")
    print(f"🎯 Task: {result['task']}")
    
    if result.get('use_hybrid'):
        print(f"🧠 Analysis: Hybrid (Pattern + AI)")
        print(f"   • Combines deterministic pattern matching")
        print(f"   • With AI-powered contextual insights")
    else:
        print(f"📊 Analysis: Pattern-Based")
        print(f"   • Fast, consistent, audit-friendly")
        print(f"   • Deterministic pattern matching")
    
    print(f"🔑 Agent Key: {result['agent_key']}")


if __name__ == "__main__":
    # Demo the progressive selection
    result = run_progressive_task_selection()
    display_selection_summary(result)
