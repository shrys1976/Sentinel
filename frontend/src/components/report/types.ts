export type ReportDatasetMeta = {
  id: string;
  name: string;
  rows: number | null;
  columns: number | null;
  target_column?: string | null;
  created_at?: string;
  status?: string;
};

export type ReportViewData = {
  dataset: ReportDatasetMeta;
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
