# backend/app/ml/inference_tasks/ner_task.py

from transformers import pipeline
from app.ml.inference_base import BaseInferenceTask
from app.ml.inference_registry import InferenceTaskRegistry
from app.ml.inference_input_def import InferenceInputDef
from app.ml.categories import AlgorithmCategory


@InferenceTaskRegistry.register("ner")
class NERTask(BaseInferenceTask):
    name = "ner"
    display_name = "Named Entity Recognition"
    category = AlgorithmCategory.DEEP_LEARNING
    description = "Identifies and classifies named entities (people, organizations, locations) in text using BERT."

    @classmethod
    def _load_pipeline(cls):
        """
        Loads dslim/bert-base-NER with aggregation_strategy="simple".
        aggregation_strategy merges B-/I- tokens (e.g. B-PER + I-PER + I-PER)
        into one entity span ("John Doe") rather than returning raw subword tokens.
        """
        return pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple",
        )

    @classmethod
    def get_input_schema(cls):
        return [
            InferenceInputDef(
                name="text",
                label="Input Text",
                type="textarea",
                required=True,
                placeholder="Enter text to analyze. e.g. 'Elon Musk founded SpaceX in Hawthorne, California.'",
                description="The model identifies PER (people), ORG (organizations), LOC (locations), and MISC entities.",
            )
        ]

    def run(self, input_data: dict) -> dict:
        text = input_data.get("text", "").strip()
        if not text:
            raise ValueError("Input text cannot be empty")

        pipe = self.get_pipeline()
        raw_entities = pipe(text)

        entities = [
            {
                "text": e["word"],
                "entity_type": e["entity_group"],
                "score": round(float(e["score"]), 4),
                "start": e["start"],
                "end": e["end"],
            }
            for e in raw_entities
        ]

        return {
            "original_text": text,
            "entities": entities,
            "entity_count": len(entities),
            "entity_type_counts": _count_entity_types(entities),
        }


def _count_entity_types(entities: list) -> dict:
    counts = {}
    for e in entities:
        t = e["entity_type"]
        counts[t] = counts.get(t, 0) + 1
    return counts