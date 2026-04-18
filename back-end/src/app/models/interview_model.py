from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from infrastructure.db import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.email"), nullable=False)

    role = Column(String, nullable=False)         # e.g. "backend", "frontend"
    difficulty = Column(String, nullable=False)   # "easy", "medium", "hard"
    status = Column(String, default="started")    # started, in_progress, completed

    created_at = Column(DateTime, default=datetime.utcnow)