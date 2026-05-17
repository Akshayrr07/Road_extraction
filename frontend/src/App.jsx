import { useState } from "react";
import axios from "axios";
import "./App.css"


function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [serverPreview, setServerPreview] = useState(null);
  const [message, setMessage] = useState("");
  // =========================
  // HANDLE IMAGE
const handleImageChange = (event) => {
  const file = event.target.files[0];

  setImage(file);
  setMessage("");

  if (file.type === "image/png" || file.type === "image/jpeg") {
    setPreview(URL.createObjectURL(file));
  } else {
    setPreview(null);
  }
};

  // =========================
  // HANDLE PREDICTION
  // =========================
  const handlePredict = async () => {
    if (!image) {
      setMessage("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      setMessage("");
      setLoading(true);

      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/predict`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setServerPreview(response.data.preview_url);
      setResult(response.data.mask_url);
    } catch (error) {
      console.error("FULL ERROR:", error);
      console.error("BACKEND RESPONSE:", error.response?.data);
      setMessage(
  error.response?.data?.error ||
  "Prediction failed. Please try again."
);
    } finally {
      setLoading(false);
    }

   
  };

  const handleRemoveImage = () => {
    setImage(null);
    setPreview(null);
    setResult(null);
    setServerPreview(null);
  };
return (
  <div className="page">
    
    <header className="hero-section">
      <h1>AI Satellite Road Extraction</h1>
      <p>Deep Learning Terrain Analysis</p>
    </header>

    <main className="workspace">

      {/* Upload Section */}
      <section className="upload-section">

        <label className="upload-label">

    <input
    type="file"
    accept=".png,.jpg,.jpeg,.tif,.tiff"
    onChange={handleImageChange}
    hidden
  />

  Select Terrain File

</label>

        <button onClick={handlePredict}>
          {loading ? "Predicting..." : "Extract Roads"}
        </button>

        {preview && (
  <button
    className="remove-btn"
    onClick={handleRemoveImage}
  >
    Remove Image
  </button>
)}

      </section>

      {/* Preview + Result Section */}
      <section className="result-section">

        {/* Uploaded / Converted Preview */}
        {(preview || serverPreview) && (
          <div className="preview-card">

            <h2>Uploaded Image</h2>

            <img
              src={serverPreview || preview}
              alt="Preview"
            />

          </div>
        )}

        {/* Prediction Result */}
        {result && (
          <div className="result-card">

            <h2>Predicted Road Mask</h2>

            <img
              src={result}
              alt="Prediction"
            />

          </div>
        )}

      </section>
      {message && (
  <p className="status-text">
    {message}
  </p>
)}

    </main>

  </div>
);
}



export default App;

