import os

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

from pathlib import Path
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

class RoadDataset(Dataset):

    def __init__(self, image_dir, mask_dir, image_size=256):

        self.image_dir = Path(image_dir)
        self.mask_dir = Path(mask_dir)

        self.image_paths = sorted(list(self.image_dir.glob("*")))
        self.mask_paths = sorted(list(self.mask_dir.glob("*")))

        assert len(self.image_paths) == len(self.mask_paths), \
            "Mismatch between images and masks"

        self.image_size = image_size

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):

        # Read image
        image = cv2.imread(str(self.image_paths[index]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Read mask
        mask = cv2.imread(
            str(self.mask_paths[index]),
            cv2.IMREAD_GRAYSCALE
        )

        # Resize image
        image = cv2.resize(
            image,
            (self.image_size, self.image_size),
            interpolation=cv2.INTER_LINEAR
        )

        # Resize mask
        mask = cv2.resize(
            mask,
            (self.image_size, self.image_size),
            interpolation=cv2.INTER_NEAREST
        )

        # Normalize image
        image = image.astype(np.float32) / 255.0

        # Normalize mask
        mask = mask.astype(np.float32) / 255.0

        # Binary threshold
        mask = (mask > 0.5).astype(np.float32)

        # Add channel dimension
        mask = np.expand_dims(mask, axis=0)

        # HWC → CHW
        image = np.transpose(image, (2, 0, 1))

        # Convert to tensors
        image = torch.tensor(image, dtype=torch.float32)
        mask = torch.tensor(mask, dtype=torch.float32)

        return image, mask