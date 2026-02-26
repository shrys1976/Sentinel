import { useEffect, useMemo, useState } from "react";

import BasicStatsCard from "../components/cards/BasicStatsCard";
import CategoricalCard from "../components/cards/CategoricalCard";
import ImbalanceCard from "../components/cards/ImbalanceCard";
import LeakageCard from "../components/cards/LeakageCard";
import MissingCard from "../components/cards/MissingCard";
import OutlierCard from "../components/cards/OutlierCard";
import IssuesPanel from "../components/report/IssuesPanel";
import PlotsGallery from "../components/report/PlotsGallery";
import ReportHeader from "../components/report/ReportHeader";
import SentinelScore from "../components/report/SentinelScore";
import type { ReportViewData } from "../components/report/types";
import DatasetSummary from "../components/sidebar/DatasetSummary";
import FailedBanner from "../components/sidebar/FailedBanner";
import QuickFacts from "../components/sidebar/QuickFacts";
import { deleteDataset } from "../services/datasetApi";
import { getReportView } from "../services/reportApi";

type ReportProps = {
  datasetId: string;
  onBackToDashboard: () => void;
  onDeleted: () => void;
};

function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      <div className="h-28 animate-pulse rounded-2xl bg-white/10" />
      <div className="h-28 animate-pulse rounded-2xl bg-white/10" />
      <div className="h-36 animate-pulse rounded-2xl bg-white/10" />
      <div className="h-48 animate-pulse rounded-2xl bg-white/10" />
    </div>
  );
}

function buildQuickFacts(data: ReportViewData) {
  const facts: string[] = [];

  if (data.sentinel_score >= 85) facts.push("Overall dataset health appears strong.");
  else if (data.sentinel_score >= 60) facts.push("Dataset has moderate risk and needs targeted cleanup.");
  else facts.push("Dataset has high risk and requires remediation before training.");

  if (data.top_issues.length) facts.push(`Top issue: ${data.top_issues[0]}`);
  if (data.warnings.length) facts.push(`Warning: ${data.warnings[0]}`);

  if (data.failed_analyzers.length > 0) {
    facts.push(`${data.failed_analyzers.length} analyzer(s) could not complete.`);
  }
  if (data.modeling_risk) facts.push(`Modeling risk: ${data.modeling_risk}`);
  if (data.recommended_actions?.length) facts.push(`Action: ${data.recommended_actions[0]}`);

  return facts.slice(0, 4);
}

function readSection(
  sections: Record<string, Record<string, unknown>>,
  key: string
): Record<string, unknown> {
  const value = sections[key];
  if (!value || typeof value !== "object") return { skipped: true, reason: "missing_section" };
  return value;
}

export default function Report({ datasetId, onBackToDashboard, onDeleted }: ReportProps) {
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ReportViewData | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getReportView(datasetId)
      .then((payload) => {
        setData(payload as ReportViewData);
      })
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : "Unable to load report.";
        if (message.includes("404")) {
          setError("Report unavailable");
        } else {
          setError("Analysis failed. Please retry upload.");
        }
      })
      .finally(() => setLoading(false));
  }, [datasetId]);

  const onDelete = async () => {
    const ok = window.confirm("Delete this dataset and all associated reports?");
    if (!ok) return;

    setDeleting(true);
    try {
      await deleteDataset(datasetId);
      onDeleted();
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Delete failed";
      setError(message);
    } finally {
      setDeleting(false);
    }
  };

  const quickFacts = useMemo(() => (data ? buildQuickFacts(data) : []), [data]);

  return (
    <div className="min-h-screen bg-black px-5 pb-12 pt-24 text-slate-100">
      <div className="mx-auto w-[min(1220px,calc(100vw-56px))]">
        {loading ? <LoadingSkeleton /> : null}

        {!loading && error ? (
          <section className="rounded-2xl border border-rose-300/30 bg-rose-500/10 p-6">
            <h1 className="instrument-serif-regular text-3xl text-rose-100">Report Error</h1>
            <p className="mt-2 text-sm text-rose-100/90">{error}</p>
            <button
              type="button"
              onClick={onBackToDashboard}
              className="mt-4 rounded-lg border border-rose-200/30 px-4 py-2 text-sm text-rose-100 transition hover:bg-rose-500/15"
            >
              Back to Dashboard
            </button>
          </section>
        ) : null}

        {!loading && !error && data ? (
          <div className="space-y-6">
            <ReportHeader
              dataset={data.dataset}
              onBack={onBackToDashboard}
              onDelete={onDelete}
              deleting={deleting}
            />

            <SentinelScore score={data.sentinel_score} />
            <IssuesPanel topIssues={data.top_issues} warnings={data.warnings} />

            <section className="grid gap-6 md:grid-cols-12">
              <div className="space-y-4 md:col-span-8">
                <BasicStatsCard data={readSection(data.sections, "basic_stats")} />
                <MissingCard data={readSection(data.sections, "missing")} />
                <LeakageCard data={readSection(data.sections, "leakage")} />
                <OutlierCard data={readSection(data.sections, "outliers")} />
                <CategoricalCard data={readSection(data.sections, "categorical")} />
                <ImbalanceCard data={readSection(data.sections, "imbalance")} />
              </div>

              <aside className="space-y-4 md:col-span-4 md:sticky md:top-24 md:self-start">
                <DatasetSummary
                  score={data.sentinel_score}
                  difficulty={data.dataset_difficulty}
                  modelingRisk={data.modeling_risk}
                  rows={data.dataset.rows}
                  columns={data.dataset.columns}
                  numericColumns={Number(readSection(data.sections, "basic_stats")["numeric_columns"] ?? 0)}
                  categoricalColumns={Number(
                    readSection(data.sections, "basic_stats")["categorical_columns"] ?? 0
                  )}
                />
                <QuickFacts facts={quickFacts} />
                <FailedBanner failedAnalyzers={data.failed_analyzers} />
              </aside>
            </section>

            <PlotsGallery datasetId={datasetId} availablePlots={data.available_plots} />
          </div>
        ) : null}
      </div>
    </div>
  );
}
