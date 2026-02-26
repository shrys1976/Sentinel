import { useEffect, useRef, useState } from "react";

import { getDatasetStatus, uploadDataset } from "../services/datasetApi";

type UploadProps = {
  initialFile: File | null;
  onUploaded: (datasetId: string) => void;
};

function stripCsv(name: string) {
  return name.replace(/\.csv$/i, "").trim() || "dataset";
}

export default function Upload({ initialFile, onUploaded }: UploadProps) {
  const [file, setFile] = useState<File | null>(initialFile);
  const [datasetName, setDatasetName] = useState(initialFile ? stripCsv(initialFile.name) : "");
  const [targetColumn, setTargetColumn] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [processingDatasetId, setProcessingDatasetId] = useState<string | null>(null);
  const [processingStatus, setProcessingStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const canSubmit = Boolean(file && datasetName.trim() && !submitting && !processingDatasetId);

  useEffect(() => {
    if (initialFile && !file) {
      setFile(initialFile);
      setDatasetName(stripCsv(initialFile.name));
    }
  }, [initialFile, file]);

  const onFileChange = (nextFile: File | null) => {
    setFile(nextFile);
    if (nextFile) setDatasetName(stripCsv(nextFile.name));
  };

  const submit = async () => {
    setError(null);
    if (!file) {
      setError("Please choose a CSV file first.");
      return;
    }

    setSubmitting(true);
    try {
      const payload = await uploadDataset(file, datasetName.trim(), targetColumn);
      setProcessingDatasetId(payload.dataset_id);
      setProcessingStatus(payload.status || "uploaded");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setSubmitting(false);
    }
  };

  useEffect(() => {
    if (!processingDatasetId) return;
    let cancelled = false;
    let timer: number | undefined;

    const tick = async () => {
      try {
        const status = await getDatasetStatus(processingDatasetId);
        if (cancelled) return;
        setProcessingStatus(status.status);
        if (status.status === "completed") {
          setProcessingDatasetId(null);
          onUploaded(processingDatasetId);
          return;
        }
        if (status.status === "failed") {
          setProcessingDatasetId(null);
          setError("Analysis failed while preparing report visuals. Please retry upload.");
          return;
        }
        timer = window.setTimeout(tick, 3000);
      } catch (err: unknown) {
        if (cancelled) return;
        setProcessingDatasetId(null);
        setError(err instanceof Error ? err.message : "Processing status check failed");
      }
    };

    timer = window.setTimeout(tick, 1500);
    return () => {
      cancelled = true;
      if (timer) window.clearTimeout(timer);
    };
  }, [processingDatasetId, onUploaded]);

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
              ref={inputRef}
              type="file"
              accept=".csv,text/csv"
              onChange={(e) => onFileChange(e.target.files?.[0] ?? null)}
              className="hidden"
            />
            <div className="rounded-xl border border-white/15 bg-black/60 px-3 py-3 text-slate-100">
              {file ? (
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-sm text-slate-200">Using selected file</p>
                    <p className="text-xs text-slate-400">
                      {file.name} ({Math.round(file.size / 1024)} KB)
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => inputRef.current?.click()}
                    className="rounded-lg border border-white/20 px-3 py-1.5 text-xs text-slate-100 transition hover:bg-white/10"
                  >
                    Change File
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => inputRef.current?.click()}
                  className="rounded-lg border border-white/20 px-3 py-1.5 text-xs text-slate-100 transition hover:bg-white/10"
                >
                  Choose CSV File
                </button>
              )}
            </div>
          </label>

          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">Target column (optional)</span>
            <input
              type="text"
              value={targetColumn}
              onChange={(e) => setTargetColumn(e.target.value)}
              className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 text-slate-100 outline-none transition focus:border-white/40"
              placeholder="e.g. churn_flag"
            />
            <p className="mt-1 text-xs text-slate-400">
              Add this to enable target-aware diagnostics and model simulation.
            </p>
          </label>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}
          {processingDatasetId ? (
            <p className="text-sm text-slate-300">
              Processing dataset and generating visuals... Status:{" "}
              <span className="font-semibold text-slate-100">{processingStatus ?? "processing"}</span>
            </p>
          ) : null}

          <button
            type="button"
            disabled={!canSubmit}
            onClick={submit}
            className="w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Uploading" : processingDatasetId ? "Processing..." : "Upload"}
          </button>
        </div>
      </div>
    </div>
  );
}
