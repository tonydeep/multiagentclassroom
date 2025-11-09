"""
Pydantic models for session management.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Problem(BaseModel):
    """A math problem for the classroom."""
    id: str
    title: str
    problem: str


class SessionCreate(BaseModel):
    """Request to create a new session."""
    problem_id: str
    user_name: str = "Student"


class SessionResponse(BaseModel):
    """Response after creating a session."""
    session_id: str
    problem: Problem
    participants: List[str]
    created_at: datetime = Field(default_factory=datetime.now)


class Message(BaseModel):
    """A message in the conversation."""
    id: str
    session_id: str
    sender: str
    text: str
    timestamp: float
    source: str = "user"  # "user" or "agent"


class MessageCreate(BaseModel):
    """Request to send a message."""
    session_id: str
    sender_name: str
    message: str


class AgentStatus(BaseModel):
    """Status update for an agent."""
    agent_name: str
    status: str  # "idle", "thinking", "typing"


class SystemStatus(BaseModel):
    """System status message."""
    message: str
    level: str = "info"  # "info", "warning", "error"


class WebSocketMessage(BaseModel):
    """WebSocket message format."""
    type: str  # "agent_status", "new_message", "system_status", "error"
    data: Dict
