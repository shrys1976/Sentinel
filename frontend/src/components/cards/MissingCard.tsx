type Props = { data: Record<string, unknown> };

export default function MissingCard({ data }: Props) {
  if (Boolean(data["skipped"])) return null;

  const overall = Number(data["overall_missing_ratio"] ?? 0);
  const missingRatio = data["missing_ratio"] as Record<string, number> | undefined;
  const topColumns = Object.entries(missingRatio ?? {})
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-xl font-semibold text-slate-100">Missing Data</h3>
      <p className="mt-2 text-sm text-slate-300">Overall missing: {(overall * 100).toFixed(2)}%</p>
      <ul className="mt-3 space-y-2 text-sm text-slate-200">
        {topColumns.length ? (
          topColumns.map(([column, value]) => (
            <li key={column} className="flex justify-between rounded-md bg-white/5 px-3 py-2">
              <span>{column}</span>
              <span>{(Number(value) * 100).toFixed(2)}%</span>
            </li>
          ))
        ) : (
          <li className="rounded-md bg-white/5 px-3 py-2">No missingness risk columns.</li>
        )}
      </ul>
    </article>
  );
}
