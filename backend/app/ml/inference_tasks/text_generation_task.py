# backend/app/ml/inference_tasks/text_generation_task.py

from transformers import pipeline
from app.ml.inference_base import BaseInferenceTask
from app.ml.inference_registry import InferenceTaskRegistry
from app.ml.inference_input_def import InferenceInputDef
from app.ml.categories import AlgorithmCategory


@InferenceTaskRegistry.register("text_generation")
class TextGenerationTask(BaseInferenceTask):
    name = "text_generation"
    display_name = "Text Generation"
    category = AlgorithmCategory.GENERATIVE_AI
    description = "Continues a text prompt using DistilGPT-2, a lightweight causal language model."

    @classmethod
    def _load_pipeline(cls):
        return pipeline("text-generation", model="distilgpt2")

    @classmethod
    def get_input_schema(cls):
        return [
            InferenceInputDef(
                name="prompt",
                label="Prompt",
                type="textarea",
                required=True,
                placeholder="e.g. 'Artificial intelligence is transforming the world by'",
                description="The model continues your text. Keep prompts short and specific.",
            ),
            InferenceInputDef(
                name="max_new_tokens",
                label="Max New Tokens",
                type="int",
                required=False,
                default=80,
                min=20,
                max=200,
                step=10,
                description="How many new tokens to generate (roughly, 1 token ≈ 0.75 words).",
            ),
            InferenceInputDef(
                name="temperature",
                label="Temperature",
                type="float",
                required=False,
                default=0.7,
                min=0.1,
                max=2.0,
                step=0.1,
                description="Higher = more creative/random. Lower = more predictable.",
            ),
        ]

    def run(self, input_data: dict) -> dict:
        prompt = input_data.get("prompt", "").strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty")

        max_new_tokens = int(input_data.get("max_new_tokens", 80))
        temperature = float(input_data.get("temperature", 0.7))

        pipe = self.get_pipeline()
        result = pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            return_full_text=False,   # return ONLY the generated part, not the prompt
        )

        generated_text = result[0]["generated_text"]

        return {
            "prompt": prompt,
            "generated_text": generated_text,
            "full_text": prompt + generated_text,
            "prompt_tokens": len(prompt.split()),
            "generated_tokens": max_new_tokens,
        }