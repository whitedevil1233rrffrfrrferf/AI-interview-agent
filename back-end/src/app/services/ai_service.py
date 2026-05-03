import os
import json
from groq import Groq
from dotenv import load_dotenv
from utils.question_fallback import generate_first_question
from repository.resume import get_latest_resume
from rag.rag import load_pdf, split_docs, create_vectorstore, retrieve_context
from repository.interview_qa_repo import get_questions_by_interview
from services.cache_service import get_cache, set_cache

import hashlib


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


def get_first_question(db, user_id: str, role: str, difficulty: str,resume_path: str = None) -> str:
    try:
        if resume_path:
            docs = load_pdf(resume_path)
            chunks = split_docs(docs)
            # STEP 3 + 4: store embeddings
            create_vectorstore(chunks)

            # STEP 5: retrieve relevant context
            context = get_resume_context_cached(role, user_id)

            print("\n===== RETRIEVED CONTEXT =====")
            print(context[:1000])

        # fallback for now
        return generate_question_with_ai(role, difficulty, resume_text=context if resume_path else None)

    except Exception:
        return generate_first_question(role, difficulty)       
    
def get_next_question(db, interview_id: int, role: str):
    try:
        # 1. Get interview history
        history = get_questions_by_interview(db, interview_id)

        # 2. Extract scores
        scores = [q.score for q in history if q.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 5

        # 3. Adaptive difficulty
        if avg_score >= 8:
            difficulty = "hard"
        elif avg_score >= 5:
            difficulty = "medium"
        else:
            difficulty = "easy"

        # 4. Build conversation context (VERY IMPORTANT)
        conversation = "\n".join([
            f"Q: {q.question}\nA: {q.answer}"
            for q in history[-3:]  # last 3 only (avoid token explosion)
        ])

        # 5. Try resume RAG context (if available in DB or cache)
        resume_context = retrieve_context(role)

        # 6. Generate next question using AI
        return generate_question_with_ai(
            role=role,
            difficulty=difficulty,
            resume_text=f"{resume_context}\n\n{conversation}"
        )

    except Exception as e:
        print("[NEXT QUESTION ERROR]", str(e))
        return generate_first_question(role, "easy")    
    
def get_resume_context_cached(role: str, user_id: str):
    cache_key = f"resume:{user_id}:{role}"

    cached = get_cache(cache_key)
    if cached:
        print("⚡ RESUME CACHE HIT")
        return cached

    print("❌ RESUME CACHE MISS")

    # Better semantic query
    query = f"{role} concepts from candidate resume"

    context = retrieve_context(query)

    set_cache(cache_key, context, ttl=3600)

    return context
    