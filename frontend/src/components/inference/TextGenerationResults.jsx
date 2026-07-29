// frontend/src/components/inference/TextGenerationResults.jsx

import { useState } from "react";
import { Copy, Check } from "lucide-react";

export default function TextGenerationResults({ output }) {
  const [copied, setCopied] = useState(false);

  if (!output) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(output.full_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="bg-canvas border border-line rounded-lg p-4">
        <span className="text-muted text-sm font-mono">{output.prompt}</span>
        <span className="text-ink text-sm font-mono">{output.generated_text}</span>
      </div>

      <div className="flex items-center justify-between">
        <p className="text-xs text-faint font-mono">
          ~{output.generated_tokens} tokens generated
        </p>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-line
            text-sm text-muted hover:text-ink hover:bg-surface-hover transition-colors cursor-pointer"
        >
          {copied ? <Check size={14} /> : <Copy size={14} />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
    </div>
  );
}