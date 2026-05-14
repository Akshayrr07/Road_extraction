from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

from pathlib import Path
import uuid
import cv2

from app.inference import predict_mask

# =========================
# BASE PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR.parent / "uploads"
OUTPUT_FOLDER = BASE_DIR.parent / "outputs"

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# =========================
# ALLOWED FILE TYPES
# =========================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "tif",
    "tiff"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

# =========================
# APP CONFIG
# =========================

app = Flask(__name__)

CORS(app)


# =========================
# HEALTH ROUTE
# =========================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Road Extraction API Running"
    })



# =========================
# SERVE OUTPUT FILES
# =========================

@app.route("/outputs/<filename>")
def serve_output(filename):

    return send_from_directory(
        OUTPUT_FOLDER,
        filename
    )


# =========================
# PREDICTION ROUTE
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    # Validate upload
    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]
    if not allowed_file(file.filename):

        return jsonify({
        "error": "Unsupported file type"
    }), 400

    if file.filename == "":

        return jsonify({
            "error": "Empty filename"
        }), 400


    # =====================
    # SAVE INPUT IMAGE
    # =====================

    unique_id = uuid.uuid4().hex

    file_extension = (
        Path(file.filename).suffix
    )

    upload_filename = (
        f"{unique_id}{file_extension}"
    )

    upload_path = (
        UPLOAD_FOLDER / upload_filename
    )

    file.save(str(upload_path))

    # =====================
    # GENERATE PREVIEW PNG
    # =====================

    preview_filename = (
        f"{unique_id}_preview.png"
    )

    preview_path = (
        OUTPUT_FOLDER / preview_filename
    )

    preview_image = cv2.imread(str(upload_path))

    cv2.imwrite(
        str(preview_path),
        preview_image
    )

    # =====================
    # RUN INFERENCE
    # =====================

    original_image, predicted_mask = predict_mask(
        upload_path
    )

    # =====================
    # SAVE PREDICTED MASK
    # =====================

    output_filename = (
        f"{unique_id}_mask.png"
    )

    output_path = (
        OUTPUT_FOLDER / output_filename
    )

    cv2.imwrite(
        str(output_path),
        predicted_mask * 255
    )

    # =====================
    # RESPONSE
    # =====================

    return jsonify({
        "message": "Prediction completed",
        "preview_url": (
            f"http://127.0.0.1:5000/outputs/{preview_filename}"
        ),
        "mask_url": (
            f"http://127.0.0.1:5000/outputs/{output_filename}"
        )
    })


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    import os

    PORT = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=PORT
    )