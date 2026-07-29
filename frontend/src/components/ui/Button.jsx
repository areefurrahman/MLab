// frontend/src/components/ui/Button.jsx

import Spinner from "./Spinner";

const variants = {
  primary: "bg-ink text-canvas hover:bg-ink/90",
  secondary: "bg-transparent border border-line text-ink hover:bg-surface-hover",
  ghost: "bg-transparent text-muted hover:text-ink hover:bg-surface-hover",
  danger: "bg-transparent border border-line text-muted hover:border-red-900/50 hover:text-red-400",
};

export default function Button({
  children,
  isLoading = false,
  variant = "primary",
  className = "",   // extracted separately so it can never be overwritten by ...props
  ...props
}) {
  return (
    <button
      disabled={isLoading || props.disabled}
      className={`inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg
        text-sm font-medium transition-colors cursor-pointer
        disabled:opacity-40 disabled:cursor-not-allowed
        ${variants[variant]} ${className}`}
      {...props}
    >
      {isLoading && <Spinner size="sm" />}
      {children}
    </button>
  );
}