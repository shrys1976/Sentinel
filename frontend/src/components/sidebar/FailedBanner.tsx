type Props = {
  failedAnalyzers: string[];
};

export default function FailedBanner({ failedAnalyzers }: Props) {
  if (!failedAnalyzers.length) return null;

  return (
    <section className="rounded-2xl border border-amber-400/30 bg-amber-500/10 p-5">
      <h3 className="text-sm font-semibold uppercase tracking-[0.08em] text-amber-200">
        Some diagnostics could not be completed.
      </h3>
      <p className="mt-2 text-sm text-amber-100">Failed analyzers: {failedAnalyzers.join(", ")}</p>
    </section>
  );
}
