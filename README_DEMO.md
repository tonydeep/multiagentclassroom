# Multi-Agent Classroom - Claude Agent SDK Demo

This is a demonstration of the Multi-Agent Classroom migrated to use the **Claude Agent SDK** instead of CrewAI.

## Overview

The Multi-Agent Classroom is an interactive learning environment where students collaborate with AI agents to solve math problems. The system features three AI personalities:

- **Harry**: Creative problem solver who links math concepts to magical/fictional analogies
- **Hermione**: Rigorous scholar who ensures mathematical accuracy and theoretical depth
- **Ron**: Empathetic questioner who asks clarifying questions and keeps the tone relaxed

## Migration to Claude Agent SDK

### What Changed

**Before (CrewAI)**:
- Multiple CrewAI crews for each agent personality
- Complex crew coordination with separate think/talk/evaluate tasks
- Google Gemini API as the LLM backend
- Heavy framework overhead

**After (Claude Agent SDK)**:
- Single Claude agent with custom MCP tools
- Simpler coordination through tool calls
- Anthropic Claude API (Sonnet 4.5)
- Lightweight, Python-native implementation

### Architecture

```
┌─────────────────────────────────────────┐
│         Flask + SocketIO Server         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      ClaudeDialogueManager              │
│  - Manages conversation state           │
│  - Coordinates agent turns              │
│  - Handles real-time updates            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│       Claude Agent SDK Client           │
│  + Custom MCP Tools:                    │
│    - get_agent_persona                  │
│    - evaluate_turn_taking               │
│    - generate_agent_response            │
│    - track_stage_progress               │
└─────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ (for Claude Agent SDK)
- Anthropic API key

### Setup

1. **Install Node.js dependencies** (required for Claude Agent SDK):

```bash
# Install Claude Code CLI globally
npm install -g @anthropic-ai/claude-code
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:

Create a `.env` file in the root directory:

```env
# Anthropic API Key (required)
ANTHROPIC_API_KEY=your_api_key_here

# Flask Secret Key (optional, defaults to dev key)
SECRET_KEY=your_secret_key_here
```

To get an Anthropic API key:
- Visit: https://console.anthropic.com/
- Sign up or log in
- Generate an API key from the API Keys section

## Running the Demo

### Quick Start

```bash
python demo_app.py
```

Then open your browser to: **http://localhost:5001**

### What to Expect

1. **Problem Selection**: Choose from sample math problems
2. **Enter Your Name**: Personalize the experience
3. **Start Learning**: Begin the interactive session
4. **Chat Interface**:
   - See agent status (idle, thinking, typing)
   - Send messages to the agents
   - Receive responses from Harry, Hermione, and Ron
   - Watch them collaborate to solve the problem

## Project Structure

```
multiagentclassroom/
├── flow_sdk/                      # New Claude Agent SDK implementation
│   ├── __init__.py
│   ├── agent_tools.py             # Custom MCP tools for agent coordination
│   └── dialogue_manager.py        # Main dialogue manager using Claude SDK
│
├── demo_app.py                    # Simplified Flask demo application
├── templates/
│   └── demo.html                  # Web interface for the demo
│
├── flow/                          # Original CrewAI implementation (preserved)
│   ├── dialogueFlow.py
│   └── crews/
│
├── requirements.txt               # Updated with Claude Agent SDK
├── .env                          # Environment variables (create this)
└── README_DEMO.md                # This file
```

## Key Features

### Custom MCP Tools

The system uses custom MCP (Model Context Protocol) tools to enable multi-agent coordination:

1. **`get_agent_persona`**: Retrieves persona information for a specific agent
2. **`get_all_personas`**: Gets all available agent personas
3. **`evaluate_turn_taking`**: Determines which agent should speak next
4. **`track_stage_progress`**: Monitors learning stage progression
5. **`generate_agent_response`**: Creates character-appropriate responses

### Real-Time Communication

- **Socket.IO**: Bidirectional communication between client and server
- **Agent Status Updates**: See when agents are thinking or typing
- **Live Messages**: Instant delivery of agent responses
- **Session Management**: Proper handling of multiple concurrent sessions

### Dialogue State Management

The system tracks:
- Conversation history
- Current learning stage
- Completed tasks
- Agent turn taking
- Inner thoughts (for debugging)

## API Endpoints

### REST API

- `GET /`: Main demo page
- `GET /api/problems`: List of sample problems
- `POST /api/start-session`: Create a new learning session

### Socket.IO Events

**Client → Server**:
- `join_session`: Join a specific session room
- `send_message`: Send a message to the agents
- `end_session`: End the current session

**Server → Client**:
- `agent_status`: Agent status updates (idle, thinking, typing)
- `new_message`: New message from an agent
- `system_status`: System status messages
- `error`: Error notifications

## Configuration

### Sample Problems

Edit `demo_app.py` to add more problems:

```python
SAMPLE_PROBLEMS = [
    {
        "id": "1",
        "title": "Your Problem Title",
        "problem": "Problem description..."
    }
]
```

### Learning Script

Modify `SIMPLE_SCRIPT` in `demo_app.py` to customize learning stages:

```python
SIMPLE_SCRIPT = {
    "1": {
        "id": "1",
        "name": "Stage Name",
        "goal": "Stage goal",
        "tasks": [
            {"id": "1.1", "description": "Task 1"},
            {"id": "1.2", "description": "Task 2"}
        ]
    }
}
```

### Agent Personas

Customize agent personalities in `flow_sdk/agent_tools.py`:

```python
AGENT_PERSONAS = {
    "AgentName": {
        "role": "Agent role description",
        "personality": "Personality traits",
        "tasks": ["Task 1", "Task 2"]
    }
}
```

## Troubleshooting

### Common Issues

1. **"Claude Code not found"**
   - Solution: Install Claude Code CLI: `npm install -g @anthropic-ai/claude-code`

2. **"API key not found"**
   - Solution: Set `ANTHROPIC_API_KEY` in your `.env` file

3. **"Import error: claude_agent_sdk"**
   - Solution: Run `pip install claude-agent-sdk`

4. **Agents not responding**
   - Check the server logs for errors
   - Verify your API key is valid
   - Check your internet connection

### Debug Mode

Enable Flask debug mode in `demo_app.py`:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

View logs in the terminal for detailed error information.

## Comparison: CrewAI vs Claude Agent SDK

| Aspect | CrewAI | Claude Agent SDK |
|--------|--------|------------------|
| **Setup Complexity** | High (multiple crews, agents, tasks) | Low (single client + tools) |
| **Dependencies** | CrewAI + LLM provider | Claude SDK only |
| **Performance** | Slower (multiple LLM calls) | Faster (optimized SDK) |
| **Cost** | Multiple API calls per turn | Optimized API usage |
| **Flexibility** | Rigid crew structure | Flexible tool-based approach |
| **Debugging** | Complex (multiple layers) | Simpler (direct tool calls) |
| **Maintenance** | High (framework updates) | Lower (SDK managed by Anthropic) |

## Future Enhancements

- [ ] Persistent database integration
- [ ] User authentication
- [ ] Session history viewing
- [ ] Advanced stage progression logic
- [ ] Custom problem creation interface
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Analytics dashboard

## License

This project is for educational purposes.

## Credits

- **Original Implementation**: CrewAI-based multi-agent system
- **Migration**: Claude Agent SDK implementation
- **Framework**: Anthropic Claude Agent SDK
- **LLM**: Claude Sonnet 4.5 by Anthropic

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Claude Agent SDK documentation: https://docs.claude.com/
3. Check Anthropic API status: https://status.anthropic.com/

---

**Note**: This is a demo application. For production use, add proper error handling, authentication, rate limiting, and security measures.
