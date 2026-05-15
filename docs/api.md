# docs/api.md

# 📡 API Documentation

## Health Endpoint

### GET /

Response:

```json
{
  "message": "Road Extraction API Running"
}
```

----

## Prediction Endpoint

### POST /predict

Uploads a satellite image and returns a generated road segmentation mask.

---

## Request

Content-Type:

```text
multipart/form-data
```

Field:

```text
image
```

----

## Response

```json
{
  "message": "Prediction completed",
  "preview_url": "preview_image_url",
  "mask_url": "generated_mask_url"
}
```

----

## Supported Formats

* PNG
* JPG
* JPEG
* TIFF
* TIF
