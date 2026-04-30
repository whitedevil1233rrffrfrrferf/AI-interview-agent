from repository.interview_repo import create_interview, get_user_interviews
from schemas.interview_schema import InterviewHistoryResponse
from sqlalchemy.orm import Session
from services.ai_service import get_first_question



def start_interview_service(db, user_id: str, role: str, difficulty: str,resume_path: str = None):
    interview = create_interview(db, user_id, role, difficulty)

    question = get_first_question(db, user_id, role, difficulty,resume_path)

    return {
        "interview_id": interview.id,
        "question": question
    }

def get_interview_history(db, user_email: str):
    interviews = get_user_interviews(db, user_email)

    response = []

    for interview in interviews:
        overall_score = None

        if hasattr(interview, "score"):
            overall_score = interview.score

        response.append(
            InterviewHistoryResponse(
                id=interview.id,
                role=interview.role,
                difficulty=interview.difficulty,
                created_at=interview.created_at,
                overall_score=overall_score
            )
        )

    return response    