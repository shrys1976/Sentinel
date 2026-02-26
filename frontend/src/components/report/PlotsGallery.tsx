import { useEffect, useMemo, useState } from "react";

import { getReportPlotBlob } from "../../services/reportApi";

type PlotsGalleryProps = {
  datasetId: string;
  availablePlots?: string[];
};

type PlotItem = {
  key: string;
  title: string;
  subtitle: string;
};

const PLOT_CATALOG: PlotItem[] = [
  {
    key: "missing_heatmap",
    title: "Missing Data Heatmap",
    subtitle: "Top missing columns across sampled rows",
  },
  {
    key: "target_distribution",
    title: "Target Distribution",
    subtitle: "Target balance and class shape",
  },
  {
    key: "feature_importance",
    title: "Feature Importance",
    subtitle: "Strongest predictive signals from diagnostics",
  },
  {
    key: "numeric_distribution",
    title: "Numeric Distributions",
    subtitle: "Distributions across top numeric features",
  },
  {
    key: "correlation_heatmap",
    title: "Correlation Heatmap",
    subtitle: "Top correlated numeric feature subset",
  },
];

export default function PlotsGallery({ datasetId, availablePlots }: PlotsGalleryProps) {
  const [urls, setUrls] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const items = useMemo(() => {
    const allowed = new Set(availablePlots ?? PLOT_CATALOG.map((plot) => plot.key));
    return PLOT_CATALOG.filter((plot) => allowed.has(plot.key));
  }, [availablePlots]);

  if (items.length === 0) return null;

  useEffect(() => {
    let cancelled = false;
    const activeUrls: string[] = [];

    async function loadPlots() {
      setLoading(true);
      setError(null);

      try {
        const nextUrls: Record<string, string> = {};
        await Promise.all(
          items.map(async (item) => {
            const blob = await getReportPlotBlob(datasetId, item.key);
            const objectUrl = URL.createObjectURL(blob);
            activeUrls.push(objectUrl);
            nextUrls[item.key] = objectUrl;
          })
        );

        if (!cancelled) setUrls(nextUrls);
      } catch (err: unknown) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Unable to load plots.");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadPlots();

    return () => {
      cancelled = true;
      activeUrls.forEach((url) => URL.revokeObjectURL(url));
    };
  }, [datasetId, items]);

  return (
    <section className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-slate-100">Visual Diagnostics</h3>
      </div>

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2">
          {items.map((item) => (
            <div key={`loading-${item.key}`} className="rounded-xl border border-white/10 bg-black/35 p-3">
              <div className="h-48 animate-pulse rounded-lg bg-white/10" />
            </div>
          ))}
        </div>
      ) : null}

      {!loading && error ? (
        <div className="rounded-xl border border-amber-300/30 bg-amber-500/10 p-4 text-sm text-amber-100">
          {error}
        </div>
      ) : null}

      {!loading && !error ? (
        <div className="grid gap-4 md:grid-cols-2">
          {items.map((item) => (
            <article key={item.key} className="rounded-xl border border-white/10 bg-black/35 p-3">
              <p className="text-sm font-semibold text-slate-100">{item.title}</p>
              <p className="mt-1 text-xs text-slate-400">{item.subtitle}</p>
              <div className="mt-3 overflow-hidden rounded-lg border border-white/10 bg-slate-900/50">
                {urls[item.key] ? (
                  <img
                    src={urls[item.key]}
                    alt={item.title}
                    className="h-72 w-full object-contain bg-slate-950 p-2 md:h-80"
                    loading="lazy"
                  />
                ) : (
                  <div className="flex h-72 items-center justify-center text-xs text-slate-400 md:h-80">
                    Plot unavailable
                  </div>
                )}
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}
