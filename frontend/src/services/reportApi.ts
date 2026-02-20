import { api } from "./api";

export async function getReport(id: string) {
  const res = await fetch(`${api.baseUrl}/reports/${id}`);
  return res.json();
}
