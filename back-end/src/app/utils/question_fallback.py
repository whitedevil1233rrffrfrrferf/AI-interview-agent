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