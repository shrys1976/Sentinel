import { useEffect, useMemo, useState } from "react";

import { listDatasets, type DatasetHistoryItem } from "../services/datasetApi";

type AnalysesProps = {
  onOpenAnalysis: (datasetId: string) => void;
  onViewReport: (datasetId: string) => void;
};

const POLL_MS = 4000;

export default function Analyses({ onOpenAnalysis, onViewReport }: AnalysesProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [items, setItems] = useState<DatasetHistoryItem[]>([]);

  useEffect(() => {
    let cancelled = false;
    let timer: number | undefined;

    const tick = async () => {
      try {
        const data = await listDatasets();
        if (cancelled) return;
        setItems(data);
        setError(null);
        setLoading(false);

        const hasRunning = data.some((d) => d.status === "processing" || d.status === "uploaded");
        if (hasRunning) timer = window.setTimeout(tick, POLL_MS);
      } catch (err: unknown) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "Failed to fetch analyses");
        setLoading(false);
      }
    };

    tick();

    return () => {
      cancelled = true;
      if (timer) window.clearTimeout(timer);
    };
  }, []);

  const ordered = useMemo(
    () => [...items].sort((a, b) => String(b.created_at).localeCompare(String(a.created_at))),
    [items]
  );

  return (
    <div className="min-h-screen bg-black px-5 py-24 text-slate-100">
      <div className="mx-auto w-[min(1120px,calc(100vw-56px))]">
        <h1 className="instrument-serif-regular text-5xl tracking-tight">Analyses</h1>
        <p className="mt-2 text-sm text-slate-400">Track processing status and open completed reports.</p>

        {loading ? <p className="mt-6 text-slate-300">Loading analyses...</p> : null}
        {error ? <p className="mt-6 text-rose-300">{error}</p> : null}

        {!loading && !error ? (
          <div className="mt-6 rounded-2xl border border-white/10 bg-slate-950/70 p-4 backdrop-blur-sm">
            {ordered.length ? (
              <div className="space-y-3">
                {ordered.map((item) => (
                  <div
                    key={item.dataset_id}
                    className="flex flex-col gap-3 rounded-xl border border-white/10 bg-black/35 p-4 md:flex-row md:items-center md:justify-between"
                  >
                    <div>
                      <p className="text-lg font-semibold text-slate-100">{item.name}</p>
                      <p className="text-xs text-slate-400">
                        {item.rows ?? "-"} rows • {item.columns ?? "-"} columns • {item.status}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => onOpenAnalysis(item.dataset_id)}
                        className="rounded-lg border border-white/20 px-3 py-1.5 text-xs text-slate-100 transition hover:bg-white/10"
                      >
                        Open Analysis
                      </button>
                      {item.status === "completed" ? (
                        <button
                          type="button"
                          onClick={() => onViewReport(item.dataset_id)}
                          className="rounded-lg bg-white px-3 py-1.5 text-xs font-semibold text-black transition hover:bg-slate-200"
                        >
                          View Report
                        </button>
                      ) : null}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-300">No previous uploads found.</p>
            )}
          </div>
        ) : null}
      </div>
    </div>
  );
}
