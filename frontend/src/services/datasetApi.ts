import { api } from "./api";

export async function listDatasets() {
  return api.fetchJson<unknown[]>("/datasets");
}
