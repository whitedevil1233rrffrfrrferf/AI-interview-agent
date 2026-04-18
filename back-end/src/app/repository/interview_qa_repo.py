from sqlalchemy.orm import Session
from models.interview_qa_model import InterviewQA

def create_qa_record(db: Session, interview_id: int, question: str, answer: str):
    qa = InterviewQA(
        interview_id=interview_id,
        question=question,
        answer=answer
    )
    db.add(qa)
    db.commit()
    db.refresh(qa)
    return qa


def update_qa_evaluation(db: Session, qa: InterviewQA, score: int, feedback: str):
    qa.score = score
    qa.feedback = feedback
    db.commit()
    db.refresh(qa)
    return qa