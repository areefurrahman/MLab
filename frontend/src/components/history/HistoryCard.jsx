// frontend/src/components/history/HistoryCard.jsx

import { Link } from "react-router-dom";
import { FlaskConical, GitCompare, Brain, Clock } from "lucide-react";
import StatusIndicator from "../ui/StatusIndicator";

const TYPE_CONFIG = {
  experiment: { icon: FlaskConical, label: "Experiment" },
  comparison: { icon: GitCompare, label: "Comparison" },
  inference:  { icon: Brain,       label: "Inference" },
};

export default function HistoryCard({ item }) {
  const config = TYPE_CONFIG[item.type] || TYPE_CONFIG.experiment;
  const Icon = config.icon;

  return (
    <Link
      to={item.detail_url}
      className="block bg-surface border border-line rounded-xl p-5
        hover:border-ink/20 hover:bg-surface-hover transition-colors cursor-pointer"
    >
      <div className="flex items-start justify-between gap-4">

        {/* Left — icon + title + subtitle */}
        <div className="flex items-start gap-3 min-w-0">
          <div className="mt-0.5 shrink-0">
            <Icon size={16} className="text-faint" />
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-ink truncate">{item.title}</p>
            <p className="text-xs text-faint mt-0.5">{item.subtitle}</p>
          </div>
        </div>

        {/* Right — status + time */}
        <div className="flex flex-col items-end gap-1 shrink-0">
          <StatusIndicator status={item.status} size={14} />
          <p className="text-xs text-faint font-mono">
            {formatRelativeTime(item.created_at)}
          </p>
        </div>
      </div>

      {/* Summary row */}
      <SummaryRow item={item} />
    </Link>
  );
}

function SummaryRow({ item }) {
  const s = item.summary;

  if (item.type === "experiment") {
    return (
      <div className="mt-3 flex items-center gap-4 text-xs font-mono text-muted">
        {s.accuracy != null && <span>accuracy {s.accuracy}%</span>}
        {s.rule_count != null && <span>{s.rule_count} rules mined</span>}
        {item.duration_seconds != null && <span>{item.duration_seconds}s</span>}
      </div>
    );
  }

  if (item.type === "comparison") {
    return (
      <div className="mt-3 flex items-center gap-4 text-xs font-mono text-muted">
        <span>{s.algorithm_count} algorithms</span>
        <span>{s.dataset}</span>
      </div>
    );
  }

  if (item.type === "inference") {
    const detail = s.entity_count != null ? `${s.entity_count} entities`
      : s.predicted_label ? `${s.predicted_label} · ${s.confidence}%`
      : s.question ? `"${s.question.slice(0, 50)}${s.question.length > 50 ? "…" : ""}"`
      : s.prompt_preview ? `"${s.prompt_preview}"`
      : "";
    return (
      <div className="mt-3 text-xs font-mono text-muted">
        {detail}
      </div>
    );
  }

  return null;
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