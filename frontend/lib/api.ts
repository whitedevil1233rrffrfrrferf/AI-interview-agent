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
  getCurrentUser: async () => {
    const res = await fetch(`${BASE_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });

  if (!res.ok) throw new Error("Failed");

  return res.json();
  },
  
  startInterview: async (
    role: string,
    difficulty: string,
    resume?: File | null
  ) => {
    const formData = new FormData();

    formData.append("role", role);
    formData.append("difficulty", difficulty);

    if (resume) {
      formData.append("resume", resume);
    }

    const res = await fetch(`${BASE_URL}/interview/start`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`, // no Content-Type
      },
      body: formData,
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
  getReport: async (interview_id: number) => {
    const res = await fetch(
      `${BASE_URL}/interview/${interview_id}/report`,
      {
        headers: getHeaders(),
      }
    );
    return res.json();
  },
  getInterviewHistory: async () => {
    const res = await fetch(`${BASE_URL}/interview/history`, {
      headers: getHeaders(),
    });

    if (!res.ok) throw new Error("Failed to fetch history");

    return res.json();
  },

  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${BASE_URL}/resume/upload`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`, // no content-type
      },
      body: formData,
    });

    if (!res.ok) throw new Error("Upload failed");

    return res.json();
  },
};