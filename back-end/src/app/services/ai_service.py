import os
import json
from groq import Groq
from dotenv import load_dotenv
from utils.question_fallback import generate_first_question
from repository.resume import get_latest_resume

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_answer_with_ai(question: str, answer: str):
    prompt = f"""
    You are a strict technical interviewer.

    Evaluate the candidate's answer.

    Return ONLY valid JSON in this format:
    {{
    "score": number (0-10),
    "feedback": "short feedback",
    "strengths": "what was good",
    "improvements": "what to improve"
    }}

    Question: {question}
    Answer: {answer}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict evaluator."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content

        return json.loads(content)

    except Exception as e:
        print("AI ERROR:", str(e))

        return {
            "score": 5,
            "feedback": "AI evaluation failed.",
            "strengths": "",
            "improvements": "",
        }

def generate_question_with_ai(
    role: str,
    difficulty: str,
    resume_text: str | None = None
) -> str:

    try:
        if resume_text:
            context = f"""
            Candidate Resume:
            {resume_text[:1500]}
            """
        else:
            context = "No resume provided."

        prompt = f"""
        You are a senior technical interviewer.

        {context}

        Generate a {difficulty} level interview question for a {role} developer.

        Rules:
        - Ask only ONE question
        - No explanations
        - No extra text
        - If resume exists → tailor question to candidate experience
        - If no resume → ask a standard question
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        question = response.choices[0].message.content.strip()

        if not question:
            raise ValueError("Empty AI response")

        return question

    except Exception as e:
        print("[AI ERROR]", str(e))
        raise


def get_first_question(db, user_id: str, role: str, difficulty: str) -> str:
    try:
        resume = get_latest_resume(db, user_id)

        # Use resume only if valid
        if resume and resume.content and len(resume.content.strip()) > 50:
            return generate_question_with_ai(
                role,
                difficulty,
                resume_text=resume.content
            )

        # No resume → normal AI
        return generate_question_with_ai(
            role,
            difficulty,
            resume_text=None
        )

    except Exception:
        return generate_first_question(role, difficulty)       