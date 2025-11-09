"""
WebSocket connection manager for real-time communication.
"""
from typing import Dict, Set
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for multiple sessions."""

    def __init__(self):
        # session_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()

        self.active_connections[session_id].add(websocket)
        logger.info(f"Client connected to session {session_id}")

    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove a WebSocket connection."""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)

            # Clean up empty sessions
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

        logger.info(f"Client disconnected from session {session_id}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast_to_session(self, message: dict, session_id: str):
        """Broadcast a message to all connections in a session."""
        if session_id not in self.active_connections:
            logger.warning(f"No active connections for session {session_id}")
            return

        disconnected = set()

        for connection in self.active_connections[session_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.add(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection, session_id)

    async def send_agent_status(self, session_id: str, agent_name: str, status: str):
        """Send agent status update to session."""
        message = {
            "type": "agent_status",
            "data": {
                "agent_name": agent_name,
                "status": status
            }
        }
        await self.broadcast_to_session(message, session_id)

    async def send_message(self, session_id: str, source: str, content: dict):
        """Send a chat message to session."""
        message = {
            "type": "new_message",
            "data": {
                "source": source,
                "content": content
            }
        }
        await self.broadcast_to_session(message, session_id)

    async def send_system_status(self, session_id: str, text: str, level: str = "info"):
        """Send system status message to session."""
        message = {
            "type": "system_status",
            "data": {
                "message": text,
                "level": level
            }
        }
        await self.broadcast_to_session(message, session_id)

    async def send_error(self, session_id: str, error: str):
        """Send error message to session."""
        message = {
            "type": "error",
            "data": {
                "error": error
            }
        }
        await self.broadcast_to_session(message, session_id)


# Global connection manager instance
manager = ConnectionManager()
