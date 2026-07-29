// frontend/src/pages/Dashboard.jsx

import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { FlaskConical, GitCompare, Brain } from "lucide-react";
import useAuthStore from "../store/authStore";
import { historyApi } from "../api/historyApi";
import Spinner from "../components/ui/Spinner";

export default function Dashboard() {
  const { user } = useAuthStore();

  const { data: history = [], isLoading } = useQuery({
    queryKey: ["history"],
    queryFn: () => historyApi.list(),
  });

  const counts = history?.reduce(
    (acc, item) => {
      acc[item.type] = (acc[item.type] || 0) + 1;
      return acc;
    },
    { experiment: 0, comparison: 0, inference: 0 }
  ) ?? {};

  const completedCount = history?.filter((i) => i.status === "completed").length ?? 0;

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto flex flex-col gap-8">

        <div>
          <h1 className="text-2xl font-semibold text-ink">Welcome back, {user?.username}</h1>
          <p className="text-muted text-sm mt-1">Here's what you've been building.</p>
        </div>

        {/* Stats */}
        {isLoading ? <Spinner size="sm" /> : (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <StatCard label="Total Runs" value={history?.length ?? 0} />
            <StatCard label="Completed" value={completedCount} />
            <StatCard label="Experiments" value={counts.experiment} />
            <StatCard label="Inference Runs" value={counts.inference} />
          </div>
        )}

        {/* Quick actions */}
        <div className="grid grid-cols-3 gap-3">
          <QuickLink to="/studio" icon={FlaskConical} label="New Experiment"
            desc="Run an ML algorithm on a dataset" />
          <QuickLink to="/compare" icon={GitCompare} label="Compare Algorithms"
            desc="Run multiple algorithms side by side" />
          <QuickLink to="/infer/ner" icon={Brain} label="Run Inference"
            desc="NER, Text Generation, Voice QA, CNN" />
        </div>

        {/* Recent history */}
        {history && history.length > 0 && (
          <div>
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm font-medium text-muted">Recent Activity</p>
              <Link to="/history" className="text-xs text-muted hover:text-ink cursor-pointer">
                View all →
              </Link>
            </div>
            <div className="flex flex-col gap-2">
              {history.slice(0, 5).map((item) => (
                <Link
                  key={`${item.type}-${item.id}`}
                  to={item.detail_url}
                  className="flex items-center justify-between px-4 py-3 rounded-lg
                    bg-surface border border-line hover:bg-surface-hover transition-colors cursor-pointer"
                >
                  <div>
                    <p className="text-sm text-ink">{item.title}</p>
                    <p className="text-xs text-faint">{item.subtitle}</p>
                  </div>
                  <p className="text-xs text-faint font-mono shrink-0 ml-4">
                    {formatRelativeTime(item.created_at)}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="bg-surface border border-line rounded-xl p-4 text-center">
      <p className="text-2xl font-semibold text-ink font-mono">{value}</p>
      <p className="text-xs text-faint mt-1">{label}</p>
    </div>
  );
}

function QuickLink({ to, icon: Icon, label, desc }) {
  return (
    <Link to={to}
      className="block bg-surface border border-line rounded-xl p-4
        hover:border-ink/20 hover:bg-surface-hover transition-colors cursor-pointer">
      <Icon size={18} className="text-faint mb-3" />
      <p className="text-sm font-medium text-ink">{label}</p>
      <p className="text-xs text-muted mt-1">{desc}</p>
    </Link>
  );
}

function formatRelativeTime(isoString) {
  const diff = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}