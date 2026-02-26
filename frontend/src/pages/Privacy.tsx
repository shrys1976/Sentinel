export default function Privacy() {
  return (
    <section className="min-h-screen bg-[linear-gradient(180deg,#020202_0%,#040917_52%,#020202_100%)] px-5 py-28 text-slate-100 md:px-8">
      <div className="mx-auto w-full max-w-4xl rounded-2xl border border-white/10 bg-slate-950/60 p-8 backdrop-blur-sm">
        <h1 className="instrument-serif-regular text-5xl tracking-tight md:text-6xl">Privacy</h1>
        <p className="mt-5 text-base leading-relaxed text-slate-300 md:text-lg">
          Sentinel is built with privacy first. Your uploaded datasets and analysis outputs are
          treated as confidential and are only accessible to your authenticated account or active
          guest session context.
        </p>
        <div className="mt-8 space-y-5 text-slate-300">
          <p>
            We store only the data required to run analysis, present results, and maintain your
            upload history. We do not sell your dataset contents to third parties.
          </p>
          <p>
            Access control checks are enforced on dataset and report endpoints. If a dataset is not
            owned by the requesting account/session, access is denied.
          </p>
          <p>
            You can remove uploaded datasets and associated reports from your history using the
            delete action in the product.
          </p>
        </div>
      </div>
    </section>
  );
}
