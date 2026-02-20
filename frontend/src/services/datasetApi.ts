import { api } from "./api";

export async function listDatasets() {
  const res = await fetch(`${api.baseUrl}/datasets`);
  return res.json();
}
