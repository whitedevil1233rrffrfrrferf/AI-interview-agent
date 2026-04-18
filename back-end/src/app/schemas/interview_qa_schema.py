from pydantic import BaseModel

class SubmitAnswerRequest(BaseModel):
    interview_id: int
    question: str
    answer: str


class SubmitAnswerResponse(BaseModel):
    score: int
    feedback: str
    next_question: str