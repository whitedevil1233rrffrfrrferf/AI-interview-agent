"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

export default function ReportPage() {
  const { id } = useParams();
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    api.getReport(Number(id))
      .then((data) => {
        setReport(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="p-6">Loading report...</div>;

  if (!report) return <div className="p-6">Failed to load report</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">

      {/* HEADER */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Interview Report</h1>
        <p className="text-gray-500">Detailed performance analysis</p>
      </div>

      {/* SCORE CARD */}
      <div className="bg-white shadow rounded-xl p-6 mb-6">
        <p className="text-gray-500">Overall Score</p>
        <p className="text-5xl font-bold">{report.overall_score}</p>

        <span
          className={`inline-block mt-3 px-4 py-1 rounded-full text-sm font-medium
          ${
            report.verdict === "hire"
              ? "bg-green-100 text-green-700"
              : report.verdict === "maybe"
              ? "bg-yellow-100 text-yellow-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {report.verdict.toUpperCase()}
        </span>
      </div>

      {/* STRENGTHS & WEAKNESSES
      <div className="grid md:grid-cols-2 gap-6 mb-6"> */}

        {/* Strengths */}
        {/* <div className="bg-green-50 p-5 rounded-xl">
          <h2 className="font-semibold mb-3 text-green-700">Strengths</h2>
          <ul className="list-disc pl-5 space-y-1">
            {report.strengths.length > 0 ? (
              report.strengths.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))
            ) : (
              <p className="text-sm text-gray-500">No strong signals</p>
            )}
          </ul>
        </div> */}

        {/* Weaknesses */}
        {/* <div className="bg-red-50 p-5 rounded-xl">
          <h2 className="font-semibold mb-3 text-red-700">Weaknesses</h2>
          <ul className="list-disc pl-5 space-y-1">
            {report.weaknesses.length > 0 ? (
              report.weaknesses.map((w: string, i: number) => (
                <li key={i}>{w}</li>
              ))
            ) : (
              <p className="text-sm text-gray-500">No major issues</p>
            )}
          </ul>
        </div>

      </div> */}

      {/* QUESTIONS */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Question-wise Analysis
        </h2>

        {report.questions.map((q: any, index: number) => (
          <div
            key={index}
            className="border rounded-xl p-5 mb-4 bg-white shadow-sm"
          >
            <p className="font-semibold text-lg">
              {index + 1}. {q.question}
            </p>

            <p className="text-sm text-gray-600 mt-2">
              <span className="font-medium">Your Answer:</span> {q.answer}
            </p>

            <div className="mt-3 flex justify-between items-center">
              <span className="font-medium">Score: {q.score}</span>
            </div>

            <p className="mt-2 text-gray-700">{q.feedback}</p>
          </div>
        ))}
      </div>

    </div>
  );
}