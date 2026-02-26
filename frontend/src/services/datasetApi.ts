import { api } from "./api";

export type DatasetHistoryItem = {
  dataset_id: string;
  name: string;
  status: string;
  rows: number | null;
  columns: number | null;
  target_column: string | null;
  created_at: string;
};

export async function listDatasets() {
  try {
    const payload = await api.fetchJson<{ datasets?: DatasetHistoryItem[] }>("/datasets");
    return Array.isArray(payload.datasets) ? payload.datasets : [];
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "";
    if (message.includes("404")) return [];
    throw err;
  }
}

export async function deleteDataset(datasetId: string) {
  return api.fetchJson<{ message: string }>(`/datasets/${datasetId}`, { method: "DELETE" });
}

export type DatasetStatus = {
  dataset_id: string;
  status: string;
  rows: number | null;
  columns: number | null;
  target_column: string | null;
};

export type DatasetUploadResult = {
  dataset_id: string;
  rows: number;
  columns: number;
  status: string;
  target_column: string | null;
};

export async function uploadDataset(file: File, datasetName: string, targetColumn?: string) {
  const body = new FormData();
  body.append("file", file);
  body.append("dataset_name", datasetName);
  if (targetColumn && targetColumn.trim()) {
    body.append("target_column", targetColumn.trim());
  }

  const res = await api.request(`${api.baseUrl}/datasets/upload`, {
    method: "POST",
    body,
  });

  if (!res.ok) {
    let detail = "Upload failed";
    try {
      const payload = await res.json();
      detail = payload?.detail ?? payload?.message ?? detail;
    } catch {
      // keep fallback
    }
    throw new Error(`${res.status} ${detail}`);
  }

  return (await res.json()) as DatasetUploadResult;
}

export async function getDatasetStatus(datasetId: string) {
  return api.fetchJson<DatasetStatus>(`/datasets/${datasetId}/status`);
}
