// frontend/src/components/studio/ComparisonResultsTable.jsx

import StatusIndicator from "../ui/StatusIndicator";
import { useCountUp } from "../../hooks/useCountUp";

const CLASSIFICATION_METRICS = [
  { key: "accuracy", label: "Accuracy", higherIsBetter: true },
  { key: "precision", label: "Precision", higherIsBetter: true },
  { key: "recall", label: "Recall", higherIsBetter: true },
  { key: "f1_score", label: "F1 Score", higherIsBetter: true },
];

const CLUSTERING_METRICS = [
  { key: "n_clusters_found", label: "Clusters Found", higherIsBetter: false },
  { key: "silhouette_score", label: "Silhouette", higherIsBetter: true },
];

export default function ComparisonResultsTable({ group }) {
  if (!group?.experiments) return null;

  const metricDefs = group.task_type === "clustering" ? CLUSTERING_METRICS : CLASSIFICATION_METRICS;
  const allDone = group.experiments.every((e) => ["completed", "failed"].includes(e.status));

  const bestValues = {};
  metricDefs.forEach(({ key, higherIsBetter }) => {
    if (!higherIsBetter) { bestValues[key] = null; return; }
    const values = group.experiments
      .filter((e) => e.status === "completed")
      .map((e) => e.result?.metrics?.[key])
      .filter((v) => typeof v === "number");
    bestValues[key] = values.length ? Math.max(...values) : null;
  });

  return (
    <div className="bg-surface border border-line rounded-xl overflow-hidden">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-line">
            <th className="text-left px-4 py-3 text-faint font-medium uppercase text-xs tracking-wide">Algorithm</th>
            {metricDefs.map(({ key, label }) => (
              <th key={key} className="text-right px-4 py-3 text-faint font-medium uppercase text-xs tracking-wide">{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {group.experiments.map((exp) => (
            <tr key={exp.id} className="border-b border-line last:border-0">
              <td className="px-4 py-3 text-ink font-medium">{exp.algorithm_display_name}</td>
              {metricDefs.map(({ key, higherIsBetter }) => {
                if (exp.status !== "completed") {
                  return (
                    <td key={key} className="px-4 py-3 text-right">
                      {exp.status === "failed"
                        ? <span className="text-faint text-xs">—</span>
                        : <StatusIndicator status={exp.status} size={14} />}
                    </td>
                  );
                }
                const value = exp.result?.metrics?.[key];
                const isBest = higherIsBetter && value != null && value === bestValues[key];
                return (
                  <td key={key} className="px-4 py-3 text-right font-mono">
                    <MetricCell value={value} isBest={isBest} isClusterCount={key === "n_clusters_found"} />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      {!allDone && (
        <div className="px-4 py-2 text-xs text-faint border-t border-line">Waiting for all runs to finish...</div>
      )}
    </div>
  );
}

function MetricCell({ value, isBest, isClusterCount }) {
  const target = isClusterCount ? (value ?? 0) : (value ?? 0) * 100;
  const animated = useCountUp(target, 600);
  if (value == null) return <span className="text-faint">—</span>;
  const display = isClusterCount ? Math.round(animated) : `${animated.toFixed(1)}%`;
  return (
    <span className={isBest ? "text-ink font-semibold" : "text-muted"}>
      {isBest && <span className="mr-1">▲</span>}
      {display}
    </span>
  );
}