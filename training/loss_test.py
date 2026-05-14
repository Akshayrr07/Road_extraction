import torch
from utils import combined_loss


# Dummy predictions (logits)
predictions = torch.randn(
    4,
    1,
    256,
    256
)

# Dummy binary masks
targets = torch.randint(
    0,
    2,
    (4, 1, 256, 256)
).float()

# Compute loss
loss = combined_loss(
    predictions,
    targets
)

print("Loss:", loss.item())