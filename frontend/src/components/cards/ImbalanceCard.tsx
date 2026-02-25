type Props = { data: Record<string, unknown> };

export default function ImbalanceCard({ data }: Props) {
  if (Boolean(data["skipped"])) {
    return (
      <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
        <h3 className="text-xl font-semibold text-slate-100">Class Imbalance</h3>
        <p className="mt-2 text-sm text-slate-300">Skipped: {String(data["reason"] ?? "no target column")}</p>
      </article>
    );
  }

  const distribution = data["class_distribution"] as Record<string, number> | undefined;
  const minorityRatio = Number(data["minority_ratio"] ?? 0);
  const imbalanceDetected = Boolean(data["imbalance_detected"]);

  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-xl font-semibold text-slate-100">Class Imbalance</h3>
        {imbalanceDetected ? (
          <span className="rounded-full bg-amber-400/20 px-3 py-1 text-xs font-semibold uppercase tracking-[0.08em] text-amber-200">
            Imbalance Detected
          </span>
        ) : null}
      </div>

      <p className="mt-2 text-sm text-slate-300">Minority ratio: {(minorityRatio * 100).toFixed(2)}%</p>
      <ul className="mt-3 space-y-2 text-sm text-slate-200">
        {Object.entries(distribution ?? {}).map(([cls, value]) => (
          <li key={cls} className="flex justify-between rounded-md bg-white/5 px-3 py-2">
            <span>{cls}</span>
            <span>{Number(value).toFixed(4)}</span>
          </li>
        ))}
      </ul>
    </article>
  );
}
