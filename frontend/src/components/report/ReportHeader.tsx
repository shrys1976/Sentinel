import type { ReportDatasetMeta } from "./types";

type ReportHeaderProps = {
  dataset: ReportDatasetMeta;
  onBack: () => void;
  onDelete: () => void;
  deleting: boolean;
};

function formatDate(value?: string) {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString();
}

export default function ReportHeader({ dataset, onBack, onDelete, deleting }: ReportHeaderProps) {
  return (
    <section className="rounded-2xl border border-white/10 bg-slate-950/70 p-6 backdrop-blur-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <h1 className="instrument-serif-regular text-4xl tracking-tight text-slate-100 md:text-5xl">
            {dataset.name}
          </h1>
          <div className="mt-3 flex flex-wrap gap-4 text-sm text-slate-300">
            <span>Rows: {dataset.rows}</span>
            <span>Columns: {dataset.columns}</span>
            <span>Status: {dataset.status ?? "-"}</span>
            <span>Created: {formatDate(dataset.created_at)}</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onBack}
            className="rounded-lg border border-white/20 px-4 py-2 text-sm text-slate-100 transition hover:bg-white/10"
          >
            Back to Dashboard
          </button>
          <button
            type="button"
            onClick={onDelete}
            disabled={deleting}
            className="rounded-lg border border-rose-300/40 px-4 py-2 text-sm text-rose-200 transition hover:bg-rose-500/15 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {deleting ? "Deleting..." : "Delete Dataset"}
          </button>
        </div>
      </div>
    </section>
  );
}
