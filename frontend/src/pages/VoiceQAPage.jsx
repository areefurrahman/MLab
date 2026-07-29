// frontend/src/pages/VoiceQAPage.jsx

import { useState, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import { Upload, Mic } from "lucide-react";
import toast from "react-hot-toast";

import { inferenceApi } from "../api/inferenceApi";
import { useInferencePolling } from "../hooks/useInferencePolling";
import VoiceQAResults from "../components/inference/VoiceQAResults";
import StatusIndicator from "../components/ui/StatusIndicator";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

const ACCEPTED_TYPES = ".wav,.mp3,.ogg,.flac,.m4a";
const PIPELINE_STAGES = [
  { key: "transcribing", label: "Stage 1 — Transcribing audio (Whisper)" },
  { key: "answering", label: "Stage 2 — Generating answer (Flan-T5)" },
  { key: "synthesizing", label: "Stage 3 — Synthesizing speech (MMS-TTS)" },
];

export default function VoiceQAPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [activeRunId, setActiveRunId] = useState(null);
  const [currentStage, setCurrentStage] = useState(0);
  const fileInputRef = useRef(null);

  const { data: run } = useInferencePolling(activeRunId);

  // Animate through pipeline stages while running
  // Each stage takes roughly the same time, so we step every 8 seconds
  const stageTimerRef = useRef(null);
  const startStageAnimation = () => {
    setCurrentStage(0);
    let stage = 0;
    stageTimerRef.current = setInterval(() => {
      stage = Math.min(stage + 1, PIPELINE_STAGES.length - 1);
      setCurrentStage(stage);
    }, 8000);
  };
  const stopStageAnimation = () => {
    if (stageTimerRef.current) clearInterval(stageTimerRef.current);
  };

  const { mutate: runVoiceQA, isLoading: launching } = useMutation({
    mutationFn: () => inferenceApi.runVoiceQA(selectedFile),
    onSuccess: (data) => {
      setActiveRunId(data.id);
      startStageAnimation();
      toast.success("Processing your question...");
    },
    onError: (error) => {
      const details = error.response?.data?.details;
      toast.error(details?.audio?.[0] || error.response?.data?.error || "Upload failed");
    },
  });

  // Stop animation when run completes
  if (run && ["completed", "failed"].includes(run.status) && stageTimerRef.current) {
    stopStageAnimation();
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setActiveRunId(null);   // reset previous result
    }
  };

  const handleDropZoneClick = () => fileInputRef.current?.click();

  const isRunning = run?.status === "pending" || run?.status === "running";

  return (
    <div className="p-8">
      <div className="max-w-3xl mx-auto flex flex-col gap-6">

        <div>
          <h1 className="text-2xl font-semibold text-ink">Voice Question Answering</h1>
          <p className="text-muted text-sm mt-1">
            Speak your question — the pipeline transcribes it, answers it, and reads the answer back.
          </p>
        </div>

        {/* Pipeline diagram */}
        <div className="flex items-center gap-2 text-xs text-faint font-mono">
          <span className="px-2 py-1 border border-line rounded">Whisper</span>
          <span>→</span>
          <span className="px-2 py-1 border border-line rounded">Flan-T5</span>
          <span>→</span>
          <span className="px-2 py-1 border border-line rounded">MMS-TTS</span>
        </div>

        {/* Upload area */}
        <div className="bg-surface border border-line rounded-xl p-6 flex flex-col gap-4">
          <input
            ref={fileInputRef}
            type="file"
            accept={ACCEPTED_TYPES}
            onChange={handleFileChange}
            className="hidden"
          />

          <div
            onClick={handleDropZoneClick}
            className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center gap-3
              cursor-pointer transition-colors
              ${selectedFile ? "border-ink/30 bg-surface-hover" : "border-line hover:border-ink/20"}`}
          >
            <Upload size={24} className="text-faint" />
            {selectedFile ? (
              <>
                <p className="text-ink text-sm font-medium">{selectedFile.name}</p>
                <p className="text-xs text-faint font-mono">
                  {(selectedFile.size / 1024).toFixed(1)} KB — click to change
                </p>
              </>
            ) : (
              <>
                <p className="text-muted text-sm">Click to select an audio file</p>
                <p className="text-xs text-faint">WAV, MP3, OGG, FLAC, M4A supported</p>
              </>
            )}
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={() => runVoiceQA()}
              isLoading={launching}
              disabled={!selectedFile || isRunning}
              className="w-fit"
            >
              <Mic size={16} />
              Ask Question
            </Button>
            {selectedFile && !isRunning && (
              <p className="text-xs text-faint">
                First run downloads ~880MB — subsequent runs are fast.
              </p>
            )}
          </div>
        </div>

        {/* Running state — stage progress */}
        {isRunning && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <StatusIndicator status="running" size={16} />
            <div className="mt-4 flex flex-col gap-2">
              {PIPELINE_STAGES.map((stage, i) => (
                <div key={stage.key} className="flex items-center gap-3">
                  <div className={`h-1.5 w-1.5 rounded-full shrink-0
                    ${i < currentStage ? "bg-ink" : i === currentStage ? "bg-ink animate-pulse" : "bg-line"}`}
                  />
                  <p className={`text-sm transition-colors
                    ${i === currentStage ? "text-ink" : i < currentStage ? "text-muted line-through" : "text-faint"}`}>
                    {stage.label}
                  </p>
                </div>
              ))}
            </div>
            <p className="text-xs text-faint mt-4">
              First run includes model downloads — this may take 1-3 minutes.
            </p>
          </div>
        )}

        {/* Failed state */}
        {run?.status === "failed" && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <StatusIndicator status="failed" size={16} />
            <p className="text-sm text-muted font-mono mt-3">{run.error_message}</p>
          </div>
        )}

        {/* Completed — results */}
        {run?.status === "completed" && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-semibold text-ink">Response</h3>
              <StatusIndicator status="completed" size={16} />
            </div>
            <VoiceQAResults output={run.output_data} />
            <p className="text-xs text-faint font-mono mt-4">
              {run.duration_seconds}s total pipeline time
            </p>
          </div>
        )}

      </div>
    </div>
  );
}