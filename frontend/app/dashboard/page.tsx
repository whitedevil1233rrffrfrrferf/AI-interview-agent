"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const [role, setRole] = useState("backend");
  const [difficulty, setDifficulty] = useState("easy");
  const router = useRouter();

  const startInterview = async () => {
    const token = getToken();

    const res = await api.startInterview( role, difficulty);

    localStorage.setItem("interview_id", res.interview_id);
    localStorage.setItem("question", res.question);

    router.push("/interview");
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Start Interview</h2>

      <select onChange={(e) => setRole(e.target.value)}>
        <option value="backend">Backend</option>
        <option value="frontend">Frontend</option>
      </select>

      <select onChange={(e) => setDifficulty(e.target.value)}>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>

      <button onClick={startInterview}>Start</button>
    </div>
  );
}