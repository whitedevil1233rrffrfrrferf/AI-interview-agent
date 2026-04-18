"use client";

import { api } from "@/lib/api";
import { User } from "@/types/auth";

export default function Home() {
  return (<div style={{ padding: 40 }}>
      <h1>Welcome to the AI Interview Simulator</h1>
      <p>Please login to start your interview preparation.</p>
    </div>
  );
}