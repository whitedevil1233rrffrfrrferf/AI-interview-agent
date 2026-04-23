from repository.interview_repo import create_interview, get_user_interviews
from schemas.interview_schema import InterviewHistoryResponse
from sqlalchemy.orm import Session

def generate_first_question(role: str, difficulty: str) -> str:
    # Simple hardcoded logic (replace later with AI)

    question_bank = {
        "backend": {
            "easy": "What is REST API?",
            "medium": "Explain difference between sync and async in FastAPI.",
            "hard": "Design a scalable rate limiter."
        },
        "frontend": {
            "easy": "What is React?",
            "medium": "Explain useEffect hook.",
            "hard": "How would you optimize performance in a large React app?"
        }
    }

    return question_bank.get(role, {}).get(
        difficulty,
        "Tell me about yourself."
    )


def start_interview_service(db, user_id: str, role: str, difficulty: str):
    interview = create_interview(db, user_id, role, difficulty)

    question = generate_first_question(role, difficulty)

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