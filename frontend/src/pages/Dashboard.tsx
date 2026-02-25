import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";
import { listDatasets } from "../services/datasetApi";

type DashboardProps = {
  onLogout: () => void;
};

export default function Dashboard({ onLogout }: DashboardProps) {
  const [loading, setLoading] = useState(true);
  const [datasets, setDatasets] = useState<unknown[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listDatasets()
      .then((data) => setDatasets(Array.isArray(data) ? data : []))
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Failed to load datasets.");
      })
      .finally(() => setLoading(false));
  }, []);

  const logout = async () => {
    await supabase.auth.signOut();
    onLogout();
  };

  return (
    <div className="min-h-screen bg-black px-5 py-24 text-slate-100">
      <div className="mx-auto w-[min(1120px,calc(100vw-56px))]">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="instrument-serif-regular text-5xl tracking-tight">Dashboard</h1>
          <button
            type="button"
            onClick={logout}
            className="rounded-lg border border-white/20 px-4 py-2 text-sm text-slate-100 transition hover:bg-white/10"
          >
            Logout
          </button>
        </div>

        {loading ? <p className="text-slate-300">Loading datasets...</p> : null}
        {error ? <p className="text-rose-300">{error}</p> : null}

        {!loading && !error ? (
          <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-6 backdrop-blur-sm">
            <h2 className="text-xl font-semibold text-slate-100">Past Dataset History</h2>
            <p className="mt-2 text-sm text-slate-400">
              {datasets.length ? `${datasets.length} datasets found.` : "No datasets found yet."}
            </p>
          </div>
        ) : null}
      </div>
    </div>
  );
}
