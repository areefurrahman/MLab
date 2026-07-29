// frontend/src/components/studio/AlgorithmPicker.jsx

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { algorithmsApi } from "../../api/algorithmsApi";
import Spinner from "../ui/Spinner";

export default function AlgorithmPicker({ selected, onSelect, initialAlgorithmName  }) {

  const { data: algorithms, isLoading } = useQuery({
    queryKey: ["algorithms"],
    queryFn: algorithmsApi.list,
  });

  useEffect(() => {
    if (!selected && initialAlgorithmName && algorithms) {
      const match = algorithms.find((a) => a.name === initialAlgorithmName);
      if (match) onSelect(match);
    }
  }, [algorithms, initialAlgorithmName]);

  if (isLoading) return <Spinner size="md" />;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {algorithms.map((algo) => (
        <button
          key={algo.name}
          onClick={() => onSelect(algo)}
          className={`text-left p-4 rounded-xl border transition-colors cursor-pointer
            ${selected?.name === algo.name
              ? "border-ink/40 bg-surface-hover"
              : "border-line bg-surface hover:border-ink/20 hover:bg-surface-hover"}`}
        >
          <p className="font-medium text-ink">{algo.display_name}</p>
          <p className="text-xs text-faint mt-1 uppercase tracking-wide">{algo.task_type}</p>
          <p className="text-xs text-muted mt-2 line-clamp-2">{algo.description}</p>
        </button>
      ))}
    </div>
  );
}