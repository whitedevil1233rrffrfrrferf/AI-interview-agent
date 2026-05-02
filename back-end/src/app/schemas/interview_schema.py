from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StartInterviewRequest(BaseModel):
    role: str
    difficulty: str


class StartInterviewResponse(BaseModel):
    interview_id: int
    question: str

class InterviewHistoryResponse(BaseModel):
    id: int
    role: str
    difficulty: str
    created_at: datetime
    overall_score: Optional[int] = None

    class Config:
        from_attributes = True    

     