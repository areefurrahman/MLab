// frontend/src/components/studio/ParamInput.jsx

export default function ParamInput({ paramDef, value, onChange }) {
  const { name, label, type, min, max, step, options, description } = paramDef;

  const handleChange = (e) => {
    let val = e.target.value;
    if (type === "int") val = parseInt(val, 10);
    if (type === "float") val = parseFloat(val);
    if (type === "bool") val = e.target.checked;
    onChange(name, val);
  };

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-muted">{label}</label>

      {(type === "int" || type === "float") && (
        <div className="flex items-center gap-3">
          <input
            type="range" min={min} max={max} step={step} value={value} onChange={handleChange}
            className="flex-1 accent-ink cursor-pointer"
          />
          <span className="text-sm font-mono text-ink w-14 text-right">{value}</span>
        </div>
      )}

      {type === "select" && (
        <select
          value={value} onChange={handleChange}
          className="px-3 py-2 bg-surface border border-line rounded-lg outline-none text-ink
            cursor-pointer focus:ring-2 focus:ring-ink/20"
        >
          {options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
        </select>
      )}

      {type === "bool" && (
        <input type="checkbox" checked={value} onChange={handleChange} className="h-4 w-4 accent-ink cursor-pointer" />
      )}

      {description && <p className="text-xs text-faint">{description}</p>}
    </div>
  );
}