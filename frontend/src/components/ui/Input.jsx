// frontend/src/components/ui/Input.jsx

export default function Input({ label, error, ...props }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <label className="text-sm font-medium text-muted">{label}</label>}
      <input
        className={`px-3 py-2 bg-surface border rounded-lg outline-none text-ink placeholder:text-faint
          transition-colors focus:ring-2 focus:ring-ink/20
          ${error ? "border-red-900/50" : "border-line"}`}
        {...props}
      />
      {error && <p className="text-sm text-red-400">{error}</p>}
    </div>
  );
}