type Props = {
  score: number;
  rows: number;
  columns: number;
  numericColumns: number;
  categoricalColumns: number;
};

export default function DatasetSummary({ score, rows, columns, numericColumns, categoricalColumns }: Props) {
  return (
    <section className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-slate-100">Dataset Summary</h3>
      <ul className="mt-3 space-y-2 text-sm text-slate-200">
        <li className="flex justify-between"><span>Sentinel score</span><span>{score}/100</span></li>
        <li className="flex justify-between"><span>Rows</span><span>{rows}</span></li>
        <li className="flex justify-between"><span>Columns</span><span>{columns}</span></li>
        <li className="flex justify-between"><span>Numeric columns</span><span>{numericColumns}</span></li>
        <li className="flex justify-between"><span>Categorical columns</span><span>{categoricalColumns}</span></li>
      </ul>
    </section>
  );
}
