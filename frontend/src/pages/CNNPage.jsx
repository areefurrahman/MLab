// frontend/src/pages/CNNPage.jsx

import { useState, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import { Upload } from "lucide-react";
import toast from "react-hot-toast";
import axios from "axios";

import axiosInstance from "../api/axiosInstance";
import { useInferencePolling } from "../hooks/useInferencePolling";
import CNNResults from "../components/inference/CNNResults";
import StatusIndicator from "../components/ui/StatusIndicator";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

export default function CNNPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [activeRunId, setActiveRunId] = useState(null);
  const fileInputRef = useRef(null);

  const { data: run } = useInferencePolling(activeRunId);

  const { mutate: runCNN, isLoading: launching } = useMutation({
    mutationFn: async () => {
      const formData = new FormData();
      formData.append("image", selectedFile);
      const res = await axiosInstance.post("/inference/run-cnn", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return res.data;
    },
    onSuccess: (data) => {
      setActiveRunId(data.id);
      toast.success("Classifying image...");
    },
    onError: (error) => {
      const details = error.response?.data?.details;
      toast.error(details?.image?.[0] || error.response?.data?.error || "Upload failed");
    },
  });

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setActiveRunId(null);
  };

  const isRunning = run?.status === "pending" || run?.status === "running";

  return (
    <div className="p-8">
      <div className="max-w-2xl mx-auto flex flex-col gap-6">

        <div>
          <h1 className="text-2xl font-semibold text-ink">CNN Image Classification</h1>
          <p className="text-muted text-sm mt-1">
            Convolutional Neural Network — upload a face image to classify as Female or Male.
          </p>
        </div>

        {/* Architecture tag */}
        <div className="flex items-center gap-2 text-xs text-faint font-mono">
          <span className="px-2 py-1 border border-line rounded">Conv2D × 3</span>
          <span>→</span>
          <span className="px-2 py-1 border border-line rounded">MaxPooling</span>
          <span>→</span>
          <span className="px-2 py-1 border border-line rounded">Dense</span>
          <span>→</span>
          <span className="px-2 py-1 border border-line rounded">Softmax</span>
        </div>

        {/* Upload area */}
        <div className="bg-surface border border-line rounded-xl p-6 flex flex-col gap-4">
          <input
            ref={fileInputRef}
            type="file"
            accept=".jpg,.jpeg,.png,.webp"
            onChange={handleFileChange}
            className="hidden"
          />

          <div
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center gap-3
              cursor-pointer transition-colors
              ${previewUrl ? "border-ink/30 bg-surface-hover" : "border-line hover:border-ink/20"}`}
          >
            {previewUrl ? (
              <>
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="max-h-40 rounded-lg object-cover"
                />
                <p className="text-xs text-faint">{selectedFile?.name} — click to change</p>
              </>
            ) : (
              <>
                <Upload size={24} className="text-faint" />
                <p className="text-muted text-sm">Click to upload a face image</p>
                <p className="text-xs text-faint">JPG, PNG, WEBP supported</p>
              </>
            )}
          </div>

          <Button
            onClick={() => runCNN()}
            isLoading={launching}
            disabled={!selectedFile || isRunning}
            className="w-fit"
          >
            Classify Image
          </Button>
        </div>

        {/* Running */}
        {isRunning && (
          <div className="bg-surface border border-line rounded-xl p-6 flex items-center gap-3">
            <Spinner size="sm" />
            <div>
              <StatusIndicator status="running" size={16} />
              <p className="text-xs text-faint mt-1">
                First run loads the Keras model — subsequent runs are instant.
              </p>
            </div>
          </div>
        )}

        {/* Failed */}
        {run?.status === "failed" && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <StatusIndicator status="failed" size={16} />
            <p className="text-sm text-muted font-mono mt-3">{run.error_message}</p>
          </div>
        )}

        {/* Completed */}
        {run?.status === "completed" && (
          <div className="bg-surface border border-line rounded-xl p-6">
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-semibold text-ink">Classification Result</h3>
              <StatusIndicator status="completed" size={16} />
            </div>
            <CNNResults output={run.output_data} />
            <p className="text-xs text-faint font-mono mt-5">
              {run.duration_seconds}s · gender_model.pth
            </p>
          </div>
        )}

      </div>
    </div>
  );
}