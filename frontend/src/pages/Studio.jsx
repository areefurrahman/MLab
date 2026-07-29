// frontend/src/pages/Studio.jsx

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { experimentsApi } from "../api/experimentsApi";
import { useExperimentPolling } from "../hooks/useExperimentPolling";

import AlgorithmPicker from "../components/studio/AlgorithmPicker";
import DatasetSelector from "../components/studio/DatasetSelector";
import HyperparamForm from "../components/studio/HyperparamForm";
import TargetColumnPicker from "../components/studio/TargetColumnPicker";
import ResultsPanel from "../components/studio/ResultsPanel";
import Button from "../components/ui/Button";

import { useSearchParams } from "react-router-dom";

export default function Studio() {

    const [searchParams] = useSearchParams();
    const initialAlgorithmName = searchParams.get("algorithm");

    const [algorithm, setAlgorithm] = useState(null);
    const [datasetSelection, setDatasetSelection] = useState(null);
    const [params, setParams] = useState({});
    const [targetColumn, setTargetColumn] = useState("");
    const [activeExperimentId, setActiveExperimentId] = useState(null);


    // Polls automatically once an experiment is running
    const { data: experiment } = useExperimentPolling(activeExperimentId);

    const { mutate: runExperiment, isLoading: launching } = useMutation({
        mutationFn: experimentsApi.run,
        onSuccess: (data) => {
            setActiveExperimentId(data.id);
            toast.success("Experiment queued");
        },
        onError: (error) => {
            toast.error(error.response?.data?.error || "Failed to start experiment");
        },
    });



    const [itemsColumn, setItemsColumn] = useState("");

    const needsTargetColumn = algorithm?.task_type !== "clustering" && algorithm?.task_type !== "association_rules"
        && datasetSelection?.source === "uploaded";
    const needsItemsColumn = algorithm?.task_type === "association_rules" && datasetSelection?.source === "uploaded";

    const canRun =
        algorithm && datasetSelection &&
        (!needsTargetColumn || targetColumn) &&
        (!needsItemsColumn || itemsColumn);

    const handleRun = () => {
        runExperiment({
            algorithm_name: algorithm.name,
            dataset_source: datasetSelection.source,
            dataset_key: datasetSelection.source === "builtin" ? datasetSelection.dataset.key : undefined,
            dataset_id: datasetSelection.source === "uploaded" ? datasetSelection.dataset.id : undefined,
            target_column: needsTargetColumn ? targetColumn : undefined,
            items_column: needsItemsColumn ? itemsColumn : undefined,
            parameters: params,
        });
    };






    return (
        <div className="p-8">
            <div className="max-w-5xl mx-auto flex flex-col gap-6">
                <h1 className="text-2xl font-semibold text-ink">Experiment Studio</h1>

                {/* Step 1 — Algorithm */}
                <Section title="1. Choose an Algorithm">
                    <AlgorithmPicker
                        selected={algorithm}
                        initialAlgorithmName={initialAlgorithmName}
                        onSelect={(a) => {
                            setAlgorithm(a);
                            setDatasetSelection(null);
                            setTargetColumn("");
                        }}
                    />
                </Section>

                {/* Step 2 — Dataset (only after algorithm chosen) */}
                {algorithm && (
                    <Section title="2. Choose a Dataset">
                        <DatasetSelector
                            taskType={algorithm.task_type}
                            selected={datasetSelection}
                            onSelect={setDatasetSelection}
                        />
                    </Section>
                )}

                {/* Step 2.5 — Target column, only for uploaded classification data */}
                {(needsTargetColumn || needsItemsColumn) && datasetSelection?.dataset?.columns_info && (
                    <Section title="2.5 Configure Columns">
                        {needsTargetColumn && (
                            <TargetColumnPicker
                                columnsInfo={datasetSelection.dataset.columns_info}
                                value={targetColumn}
                                onChange={setTargetColumn}
                            />
                        )}
                        {needsItemsColumn && (
                            <TargetColumnPicker
                                label="Items Column (comma-separated items per transaction)"
                                columnsInfo={datasetSelection.dataset.columns_info}
                                value={itemsColumn}
                                onChange={setItemsColumn}
                            />
                        )}
                    </Section>
                )}

                {/* Step 3 — Hyperparameters */}
                {algorithm && (
                    <Section title="3. Configure Hyperparameters">
                        <HyperparamForm algorithm={algorithm} onChange={setParams} />
                    </Section>
                )}

                {/* Step 4 — Run */}
                {algorithm && datasetSelection && (
                    <Button onClick={handleRun} isLoading={launching} disabled={!canRun} className="w-fit">
                        Run Experiment
                    </Button>
                )}

                {/* Results */}
                {experiment && <ResultsPanel experiment={experiment} />}
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