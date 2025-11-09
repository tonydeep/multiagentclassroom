"""
Multi-Agent Classroom - Claude Agent SDK Implementation

This package provides a multi-agent learning environment using Claude Agent SDK.
"""

__version__ = "1.0.0"

from flow_sdk.dialogue_manager import ClaudeDialogueManager, DialogueState
from flow_sdk.agent_tools import (
    get_agent_persona,
    get_all_personas,
    evaluate_turn_taking,
    track_stage_progress,
    generate_agent_response,
    AGENT_PERSONAS
)

__all__ = [
    'ClaudeDialogueManager',
    'DialogueState',
    'get_agent_persona',
    'get_all_personas',
    'evaluate_turn_taking',
    'track_stage_progress',
    'generate_agent_response',
    'AGENT_PERSONAS'
]
