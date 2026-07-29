# backend/app/ml/inference_input_def.py

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class InferenceInputDef:
    """
    Describes ONE input field for an inference task.
    The frontend reads this and renders the correct control automatically.
    """
    name: str           # "text", "prompt", "max_new_tokens"
    label: str          # "Input Text", "Prompt", "Max New Tokens"
    type: str           # "textarea" | "text" | "int" | "float" | "select"
    required: bool = True
    default: Any = None
    placeholder: str = ""
    description: str = ""
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    options: Optional[List[str]] = None

    def to_dict(self) -> dict:
        d = {
            "name": self.name, "label": self.label, "type": self.type,
            "required": self.required, "default": self.default,
            "placeholder": self.placeholder, "description": self.description,
        }
        if self.min is not None: d["min"] = self.min
        if self.max is not None: d["max"] = self.max
        if self.step is not None: d["step"] = self.step
        if self.options is not None: d["options"] = self.options
        return d