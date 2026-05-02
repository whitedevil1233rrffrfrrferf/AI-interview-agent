from pydantic import BaseModel
from typing import Optional


class SubmitAnswerRequest(BaseModel):
    interview_id: int
    question: str
    answer: str


class SubmitAnswerResponse(BaseModel):
    completed: bool

    # ongoing case
    score: Optional[int] = None
    feedback: Optional[str] = None
    next_question: Optional[str] = None

    # completed case
    overall_score: Optional[float] = None   