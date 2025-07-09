"""
Progressive Selection Validation Script (Updated for progressive_agent_selection.py)
Validates that the progressive selection system is properly installed and configured
"""
import os
import sys
import traceback

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def validate_file_structure():
    """Validate that all required files are present"""
    print("📁 Validating File Structure...")

    required_files = [
        "src/agents/file_explorer/progressive_agent_selection.py",  # CORRECTED FILENAME
        "src/agents/file_explorer/__init__.py",
        "src/agents/file_explorer/agent_registry.py",
        "src/agents/file_explorer/basic_agents.py",
        "src/agents/file_explorer/fintech_agents.py",
        "src/agents/file_explorer/hybrid_agents.py",
        "src/agents/file_explorer/actions.py",
        "src/examples/run_fintech_agents.py",
        "src/framework/llm/client.py"
    ]

    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n⚠️  {len(missing_files)} required files are missing!")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files found!")
        return True

def validate_imports():
    """Validate that all imports work correctly"""
    print("\n📦 Validating Module Imports...")

    import_tests = [
        ("Progressive Selection", "from src.agents.file_explorer.progressive_agent_selection import run_progressive_task_selection"),  # CORRECTED IMPORT
        ("Agent Registry", "from src.agents.file_explorer.agent_registry import create_agent_by_key"),
        ("Basic Agents", "from src.agents.file_explorer.basic_agents import create_file_explorer_agent"),
        ("FinTech Agents", "from src.agents.file_explorer.fintech_agents import create_risk_management_agent"),
        ("Hybrid Agents", "from src.agents.file_explorer.hybrid_agents import create_hybrid_risk_management_agent"),
        ("LLM Client", "from src.framework.llm.client import LLMClient"),
        ("Actions", "from src.agents.file_explorer.actions import analyze_financial_risk_patterns")
    ]

    failed_imports = []
    for test_name, import_statement in import_tests:
        try:
            exec(import_statement)
            print(f"✅ {test_name}")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
            failed_imports.append((test_name, str(e)))

    if failed_imports:
        print(f"\n⚠️  {len(failed_imports)} import errors found!")
        for test_name, error in failed_imports:
            print(f"   {test_name}: {error}")
        return False
    else:
        print(f"\n✅ All {len(import_tests)} imports successful!")
        return True

def validate_agent_creation():
    """Validate that all agents can be created successfully"""
    print("\n🤖 Validating Agent Creation...")

    try:
        from src.agents.file_explorer import AGENT_KEY_MAPPING, create_agent_by_key

        agent_tests = [
            ("risk_management", "Trading Risk Management Agent"),
            ("performance", "HFT Performance Agent"),
            ("compliance", "Regulatory Compliance Agent"),
            ("architecture", "Architecture Evaluation Agent"),
            ("comprehensive", "Comprehensive FinTech Agent"),
            ("hybrid_risk_management", "Hybrid Risk Management Agent"),
            ("hybrid_compliance", "Hybrid Compliance Agent"),
            ("readme", "Documentation Agent"),
            ("code_analysis", "Code Analysis Agent"),
            ("file_explorer", "File Explorer Agent")
        ]

        failed_agents = []
        for agent_key, agent_name in agent_tests:
            try:
                agent = create_agent_by_key(agent_key)

                # Validate agent has required components
                if hasattr(agent, 'goals') and hasattr(agent, 'actions'):
                    actions_count = len(agent.actions.get_actions())
                    print(f"✅ {agent_name} ({actions_count} tools)")
                else:
                    print(f"⚠️  {agent_name} - Missing required components")
                    failed_agents.append((agent_key, "Missing goals or actions"))

            except Exception as e:
                print(f"❌ {agent_name} - ERROR: {str(e)}")
                failed_agents.append((agent_key, str(e)))

        if failed_agents:
            print(f"\n⚠️  {len(failed_agents)} agent creation errors!")
            return False
        else:
            print(f"\n✅ All {len(agent_tests)} agents created successfully!")
            return True

    except Exception as e:
        print(f"❌ Agent validation failed: {str(e)}")
        return False

def validate_progressive_selection_functions():
    """Validate that progressive selection functions work"""
    print("\n🎯 Validating Progressive Selection Functions...")

    try:
        from src.agents.file_explorer.progressive_agent_selection import (  # CORRECTED IMPORT
            step3_select_analysis_focus,
            step3a_select_fintech_agent,
            step3b_select_utility_agent,
            step4_select_specific_tasks,
            step4_select_utility_tasks,
            step5_hybrid_analysis_option,
            run_progressive_task_selection,
            display_selection_summary
        )

        functions = [
            "step3_select_analysis_focus",
            "step3a_select_fintech_agent",
            "step3b_select_utility_agent",
            "step4_select_specific_tasks",
            "step4_select_utility_tasks",
            "step5_hybrid_analysis_option",
            "run_progressive_task_selection",
            "display_selection_summary"
        ]

        for func_name in functions:
            if func_name in locals():
                print(f"✅ {func_name}")
            else:
                print(f"❌ {func_name} - NOT FOUND")
                return False

        print(f"\n✅ All {len(functions)} progressive selection functions available!")
        return True

    except Exception as e:
        print(f"❌ Progressive selection validation failed: {str(e)}")
        return False

def validate_llm_configuration():
    """Validate LLM provider configuration"""
    print("\n🔧 Validating LLM Configuration...")

    try:
        from src.framework.llm.client import LLMClient, LLMConfig

        # Test configuration
        config = LLMConfig()
        print(f"✅ LLMConfig created")

        # Check for API keys
        openai_key = config.openai_api_key is not None
        anthropic_key = config.anthropic_api_key is not None

        print(f"{'✅' if openai_key else '❌'} OpenAI API Key: {'Set' if openai_key else 'Not Set'}")
        print(f"{'✅' if anthropic_key else '❌'} Anthropic API Key: {'Set' if anthropic_key else 'Not Set'}")

        if not openai_key and not anthropic_key:
            print("⚠️  No API keys configured - LLM functionality will not work")
            print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables")
            return False

        # Test client creation
        try:
            client = LLMClient()
            status = client.get_provider_status()
            available_providers = [p for p, info in status.items() if info['available']]

            print(f"✅ LLMClient created")
            print(f"✅ Available providers: {', '.join(available_providers)}")

            return True

        except Exception as e:
            print(f"❌ LLMClient creation failed: {str(e)}")
            return False

    except Exception as e:
        print(f"❌ LLM configuration validation failed: {str(e)}")
        return False

def validate_fintech_tools():
    """Validate that FinTech analysis tools are available"""
    print("\n🏦 Validating FinTech Analysis Tools...")

    try:
        from src.agents.file_explorer.actions import (
            analyze_financial_risk_patterns,
            analyze_hft_performance_patterns,
            analyze_regulatory_compliance,
            analyze_fintech_architecture_patterns,
            analyze_fintech_project_comprehensive
        )

        tools = [
            "analyze_financial_risk_patterns",
            "analyze_hft_performance_patterns",
            "analyze_regulatory_compliance",
            "analyze_fintech_architecture_patterns",
            "analyze_fintech_project_comprehensive"
        ]

        for tool_name in tools:
            print(f"✅ {tool_name}")

        print(f"\n✅ All {len(tools)} FinTech analysis tools available!")
        return True

    except Exception as e:
        print(f"❌ FinTech tools validation failed: {str(e)}")
        return False

def run_comprehensive_validation():
    """Run all validation tests"""
    print("🔍 Comprehensive Progressive Selection Validation")
    print("=" * 60)

    validation_results = {
        "File Structure": validate_file_structure(),
        "Module Imports": validate_imports(),
        "Agent Creation": validate_agent_creation(),
        "Progressive Selection": validate_progressive_selection_functions(),
        "LLM Configuration": validate_llm_configuration(),
        "FinTech Tools": validate_fintech_tools()
    }

    print("\n📊 Validation Summary")
    print("=" * 30)

    passed = 0
    total = len(validation_results)

    for test_name, result in validation_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n📈 Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("\n🎉 VALIDATION SUCCESSFUL!")
        print("Your progressive selection system is ready to use!")
        print("\n🚀 To run: python src/examples/run_fintech_agents.py")
        return True
    else:
        print(f"\n⚠️  VALIDATION INCOMPLETE!")
        print(f"Please fix the {total - passed} failing test(s) before using the system.")
        return False

def test_sample_selection():
    """Test a sample progressive selection flow (without user input)"""
    print("\n🧪 Testing Sample Selection Flow...")

    try:
        # Test creating a sample selection result
        sample_result = {
            'agent_key': 'risk_management',
            'agent_name': 'TRADING RISK MANAGEMENT AGENT',
            'task': 'Trading system risk controls assessment',
            'use_hybrid': False,
            'category': 'FinTech Specialized'
        }

        # Test that we can create the agent from this result
        from src.agents.file_explorer import create_agent_by_key
        agent = create_agent_by_key(sample_result['agent_key'])

        print("✅ Sample selection flow test successful")
        print(f"   Agent: {sample_result['agent_name']}")
        print(f"   Tools available: {len(agent.actions.get_actions())}")

        return True

    except Exception as e:
        print(f"❌ Sample selection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        print(f"Progressive Selection Validation Script")
        print(f"Project Root: {project_root}")
        print()

        # Run comprehensive validation
        success = run_comprehensive_validation()

        if success:
            # Run additional sample test
            test_sample_selection()

            print("\n💡 Next Steps:")
            print("1. Run: python src/examples/run_fintech_agents.py")
            print("2. Test the progressive selection with real user input")
            print("3. Try different agent types and analysis modes")
            print("4. Verify that your existing functionality still works")

        exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Validation interrupted by user.")
        exit(1)
    except Exception as e:
        print(f"\n💥 Validation script error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        exit(1)