// frontend/src/components/studio/DatasetSelector.jsx

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { datasetsApi } from "../../api/datasetsApi";
import Spinner from "../ui/Spinner";

export default function DatasetSelector({ taskType, onSelect, selected }) {
  const [tab, setTab] = useState("builtin");
  const queryClient = useQueryClient();

  const { data: builtinDatasets, isLoading: loadingBuiltin } = useQuery({
    queryKey: ["datasets", "builtin"],
    queryFn: datasetsApi.listBuiltin,
  });

  const { data: myDatasets, isLoading: loadingMine } = useQuery({
    queryKey: ["datasets", "mine"],
    queryFn: datasetsApi.listMine,
    enabled: tab === "upload",
  });

  const { mutate: uploadFile, isLoading: uploading } = useMutation({
    mutationFn: ({ file, name }) => datasetsApi.upload(file, name),
    onSuccess: (dataset) => {
      toast.success(`Uploaded "${dataset.name}" (${dataset.row_count} rows)`);
      queryClient.invalidateQueries({ queryKey: ["datasets", "mine"] });
      onSelect({ source: "uploaded", dataset });
    },
    onError: (error) => {
      const details = error.response?.data?.details;
      toast.error(details?.file?.[0] || error.response?.data?.error || "Upload failed");
    },
  });

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) uploadFile({ file, name: file.name });
  };

  const filteredBuiltin = builtinDatasets?.filter((d) => d.task_type === taskType);

  const tabClass = (active) =>
    `px-3 py-1.5 rounded-lg text-sm font-medium transition-colors cursor-pointer
    ${active ? "bg-ink text-canvas" : "bg-surface border border-line text-muted hover:text-ink"}`;

  const cardClass = (active) =>
    `text-left p-3 rounded-lg border text-sm cursor-pointer transition-colors
    ${active ? "border-ink/40 bg-surface-hover" : "border-line bg-surface hover:border-ink/20"}`;

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <button onClick={() => setTab("builtin")} className={tabClass(tab === "builtin")}>
          Built-in Datasets
        </button>
        <button onClick={() => setTab("upload")} className={tabClass(tab === "upload")}>
          Upload CSV
        </button>
      </div>

      {tab === "builtin" && (
        loadingBuiltin ? <Spinner size="sm" /> : (
          <div className="grid grid-cols-2 gap-2">
            {filteredBuiltin?.length === 0 && (
              <p className="text-sm text-faint col-span-2">No built-in datasets match this task type.</p>
            )}
            {filteredBuiltin?.map((ds) => (
              <button
                key={ds.key}
                onClick={() => onSelect({ source: "builtin", dataset: ds })}
                className={cardClass(selected?.dataset?.key === ds.key)}
              >
                <p className="font-medium text-ink">{ds.name}</p>
                <p className="text-xs text-faint font-mono">{ds.rows} rows · {ds.features} features</p>
              </button>
            ))}
          </div>
        )
      )}

      {tab === "upload" && (
        <div>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={uploading}
            className="block w-full text-sm text-muted cursor-pointer
              file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border file:border-line
              file:bg-surface file:text-ink file:cursor-pointer hover:file:bg-surface-hover"
          />
          {uploading && <p className="text-sm text-faint mt-2">Uploading...</p>}
          <p className="text-xs text-faint mt-2">Max 1000 rows, .csv only</p>

          {!loadingMine && myDatasets?.length > 0 && (
            <div className="mt-4 flex flex-col gap-2">
              <p className="text-sm font-medium text-muted">Your datasets</p>
              {myDatasets.map((ds) => (
                <button
                  key={ds.id}
                  onClick={() => onSelect({ source: "uploaded", dataset: ds })}
                  className={cardClass(selected?.dataset?.id === ds.id)}
                >
                  <p className="font-medium text-ink">{ds.name}</p>
                  <p className="text-xs text-faint font-mono">{ds.row_count} rows</p>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}