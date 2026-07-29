// frontend/src/components/inference/InferenceInputField.jsx

export default function InferenceInputField({ fieldDef, value, onChange }) {
  const { name, label, type, placeholder, description, min, max, step, options } = fieldDef;

  const handleChange = (e) => {
    let val = e.target.value;
    if (type === "int") val = parseInt(val, 10);
    if (type === "float") val = parseFloat(val);
    onChange(name, val);
  };

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-muted">{label}</label>

      {(type === "textarea") && (
        <textarea
          value={value || ""}
          onChange={(e) => onChange(name, e.target.value)}
          placeholder={placeholder}
          rows={4}
          className="px-3 py-2 bg-surface border border-line rounded-lg outline-none
            text-ink placeholder:text-faint resize-none focus:ring-2 focus:ring-ink/20
            text-sm font-mono"
        />
      )}

      {type === "text" && (
        <input
          type="text"
          value={value || ""}
          onChange={(e) => onChange(name, e.target.value)}
          placeholder={placeholder}
          className="px-3 py-2 bg-surface border border-line rounded-lg outline-none
            text-ink placeholder:text-faint focus:ring-2 focus:ring-ink/20"
        />
      )}

      {(type === "int" || type === "float") && (
        <div className="flex items-center gap-3">
          <input
            type="range" min={min} max={max} step={step}
            value={value ?? fieldDef.default}
            onChange={handleChange}
            className="flex-1 accent-ink cursor-pointer"
          />
          <span className="text-sm font-mono text-ink w-14 text-right">{value ?? fieldDef.default}</span>
        </div>
      )}

      {type === "select" && (
        <select
          value={value ?? fieldDef.default}
          onChange={handleChange}
          className="px-3 py-2 bg-surface border border-line rounded-lg outline-none
            text-ink cursor-pointer focus:ring-2 focus:ring-ink/20"
        >
          {options?.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
        </select>
      )}

      {description && <p className="text-xs text-faint">{description}</p>}
    </div>
  );
}