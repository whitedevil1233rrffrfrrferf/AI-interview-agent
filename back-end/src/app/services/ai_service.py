import os
import json
from groq import Groq
from dotenv import load_dotenv

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