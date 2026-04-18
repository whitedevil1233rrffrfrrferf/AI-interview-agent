const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;


const getHeaders = () => {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};

export const api = {
  login: async (email: string, password: string) => {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return res.json();
  },

  startInterview: async ( role: string, difficulty: string) => {
    const res = await fetch(`${BASE_URL}/interview/start`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify({ role, difficulty }),
    });
    return res.json();
  },

  submitAnswer: async (
    interview_id: number,
    question: string,
    answer: string
  ) => {
    const res = await fetch(`${BASE_URL}/interview/answer`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify({ interview_id, question, answer }),
    });
    return res.json();
  },
};