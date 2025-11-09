"""
API routes for the Multi-Agent Classroom.
"""
from .problems import router as problems_router
from .sessions import router as sessions_router

__all__ = ["problems_router", "sessions_router"]
