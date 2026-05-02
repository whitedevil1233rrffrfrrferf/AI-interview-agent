from sqlalchemy.orm import Session
from models.interview_qa_model import InterviewQA
from models.interview_questions import InterviewQuestion
from sqlalchemy import func

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

def create_interview_question(
    db: Session,
    interview_id: int,
    question: str,
    answer: str,
    score: int,
    feedback: str
):
    interview_q = InterviewQuestion(
        interview_id=interview_id,
        question=question,
        answer=answer,
        score=score,
        feedback=feedback
    )

    db.add(interview_q)
    db.commit()
    db.refresh(interview_q)

    return interview_q

def get_question_count(db: Session, interview_id: int) -> int:
    return db.query(func.count(InterviewQuestion.id))\
        .filter(InterviewQuestion.interview_id == interview_id)\
        .scalar()

def get_questions_by_interview(db: Session, interview_id: int):
    return db.query(InterviewQuestion)\
        .filter(InterviewQuestion.interview_id == interview_id)\
        .order_by(InterviewQuestion.created_at.asc())\
        .all()