// frontend/src/components/studio/ResultsPanel.jsx

import StatusIndicator from "../ui/StatusIndicator";
import { useCountUp } from "../../hooks/useCountUp";
import RulesTable from "./RulesTable";

export default function ResultsPanel({ experiment }) {
  if (!experiment) return null;

  const isActive = experiment.status === "pending" || experiment.status === "running";

  if (isActive) {
    return (
      <div className="tracing-border bg-surface">
        <div className="px-6 py-5 flex items-center justify-between">
          <StatusIndicator status={experiment.status} size={18} />
          <span className="text-xs text-faint font-mono">#{experiment.id}</span>
        </div>
      </div>
    );
  }

  if (experiment.status === "failed") {
    return (
      <div className="bg-surface border border-line rounded-xl p-6">
        <StatusIndicator status="failed" size={18} />
        <p className="text-sm text-muted mt-2 font-mono">{experiment.error_message}</p>
      </div>
    );
  }

  if (experiment.task_type === "association_rules") {
  return (
    <div className="bg-surface border border-line rounded-xl p-6">
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-semibold text-ink">Association Rules</h3>
        <StatusIndicator status="completed" size={16} />
      </div>
      <RulesTable result={experiment.result} />
    </div>
  );
}

  const { confusion_matrix, ...metrics } = experiment.result?.metrics || {};
  const targetNames = experiment.result?.target_names;

  return (
    <div className="bg-surface border border-line rounded-xl p-6">
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-semibold text-ink">Results</h3>
        <StatusIndicator status="completed" size={16} />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {Object.entries(metrics).map(([key, val]) =>
          typeof val === "number" ? (
            <MetricCard key={key} label={key.replace("_", " ")} value={val} />
          ) : null
        )}
      </div>

      {confusion_matrix && <ConfusionMatrix matrix={confusion_matrix} labels={targetNames} />}

      <p className="text-xs text-faint font-mono mt-4">
        train {experiment.result?.train_size} · test {experiment.result?.test_size} · {experiment.duration_seconds}s
      </p>
    </div>
  );
}

function MetricCard({ label, value }) {
  const animated = useCountUp(value * 100, 700);
  return (
    <div className="bg-canvas border border-line rounded-lg p-3 text-center">
      <p className="text-[11px] text-faint uppercase tracking-wide">{label}</p>
      <p className="text-xl font-semibold text-ink font-mono mt-1">{animated.toFixed(1)}%</p>
    </div>
  );
}

function ConfusionMatrix({ matrix, labels }) {
  return (
    <table className="text-sm border-collapse font-mono">
      <tbody>
        {matrix.map((row, i) => (
          <tr key={i}>
            {row.map((cell, j) => (
              <td
                key={j}
                className={`border border-line px-3 py-2 text-center
                  ${i === j ? "bg-surface-hover text-ink font-semibold" : "text-muted"}`}
              >
                {cell}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}