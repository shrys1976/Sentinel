import { api } from "./api";

export async function getReport(id: string) {
  return api.fetchJson<Record<string, unknown>>(`/reports/${id}`);
}

export type ReportView = {
  dataset: {
    id: string;
    name: string;
    rows: number | null;
    columns: number | null;
    target_column?: string | null;
    created_at?: string;
    status?: string;
  };
  sentinel_score: number;
  dataset_difficulty?: string | null;
  modeling_risk?: string | null;
  top_issues: string[];
  warnings: string[];
  failed_analyzers: string[];
  recommended_actions?: string[];
  available_plots?: string[];
  sections: Record<string, Record<string, unknown>>;
};

export async function getReportView(datasetId: string) {
  return api.fetchJson<ReportView>(`/reports/${datasetId}/view`);
}

export async function getReportPlotBlob(datasetId: string, plotName: string) {
  const res = await api.request(`${api.baseUrl}/plots/${datasetId}/${plotName}`, {
    method: "GET",
  });

  if (!res.ok) {
    let detail = "Failed to load plot";
    try {
      const payload = await res.json();
      detail = payload?.detail ?? payload?.message ?? detail;
    } catch {
      // keep fallback
    }
    throw new Error(`${res.status} ${detail}`);
  }

  return res.blob();
}
