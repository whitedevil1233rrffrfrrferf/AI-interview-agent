from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.interview_qa_schema import SubmitAnswerRequest, SubmitAnswerResponse
from services.interview_qa_service import submit_answer_service
from infrastructure.db import get_db
from utils.auth_utils import get_current_user
from repository.interview_repo import get_interview_by_id

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/answer", response_model=SubmitAnswerResponse)
def submit_answer(
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    interview = get_interview_by_id(db, request.interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = submit_answer_service(
        db,
        interview,
        request.question,
        request.answer
    )

    return result