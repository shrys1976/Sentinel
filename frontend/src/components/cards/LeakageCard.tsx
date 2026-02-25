type Props = { data: Record<string, unknown> };

export default function LeakageCard({ data }: Props) {
  if (Boolean(data["skipped"])) return null;

  const suspicious = Array.isArray(data["suspicious_features"])
    ? (data["suspicious_features"] as Array<{ feature: string; correlation: number }>)
    : [];

  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-xl font-semibold text-slate-100">Leakage Risk</h3>
      <ul className="mt-3 space-y-2 text-sm text-slate-200">
        {suspicious.length ? (
          suspicious.map((item) => (
            <li key={item.feature} className="flex justify-between rounded-md bg-rose-400/10 px-3 py-2 text-rose-100">
              <span>{item.feature}</span>
              <span>{Number(item.correlation).toFixed(3)}</span>
            </li>
          ))
        ) : (
          <li className="rounded-md bg-white/5 px-3 py-2">No suspicious leakage features found.</li>
        )}
      </ul>
    </article>
  );
}
