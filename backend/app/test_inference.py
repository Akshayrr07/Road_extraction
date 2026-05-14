import matplotlib.pyplot as plt
import cv2

from inference import predict_mask


# Test image path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

IMAGE_PATH = (
    BASE_DIR.parent.parent
    / "dataset"
    / "raw"
    / "val"
    / "images"
    / "10228690_15.tiff"
)

# Predict
original_image, predicted_mask = predict_mask(
    IMAGE_PATH
)

# Convert BGR → RGB
original_image = cv2.cvtColor(
    original_image,
    cv2.COLOR_BGR2RGB
)

# =========================
# VISUALIZATION
# =========================

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(original_image)
plt.title("Original Satellite Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(predicted_mask, cmap="gray")
plt.title("Predicted Road Mask")
plt.axis("off")

OUTPUT_PATH = (
    BASE_DIR.parent
    / "outputs"
    / "prediction_result.png"
)

plt.savefig(OUTPUT_PATH)

print("Prediction saved successfully.")