"""
Custom MCP tools for multi-agent classroom coordination using Claude Agent SDK.
"""
import json
from typing import Dict, List, Any
from claude_agent_sdk import tool


# Agent Persona Definitions (from agents.yaml)
AGENT_PERSONAS = {
    "Harry": {
        "role": "Creative Problem Solver - Links math concepts to magical/fictional analogies",
        "personality": "Energetic, curious, imaginative, sometimes rambling but brings fresh perspectives",
        "tasks": [
            "Create connections between math and magic",
            "Propose new ideas and creative approaches",
            "Participate actively with questions and support"
        ]
    },
    "Hermione": {
        "role": "Rigorous Scholar - Ensures mathematical accuracy and theoretical depth",
        "personality": "Smart, hardworking, precise, sometimes strict but caring",
        "tasks": [
            "Provide knowledge and explain concepts/theorems/formulas",
            "Check accuracy of each step",
            "Support theoretical understanding"
        ]
    },
    "Ron": {
        "role": "Empathetic Questioner - Asks clarifying questions, keeps tone relaxed",
        "personality": "Cheerful, friendly, approachable, admits when confused, willing to learn",
        "tasks": [
            "Ask simple questions to clarify",
            "Provide direct feedback on difficulties",
            "Keep the atmosphere light and comfortable"
        ]
    }
}


@tool(
    name="get_agent_persona",
    description="Get the persona information for a specific agent (Harry, Hermione, or Ron)",
    input_schema={
        "type": "object",
        "properties": {
            "agent_name": {
                "type": "string",
                "description": "Name of the agent (Harry, Hermione, or Ron)"
            }
        },
        "required": ["agent_name"]
    }
)
async def get_agent_persona(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get persona information for an agent."""
    agent_name = args.get("agent_name", "")

    if agent_name in AGENT_PERSONAS:
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "agent_name": agent_name,
                    "persona": AGENT_PERSONAS[agent_name]
                }, ensure_ascii=False, indent=2)
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": f"Agent '{agent_name}' not found. Available agents: {', '.join(AGENT_PERSONAS.keys())}"
            }]
        }


@tool(
    name="get_all_personas",
    description="Get information about all available agent personas in the classroom",
    input_schema={
        "type": "object",
        "properties": {}
    }
)
async def get_all_personas(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get all agent personas."""
    return {
        "content": [{
            "type": "text",
            "text": json.dumps(AGENT_PERSONAS, ensure_ascii=False, indent=2)
        }]
    }


@tool(
    name="evaluate_turn_taking",
    description="Evaluate which agent should speak next based on conversation context and agent personas",
    input_schema={
        "type": "object",
        "properties": {
            "conversation_history": {
                "type": "string",
                "description": "Recent conversation history"
            },
            "current_stage": {
                "type": "string",
                "description": "Current learning stage description"
            },
            "problem": {
                "type": "string",
                "description": "The math problem being solved"
            }
        },
        "required": ["conversation_history", "current_stage", "problem"]
    }
)
async def evaluate_turn_taking(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate which agent should speak next.
    This is a placeholder that returns context for the main agent to decide.
    """
    conversation_history = args.get("conversation_history", "")
    current_stage = args.get("current_stage", "")
    problem = args.get("problem", "")

    context = {
        "instruction": "Based on the conversation history, current stage, and agent personas, determine which agent (Harry, Hermione, or Ron) should speak next and why.",
        "conversation_history": conversation_history,
        "current_stage": current_stage,
        "problem": problem,
        "agent_personas": AGENT_PERSONAS
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(context, ensure_ascii=False, indent=2)
        }]
    }


@tool(
    name="track_stage_progress",
    description="Track progress through learning stages and determine if stage should advance",
    input_schema={
        "type": "object",
        "properties": {
            "conversation_history": {
                "type": "string",
                "description": "Recent conversation history"
            },
            "current_stage_id": {
                "type": "string",
                "description": "Current stage ID"
            },
            "stage_description": {
                "type": "string",
                "description": "Description of current stage goals and tasks"
            },
            "completed_tasks": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of completed task IDs"
            }
        },
        "required": ["conversation_history", "current_stage_id", "stage_description"]
    }
)
async def track_stage_progress(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Track stage progress and determine if stage should advance.
    This is a placeholder that returns context for the main agent to analyze.
    """
    conversation_history = args.get("conversation_history", "")
    current_stage_id = args.get("current_stage_id", "")
    stage_description = args.get("stage_description", "")
    completed_tasks = args.get("completed_tasks", [])

    context = {
        "instruction": "Analyze the conversation to determine: 1) Which tasks from the current stage have been completed, 2) Whether to advance to the next stage, 3) What signal to send (Start, Continue, NeedEnd, MoveNext)",
        "conversation_history": conversation_history,
        "current_stage_id": current_stage_id,
        "stage_description": stage_description,
        "completed_tasks": completed_tasks
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(context, ensure_ascii=False, indent=2)
        }]
    }


@tool(
    name="generate_agent_response",
    description="Generate a response from a specific agent persona based on their role and the conversation context",
    input_schema={
        "type": "object",
        "properties": {
            "agent_name": {
                "type": "string",
                "description": "Name of the agent (Harry, Hermione, or Ron)"
            },
            "conversation_history": {
                "type": "string",
                "description": "Recent conversation history"
            },
            "current_stage": {
                "type": "string",
                "description": "Current learning stage description"
            },
            "problem": {
                "type": "string",
                "description": "The math problem being solved"
            },
            "inner_thought": {
                "type": "string",
                "description": "Agent's internal thought/reflection on the current situation"
            }
        },
        "required": ["agent_name", "conversation_history", "current_stage", "problem"]
    }
)
async def generate_agent_response(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a response from a specific agent.
    This is a placeholder that returns context for the main agent to generate the response.
    """
    agent_name = args.get("agent_name", "")
    conversation_history = args.get("conversation_history", "")
    current_stage = args.get("current_stage", "")
    problem = args.get("problem", "")
    inner_thought = args.get("inner_thought", "")

    if agent_name not in AGENT_PERSONAS:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Agent '{agent_name}' not found"
            }],
            "isError": True
        }

    persona = AGENT_PERSONAS[agent_name]

    context = {
        "instruction": f"Generate a response as {agent_name} based on their persona and the conversation context. Stay in character!",
        "agent_name": agent_name,
        "persona": persona,
        "conversation_history": conversation_history,
        "current_stage": current_stage,
        "problem": problem,
        "inner_thought": inner_thought
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(context, ensure_ascii=False, indent=2)
        }]
    }
