from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from infrastructure.db import Base

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question = Column(Text)
    answer = Column(Text)
    score = Column(Integer)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)