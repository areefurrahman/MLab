// frontend/src/components/inference/VoiceQAResults.jsx

import { useState } from "react";
import { Download } from "lucide-react";

export default function VoiceQAResults({ output }) {
  const [isPlaying, setIsPlaying] = useState(false);

  if (!output) return null;

  const { transcribed_question, answer_text, audio_base64, audio_format } = output;
  const audioSrc = `data:audio/${audio_format};base64,${audio_base64}`;

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = audioSrc;
    link.download = `mlab_answer.${audio_format}`;
    link.click();
  };

  return (
    <div className="flex flex-col gap-5">

      {/* Stage 1 — Transcription */}
      <div>
        <p className="text-[11px] text-faint uppercase tracking-wide mb-2">
          You asked (transcribed)
        </p>
        <div className="bg-canvas border border-line rounded-lg px-4 py-3">
          <p className="text-ink text-sm font-mono">{transcribed_question}</p>
        </div>
      </div>

      {/* Stage 2 — Answer text */}
      <div>
        <p className="text-[11px] text-faint uppercase tracking-wide mb-2">Answer</p>
        <div className="bg-canvas border border-line rounded-lg px-4 py-3">
          <p className="text-ink text-sm">{answer_text}</p>
        </div>
      </div>

      {/* Stage 3 — Audio playback */}
      <div>
        <p className="text-[11px] text-faint uppercase tracking-wide mb-2">
          Listen to answer
        </p>
        <div className="bg-canvas border border-line rounded-lg px-4 py-3 flex items-center gap-4">
          <audio
            controls
            src={audioSrc}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onEnded={() => setIsPlaying(false)}
            className="flex-1 h-8"
            style={{ filter: "invert(1) brightness(0.8)" }}  // adapts to dark background
          />
          <button
            onClick={handleDownload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-line
              text-sm text-muted hover:text-ink hover:bg-surface-hover transition-colors cursor-pointer shrink-0"
          >
            <Download size={14} />
            Save
          </button>
        </div>
      </div>

      {/* Pipeline label */}
      <p className="text-xs text-faint font-mono">
        Whisper tiny.en → Flan-T5 small → MMS-TTS
      </p>
    </div>
  );
}