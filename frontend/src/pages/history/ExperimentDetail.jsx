// frontend/src/pages/history/ExperimentDetail.jsx

import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import { historyApi } from "../../api/historyApi";
import ResultsPanel from "../../components/studio/ResultsPanel";
import StatusIndicator from "../../components/ui/StatusIndicator";
import Spinner from "../../components/ui/Spinner";

export default function ExperimentDetail() {
  const { id } = useParams();
  const { data: experiment, isLoading } = useQuery({
    queryKey: ["history", "experiment", id],
    queryFn: () => historyApi.getExperiment(id),
  });

  if (isLoading) return <div className="p-8"><Spinner size="md" /></div>;
  if (!experiment) return <div className="p-8"><p className="text-muted">Not found.</p></div>;

  // Strip private routing keys from parameters for display
  const displayParams = Object.fromEntries(
    Object.entries(experiment.parameters || {}).filter(([k]) => !k.startsWith("_"))
  );

  return (
    <div className="p-8">
      <div className="max-w-3xl mx-auto flex flex-col gap-6">
        <Link to="/history" className="flex items-center gap-2 text-sm text-muted hover:text-ink cursor-pointer w-fit">
          <ArrowLeft size={16} />Back to History
        </Link>

        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-ink">{experiment.algorithm_display_name}</h1>
            <p className="text-muted text-sm mt-1">{experiment.task_type} · #{experiment.id}</p>
          </div>
          <StatusIndicator status={experiment.status} size={16} />
        </div>

        {Object.keys(displayParams).length > 0 && (
          <div className="bg-surface border border-line rounded-xl p-5">
            <p className="text-xs text-faint uppercase tracking-wide mb-3">Hyperparameters</p>
            <div className="flex flex-wrap gap-3">
              {Object.entries(displayParams).map(([k, v]) => (
                <div key={k} className="bg-canvas border border-line rounded-lg px-3 py-1.5">
                  <span className="text-xs text-faint">{k}: </span>
                  <span className="text-xs font-mono text-ink">{String(v)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <ResultsPanel experiment={experiment} />
      </div>
    </div>
  );
}