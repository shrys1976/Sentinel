import { useEffect, useMemo, useState } from "react";

import { getDatasetStatus, type DatasetStatus } from "../services/datasetApi";

type AnalysisProps = {
  datasetId: string;
  onGoAnalyses: () => void;
  onViewReport: (datasetId: string) => void;
};

export default function Analysis({ datasetId, onGoAnalyses, onViewReport }: AnalysisProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<DatasetStatus | null>(null);

  useEffect(() => {
    let cancelled = false;
    let timer: number | undefined;

    const tick = async () => {
      try {
        const next = await getDatasetStatus(datasetId);
        if (cancelled) return;
        setStatus(next);
        setError(null);
        setLoading(false);

        if (next.status === "processing" || next.status === "uploaded") {
          timer = window.setTimeout(tick, 3000);
        }
      } catch (err: unknown) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "Failed to load analysis status.");
        setLoading(false);
      }
    };

    tick();

    return () => {
      cancelled = true;
      if (timer) window.clearTimeout(timer);
    };
  }, [datasetId]);

  const subtitle = useMemo(() => {
    if (!status) return "";
    if (status.status === "completed") return "Analysis complete. You can now view your report.";
    if (status.status === "failed") return "Analysis failed. Please re-upload and try again.";
    return "Analysis is running. This page updates automatically.";
  }, [status]);

  return (
    <div className="min-h-screen bg-black px-5 py-24 text-slate-100">
      <div className="mx-auto w-full max-w-3xl rounded-2xl border border-white/10 bg-slate-950/70 p-7 backdrop-blur-sm">
        <h1 className="instrument-serif-regular text-5xl tracking-tight">Analysis</h1>
        <p className="mt-2 text-sm text-slate-400">Dataset ID: {datasetId}</p>

        {loading ? <p className="mt-6 text-slate-300">Preparing analysis...</p> : null}
        {error ? <p className="mt-6 text-rose-300">{error}</p> : null}

        {status ? (
          <div className="mt-6 rounded-xl border border-white/10 bg-black/30 p-4">
            <p className="text-sm uppercase tracking-[0.08em] text-slate-400">Current status</p>
            <p className="mt-1 text-2xl font-semibold text-slate-100">{status.status}</p>
            <p className="mt-2 text-sm text-slate-300">{subtitle}</p>
          </div>
        ) : null}

        <div className="mt-6 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onGoAnalyses}
            className="rounded-lg border border-white/20 px-4 py-2 text-sm text-slate-100 transition hover:bg-white/10"
          >
            Go to Analyses
          </button>
          {status?.status === "completed" ? (
            <button
              type="button"
              onClick={() => onViewReport(datasetId)}
              className="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-slate-200"
            >
              View Report
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}
