"""
API routes for problem management.
"""
from fastapi import APIRouter
from typing import List
from backend.models import Problem

router = APIRouter(prefix="/api/problems", tags=["problems"])

# Sample problems
SAMPLE_PROBLEMS = [
    Problem(
        id="1",
        title="Phương trình bậc hai",
        problem="Giải phương trình: x² + 5x + 6 = 0"
    ),
    Problem(
        id="2",
        title="Hệ phương trình tuyến tính",
        problem="Giải hệ phương trình:\n2x + y = 5\nx - y = 1"
    ),
    Problem(
        id="3",
        title="Bất đẳng thức",
        problem="Chứng minh: (a + b)² ≥ 4ab với mọi a, b ∈ R"
    )
]


@router.get("", response_model=List[Problem])
async def get_problems():
    """Get list of available problems."""
    return SAMPLE_PROBLEMS


@router.get("/{problem_id}", response_model=Problem)
async def get_problem(problem_id: str):
    """Get a specific problem by ID."""
    for problem in SAMPLE_PROBLEMS:
        if problem.id == problem_id:
            return problem

    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Problem not found")
