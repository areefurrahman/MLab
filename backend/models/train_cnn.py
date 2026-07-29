# backend/models/train_cnn.py

import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# ── Config ────────────────────────────────────────────────────────────────────
TRAIN_DIR = "dataset/train"
TEST_DIR = "dataset/test"
IMG_SIZE = 128
BATCH_SIZE = 8
EPOCHS = 10
MODEL_SAVE_PATH = "gender_model.pth"

# ── Same preprocessing as before: resize + normalize to [0,1] ────────────────
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),   # converts to float32, divides by 255
])

train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=transform)
test_dataset = datasets.ImageFolder(TEST_DIR, transform=transform)

# ImageFolder sorts class names alphabetically — same as Keras
# female=0, male=1 (alphabetical)
CLASS_NAMES = train_dataset.classes
print("Classes detected:", CLASS_NAMES)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

num_classes = len(CLASS_NAMES)


# ── Same architecture: Conv2D×3 → MaxPool → Flatten → Dense → Softmax ────────
class GenderCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.LazyLinear(64), nn.ReLU(),   # LazyLinear infers input size automatically
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


model = GenderCNN(num_classes)
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()


# ── Training loop ─────────────────────────────────────────────────────────────
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(images), labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{EPOCHS} — loss: {total_loss:.4f}")

# ── Evaluation ────────────────────────────────────────────────────────────────
model.eval()
correct = total = 0
with torch.no_grad():
    for images, labels in test_loader:
        preds = model(images).argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += len(labels)

print(f"Test accuracy: {correct/total:.2f}")

# ── Save ──────────────────────────────────────────────────────────────────────
# Save full model state dict + class names together
torch.save({"state_dict": model.state_dict(), "class_names": CLASS_NAMES}, MODEL_SAVE_PATH)
print(f"Saved to {MODEL_SAVE_PATH}")