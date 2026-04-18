import random
from repository.interview_qa_repo import create_qa_record, update_qa_evaluation
from services.ai_service import evaluate_answer_with_ai

# 🔥 MOCK AI EVALUATION (replace later)
def evaluate_answer(question: str, answer: str):
    score = random.randint(4, 9)

    feedback = "Decent answer, but can be improved with more depth."

    return {
        "score": score,
        "feedback": feedback
    }


# 🔥 Adaptive Difficulty
def get_next_question(role: str, score: int):
    if score >= 8:
        difficulty = "hard"
    elif score >= 5:
        difficulty = "medium"
    else:
        difficulty = "easy"

    question_bank = {
        "backend": {
            "easy": "What is HTTP?",
            "medium": "Explain async vs sync in FastAPI.",
            "hard": "Design a distributed caching system."
        },
        "frontend": {
            "easy": "What is DOM?",
            "medium": "Explain React lifecycle.",
            "hard": "How does React Fiber work?"
        }
    }

    question = question_bank.get(role, {}).get(
        difficulty,
        "Tell me about yourself."
    )

    return question


def submit_answer_service(db, interview, question: str, answer: str):
    # 1. Save answer
    qa = create_qa_record(db, interview.id, question, answer)

    # 2. Evaluate answer (mock for now)
    evaluation = evaluate_answer_with_ai(question, answer)

    # 3. Update QA with score
    update_qa_evaluation(
        db,
        qa,
        evaluation["score"],
        evaluation["feedback"]
    )

    # 4. Generate next question
    next_question = get_next_question(interview.role, evaluation["score"])

    return {
        "score": evaluation["score"],
        "feedback": evaluation["feedback"],
        "next_question": next_question
    }