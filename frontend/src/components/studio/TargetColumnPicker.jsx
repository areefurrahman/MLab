// frontend/src/components/studio/TargetColumnPicker.jsx

export default function TargetColumnPicker({ columnsInfo, value, onChange, label = "Target Column (what to predict)" }) {
  if (!columnsInfo) return null;
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-muted">{label}</label>
      <select
        value={value || ""}
        onChange={(e) => onChange(e.target.value)}
        className="px-3 py-2 bg-surface border border-line rounded-lg outline-none text-ink
          cursor-pointer focus:ring-2 focus:ring-ink/20"
      >
        <option value="" disabled>Select a column</option>
        {Object.keys(columnsInfo).map((col) => <option key={col} value={col}>{col}</option>)}
      </select>
    </div>
  );
}