// frontend/src/pages/history/ComparisonDetail.jsx

import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import { historyApi } from "../../api/historyApi";
import ComparisonResultsTable from "../../components/studio/ComparisonResultsTable";
import StatusIndicator from "../../components/ui/StatusIndicator";
import Spinner from "../../components/ui/Spinner";

export default function ComparisonDetail() {
  const { id } = useParams();
  const { data: group, isLoading } = useQuery({
    queryKey: ["history", "comparison", id],
    queryFn: () => historyApi.getComparison(id),
  });

  if (isLoading) return <div className="p-8"><Spinner size="md" /></div>;
  if (!group) return <div className="p-8"><p className="text-muted">Not found.</p></div>;

  const allDone = group.experiments?.every((e) => ["completed", "failed"].includes(e.status));

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto flex flex-col gap-6">
        <Link to="/history" className="flex items-center gap-2 text-sm text-muted hover:text-ink cursor-pointer w-fit">
          <ArrowLeft size={16} />Back to History
        </Link>

        <div>
          <h1 className="text-2xl font-semibold text-ink">Algorithm Comparison</h1>
          <p className="text-muted text-sm mt-1">{group.dataset_label} · {group.task_type}</p>
        </div>

        <ComparisonResultsTable group={group} />

        <p className="text-xs text-faint font-mono">
          {group.experiments?.length} algorithms · created {new Date(group.created_at).toLocaleString()}
        </p>
      </div>
    </div>
  );
}