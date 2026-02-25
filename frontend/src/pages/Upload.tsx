import { useMemo, useState } from "react";

import { uploadDataset } from "../services/datasetApi";

type UploadProps = {
  initialFile: File | null;
  onNavigateLogin: () => void;
  onUploaded: (datasetId: string) => void;
  isAuthenticated: boolean;
};

function stripCsv(name: string) {
  return name.replace(/\.csv$/i, "").trim() || "dataset";
}

export default function Upload({ initialFile, onNavigateLogin, onUploaded, isAuthenticated }: UploadProps) {
  const [file, setFile] = useState<File | null>(initialFile);
  const [datasetName, setDatasetName] = useState(initialFile ? stripCsv(initialFile.name) : "");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = Boolean(file && datasetName.trim() && !submitting && isAuthenticated);
  const fileLabel = useMemo(() => (file ? `${file.name} (${Math.round(file.size / 1024)} KB)` : "No file selected"), [file]);

  const onFileChange = (nextFile: File | null) => {
    setFile(nextFile);
    if (nextFile) setDatasetName(stripCsv(nextFile.name));
  };

  const submit = async () => {
    setError(null);
    if (!isAuthenticated) {
      onNavigateLogin();
      return;
    }
    if (!file) {
      setError("Please choose a CSV file first.");
      return;
    }

    setSubmitting(true);
    try {
      const payload = await uploadDataset(file, datasetName.trim());
      onUploaded(payload.dataset_id);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-black px-5 py-24 text-slate-100">
      <div className="mx-auto w-full max-w-2xl rounded-2xl border border-white/10 bg-slate-950/70 p-7 backdrop-blur-sm">
        <h1 className="instrument-serif-regular text-5xl tracking-tight">Upload Dataset</h1>
        <p className="mt-2 text-sm text-slate-400">Upload your CSV and start analysis immediately.</p>

        <div className="mt-6 space-y-4">
          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">Dataset name</span>
            <input
              type="text"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 text-slate-100 outline-none transition focus:border-white/40"
              placeholder="customer_churn"
            />
          </label>

          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">CSV file</span>
            <input
              type="file"
              accept=".csv,text/csv"
              onChange={(e) => onFileChange(e.target.files?.[0] ?? null)}
              className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 text-slate-100 outline-none"
            />
          </label>

          <p className="text-xs text-slate-400">{fileLabel}</p>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}

          {!isAuthenticated ? (
            <button
              type="button"
              onClick={onNavigateLogin}
              className="w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-slate-200"
            >
              Login to Continue
            </button>
          ) : (
            <button
              type="button"
              disabled={!canSubmit}
              onClick={submit}
              className="w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting ? "Uploading..." : "Upload Dataset"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
