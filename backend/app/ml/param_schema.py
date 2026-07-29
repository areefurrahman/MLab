# backend/app/ml/param_schema.py

from dataclasses import dataclass, field
from typing import Any, Optional, List


@dataclass
class ParamDef:
    """
    Describes ONE hyperparameter. The frontend reads these
    and renders the correct input control automatically.
    """
    name: str                    # "n_neighbors"
    label: str                   # "Number of Neighbors (K)"
    type: str                    # "int" | "float" | "select" | "bool"
    default: Any
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    options: Optional[List[str]] = None
    description: str = ""

    def to_dict(self) -> dict:
        d = {"name": self.name, "label": self.label, "type": self.type, "default": self.default}
        if self.min is not None:
            d["min"] = self.min
        if self.max is not None:
            d["max"] = self.max
        if self.step is not None:
            d["step"] = self.step
        if self.options is not None:
            d["options"] = self.options
        if self.description:
            d["description"] = self.description
        return d