// frontend/src/pages/history/InferenceDetail.jsx

import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import { historyApi } from "../../api/historyApi";
import NERResults from "../../components/inference/NERResults";
import TextGenerationResults from "../../components/inference/TextGenerationResults";
import VoiceQAResults from "../../components/inference/VoiceQAResults";
import CNNResults from "../../components/inference/CNNResults";
import StatusIndicator from "../../components/ui/StatusIndicator";
import Spinner from "../../components/ui/Spinner";

function InferenceOutput({ taskName, output }) {
  if (taskName === "ner") return <NERResults output={output} />;
  if (taskName === "text_generation") return <TextGenerationResults output={output} />;
  if (taskName === "voice_qa") return <VoiceQAResults output={output} />;
  if (taskName === "cnn_gender") return <CNNResults output={output} />;
  return <pre className="text-xs font-mono text-muted">{JSON.stringify(output, null, 2)}</pre>;
}

export default function InferenceDetail() {
  const { id } = useParams();
  const { data: run, isLoading } = useQuery({
    queryKey: ["history", "inference", id],
    queryFn: () => historyApi.getInference(id),
  });

  if (isLoading) return <div className="p-8"><Spinner size="md" /></div>;
  if (!run) return <div className="p-8"><p className="text-muted">Not found.</p></div>;

  return (
    <div className="p-8">
      <div className="max-w-3xl mx-auto flex flex-col gap-6">
        <Link to="/history" className="flex items-center gap-2 text-sm text-muted hover:text-ink cursor-pointer w-fit">
          <ArrowLeft size={16} />Back to History
        </Link>

        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-ink">{run.task_display_name}</h1>
            <p className="text-muted text-sm mt-1">
              {run.category.replace("_", " ")} · #{run.id}
            </p>
          </div>
          <StatusIndicator status={run.status} size={16} />
        </div>

        {run.status === "completed" && run.output_data && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <h3 className="font-semibold text-ink mb-5">Output</h3>
            <InferenceOutput taskName={run.task_name} output={run.output_data} />
          </div>
        )}

        {run.status === "failed" && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <StatusIndicator status="failed" size={16} />
            <p className="text-sm text-muted font-mono mt-3">{run.error_message}</p>
          </div>
        )}

        <p className="text-xs text-faint font-mono">
          {run.duration_seconds != null ? `${run.duration_seconds}s · ` : ""}
          {new Date(run.created_at).toLocaleString()}
        </p>
      </div>
    </div>
  );
}