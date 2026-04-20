// lib/useRequireAuth.ts
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export function useRequireAuth() {
  const [isAuthed, setIsAuthed] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    
    if (!token) {
      router.replace("/login");
    } else {
      setIsAuthed(true);
    }
  }, []);

  return isAuthed;
}