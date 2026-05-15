# 🛰️ Satellite Road Extraction using Deep Learning

An end-to-end AI-powered road extraction system built using U-Net segmentation architecture, PyTorch, Flask, and React.

This project performs semantic segmentation on satellite imagery to automatically detect and extract road networks. The system includes model training, inference pipeline, REST API backend, and a deployed frontend application.

---

## 🚀 Live Demo

### Frontend
[https://road-extraction-livid.vercel.app/](https://road-extraction-livid.vercel.app/)

### Backend API
[https://road-extraction-api.onrender.com](https://road-extraction-api.onrender.com)

---

## 📌 Features

*   Satellite image road segmentation
*   U-Net with ResNet34 encoder
*   PyTorch-based inference pipeline
*   Flask REST API backend
*   React frontend integration
*   TIFF satellite image support
*   Deployment-ready architecture
*   Public cloud deployment

---

## 🧠 Model Architecture

The segmentation model uses:

*   U-Net Decoder
*   ResNet34 Encoder
*   Transfer Learning
*   BCE + Dice Combined Loss

### Workflow

```text
Satellite Image
    ↓
Preprocessing
    ↓
U-Net Segmentation
    ↓
Binary Road Mask
    ↓
Visualization Output

```

## 🛠️ Tech Stack

* AI / Machine Learning
* PyTorch
* segmentation_models_pytorch
* OpenCV
* NumPy
* Flask
* Flask-CORS
* Gunicorn
* React
* Vite
* Axios
* Render (Backend)
* Vercel (Frontend)

---

## 📂 Project Structure

```text
Road_extraction/
├── backend/
│   ├── app/
│   ├── saved_models/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── public/
├── training/
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   └── utils.py
├── notebooks/
└── README.md

```
# 📘 Documentation

- [Docker & Setup Guide](docs/docker.md)
---

## ⚙️ Training Configuration

* **Image Size:** 128 × 128
* **Batch Size:** 4
* **Optimizer:** Adam
* **Learning Rate:** 1e-4
* **Loss Function:** BCE + Dice
* **Encoder:** ResNet34
* **Framework:** PyTorch

---

## 📡 API Endpoint

**`POST /predict`**

Uploads a satellite image and returns the predicted road mask.

### Request

* **Multipart form-data:** `image`

### Response

```json
{
  "message": "Prediction completed",
  "mask_url": "generated_mask_url"
}

```

---

## 🖼️ Supported Formats

* PNG
* JPG
* JPEG
* TIFF
* TIF

---

## 🧪 Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
python app/app.py

```

### Frontend

```bash
cd frontend
npm install
npm run dev

```

---

## 📈 Future Improvements

* Interactive map visualization
* Overlay rendering
* ONNX optimization
* Docker deployment
* FastAPI migration
* Advanced postprocessing
* Better UI/UX enhancements

---

## 👨‍💻 Author

**Akshay RR**

Focused on:

* AI/ML Engineering
* Full Stack Development
* Computer Vision Systems
* Deployment Engineering

---

## 📜 License

This project is licensed under the MIT License.
