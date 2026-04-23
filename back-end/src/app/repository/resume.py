from sqlalchemy.orm import Session
from models.resume import Resume

def create_resume(db: Session, user_email: str, file_name: str, content: str):
    resume = Resume(
        user_id=user_email,
        file_name=file_name,
        content=content
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_latest_resume(db: Session, user_email: str):
    return (
        db.query(Resume)
        .filter(Resume.user_id == user_email)
        .order_by(Resume.created_at.desc())
        .first()
    )