"""
Dialogue Manager using Claude Agent SDK for multi-agent classroom.
Replaces the CrewAI-based dialogue flow with a simpler Claude-powered system.
"""
import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import deque

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server
from flow_sdk.agent_tools import (
    get_agent_persona,
    get_all_personas,
    evaluate_turn_taking,
    track_stage_progress,
    generate_agent_response
)


@dataclass
class DialogueState:
    """State management for the dialogue session."""
    conversation: str = ""
    participants: List[str] = field(default_factory=lambda: ["Harry", "Hermione", "Ron"])
    turn_number: int = 0
    problem: str = ""
    current_stage_description: str = ""
    current_stage_id: str = "1"
    completed_task_ids: List[str] = field(default_factory=list)
    script: Dict = field(default_factory=dict)
    stage_state: Dict = field(default_factory=dict)
    inner_thoughts: deque = field(default_factory=lambda: deque(maxlen=5))
    is_processing: bool = False


class ClaudeDialogueManager:
    """
    Manages multi-agent dialogue using Claude Agent SDK.
    Replaces CrewAI crews with a single Claude agent that simulates multiple personas.
    """

    def __init__(self, socketio, **kwargs):
        """
        Initialize the dialogue manager.

        Args:
            socketio: Socket.IO instance for real-time communication
            **kwargs: Configuration parameters including:
                - conversation: Initial conversation history
                - problem: The math problem
                - participants: List of agent names
                - script: Learning script with stages
                - current_stage_id: Current stage ID
                - session_id: Session identifier
                - user_name: User's name
                - etc.
        """
        self.socketio = socketio
        self.session_id = kwargs.get("session_id", "")
        self.user_name = kwargs.get("user_name", "User")
        self.filename = kwargs.get("filename", f"logs/{self.session_id}.log")

        # Initialize state
        self.state = DialogueState(
            conversation=kwargs.get("conversation", ""),
            problem=kwargs.get("problem", ""),
            participants=kwargs.get("participants", ["Harry", "Hermione", "Ron"]),
            script=kwargs.get("script", {}),
            current_stage_id=kwargs.get("current_stage_id", "1"),
            turn_number=kwargs.get("turn_number", 0),
            inner_thoughts=kwargs.get("inner_thought", deque(maxlen=5))
        )

        # Extract current stage description from script
        self._update_stage_description()

        # Create MCP server with custom tools
        self.mcp_server = create_sdk_mcp_server(
            name="classroom-tools",
            version="1.0.0",
            tools=[
                get_agent_persona,
                get_all_personas,
                evaluate_turn_taking,
                track_stage_progress,
                generate_agent_response
            ]
        )

        # Claude Agent SDK options
        self.agent_options = ClaudeAgentOptions(
            mcp_servers={"classroom": self.mcp_server},
            allowed_tools=[
                "mcp__classroom__get_agent_persona",
                "mcp__classroom__get_all_personas",
                "mcp__classroom__evaluate_turn_taking",
                "mcp__classroom__track_stage_progress",
                "mcp__classroom__generate_agent_response"
            ],
            max_turns=10,
            system_prompt=self._build_system_prompt()
        )

        self._is_cancelled = False
        self._processing_lock = asyncio.Lock()

        # Initialize log file
        if self.state.turn_number == 0:
            self._initialize_log_file()

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Claude."""
        return f"""You are orchestrating a multi-agent learning environment where students discuss math problems.

**Your Role**: You manage a classroom with three AI student agents:
- **Harry**: Creative problem solver who links math to magical/fictional analogies
- **Hermione**: Rigorous scholar who ensures mathematical accuracy
- **Ron**: Empathetic questioner who asks clarifying questions

**Current Problem**: {self.state.problem}

**Current Learning Stage**: {self.state.current_stage_description}

**Your Tasks**:
1. When a user sends a message, analyze the conversation context
2. Decide which agent (Harry, Hermione, or Ron) should respond next based on:
   - The conversation flow
   - Each agent's persona and strengths
   - The current learning stage objectives
3. Generate the agent's response staying true to their character
4. Track learning progress through stages

**Important Guidelines**:
- Each agent has a distinct personality - maintain it consistently
- Responses should be in Vietnamese (as seen in the agent descriptions)
- Keep responses concise and student-appropriate (high school level)
- Encourage collaborative problem-solving
- Balance creativity (Harry), accuracy (Hermione), and clarity (Ron)

**Available Tools**:
Use the provided tools to:
- Get agent persona details
- Evaluate who should speak next
- Track stage progress
- Generate character-appropriate responses
"""

    def _update_stage_description(self):
        """Update current stage description from script."""
        if self.state.script and self.state.current_stage_id in self.state.script:
            stage_info = self.state.script[self.state.current_stage_id]
            self.state.current_stage_description = f"{stage_info.get('goal', '')}\nTasks: {', '.join([t.get('description', '') for t in stage_info.get('tasks', [])])}"
        else:
            self.state.current_stage_description = "General discussion and problem-solving"

    def _initialize_log_file(self):
        """Initialize the log file with script information."""
        with open(self.filename, "w") as f:
            script_str = "\n\n".join([
                f"{k}: {v}" for key, value in self.state.script.items()
                for k, v in value.items()
            ])
            f.write(f'Script:\n{script_str}\n\n')
            f.write(f"Conversation:\n{self.state.conversation}\n")

    def _save_to_log(self, content: str):
        """Append content to log file."""
        with open(self.filename, "a") as f:
            f.write(content)

    def _send_agent_status(self, agent_name: str, status: str):
        """Send agent status update via Socket.IO."""
        if self.session_id and self.socketio:
            try:
                from flow.utils.socket_utils import send_agent_status_via_socketio
                send_agent_status_via_socketio(agent_name, status, self.session_id)
            except Exception as e:
                print(f"Error sending agent status: {e}")

    def _send_system_status(self, message: str):
        """Send system status message via Socket.IO."""
        if self.session_id and self.socketio:
            try:
                from flow.utils.socket_utils import send_system_status
                send_system_status(message, self.session_id)
            except Exception as e:
                print(f"Error sending system status: {e}")

    def _send_message(self, message_data: Dict):
        """Send message via Socket.IO."""
        if self.session_id and self.socketio:
            try:
                from flow.utils.socket_utils import send_message_via_socketio
                send_message_via_socketio(message_data, self.session_id)
            except Exception as e:
                print(f"Error sending message: {e}")

    async def process_message(self, sender_name: str, text: str) -> Optional[Dict[str, str]]:
        """
        Process a new message from user or system.

        Args:
            sender_name: Name of the sender
            text: Message text

        Returns:
            Dict with 'agent' and 'response' keys if successful, None otherwise
        """
        if self._is_cancelled:
            print(f"Dialogue manager [{self.session_id}] is cancelled. Ignoring message.")
            self._send_system_status("Phiên trò chuyện đã kết thúc. Vui lòng tạo phiên mới.")
            return None

        # Acquire lock to prevent concurrent processing
        async with self._processing_lock:
            if self.state.is_processing:
                print("Already processing a message. Please wait.")
                self._send_system_status("Hệ thống đang xử lý tin nhắn trước đó. Vui lòng đợi.")
                return None

            self.state.is_processing = True

            try:
                # Add message to conversation
                self.state.turn_number += 1
                timestamp = time.time()
                message_entry = (
                    f"TIME={timestamp} | "
                    f"CON#{self.state.turn_number} | "
                    f"SENDER={sender_name} | "
                    f"TEXT={text}\n"
                )
                self.state.conversation += message_entry

                # Log user message
                self._save_to_log(f"Turn: {self.state.turn_number}.\n{message_entry}\n")

                # Send status update
                self._send_system_status("Đang phân tích tin nhắn...")

                # Wait a bit before processing (simulate thinking time)
                await asyncio.sleep(2)

                # Set all agents to "thinking" status
                for agent in self.state.participants:
                    self._send_agent_status(agent, "thinking")

                # Process with Claude Agent SDK
                response_data = await self._generate_agent_turn(text, sender_name)

                # Set all agents back to idle
                for agent in self.state.participants:
                    self._send_agent_status(agent, "idle")

                return response_data

            except Exception as e:
                print(f"Error processing message: {e}")
                self._send_system_status(f"Đã xảy ra lỗi: {e}")
                return None
            finally:
                self.state.is_processing = False

    async def _generate_agent_turn(self, user_message: str, sender_name: str) -> Optional[Dict[str, str]]:
        """
        Generate an agent response using Claude Agent SDK.

        Returns:
            Dict with 'agent' and 'response' keys
        """
        try:
            # Build the prompt for Claude
            prompt = f"""A new message has been received in the classroom discussion:

**Sender**: {sender_name}
**Message**: {user_message}

**Recent Conversation**:
{self._get_recent_conversation(5)}

**Task**:
1. Analyze the message and conversation context
2. Use the evaluate_turn_taking tool to determine which agent (Harry, Hermione, or Ron) should respond next
3. Use the generate_agent_response tool to create the response from that agent
4. Respond in this exact JSON format:
{{
    "selected_agent": "agent_name",
    "response": "the agent's response in Vietnamese",
    "reasoning": "brief explanation of why this agent was chosen"
}}

Remember: Stay in character for each agent!
"""

            # Create Claude SDK client
            async with ClaudeSDKClient(options=self.agent_options) as client:
                # Send the query
                await client.query(prompt)

                # Collect the response
                full_response = ""
                async for message in client.receive_response():
                    if hasattr(message, 'content'):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                full_response += block.text

                # Parse the response
                response_data = self._parse_agent_response(full_response)

                if response_data:
                    # Log the agent response
                    agent_name = response_data['agent']
                    response_text = response_data['response']

                    self.state.turn_number += 1
                    timestamp = time.time()
                    message_entry = (
                        f"TIME={timestamp} | "
                        f"CON#{self.state.turn_number} | "
                        f"SENDER={agent_name} | "
                        f"TEXT={response_text}\n"
                    )
                    self.state.conversation += message_entry
                    self._save_to_log(f"Turn: {self.state.turn_number}.\n{message_entry}\n")

                    # Send the message via Socket.IO
                    self._send_message({
                        'source': 'agent',
                        'content': {
                            'text': response_text,
                            'sender_name': agent_name
                        }
                    })

                    return response_data

                return None

        except Exception as e:
            print(f"Error generating agent turn: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _get_recent_conversation(self, num_turns: int = 5) -> str:
        """Get the most recent conversation turns."""
        lines = self.state.conversation.strip().split('\n')
        recent_lines = lines[-num_turns:] if len(lines) > num_turns else lines
        return '\n'.join(recent_lines)

    def _parse_agent_response(self, response_text: str) -> Optional[Dict[str, str]]:
        """
        Parse the agent response from Claude.

        Returns:
            Dict with 'agent' and 'response' keys, or None if parsing fails
        """
        try:
            # Try to find JSON in the response
            import re

            # Look for JSON object in the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)

                if 'selected_agent' in data and 'response' in data:
                    return {
                        'agent': data['selected_agent'],
                        'response': data['response'],
                        'reasoning': data.get('reasoning', '')
                    }

            # If JSON parsing fails, try to extract agent and response heuristically
            # This is a fallback
            print(f"Could not parse JSON from response: {response_text[:200]}")
            return None

        except Exception as e:
            print(f"Error parsing agent response: {e}")
            return None

    def cancel(self):
        """Cancel the dialogue manager."""
        print(f"Dialogue manager [{self.session_id}] cancelled.")
        self._is_cancelled = True

    def export_session_data(self) -> Dict[str, Any]:
        """
        Export session data for database storage.

        Returns:
            Dict containing session data
        """
        return {
            "session_id": self.session_id,
            "problem": self.state.problem,
            "script": self.state.script,
            "roles": {},  # Roles are now embedded in the agent personas
            "current_stage_id": self.state.current_stage_id,
            "conversation": self.state.conversation,
            "log_file": self.filename,
            "stage_state": self.state.stage_state or {
                "completed_task_ids": [],
                "signal": "1"
            },
            "inner_thought": list(self.state.inner_thoughts),
            "turn_number": self.state.turn_number,
            "user_name": self.user_name
        }
