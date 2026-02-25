import { api } from "./api";

export async function getReport(id: string) {
  return api.fetchJson<Record<string, unknown>>(`/reports/${id}`);
}
