type Props = { data: Record<string, unknown> };

export default function BasicStatsCard({ data }: Props) {
  if (Boolean(data["skipped"])) return null;

  const numeric = Number(data["numeric_columns"] ?? 0);
  const categorical = Number(data["categorical_columns"] ?? 0);
  const duplicateRatio = Number(data["duplicate_ratio"] ?? 0);
  const constants = Array.isArray(data["constant_columns"]) ? data["constant_columns"] : [];

  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-xl font-semibold text-slate-100">Basic Stats</h3>
      <div className="mt-3 grid gap-2 text-sm text-slate-300 md:grid-cols-2">
        <p>Numeric columns: {numeric}</p>
        <p>Categorical columns: {categorical}</p>
        <p>Duplicate ratio: {(duplicateRatio * 100).toFixed(2)}%</p>
        <p>Constant columns: {constants.length}</p>
      </div>
    </article>
  );
}
