# backend/app/ml/inference_tasks/voice_qa_task.py

import io
import base64
import numpy as np
import scipy.io.wavfile
import torch

from transformers import pipeline, VitsModel, AutoTokenizer

from app.ml.inference_base import BaseInferenceTask
from app.ml.inference_registry import InferenceTaskRegistry
from app.ml.inference_input_def import InferenceInputDef
from app.ml.categories import AlgorithmCategory
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


@InferenceTaskRegistry.register("voice_qa")
class VoiceQATask(BaseInferenceTask):
    name = "voice_qa"
    display_name = "Voice Question Answering"
    category = AlgorithmCategory.GENERATIVE_AI
    description = (
        "Three-stage pipeline: Whisper transcribes your spoken question, "
        "Flan-T5 generates an answer, MMS-TTS speaks the answer back."
    )

    # ─── Three independent caches ─────────────────────────────────────────────
    _stt_pipeline = None     # Whisper
    _tts_model = None        # MMS-TTS model
    _tts_tokenizer = None    # MMS-TTS tokenizer
    _qa_model = None
    _qa_tokenizer = None


    # BaseInferenceTask requires this — VoiceQA doesn't use a single pipeline
    # so we return None and use the per-model loaders below instead
    @classmethod
    def _load_pipeline(cls):
        return None

    @classmethod
    def get_stt(cls):
        if cls._stt_pipeline is None:
            print("[VoiceQA] Loading Whisper tiny.en...")
            cls._stt_pipeline = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-tiny.en",
            )
            print("[VoiceQA] Whisper ready.")
        return cls._stt_pipeline

    @classmethod
    def get_qa(cls):
        if cls._qa_model is None:
            print("[VoiceQA] Loading Flan-T5 small...")
            cls._qa_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
            cls._qa_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
            print("[VoiceQA] Flan-T5 ready.")
        return cls._qa_model, cls._qa_tokenizer

    @classmethod
    def get_tts(cls):
        if cls._tts_model is None:
            print("[VoiceQA] Loading MMS-TTS...")
            cls._tts_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
            cls._tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
            print("[VoiceQA] MMS-TTS ready.")
        return cls._tts_model, cls._tts_tokenizer

    @classmethod
    def get_input_schema(cls):
        return [
            InferenceInputDef(
                name="audio",
                label="Audio Question",
                type="audio",
                required=True,
                description="Upload a WAV, MP3, OGG, or FLAC file with your spoken question.",
            )
        ]

    def run(self, input_data: dict) -> dict:
        audio_path = input_data.get("audio_path")
        if not audio_path:
            raise ValueError("audio_path is required in input_data")

        # ── Stage 1: Speech → Text ───────────────────────────────────────────
        stt = self.get_stt()
        stt_result = stt(audio_path)
        question = stt_result["text"].strip()

        if not question:
            raise ValueError("Could not transcribe audio — check the file is clear speech")

        # ── Stage 2: Text → Answer ───────────────────────────────────────────
        model, tokenizer = self.get_qa()
        prompt = f"Question: {question} Answer:"
        inputs = tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=120)

        answer = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

        # ── Stage 3: Answer → Speech ─────────────────────────────────────────
        audio_b64, sample_rate = self._synthesize_speech(answer)

        return {
            "transcribed_question": question,
            "answer_text": answer,
            "audio_base64": audio_b64,
            "sample_rate": sample_rate,
            "audio_format": "wav",
        }

    @classmethod
    def _synthesize_speech(cls, text: str):
        model, tokenizer = cls.get_tts()

        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = model(**inputs)

        waveform = output.waveform[0].numpy()           # float32, shape (samples,)
        sample_rate = model.config.sampling_rate        # 16000 Hz

        # float32 → int16 for standard WAV encoding
        waveform_int16 = (waveform * 32767).clip(-32768, 32767).astype(np.int16)

        buffer = io.BytesIO()
        scipy.io.wavfile.write(buffer, sample_rate, waveform_int16)
        audio_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return audio_b64, sample_rate