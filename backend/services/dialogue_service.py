"""
Dialogue service integrating Claude Agent SDK with the API.
"""
import os
import asyncio
from typing import Dict, Optional
from datetime import datetime
import sys

# Add parent directory to path to import flow_sdk
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flow_sdk.dialogue_manager import ClaudeDialogueManager
from backend.api.websocket.manager import manager

# Store active dialogue managers
active_managers: Dict[str, ClaudeDialogueManager] = {}

# Simple learning script
SIMPLE_SCRIPT = {
    "1": {
        "id": "1",
        "name": "Hiểu vấn đề",
        "goal": "Hiểu rõ đề bài và xác định các thông tin cho trước",
        "tasks": [
            {"id": "1.1", "description": "Xác định dạng bài toán"},
            {"id": "1.2", "description": "Liệt kê các thông tin đã biết"}
        ]
    },
    "2": {
        "id": "2",
        "name": "Lập kế hoạch",
        "goal": "Đề xuất phương pháp giải",
        "tasks": [
            {"id": "2.1", "description": "Chọn công thức/phương pháp phù hợp"},
            {"id": "2.2", "description": "Vạch ra các bước giải"}
        ]
    },
    "3": {
        "id": "3",
        "name": "Thực hiện",
        "goal": "Giải bài toán theo kế hoạch",
        "tasks": [
            {"id": "3.1", "description": "Thực hiện các bước tính toán"},
            {"id": "3.2", "description": "Kiểm tra kết quả"}
        ]
    }
}


class WebSocketIOAdapter:
    """Adapter to make WebSocket manager compatible with dialogue manager."""

    def __init__(self, session_id: str):
        self.session_id = session_id

    def sleep(self, seconds: int):
        """Non-blocking sleep using asyncio."""
        # For FastAPI, we'll use asyncio.sleep instead
        import time
        time.sleep(seconds)


async def create_dialogue_manager(
    session_id: str,
    user_name: str,
    problem: str
) -> ClaudeDialogueManager:
    """
    Create a new dialogue manager for a session.

    Args:
        session_id: Unique session identifier
        user_name: User's name
        problem: The math problem to solve

    Returns:
        ClaudeDialogueManager instance
    """
    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Create adapter for WebSocket
    socketio_adapter = WebSocketIOAdapter(session_id)

    # Initialize dialogue manager
    dialogue_manager = ClaudeDialogueManager(
        socketio=socketio_adapter,
        session_id=session_id,
        user_name=user_name,
        problem=problem,
        script=SIMPLE_SCRIPT,
        conversation="",
        participants=["Harry", "Hermione", "Ron"],
        current_stage_id="1",
        turn_number=0,
        filename=f"logs/{session_id}.log"
    )

    # Store in active managers
    active_managers[session_id] = dialogue_manager

    return dialogue_manager


async def process_user_message(
    session_id: str,
    sender_name: str,
    message_text: str
) -> Optional[Dict[str, str]]:
    """
    Process a user message through the dialogue manager.

    Args:
        session_id: Session identifier
        sender_name: Name of the sender
        message_text: Message content

    Returns:
        Response from agent or None
    """
    if session_id not in active_managers:
        raise ValueError(f"No active dialogue manager for session {session_id}")

    dialogue_manager = active_managers[session_id]

    try:
        # Send status update
        await manager.send_system_status(session_id, "Đang phân tích tin nhắn...")

        # Set agents to thinking
        for agent in ["Harry", "Hermione", "Ron"]:
            await manager.send_agent_status(session_id, agent, "thinking")

        # Process the message
        result = await dialogue_manager.process_message(sender_name, message_text)

        # Set agents back to idle
        for agent in ["Harry", "Hermione", "Ron"]:
            await manager.send_agent_status(session_id, agent, "idle")

        return result

    except Exception as e:
        await manager.send_error(session_id, str(e))
        return None


def cleanup_session(session_id: str):
    """
    Clean up a session and its dialogue manager.

    Args:
        session_id: Session to clean up
    """
    if session_id in active_managers:
        dialogue_manager = active_managers[session_id]
        dialogue_manager.cancel()
        del active_managers[session_id]


def get_session_data(session_id: str) -> Optional[Dict]:
    """
    Get session data for export.

    Args:
        session_id: Session identifier

    Returns:
        Session data dictionary or None
    """
    if session_id not in active_managers:
        return None

    return active_managers[session_id].export_session_data()
