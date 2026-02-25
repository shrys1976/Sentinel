export type ReportDatasetMeta = {
  id: string;
  name: string;
  rows: number;
  columns: number;
  created_at?: string;
  status?: string;
};

export type ReportViewData = {
  dataset: ReportDatasetMeta;
  sentinel_score: number;
  top_issues: string[];
  warnings: string[];
  failed_analyzers: string[];
  sections: Record<string, Record<string, unknown>>;
};
