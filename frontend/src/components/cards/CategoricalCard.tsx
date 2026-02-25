type Props = { data: Record<string, unknown> };

export default function CategoricalCard({ data }: Props) {
  if (Boolean(data["skipped"])) return null;

  const highCardinality = Array.isArray(data["high_cardinality_columns"])
    ? (data["high_cardinality_columns"] as string[])
    : [];
  const constantCategorical = Array.isArray(data["constant_categorical_columns"])
    ? (data["constant_categorical_columns"] as string[])
    : [];

  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-xl font-semibold text-slate-100">Categorical Risks</h3>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        <div>
          <p className="text-sm font-medium text-slate-300">High cardinality columns</p>
          <ul className="mt-2 space-y-2 text-sm text-slate-200">
            {(highCardinality.length ? highCardinality : ["None"]).map((item) => (
              <li key={`hc-${item}`} className="rounded-md bg-white/5 px-3 py-2">
                {item}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-sm font-medium text-slate-300">Constant categorical columns</p>
          <ul className="mt-2 space-y-2 text-sm text-slate-200">
            {(constantCategorical.length ? constantCategorical : ["None"]).map((item) => (
              <li key={`cc-${item}`} className="rounded-md bg-white/5 px-3 py-2">
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </article>
  );
}
