import torch
import torch.nn as nn


# Binary Cross Entropy Loss
bce_loss = nn.BCEWithLogitsLoss()


def dice_loss(predictions, targets, smooth=1e-6):

    # Convert logits to probabilities
    predictions = torch.sigmoid(predictions)

    # Flatten tensors
    predictions = predictions.contiguous().view(-1)
    targets = targets.contiguous().view(-1)

    # Compute intersection
    intersection = (predictions * targets).sum()

    # Dice coefficient
    dice = (
        (2.0 * intersection + smooth)
        /
        (
            predictions.sum()
            + targets.sum()
            + smooth
        )
    )

    # Dice loss
    return 1 - dice


def combined_loss(predictions, targets):

    bce = bce_loss(predictions, targets)

    dice = dice_loss(predictions, targets)

    return bce + dice