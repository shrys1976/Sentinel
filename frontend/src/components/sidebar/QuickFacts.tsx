type Props = {
  facts: string[];
};

export default function QuickFacts({ facts }: Props) {
  return (
    <section className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-slate-100">Quick Facts</h3>
      <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-200">
        {facts.map((fact, index) => (
          <li key={`fact-${index}`}>{fact}</li>
        ))}
      </ul>
    </section>
  );
}
