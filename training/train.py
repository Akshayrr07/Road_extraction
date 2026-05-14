import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
from dataset import RoadDataset
from model import UNetModel
from utils import combined_loss


# =========================
# CONFIG
# =========================

TRAIN_IMAGE_DIR = "dataset/raw/train/images"
TRAIN_MASK_DIR = "dataset/raw/train/masks"

VAL_IMAGE_DIR = "dataset/raw/val/images"
VAL_MASK_DIR = "dataset/raw/val/masks"

IMAGE_SIZE = 256
BATCH_SIZE = 4
LEARNING_RATE = 1e-4
EPOCHS = 10
NUM_WORKERS = 2
PIN_MEMORY = False

DEVICE = torch.device("cpu")


# =========================
# DATASETS
# =========================

train_dataset = RoadDataset(
    image_dir=TRAIN_IMAGE_DIR,
    mask_dir=TRAIN_MASK_DIR,
    image_size=IMAGE_SIZE
)

val_dataset = RoadDataset(
    image_dir=VAL_IMAGE_DIR,
    mask_dir=VAL_MASK_DIR,
    image_size=IMAGE_SIZE
)


# =========================
# DATALOADERS
# =========================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS,
    pin_memory=PIN_MEMORY
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS,
    pin_memory=PIN_MEMORY
)


print("Train Samples:", len(train_dataset))
print("Validation Samples:", len(val_dataset))


# =========================
# MODEL
# =========================

model = UNetModel().to(DEVICE)

for param in model.model.encoder.parameters():
    param.requires_grad = False

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    factor=0.5,
    patience=3
)


# =========================
# IOU METRIC
# =========================

def calculate_iou(predictions, targets, threshold=0.5):

    predictions = torch.sigmoid(predictions)

    predictions = (predictions > threshold).float()

    intersection = (predictions * targets).sum()

    union = predictions.sum() + targets.sum() - intersection

    iou = (intersection + 1e-6) / (union + 1e-6)

    return iou.item()


# =========================
# TRAINING LOOP
# =========================

best_val_loss = float("inf")

for epoch in range(EPOCHS):

    # =====================
    # TRAINING
    # =====================

    model.train()

    train_loss = 0.0
    train_iou = 0.0

    train_bar = tqdm(train_loader)

    for images, masks in train_bar:

        images = images.to(DEVICE)
        masks = masks.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = combined_loss(outputs, masks)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

        train_iou += calculate_iou(outputs, masks)

        train_bar.set_description(
            f"Epoch {epoch+1}/{EPOCHS}"
        )

    avg_train_loss = train_loss / len(train_loader)
    avg_train_iou = train_iou / len(train_loader)

    # =====================
    # VALIDATION
    # =====================

    model.eval()

    val_loss = 0.0
    val_iou = 0.0

    with torch.no_grad():

        for images, masks in val_loader:

            images = images.to(DEVICE)
            masks = masks.to(DEVICE)

            outputs = model(images)

            loss = combined_loss(outputs, masks)

            val_loss += loss.item()

            val_iou += calculate_iou(outputs, masks)

    avg_val_loss = val_loss / len(val_loader)
    avg_val_iou = val_iou / len(val_loader)

    scheduler.step(avg_val_loss)

    # =====================
    # LOGGING
    # =====================

    print(f"\nEpoch {epoch+1}/{EPOCHS}")

    print(f"Train Loss: {avg_train_loss:.4f}")
    print(f"Train IoU : {avg_train_iou:.4f}")

    print(f"Val Loss  : {avg_val_loss:.4f}")
    print(f"Val IoU   : {avg_val_iou:.4f}")

    # =====================
    # SAVE BEST MODEL
    # =====================

    if avg_val_loss < best_val_loss:

        best_val_loss = avg_val_loss

        torch.save(
            model.state_dict(),
            "backend/saved_models/best_model.pth"
        )

        print("Best model saved.")