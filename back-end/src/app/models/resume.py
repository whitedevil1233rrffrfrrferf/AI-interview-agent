from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from datetime import datetime
from infrastructure.db import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.email"))
    file_name = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)