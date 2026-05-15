# docs/architecture.md

# 🏗️ System Architecture

## Full Stack Architecture

```text
React Frontend
       ↓
Axios API Requests
       ↓
Flask Backend API
       ↓
PyTorch Inference Engine
       ↓
U-Net Segmentation Model
       ↓
Road Extraction Mask
```

----

## Backend Architecture

```text
Client Request
      ↓
Flask Upload API
      ↓
Image Validation
      ↓
Inference Pipeline
      ↓
Segmentation Prediction
      ↓
Mask Generation
      ↓
JSON Response
```

----

## AI Pipeline

```text
Satellite Image
      ↓
Preprocessing
      ↓
Tensor Conversion
      ↓
U-Net Inference
      ↓
Sigmoid Thresholding
      ↓
Binary Segmentation Mask
```
