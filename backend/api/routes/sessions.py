"""
API routes for session management.
"""
from fastapi import APIRouter, HTTPException
from backend.models import SessionCreate, SessionResponse, Problem
from backend.services.dialogue_service import create_dialogue_manager, get_session_data
from backend.api.routes.problems import SAMPLE_PROBLEMS
import uuid

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse)
async def create_session(session_data: SessionCreate):
    """
    Create a new learning session.

    Args:
        session_data: Session creation data

    Returns:
        Session information including ID and problem
    """
    # Find the problem
    problem = next(
        (p for p in SAMPLE_PROBLEMS if p.id == session_data.problem_id),
        SAMPLE_PROBLEMS[0]
    )

    # Generate session ID
    session_id = str(uuid.uuid4())

    try:
        # Create dialogue manager
        await create_dialogue_manager(
            session_id=session_id,
            user_name=session_data.user_name,
            problem=problem.problem
        )

        return SessionResponse(
            session_id=session_id,
            problem=problem,
            participants=["Harry", "Hermione", "Ron"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/{session_id}")
async def get_session(session_id: str):
    """
    Get session data.

    Args:
        session_id: Session identifier

    Returns:
        Session data
    """
    data = get_session_data(session_id)

    if not data:
        raise HTTPException(status_code=404, detail="Session not found")

    return data
