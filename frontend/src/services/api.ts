import { supabase } from "../lib/supabase";

const baseUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const SESSION_KEY = "sentinel_guest_session_id";

function getOrCreateSessionId() {
  const existing = window.localStorage.getItem(SESSION_KEY);
  if (existing) return existing;

  const generated =
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `guest_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;

  window.localStorage.setItem(SESSION_KEY, generated);
  return generated;
}

async function getAccessToken() {
  if (!supabase) return null;
  try {
    const { data } = await supabase.auth.getSession();
    return data.session?.access_token ?? null;
  } catch {
    return null;
  }
}

async function request(input: string, init: RequestInit = {}) {
  const token = await getAccessToken();
  const headers = new Headers(init.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  headers.set("X-Session-Id", getOrCreateSessionId());
  const isFormData = typeof FormData !== "undefined" && init.body instanceof FormData;
  if (!headers.has("Content-Type") && init.body && !isFormData) {
    headers.set("Content-Type", "application/json");
  }

  try {
    return await fetch(input, { ...init, headers });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "";
    if (message.includes("Failed to fetch") || message.includes("NetworkError")) {
      throw new Error("Backend is not reachable at VITE_API_URL. Start backend server and retry.");
    }
    throw error;
  }
}

async function fetchJson<T>(path: string, init: RequestInit = {}) {
  const res = await request(`${baseUrl}${path}`, init);
  if (!res.ok) {
    let detail = "Request failed";
    try {
      const payload = await res.json();
      detail = payload?.detail ?? payload?.message ?? detail;
    } catch {
      // keep default message
    }
    throw new Error(`${res.status} ${detail}`);
  }
  return (await res.json()) as T;
}

export const api = {
  baseUrl,
  request,
  fetchJson,
};
