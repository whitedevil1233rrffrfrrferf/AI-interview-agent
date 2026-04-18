from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from infrastructure.db import Base

class InterviewQA(Base):
    __tablename__ = "interview_qas"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)