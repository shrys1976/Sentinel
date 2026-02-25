type IssuesPanelProps = {
  topIssues: string[];
  warnings: string[];
};

function ListBlock({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-xl border border-white/10 bg-black/30 p-4">
      <h3 className="text-sm font-semibold uppercase tracking-[0.08em] text-slate-300">{title}</h3>
      <ul className="mt-3 space-y-2 text-sm text-slate-200">
        {(items.length ? items.slice(0, 5) : ["None"]).map((item, i) => (
          <li key={`${title}-${i}`} className="rounded-md bg-white/5 px-3 py-2">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function IssuesPanel({ topIssues, warnings }: IssuesPanelProps) {
  return (
    <section className="grid gap-4 md:grid-cols-2">
      <ListBlock title="Critical Issues" items={topIssues} />
      <ListBlock title="Warnings" items={warnings} />
    </section>
  );
}
