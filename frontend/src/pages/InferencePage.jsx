// frontend/src/pages/InferencePage.jsx

import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { inferenceApi } from "../api/inferenceApi";
import { useInferencePolling } from "../hooks/useInferencePolling";

import InferenceInputField from "../components/inference/InferenceInputField";
import NERResults from "../components/inference/NERResults";
import TextGenerationResults from "../components/inference/TextGenerationResults";
import StatusIndicator from "../components/ui/StatusIndicator";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

import VoiceQAResults from "../components/inference/VoiceQAResults";
import CNNResults from "../components/inference/CNNResults";

export default function InferencePage() {
  const { taskName } = useParams();
  const [inputValues, setInputValues] = useState({});
  const [activeRunId, setActiveRunId] = useState(null);

  const { data: tasks, isLoading: loadingTasks } = useQuery({
    queryKey: ["inference", "tasks"],
    queryFn: inferenceApi.listTasks,
  });

  const taskDef = tasks?.find((t) => t.name === taskName);

  // Build initial input state from schema defaults when task loads
  useEffect(() => {
    if (!taskDef) return;
    const defaults = {};
    taskDef.input_schema.forEach((field) => {
      if (field.default !== null && field.default !== undefined) {
        defaults[field.name] = field.default;
      }
    });
    setInputValues(defaults);
    setActiveRunId(null);
  }, [taskName, taskDef?.name]);

  const { data: run } = useInferencePolling(activeRunId);

  const { mutate: runInference, isLoading: launching } = useMutation({
    mutationFn: () => inferenceApi.run(taskName, inputValues),
    onSuccess: (data) => {
      setActiveRunId(data.id);
      toast.success("Running...");
    },
    onError: (error) => {
      toast.error(error.response?.data?.error || "Failed to start");
    },
  });

  const handleFieldChange = (name, value) => {
    setInputValues((prev) => ({ ...prev, [name]: value }));
  };

  const requiredFields = taskDef?.input_schema.filter((f) => f.required) || [];
  const canRun = requiredFields.every((f) => {
    const val = inputValues[f.name];
    return val !== undefined && val !== null && val !== "";
  });

  if (loadingTasks) return <div className="p-8"><Spinner size="md" /></div>;

  if (!taskDef) {
    return (
      <div className="p-8">
        <p className="text-muted">Inference task "{taskName}" not found.</p>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="max-w-3xl mx-auto flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-semibold text-ink">{taskDef.display_name}</h1>
          <p className="text-muted text-sm mt-1">{taskDef.description}</p>
        </div>

        <div className="bg-surface border border-line rounded-xl p-6 flex flex-col gap-5">
          {taskDef.input_schema.map((field) => (
            <InferenceInputField
              key={field.name}
              fieldDef={field}
              value={inputValues[field.name]}
              onChange={handleFieldChange}
            />
          ))}
          <Button onClick={() => runInference()} isLoading={launching} disabled={!canRun} className="w-fit mt-2">
            Run
          </Button>
        </div>

        {run && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-semibold text-ink">Output</h3>
              <StatusIndicator status={run.status} size={16} />
            </div>

            {(run.status === "pending" || run.status === "running") && (
              <div className="flex items-center gap-3">
                <Spinner size="sm" />
                <p className="text-sm text-muted">
                  {run.status === "pending" ? "Queued..." : "Running inference..."}
                </p>
              </div>
            )}

            {run.status === "failed" && (
              <p className="text-sm text-muted font-mono">{run.error_message}</p>
            )}

            {run.status === "completed" && (
              <InferenceOutput taskName={taskName} output={run.output_data} />
            )}

            {run.duration_seconds && run.status === "completed" && (
              <p className="text-xs text-faint font-mono mt-4">{run.duration_seconds}s</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// Routes completed results to the correct display component
function InferenceOutput({ taskName, output }) {
  if (taskName === "ner") return <NERResults output={output} />;
  if (taskName === "text_generation") return <TextGenerationResults output={output} />;
  if (taskName === "voice_qa") return <VoiceQAResults output={output} />;
  if (taskName === "cnn_gender") return <CNNResults output={output} />;
  return <pre className="text-xs font-mono text-muted">{JSON.stringify(output, null, 2)}</pre>;
}