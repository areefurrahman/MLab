// frontend/src/pages/History.jsx

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { historyApi } from "../api/historyApi";
import HistoryCard from "../components/history/HistoryCard";
import Spinner from "../components/ui/Spinner";

const TYPE_FILTERS = [
    { value: null, label: "All" },
    { value: "experiment", label: "Experiments" },
    { value: "comparison", label: "Comparisons" },
    { value: "inference", label: "Inference" },
];

const STATUS_FILTERS = [
    { value: null, label: "Any Status" },
    { value: "completed", label: "Completed" },
    { value: "failed", label: "Failed" },
    { value: "running", label: "Running" },
];

export default function History() {



    const [typeFilter, setTypeFilter] = useState(null);
    const [statusFilter, setStatusFilter] = useState(null);


    const { data: items = [], isLoading, isError } = useQuery({
        queryKey: ["history", typeFilter, statusFilter],
        queryFn: () => historyApi.list({ type: typeFilter, status: statusFilter }),
    });

    const filterBtnClass = (active) =>
        `px-3 py-1.5 rounded-lg text-sm font-medium transition-colors cursor-pointer
    ${active ? "bg-ink text-canvas" : "bg-surface border border-line text-muted hover:text-ink"}`;

    return (
        <div className="p-8">
            <div className="max-w-4xl mx-auto flex flex-col gap-6">

                <div>
                    <h1 className="text-2xl font-semibold text-ink">History</h1>
                    <p className="text-muted text-sm mt-1">Every experiment, comparison, and inference run you've made.</p>
                </div>

                {/* Filters */}
                <div className="flex flex-wrap items-center gap-4">
                    <div className="flex gap-2 flex-wrap">
                        {TYPE_FILTERS.map((f) => (
                            <button
                                key={String(f.value)}
                                onClick={() => setTypeFilter(f.value)}
                                className={filterBtnClass(typeFilter === f.value)}
                            >
                                {f.label}
                            </button>
                        ))}
                    </div>
                    <div className="h-4 w-px bg-line" />
                    <div className="flex gap-2 flex-wrap">
                        {STATUS_FILTERS.map((f) => (
                            <button
                                key={String(f.value)}
                                onClick={() => setStatusFilter(f.value)}
                                className={filterBtnClass(statusFilter === f.value)}
                            >
                                {f.label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Feed */}
                {isLoading ? (
                    <Spinner size="md" />
                ) : isError ? (
                    <div className="bg-surface border border-line rounded-xl p-12 text-center">
                        <p className="text-muted text-sm">Failed to load history — check the backend is running.</p>
                    </div>
                ) : items.length === 0 ? (
                    <div className="bg-surface border border-line rounded-xl p-12 text-center">
                        <p className="text-muted text-sm">
                            Nothing here yet — run an experiment or inference task to see it here.
                        </p>
                    </div>
                ) : (
                    <div className="flex flex-col gap-3">
                        {items.map((item) => (
                            <HistoryCard key={`${item.type}-${item.id}`} item={item} />
                        ))}
                    </div>
                )}

            </div>
        </div>
    );
}