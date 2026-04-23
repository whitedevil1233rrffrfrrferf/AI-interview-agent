from pydantic import BaseModel
from typing import List, Optional

class QuestionAnalysis(BaseModel):
    question: str
    answer: str
    score: float
    feedback: str
    

class InterviewReport(BaseModel):
    interview_id: int
    overall_score: float
    total_questions: int
    average_score: float
    verdict: str  # "hire" | "no_hire" | "maybe"
    questions: List[QuestionAnalysis]