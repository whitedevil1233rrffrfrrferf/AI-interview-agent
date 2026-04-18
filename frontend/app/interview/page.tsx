"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function InterviewPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState<number | null>(null);
  const [interviewId, setInterviewId] = useState<number | null>(null);

  useEffect(() => {
    const q = localStorage.getItem("question");
    const id = localStorage.getItem("interview_id");

    if (q) setQuestion(q);
    if (id) setInterviewId(Number(id));
  }, []);

  const submitAnswer = async () => {
    if (!interviewId) return;

    const res = await api.submitAnswer(
      interviewId,
      question,
      answer
    );

    setScore(res.score);
    setFeedback(res.feedback);
    setQuestion(res.next_question);
    setAnswer("");
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Interview</h2>

      <h3>Question:</h3>
      <p>{question}</p>

      <textarea
        rows={5}
        placeholder="Your answer..."
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <br />

      <button onClick={submitAnswer}>Submit</button>

      {score !== null && (
        <div>
          <h3>Score: {score}</h3>
          <p>{feedback}</p>
        </div>
      )}
    </div>
  );
}