"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useRequireAuth } from "@/lib/useRequireAuth";

export default function InterviewPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState<number | null>(null);
  const [interviewId, setInterviewId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [questionsAnswered, setQuestionsAnswered] = useState(0);
  const router = useRouter();

  const isAuthed = useRequireAuth();

  useEffect(() => {
    const q = localStorage.getItem("question");
    const id = localStorage.getItem("interview_id");

    if (q) setQuestion(q);
    if (id) setInterviewId(Number(id));
  }, []);

  if (!isAuthed) return null;

  const submitAnswer = async () => {
    if (!interviewId || !answer.trim()) return;
    
    setLoading(true);
    try {
      const res = await api.submitAnswer(
        interviewId,
        question,
        answer
      );

      setScore(res.score);
      setFeedback(res.feedback);
      setQuestion(res.next_question);
      setAnswer("");
      setQuestionsAnswered(questionsAnswered + 1);
    } catch (err) {
      console.error("Failed to submit answer", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEndInterview = () => {
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Interview in Progress</h1>
          <div className="text-sm font-semibold text-gray-600 bg-white px-4 py-2 rounded-lg">
            Questions Answered: {questionsAnswered}
          </div>
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Question Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Question</h2>
            <div className="bg-indigo-50 border-l-4 border-indigo-600 p-6 rounded">
              <p className="text-gray-800 text-lg leading-relaxed">{question}</p>
            </div>
          </div>

          {/* Answer Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <label htmlFor="answer" className="block text-lg font-bold text-gray-900 mb-4">
              Your Answer
            </label>
            <textarea
              id="answer"
              rows={7}
              placeholder="Type your answer here. Be detailed and clear in your explanation..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition font-mono text-sm"
            />
            <p className="text-gray-500 text-xs mt-2">{answer.length} characters</p>
          </div>

          {/* Feedback Section - Show after submission */}
          {feedback && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-bold text-gray-900">Score</h3>
                  <div className="text-4xl font-bold text-indigo-600">{score}/10</div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-indigo-600 h-2 rounded-full"
                    style={{ width: `${(score || 0) * 10}%` }}
                  ></div>
                </div>
              </div>

              <h3 className="text-lg font-bold text-gray-900 mb-3">AI Feedback</h3>
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <p className="text-gray-700 leading-relaxed">{feedback}</p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={submitAnswer}
              disabled={loading || !answer.trim()}
              className={`flex-1 font-bold py-3 px-6 rounded-lg transition duration-200 text-white text-lg ${
                loading || !answer.trim()
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-indigo-600 hover:bg-indigo-700"
              }`}
            >
              {loading ? "Evaluating..." : feedback ? "Next Question" : "Submit Answer"}
            </button>
            <button
              onClick={handleEndInterview}
              className="font-bold py-3 px-6 rounded-lg transition duration-200 text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 text-lg"
            >
              End Interview
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}