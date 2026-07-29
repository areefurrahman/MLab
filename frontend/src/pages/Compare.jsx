// frontend/src/pages/Compare.jsx

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { comparisonsApi } from "../api/comparisonsApi";
import { useComparisonPolling } from "../hooks/useComparisonPolling";

import MultiAlgorithmPicker from "../components/studio/MultiAlgorithmPicker";
import DatasetSelector from "../components/studio/DatasetSelector";
import TargetColumnPicker from "../components/studio/TargetColumnPicker";
import ComparisonResultsTable from "../components/studio/ComparisonResultsTable";
import Button from "../components/ui/Button";

export default function Compare() {
  const [selectedAlgorithms, setSelectedAlgorithms] = useState([]);
  const [datasetSelection, setDatasetSelection] = useState(null);
  const [targetColumn, setTargetColumn] = useState("");
  const [activeGroupId, setActiveGroupId] = useState(null);

  const { data: group } = useComparisonPolling(activeGroupId);

  const { mutate: runComparison, isLoading: launching } = useMutation({
    mutationFn: comparisonsApi.run,
    onSuccess: (data) => {
      setActiveGroupId(data.id);
      toast.success(`Comparing ${data.experiments.length} algorithms`);
    },
    onError: (error) => {
      const details = error.response?.data?.details;
      toast.error(details?.algorithm_names?.[0] || error.response?.data?.error || "Failed to start comparison");
    },
  });

  const taskType = selectedAlgorithms[0]?.task_type;
  const needsTargetColumn = taskType !== "clustering" && datasetSelection?.source === "uploaded";
  const canRun = selectedAlgorithms.length >= 2 && datasetSelection && (!needsTargetColumn || targetColumn);

  const handleRun = () => {
    runComparison({
      algorithm_names: selectedAlgorithms.map((a) => a.name),
      dataset_source: datasetSelection.source,
      dataset_key: datasetSelection.source === "builtin" ? datasetSelection.dataset.key : undefined,
      dataset_id: datasetSelection.source === "uploaded" ? datasetSelection.dataset.id : undefined,
      target_column: needsTargetColumn ? targetColumn : undefined,
    });
  };

  return (
    <div className="p-8">
      <div className="max-w-5xl mx-auto flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-semibold text-ink">Compare Algorithms</h1>
          <p className="text-muted text-sm mt-1">Run several algorithms on the same data, side by side.</p>
        </div>

        <Section title="1. Choose Algorithms (2-6)">
          <MultiAlgorithmPicker
            selected={selectedAlgorithms}
            onChange={(algos) => { setSelectedAlgorithms(algos); setDatasetSelection(null); setTargetColumn(""); }}
          />
        </Section>

        {taskType && (
          <Section title="2. Choose a Dataset">
            <DatasetSelector taskType={taskType} selected={datasetSelection} onSelect={setDatasetSelection} />
          </Section>
        )}

        {needsTargetColumn && datasetSelection?.dataset?.columns_info && (
          <Section title="2.5 Select Target Column">
            <TargetColumnPicker
              columnsInfo={datasetSelection.dataset.columns_info}
              value={targetColumn}
              onChange={setTargetColumn}
            />
          </Section>
        )}

        {taskType && datasetSelection && (
          <Button onClick={handleRun} isLoading={launching} disabled={!canRun} className="w-fit">
            Run Comparison
          </Button>
        )}

        {group && <ComparisonResultsTable group={group} />}
      </div>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="bg-surface border border-line rounded-xl p-6">
      <h2 className="font-semibold text-ink mb-4">{title}</h2>
      {children}
    </div>
  );
}