type SentinelScoreProps = {
  score: number;
};

function scoreTone(score: number) {
  if (score >= 85) return { badge: "bg-emerald-400/20 text-emerald-200", label: "Healthy" };
  if (score >= 60) return { badge: "bg-amber-400/20 text-amber-200", label: "Moderate Risk" };
  return { badge: "bg-rose-500/20 text-rose-200", label: "High Risk" };
}

export default function SentinelScore({ score }: SentinelScoreProps) {
  const tone = scoreTone(score);

  return (
    <section className="rounded-2xl border border-white/10 bg-slate-950/70 p-6 backdrop-blur-sm">
      <p className="text-xs uppercase tracking-[0.12em] text-slate-400">Sentinel Score</p>
      <div className="mt-2 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <h2 className="instrument-serif-regular text-5xl tracking-tight text-slate-100 md:text-6xl">
          {score} <span className="text-3xl text-slate-400 md:text-4xl">/ 100</span>
        </h2>
        <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.08em] ${tone.badge}`}>
          {tone.label}
        </span>
      </div>
      <p className="mt-3 text-sm text-slate-300">
        This score summarizes dataset readiness before model training.
      </p>
    </section>
  );
}
