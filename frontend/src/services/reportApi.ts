import { api } from "./api";

export async function getReport(id: string) {
  return api.fetchJson<Record<string, unknown>>(`/reports/${id}`);
}

export type ReportView = {
  dataset: {
    id: string;
    name: string;
    rows: number;
    columns: number;
    created_at?: string;
    status?: string;
  };
  sentinel_score: number;
  top_issues: string[];
  warnings: string[];
  failed_analyzers: string[];
  sections: Record<string, Record<string, unknown>>;
};

export async function getReportView(datasetId: string) {
  return api.fetchJson<ReportView>(`/reports/${datasetId}/view`);
}
