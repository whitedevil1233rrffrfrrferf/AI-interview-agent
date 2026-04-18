from pydantic import BaseModel

class StartInterviewRequest(BaseModel):
    role: str
    difficulty: str


class StartInterviewResponse(BaseModel):
    interview_id: int
    question: str