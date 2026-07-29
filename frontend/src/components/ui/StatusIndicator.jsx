// frontend/src/components/ui/StatusIndicator.jsx
// Fully monochrome — shape/icon carries meaning, no semantic color

import { CircleDashed, Loader2, CheckCircle2, XCircle } from "lucide-react";

const STATUS_CONFIG = {
  pending:   { icon: CircleDashed, label: "Queued" },
  running:   { icon: Loader2,      label: "Running", spin: true },
  completed: { icon: CheckCircle2, label: "Completed" },
  failed:    { icon: XCircle,      label: "Failed" },
};

export default function StatusIndicator({ status, size = 16 }) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.pending;
  const Icon = config.icon;

  return (
    <span className="inline-flex items-center gap-1.5 text-sm text-muted">
      <Icon size={size} className={config.spin ? "animate-spin" : ""} />
      {config.label}
    </span>
  );
}