import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TRAINING_DIR = BASE_DIR.parent.parent / "training"

sys.path.append(str(TRAINING_DIR))

import cv2
import numpy as np
import torch

from model import UNetModel


# =========================
# CONFIG
# =========================

MODEL_PATH = BASE_DIR.parent / "saved_models" / "best_model.pth"

DEVICE = torch.device("cpu")

IMAGE_SIZE = 256


# =========================
# LOAD MODEL
# =========================

model = UNetModel().to(DEVICE)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=DEVICE)
)

model.eval()

print("Model loaded successfully.")


# =========================
# PREDICTION FUNCTION
# =========================

def predict_mask(image_path):

    # Read original image
    original_image = cv2.imread(str(image_path))

    original_height, original_width = original_image.shape[:2]

    # Convert BGR → RGB
    image = cv2.cvtColor(
        original_image,
        cv2.COLOR_BGR2RGB
    )

    # Resize
    image_resized = cv2.resize(
        image,
        (IMAGE_SIZE, IMAGE_SIZE)
    )

    # Normalize
    image_normalized = (
        image_resized.astype(np.float32) / 255.0
    )

    # HWC → CHW
    image_transposed = np.transpose(
        image_normalized,
        (2, 0, 1)
    )

    # Tensor
    image_tensor = torch.tensor(
        image_transposed,
        dtype=torch.float32
    ).unsqueeze(0).to(DEVICE)

    # Prediction
    with torch.no_grad():

        prediction = model(image_tensor)

        prediction = torch.sigmoid(prediction)

        prediction = prediction.squeeze().cpu().numpy()

    # Threshold
    prediction = (prediction > 0.5).astype(np.uint8)

    # Resize back
    prediction = cv2.resize(
        prediction,
        (original_width, original_height),
        interpolation=cv2.INTER_NEAREST
    )

    return original_image, prediction