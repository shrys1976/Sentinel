type Props = { data: Record<string, unknown> };

export default function OutlierCard({ data }: Props) {
  if (Boolean(data["skipped"])) return null;

  const ratios = data["outlier_ratio"] as Record<string, number> | undefined;
  const sorted = Object.entries(ratios ?? {})
    .sort((a, b) => b[1] - a[1])
    .filter(([, ratio]) => ratio > 0)
    .slice(0, 10);

  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-xl font-semibold text-slate-100">Outliers</h3>
      <ul className="mt-3 space-y-2 text-sm text-slate-200">
        {sorted.length ? (
          sorted.map(([column, ratio]) => (
            <li key={column} className="flex justify-between rounded-md bg-white/5 px-3 py-2">
              <span>{column}</span>
              <span>{(Number(ratio) * 100).toFixed(2)}%</span>
            </li>
          ))
        ) : (
          <li className="rounded-md bg-white/5 px-3 py-2">No meaningful outlier concentrations.</li>
        )}
      </ul>
    </article>
  );
}
