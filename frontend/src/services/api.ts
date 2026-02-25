import { supabase } from "../lib/supabase";

const baseUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function getAccessToken() {
  const { data } = await supabase.auth.getSession();
  return data.session?.access_token ?? null;
}

async function request(input: string, init: RequestInit = {}) {
  const token = await getAccessToken();
  const headers = new Headers(init.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (!headers.has("Content-Type") && init.body) headers.set("Content-Type", "application/json");

  return fetch(input, { ...init, headers });
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
