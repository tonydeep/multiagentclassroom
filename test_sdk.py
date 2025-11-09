"""
Quick test script to verify Claude Agent SDK integration.
This script tests the basic imports and MCP tool creation.
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        from flow_sdk import ClaudeDialogueManager, DialogueState, AGENT_PERSONAS
        print("✓ flow_sdk modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import flow_sdk: {e}")
        return False

    try:
        from claude_agent_sdk import create_sdk_mcp_server, tool
        print("✓ claude_agent_sdk imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import claude_agent_sdk: {e}")
        print("  → Run: pip install claude-agent-sdk")
        return False

    try:
        import flask
        import flask_socketio
        import flask_cors
        print("✓ Flask modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Flask modules: {e}")
        print("  → Run: pip install -r requirements.txt")
        return False

    return True


def test_agent_personas():
    """Test that agent personas are properly defined."""
    print("\nTesting agent personas...")

    from flow_sdk import AGENT_PERSONAS

    expected_agents = ["Harry", "Hermione", "Ron"]
    for agent in expected_agents:
        if agent in AGENT_PERSONAS:
            print(f"✓ {agent} persona found")
        else:
            print(f"✗ {agent} persona missing")
            return False

    return True


def test_mcp_server_creation():
    """Test that MCP server can be created with custom tools."""
    print("\nTesting MCP server creation...")

    try:
        from claude_agent_sdk import create_sdk_mcp_server
        from flow_sdk.agent_tools import (
            get_agent_persona,
            get_all_personas,
            evaluate_turn_taking
        )

        server = create_sdk_mcp_server(
            name="test-tools",
            version="1.0.0",
            tools=[get_agent_persona, get_all_personas, evaluate_turn_taking]
        )

        print("✓ MCP server created successfully")
        return True

    except Exception as e:
        print(f"✗ Failed to create MCP server: {e}")
        return False


def test_api_key():
    """Check if API key is set."""
    print("\nChecking API key...")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print("✓ ANTHROPIC_API_KEY is set")
        return True
    else:
        print("⚠ ANTHROPIC_API_KEY not found in environment")
        print("  → Set it in your .env file to run the demo")
        return None  # Warning, not failure


def main():
    """Run all tests."""
    print("=" * 60)
    print("Claude Agent SDK Integration - Quick Test")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Agent Personas", test_agent_personas()))
    results.append(("MCP Server", test_mcp_server_creation()))
    results.append(("API Key", test_api_key()))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    all_passed = True
    for test_name, result in results:
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
            all_passed = False
        else:
            status = "⚠ WARNING"

        print(f"{test_name:20s}: {status}")

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! You can run the demo with:")
        print("   python demo_app.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
