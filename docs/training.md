# docs/training.md

# 🧠 Training Pipeline Documentation

## Model Architecture

* U-Net
* ResNet34 Encoder
* Transfer Learning
* BCE + Dice Loss

----

## Training Configuration

| Parameter     | Value      |
| ------------- | ---------- |
| Image Size    | 128 × 128  |
| Batch Size    | 4          |
| Optimizer     | Adam       |
| Learning Rate | 1e-4       |
| Loss Function | BCE + Dice |
| Device        | CPU        |

----

## Training Workflow

```text
Satellite Image
    ↓
Preprocessing
    ↓
Dataset Loader
    ↓
U-Net Segmentation
    ↓
Loss Computation
    ↓
Backpropagation
    ↓
Checkpoint Saving
```

----

## Training Command

```bash
cd training

python train.py
```

----

## Saved Model

Location:

```text
backend/saved_models/best_model.pth
```
