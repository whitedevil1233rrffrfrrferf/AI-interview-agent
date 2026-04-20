"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useRequireAuth } from "@/lib/useRequireAuth";

export default function Dashboard() {
  const [role, setRole] = useState("backend");
  const [difficulty, setDifficulty] = useState("easy");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const isAuthed = useRequireAuth();
 
  if (!isAuthed) return null;

  const startInterview = async () => {
    setLoading(true);
    try {
      const res = await api.startInterview(role, difficulty);
      localStorage.setItem("interview_id", res.interview_id);
      localStorage.setItem("question", res.question);
      router.push("/interview");
    } catch (err) {
      console.error("Failed to start interview", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-10">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">AI Interview Simulator</h1>
          <p className="text-gray-600">Practice your interview skills with AI-powered questions</p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">Start an Interview</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            {/* Role Selection */}
            <div>
              <label htmlFor="role" className="block text-sm font-semibold text-gray-700 mb-3">
                Interview Role
              </label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition bg-white"
              >
                <option value="backend">Backend Developer</option>
                <option value="frontend">Frontend Developer</option>
              </select>
              <p className="text-gray-500 text-xs mt-2">Choose the role you want to practice for</p>
            </div>

            {/* Difficulty Selection */}
            <div>
              <label htmlFor="difficulty" className="block text-sm font-semibold text-gray-700 mb-3">
                Difficulty Level
              </label>
              <select
                id="difficulty"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition bg-white"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
              <p className="text-gray-500 text-xs mt-2">Start easy and progress to harder questions</p>
            </div>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 py-6 border-t border-b border-gray-200">
            <div className="text-center">
              <div className="text-2xl font-bold text-indigo-600 mb-1">AI-Powered</div>
              <p className="text-gray-600 text-sm">Real-time feedback on your answers</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-indigo-600 mb-1">Adaptive</div>
              <p className="text-gray-600 text-sm">Questions adjust to your level</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-indigo-600 mb-1">Scoring</div>
              <p className="text-gray-600 text-sm">Get detailed performance metrics</p>
            </div>
          </div>

          {/* Start Button */}
          <button
            onClick={startInterview}
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition duration-200 text-lg"
          >
            {loading ? "Starting Interview..." : "Start Interview"}
          </button>
        </div>
      </div>
    </div>
  );
}
