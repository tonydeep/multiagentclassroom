# Testing Guide for Multi-Agent Classroom Demo

This guide helps you test the Claude Agent SDK implementation.

## Prerequisites

Before testing, ensure you have:

1. ✅ Python 3.10+ installed
2. ✅ Node.js 18+ installed
3. ✅ Anthropic API key
4. ✅ All dependencies installed

## Step 1: Install Dependencies

```bash
# Install Node.js dependencies (required for Claude Agent SDK)
npm install -g @anthropic-ai/claude-code

# Install Python dependencies
pip install -r requirements.txt
```

Expected output:
```
Successfully installed flask flask-socketio flask-cors anthropic claude-agent-sdk python-dotenv pyyaml
```

## Step 2: Verify Installation

Run the integration test:

```bash
python test_sdk.py
```

Expected output:
```
============================================================
Claude Agent SDK Integration - Quick Test
============================================================
Testing imports...
✓ flow_sdk modules imported successfully
✓ claude_agent_sdk imported successfully
✓ Flask modules imported successfully

Testing agent personas...
✓ Harry persona found
✓ Hermione persona found
✓ Ron persona found

Testing MCP server creation...
✓ MCP server created successfully

Checking API key...
✓ ANTHROPIC_API_KEY is set

============================================================
Test Results:
============================================================
Imports             : ✓ PASS
Agent Personas      : ✓ PASS
MCP Server          : ✓ PASS
API Key             : ✓ PASS
============================================================

🎉 All tests passed! You can run the demo with:
   python demo_app.py
```

## Step 3: Set Up Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

Your `.env` file should contain:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
SECRET_KEY=any-random-string-for-flask
```

## Step 4: Run the Demo

Start the server:

```bash
python demo_app.py
```

Expected output:
```
============================================================
Multi-Agent Classroom - Claude Agent SDK Demo
============================================================

Starting server on http://localhost:5001
Make sure you have set ANTHROPIC_API_KEY in your .env file

 * Serving Flask app 'demo_app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://localhost:5001
```

## Step 5: Test the Web Interface

### 5.1 Open Browser

Navigate to: **http://localhost:5001**

You should see:
- Header: "🎓 Multi-Agent Classroom"
- Subtitle: "Powered by Claude Agent SDK"
- Three problem cards to choose from

### 5.2 Start a Session

1. Click on a problem card (it should highlight)
2. Enter your name (or use default "Student")
3. Click "Bắt đầu học" (Start Learning)

Expected behavior:
- Setup screen fades out
- Chat screen appears
- Three agent badges show: Harry, Hermione, Ron
- All agents show "idle" status (gray indicator)

### 5.3 Send a Message

1. Type a message in the input box (e.g., "Xin chào! Hãy giúp tôi giải bài này.")
2. Click "Gửi" (Send) or press Enter

Expected behavior:
- Your message appears in the chat (right side, purple bubble)
- System message appears: "Đang phân tích tin nhắn..." (Analyzing message...)
- Agent indicators change to "thinking" (yellow, pulsing)
- After 2-10 seconds, one agent responds
- Agent indicator changes to "typing" (green, pulsing) while responding
- Agent message appears (left side, white bubble with agent name/avatar)
- Agent indicator returns to "idle" (gray)

### 5.4 Continue Conversation

Send more messages to test:
- Multi-turn conversation
- Different agent responses
- Vietnamese language handling

## Step 6: Test Agent Behavior

### Test Case 1: Creative Response (Harry)
Send: "Làm thế nào để giải phương trình này?"

Expected: Harry might respond with a creative/magical analogy

### Test Case 2: Precise Explanation (Hermione)
Send: "Công thức nào được sử dụng?"

Expected: Hermione might provide a precise mathematical explanation

### Test Case 3: Clarifying Question (Ron)
Send: "Tôi không hiểu bước này."

Expected: Ron might ask clarifying questions to help understand

## Troubleshooting

### Issue 1: "No module named 'claude_agent_sdk'"

**Solution:**
```bash
# Ensure Claude Code is installed globally
npm install -g @anthropic-ai/claude-code

# Reinstall Python package
pip install --upgrade claude-agent-sdk
```

### Issue 2: "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep ANTHROPIC_API_KEY

# If missing, add it
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

### Issue 3: Agents not responding

**Check server logs for errors:**
- Look for API errors (rate limit, invalid key)
- Check for parsing errors in agent responses
- Verify Socket.IO connection in browser console

**Browser Console Check:**
```javascript
// Open browser DevTools (F12)
// Check Console tab for:
"Connected to server" ✓
"Agent status: ..." ✓
```

### Issue 4: Socket.IO connection fails

**Solution:**
```bash
# Reinstall flask-socketio
pip install --upgrade flask-socketio python-socketio

# Try different async_mode
# Edit demo_app.py line 16:
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
# or
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
```

### Issue 5: Port 5001 already in use

**Solution:**
```bash
# Use a different port
# Edit demo_app.py, change last line:
socketio.run(app, debug=True, host='0.0.0.0', port=5002)
```

## Performance Testing

### Test 1: Response Time
- Normal response: 2-10 seconds
- First response may be slower (model initialization)

### Test 2: Multiple Sessions
- Open demo in multiple browser tabs
- Each should maintain separate sessions

### Test 3: Long Conversations
- Send 10+ messages
- Verify conversation history is maintained
- Check log file in `logs/` directory

## Log Files

Check generated logs:

```bash
# List log files
ls -la logs/

# View a log file
cat logs/<session-id>.log
```

Log format:
```
Script:
[Script information]

Conversation:
[Conversation history]

Turn: 1.
TIME=... | CON#1 | SENDER=Student | TEXT=...
Turn: 2.
TIME=... | CON#2 | SENDER=Harry | TEXT=...
```

## API Usage Monitoring

Monitor your Anthropic API usage:
1. Visit: https://console.anthropic.com/
2. Check "Usage" section
3. Verify API calls are being made
4. Monitor token consumption

Expected usage per turn:
- Input tokens: ~500-2000 (depending on conversation history)
- Output tokens: ~200-500 (agent response)

## Success Criteria

✅ Demo passes all these tests:

1. **Installation**
   - [ ] All dependencies install without errors
   - [ ] test_sdk.py passes all checks

2. **Server Startup**
   - [ ] Flask server starts on port 5001
   - [ ] No errors in console

3. **Web Interface**
   - [ ] Page loads correctly
   - [ ] Problem selection works
   - [ ] Session creation succeeds

4. **Agent Interaction**
   - [ ] User messages appear correctly
   - [ ] Agents respond within 10 seconds
   - [ ] Responses are in Vietnamese
   - [ ] Responses are character-appropriate
   - [ ] Agent status indicators update

5. **Multi-Turn Conversation**
   - [ ] Can send multiple messages
   - [ ] Conversation context is maintained
   - [ ] Different agents take turns

6. **Error Handling**
   - [ ] Graceful handling of API errors
   - [ ] Proper error messages displayed
   - [ ] System status updates shown

## Advanced Testing

### Test Custom Problems

Edit `demo_app.py` to add custom problems:

```python
SAMPLE_PROBLEMS = [
    {
        "id": "custom1",
        "title": "Your Problem Title",
        "problem": "Your problem description"
    }
]
```

### Test Different Agent Configurations

Edit `flow_sdk/agent_tools.py` to modify agent personas:

```python
AGENT_PERSONAS = {
    "YourAgent": {
        "role": "Agent role",
        "personality": "Personality traits",
        "tasks": ["Task 1", "Task 2"]
    }
}
```

### Test Stage Progression

Modify `SIMPLE_SCRIPT` in `demo_app.py` to test different learning stages.

## Reporting Issues

If you encounter issues:

1. **Capture logs:**
   ```bash
   python demo_app.py > demo.log 2>&1
   ```

2. **Check browser console:**
   - Open DevTools (F12)
   - Copy any error messages

3. **Provide details:**
   - Python version: `python --version`
   - Node version: `node --version`
   - OS: `uname -a` (Linux/Mac) or `ver` (Windows)
   - Error messages from logs

## Next Steps

After successful testing:

1. **Customize the demo** for your use case
2. **Add more problems** to the problem set
3. **Extend agent personas** with new characters
4. **Implement database** for persistent sessions
5. **Add authentication** for multi-user support

---

**Need help?** Check README_DEMO.md for more detailed documentation.
