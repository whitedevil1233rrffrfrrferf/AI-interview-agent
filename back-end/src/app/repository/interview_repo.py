from sqlalchemy.orm import Session
from models.interview_model import Interview

def create_interview(db: Session, user_id: str, role: str, difficulty: str):
    interview = Interview(
        user_id=user_id,
        role=role,
        difficulty=difficulty,
        status="started"
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

def get_interview_by_id(db: Session, interview_id: int):
    return db.query(Interview).filter(Interview.id == interview_id).first()