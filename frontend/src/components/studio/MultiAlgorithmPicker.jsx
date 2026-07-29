// frontend/src/components/studio/MultiAlgorithmPicker.jsx

import { useQuery } from "@tanstack/react-query";
import { algorithmsApi } from "../../api/algorithmsApi";
import Spinner from "../ui/Spinner";

export default function MultiAlgorithmPicker({ selected, onChange }) {
  const { data: algorithms, isLoading } = useQuery({
    queryKey: ["algorithms"],
    queryFn: algorithmsApi.list,
  });

  if (isLoading) return <Spinner size="md" />;

  // Once one algorithm is picked, lock the rest to the same task_type —
  // mirrors the backend validation, so the user never hits a 422 here.
  const lockedTaskType = selected.length > 0 ? selected[0].task_type : null;
  const maxReached = selected.length >= 6;

  const toggle = (algo) => {
    const exists = selected.find((a) => a.name === algo.name);
    if (exists) {
      onChange(selected.filter((a) => a.name !== algo.name));
    } else {
      if (maxReached) return;
      onChange([...selected, algo]);
    }
  };

  return (
    <div>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {algorithms.map((algo) => {
          const isSelected = !!selected.find((a) => a.name === algo.name);
          const isDisabled = lockedTaskType && algo.task_type !== lockedTaskType && !isSelected;

          return (
            <button
              key={algo.name}
              onClick={() => toggle(algo)}
              disabled={isDisabled}
              className={`text-left p-4 rounded-xl border transition-colors
                ${isDisabled
                  ? "opacity-30 cursor-not-allowed border-line bg-surface"
                  : `cursor-pointer ${isSelected ? "border-ink/40 bg-surface-hover" : "border-line bg-surface hover:border-ink/20 hover:bg-surface-hover"}`}`}
            >
              <div className="flex items-center justify-between">
                <p className="font-medium text-ink">{algo.display_name}</p>
                {isSelected && (
                  <span className="h-4 w-4 rounded-full bg-ink flex items-center justify-center text-[10px] text-canvas">✓</span>
                )}
              </div>
              <p className="text-xs text-faint mt-1 uppercase tracking-wide">{algo.task_type}</p>
            </button>
          );
        })}
      </div>
      <p className="text-xs text-faint mt-3">
        {selected.length === 0 && "Pick 2-6 algorithms to compare"}
        {selected.length === 1 && "Pick at least 1 more"}
        {selected.length >= 2 && `${selected.length} selected`}
      </p>
    </div>
  );
}