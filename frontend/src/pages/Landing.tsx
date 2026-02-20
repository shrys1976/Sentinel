import { type ChangeEvent, type DragEvent, useState } from "react";
import { BackgroundPathsLayer } from "@/components/ui/background-paths";

export default function Landing() {
  const [uploadStatus, setUploadStatus] = useState("No file selected");
  const [isDragging, setIsDragging] = useState(false);

  const setFile = (file: File | null) => {
    if (!file) {
      setUploadStatus("No file selected");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
      setUploadStatus("Invalid file type. Please upload a CSV file.");
      return;
    }

    setUploadStatus(`Ready: ${file.name}`);
  };

  const onInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setFile(file);
  };

  const onDrop = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0] ?? null;
    setFile(file);
  };

  return (
    <>
      <section
        id="top"
        className="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_50%_-10%,#182a69_0,#06102f_45%,#04091e_75%)]"
      >
        <div className="pointer-events-none absolute inset-0 dark opacity-35">
          <BackgroundPathsLayer />
        </div>
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_15%_60%,rgba(93,110,255,0.55),transparent_42%),radial-gradient(circle_at_88%_58%,rgba(93,110,255,0.6),transparent_42%),linear-gradient(180deg,transparent_62%,rgba(237,241,251,0.95)_100%)]" />

        <div className="relative z-10 mx-auto flex w-[min(1120px,calc(100vw-56px))] flex-col items-center pb-24 pt-32 text-center text-slate-100 md:pt-36">
          <h1 className="mt-4 max-w-4xl text-5xl font-bold leading-[1.02] tracking-[-0.03em] md:text-7xl">
            Don&apos;t Train Blind.
          </h1>
          <p className="mt-5 max-w-3xl text-xl text-slate-200 md:text-3xl">
            Know if your dataset is ML-ready before training your model.
          </p>
          <p className="mt-5 max-w-3xl text-base leading-relaxed text-slate-300 md:text-xl">
            Sentinel AI automatically detects leakage risks, imbalance, missing data patterns,
            and hidden dataset failures before they cost hours of debugging.
          </p>

          <label
            onDragOver={(event) => {
              event.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={(event) => {
              event.preventDefault();
              setIsDragging(false);
            }}
            onDrop={onDrop}
            className={`mt-8 block w-full max-w-4xl cursor-pointer rounded-2xl border bg-slate-50/95 p-6 text-center text-slate-900 shadow-2xl backdrop-blur-sm transition ${
              isDragging
                ? "border-indigo-500 ring-2 ring-indigo-300"
                : "border-slate-200 hover:border-indigo-300"
            }`}
          >
            <div className="inline-flex h-14 w-14 items-center justify-center rounded-xl bg-indigo-100 text-3xl text-indigo-600">
              ⇪
            </div>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight text-slate-800 md:text-4xl">
              Drop your CSV file here
            </h2>
            <p className="mt-1 text-slate-600">or click to browse securely</p>
            <input type="file" accept=".csv,text/csv" className="hidden" onChange={onInputChange} />
            <div className="mt-5 flex flex-col items-center gap-2 border-t border-slate-200 pt-4 text-sm text-slate-600 md:flex-row md:justify-center md:gap-10">
              <span>Accepted format: .csv</span>
              <span>{uploadStatus}</span>
            </div>
          </label>
        </div>
      </section>

      <section className="bg-[radial-gradient(circle_at_20%_0%,#1a2b6d_0,#0a143f_48%,#050a21_100%)] py-24 text-slate-100">
        <div className="mx-auto w-[min(1120px,calc(100vw-56px))]">
          <p className="text-xs uppercase tracking-[0.12em] text-slate-400">( Workflow )</p>
          <h2 className="mt-3 text-4xl font-semibold tracking-tight text-slate-100 md:text-5xl">
            How It Works
          </h2>
          <div className="mt-10 grid gap-5 md:grid-cols-3">
            <article className="rounded-2xl border border-white/15 bg-slate-900/40 p-6 backdrop-blur-sm">
              <span className="rounded-full bg-indigo-400/20 px-3 py-1 text-xs font-semibold uppercase tracking-[0.08em] text-indigo-200">
                Step 1
              </span>
              <h3 className="mt-4 text-2xl font-semibold text-slate-100">Upload Dataset</h3>
              <p className="mt-2 text-slate-300">Upload CSV datasets securely.</p>
            </article>
            <article className="rounded-2xl border border-white/15 bg-slate-900/40 p-6 backdrop-blur-sm">
              <span className="rounded-full bg-indigo-400/20 px-3 py-1 text-xs font-semibold uppercase tracking-[0.08em] text-indigo-200">
                Step 2
              </span>
              <h3 className="mt-4 text-2xl font-semibold text-slate-100">Analysis Engine</h3>
              <p className="mt-2 text-slate-300">
                Statistical analysis detects ML risks and dataset problems.
              </p>
            </article>
            <article className="rounded-2xl border border-white/15 bg-slate-900/40 p-6 backdrop-blur-sm">
              <span className="rounded-full bg-indigo-400/20 px-3 py-1 text-xs font-semibold uppercase tracking-[0.08em] text-indigo-200">
                Step 3
              </span>
              <h3 className="mt-4 text-2xl font-semibold text-slate-100">Fix Issues</h3>
              <p className="mt-2 text-slate-300">
                Receive actionable recommendations before training your model.
              </p>
            </article>
          </div>
        </div>
      </section>

      <section
        id="features"
        className="bg-[linear-gradient(180deg,#050a21_0%,#0c1a4d_55%,#07102f_100%)] py-24 text-slate-100"
      >
        <div className="mx-auto w-[min(1120px,calc(100vw-56px))]">
          <p className="text-xs uppercase tracking-[0.12em] text-slate-400">( Core Features )</p>
          <h2 className="mt-3 text-4xl font-semibold tracking-tight text-slate-100 md:text-5xl">
            Feature Highlights
          </h2>
          <div className="mt-10 grid gap-5 md:grid-cols-2">
            <article className="rounded-2xl border border-white/15 bg-slate-900/45 p-6 backdrop-blur-sm">
              <h3 className="text-2xl font-semibold text-slate-100">Leakage Detection</h3>
              <p className="mt-2 text-slate-300">Identify features leaking target information.</p>
            </article>
            <article className="rounded-2xl border border-white/15 bg-slate-900/45 p-6 backdrop-blur-sm">
              <h3 className="text-2xl font-semibold text-slate-100">Missing Value Analysis</h3>
              <p className="mt-2 text-slate-300">Detect harmful missing data patterns.</p>
            </article>
            <article className="rounded-2xl border border-white/15 bg-slate-900/45 p-6 backdrop-blur-sm">
              <h3 className="text-2xl font-semibold text-slate-100">Imbalance Diagnostics</h3>
              <p className="mt-2 text-slate-300">Understand class imbalance risks.</p>
            </article>
            <article className="rounded-2xl border border-white/15 bg-slate-900/45 p-6 backdrop-blur-sm">
              <h3 className="text-2xl font-semibold text-slate-100">Outlier Detection</h3>
              <p className="mt-2 text-slate-300">Spot anomalies affecting model stability.</p>
            </article>
          </div>
        </div>
      </section>

      <section id="dashboard" className="bg-slate-200 py-24">
        <div className="mx-auto w-[min(1120px,calc(100vw-56px))]">
          <p className="text-xs uppercase tracking-[0.12em] text-slate-500">( Example Output )</p>
          <h2 className="mt-3 text-4xl font-semibold tracking-tight text-slate-800 md:text-5xl">
            Dataset Report Preview
          </h2>
          <article className="mt-10 rounded-2xl border border-slate-200 bg-slate-50 p-7 shadow-xl shadow-slate-400/20">
            <div className="flex flex-col gap-4 border-b border-slate-200 pb-5 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.08em] text-slate-500">Dataset Name</p>
                <h3 className="mt-2 text-3xl font-semibold tracking-tight text-slate-800">
                  customer_churn.csv
                </h3>
              </div>
              <span className="inline-flex rounded-full bg-indigo-100 px-4 py-2 text-sm font-bold text-indigo-700">
                Sentinel Score: 72 / 100
              </span>
            </div>

            <div className="mt-6 grid gap-6 md:grid-cols-2">
              <div>
                <h4 className="text-lg font-semibold text-slate-800">Critical Issues</h4>
                <ul className="mt-2 list-disc space-y-2 pl-5 text-slate-600">
                  <li>Target Leakage Detected</li>
                  <li>Severe Class Imbalance</li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-semibold text-slate-800">Recommendations</h4>
                <ul className="mt-2 list-disc space-y-2 pl-5 text-slate-600">
                  <li>Drop transaction_id column</li>
                  <li>Apply stratified split</li>
                </ul>
              </div>
            </div>
          </article>
        </div>
      </section>

      <section id="signup" className="bg-[linear-gradient(180deg,#070e2a_0%,#10205e_40%,#e6ebfb_100%)] py-24 text-center text-slate-100">
        <div className="mx-auto w-[min(900px,calc(100vw-56px))]">
          <h2 className="text-4xl font-semibold tracking-tight md:text-5xl">
            Stop guessing why your model fails.
          </h2>
          <button
            type="button"
            className="mt-8 rounded-xl bg-slate-200 px-7 py-3 text-sm font-extrabold uppercase tracking-[0.08em] text-slate-800 transition hover:bg-white"
          >
            Analyze Dataset
          </button>
        </div>
      </section>

      <footer className="border-t border-slate-300 bg-slate-100 py-6">
        <div className="mx-auto flex w-[min(1120px,calc(100vw-56px))] flex-col gap-4 text-sm text-slate-600 md:flex-row md:items-center md:justify-between">
          <span className="text-base font-extrabold text-slate-800">Sentinel AI</span>
          <div className="flex flex-wrap items-center gap-5">
            <a href="#" className="transition hover:text-slate-900">
              Docs
            </a>
            <a href="#" className="transition hover:text-slate-900">
              Github
            </a>
            <a href="#" className="transition hover:text-slate-900">
              Privacy
            </a>
            <a href="#" className="transition hover:text-slate-900">
              Contact
            </a>
          </div>
        </div>
      </footer>
    </>
  );
}
