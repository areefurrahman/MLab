# backend/app/ml/inference_tasks/cnn_task.py

import os
import base64
import numpy as np

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

from app.ml.inference_base import BaseInferenceTask
from app.ml.inference_registry import InferenceTaskRegistry
from app.ml.inference_input_def import InferenceInputDef
from app.ml.categories import AlgorithmCategory


MODEL_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "gender_model.pth")
)

IMG_SIZE = 128

# Same preprocessing as training — must match exactly
TRANSFORM = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])


class GenderCNN(nn.Module):
    """
    Must be defined identically to train_cnn.py.
    PyTorch's state_dict save/load requires the same class definition at load time.
    """
    def __init__(self, num_classes):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.LazyLinear(64), nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


@InferenceTaskRegistry.register("cnn_gender")
class CNNGenderTask(BaseInferenceTask):
    name = "cnn_gender"
    display_name = "CNN Image Classification"
    category = AlgorithmCategory.DEEP_LEARNING
    description = "CNN trained to classify face images as Female or Male. Uses Conv2D×3 → MaxPool → Dense architecture."

    _pipeline = None       # holds (model, class_names) tuple
    _class_names = None

    @classmethod
    def _load_pipeline(cls):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Trained model not found at {MODEL_PATH}. "
                "Run backend/models/train_cnn.py first to produce gender_model.pth."
            )

        print(f"[CNN] Loading model from {MODEL_PATH}...")
        checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
        class_names = checkpoint["class_names"]
        num_classes = len(class_names)

        model = GenderCNN(num_classes)

        # LazyLinear needs one forward pass to initialize before loading weights
        dummy = torch.zeros(1, 3, IMG_SIZE, IMG_SIZE)
        model(dummy)

        model.load_state_dict(checkpoint["state_dict"])
        model.eval()

        cls._class_names = class_names
        print(f"[CNN] Model ready. Classes: {class_names}")
        return model

    @classmethod
    def get_input_schema(cls):
        return [
            InferenceInputDef(
                name="image",
                label="Input Image",
                type="image",
                required=True,
                description="Upload a face image (JPG, PNG, WEBP). CNN classifies as Female or Male.",
            )
        ]

    def run(self, input_data: dict) -> dict:
        image_path = input_data.get("image_path")
        if not image_path or not os.path.exists(image_path):
            raise ValueError("image_path is required and must exist on disk")

        model = self.get_pipeline()
        class_names = self._class_names

        # ── Preprocess ───────────────────────────────────────────────────────
        img = Image.open(image_path).convert("RGB")
        tensor = TRANSFORM(img).unsqueeze(0)   # (1, 3, 128, 128)

        # ── Inference ────────────────────────────────────────────────────────
        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0]

        predicted_index = int(probs.argmax())
        predicted_label = class_names[predicted_index]
        confidence = round(float(probs[predicted_index]) * 100, 2)

        probabilities = {
            class_names[i]: round(float(probs[i]) * 100, 2)
            for i in range(len(class_names))
        }

        image_b64 = _encode_image_base64(image_path)

        return {
            "predicted_label": predicted_label,
            "confidence": confidence,
            "probabilities": probabilities,
            "class_names": class_names,
            "image_base64": image_b64,
        }


def _encode_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")








# FOR TENSERFLOW CNN TASK

# # backend/app/ml/inference_tasks/cnn_task.py

# import os
# import io
# import base64
# import numpy as np
# from PIL import Image

# from app.ml.inference_base import BaseInferenceTask
# from app.ml.inference_registry import InferenceTaskRegistry
# from app.ml.inference_input_def import InferenceInputDef
# from app.ml.categories import AlgorithmCategory


# MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "gender_model.h5")
# MODEL_PATH = os.path.normpath(MODEL_PATH)

# # Alphabetical order of training subfolders — must match what
# # image_dataset_from_directory detected during train_cnn.py.
# # Your training script prints "Classes detected:" — verify this matches.
# CLASS_NAMES = ["female", "male"]
# IMG_SIZE = (128, 128)


# @InferenceTaskRegistry.register("cnn_gender")
# class CNNGenderTask(BaseInferenceTask):
#     name = "cnn_gender"
#     display_name = "CNN Image Classification"
#     category = AlgorithmCategory.DEEP_LEARNING
#     description = "Convolutional Neural Network trained to classify images as Female or Male. Upload any face image."

#     _pipeline = None   # holds the loaded Keras model

#     @classmethod
#     def _load_pipeline(cls):
#         """
#         Lazy-loads the Keras model once per Celery worker.
#         Import TF here, not at module level — avoids slow TF startup
#         on every import even when CNN isn't being used.
#         """
#         if not os.path.exists(MODEL_PATH):
#             raise FileNotFoundError(
#                 f"Trained model not found at {MODEL_PATH}. "
#                 "Copy your gender_model.h5 into backend/models/ first."
#             )

#         from tensorflow.keras.models import load_model
#         print(f"[CNN] Loading model from {MODEL_PATH}...")
#         model = load_model(MODEL_PATH)
#         print("[CNN] Model ready.")
#         return model

#     @classmethod
#     def get_input_schema(cls):
#         return [
#             InferenceInputDef(
#                 name="image",
#                 label="Input Image",
#                 type="image",
#                 required=True,
#                 description="Upload a face image (JPG, PNG, WEBP). The CNN will classify it as Female or Male.",
#             )
#         ]

#     def run(self, input_data: dict) -> dict:
#         image_path = input_data.get("image_path")
#         if not image_path or not os.path.exists(image_path):
#             raise ValueError("image_path is required and must exist on disk")

#         # ── Preprocess — must exactly match training pipeline ────────────────
#         img = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
#         img_array = np.array(img, dtype=np.float32) / 255.0   # same rescaling as training
#         img_array = np.expand_dims(img_array, axis=0)          # (1, 128, 128, 3)

#         # ── Inference ────────────────────────────────────────────────────────
#         model = self.get_pipeline()
#         predictions = model.predict(img_array, verbose=0)[0]  # shape: (num_classes,)

#         predicted_index = int(np.argmax(predictions))
#         predicted_label = CLASS_NAMES[predicted_index]
#         confidence = round(float(predictions[predicted_index]) * 100, 2)

#         probabilities = {
#             CLASS_NAMES[i]: round(float(predictions[i]) * 100, 2)
#             for i in range(len(CLASS_NAMES))
#         }

#         # ── Encode image for frontend display ────────────────────────────────
#         image_b64 = _encode_image_base64(image_path)

#         return {
#             "predicted_label": predicted_label,
#             "confidence": confidence,
#             "probabilities": probabilities,
#             "class_names": CLASS_NAMES,
#             "image_base64": image_b64,
#         }


# def _encode_image_base64(image_path: str) -> str:
#     """Encodes the uploaded image to base64 so the frontend can display it."""
#     with open(image_path, "rb") as f:
#         return base64.b64encode(f.read()).decode("utf-8")