import random
from repository.interview_qa_repo import create_qa_record, update_qa_evaluation, create_interview_question, get_question_count, get_questions_by_interview
from services.ai_service import evaluate_answer_with_ai, get_next_question
from repository.interview_repo import get_interview_by_id

MAX_QUESTIONS = 5


# 🔥 MOCK AI EVALUATION (replace later)
def evaluate_answer(question: str, answer: str):
    score = random.randint(4, 9)

    feedback = "Decent answer, but can be improved with more depth."

    return {
        "score": score,
        "feedback": feedback
    }


# # 🔥 Adaptive Difficulty
# def get_next_question(role: str, score: int):
#     if score >= 8:
#         difficulty = "hard"
#     elif score >= 5:
#         difficulty = "medium"
#     else:
#         difficulty = "easy"

#     question_bank = {
#         "backend": {
#             "easy": "What is HTTP?",
#             "medium": "Explain async vs sync in FastAPI.",
#             "hard": "Design a distributed caching system."
#         },
#         "frontend": {
#             "easy": "What is DOM?",
#             "medium": "Explain React lifecycle.",
#             "hard": "How does React Fiber work?"
#         }
#     }

#     question = question_bank.get(role, {}).get(
#         difficulty,
#         "Tell me about yourself."
#     )

#     return question


def submit_answer_service(db, interview_id: int, question: str, answer: str):
    # 1. Save answer
    # qa = create_qa_record(db, interview.id, question, answer)

    # 2. Evaluate answer (mock for now)
    result = evaluate_answer_with_ai(question, answer)

    # 3. Update QA with score
    create_interview_question(
        db=db,
        interview_id=interview_id,
        question=question,
        answer=answer,
        score=result["score"],
        feedback=result["feedback"]
    )

    # 3. Count how many answered
    total_questions = get_question_count(db, interview_id)

    # 4. If interview completed
    if total_questions >= MAX_QUESTIONS:
        overall_score = calculate_overall_score(db, interview_id)

        return {
            "completed": True,
            "overall_score": overall_score
        }
    interview = get_interview_by_id(db, interview_id)
    role = interview.role
    # 4. Generate next question
    next_question = get_next_question(db, interview_id, role)

    return {
        "completed": False,
        "score": result["score"],
        "feedback": result["feedback"],
        "next_question": next_question
    }

def calculate_overall_score(db, interview_id: int):
    questions = get_questions_by_interview(db, interview_id)

    scores = [q.score for q in questions if q.score is not None]

    if not scores:
        return 0

    return round(sum(scores) / len(scores), 2)