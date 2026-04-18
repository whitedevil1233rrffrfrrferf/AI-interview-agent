from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.interview_schema import StartInterviewRequest, StartInterviewResponse
from services.interview_service import start_interview_service
from infrastructure.db import get_db
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    request: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = start_interview_service(
        db=db,
        user_id=current_user,
        role=request.role,
        difficulty=request.difficulty
    )

    return result