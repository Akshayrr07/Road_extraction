import { useState } from "react";
import axios from "axios";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [serverPreview, setServerPreview] = useState(null);

  // =========================
  // HANDLE IMAGE
  // =========================
  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setImage(file);

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
      alert("Please upload an image.");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
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
      alert(
        JSON.stringify(
          error.response?.data || "Prediction failed"
        )
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={{ color: "#222" }}>AI Satellite Road Extraction</h1>

      <input
        type="file"
        accept=".png,.jpg,.jpeg,.tif,.tiff"
        onChange={handleImageChange}
      />

      <br />

      <button onClick={handlePredict} style={styles.button}>
        {loading ? "Predicting..." : "Extract Roads"}
      </button>

      <div style={styles.resultContainer}>
        {serverPreview && (
          <div style={{ marginTop: "40px" }}>
            <h2>Uploaded Image</h2>
            <img src={serverPreview} alt="Preview" style={styles.image} />
          </div>
        )}

        {result && (
          <div style={{ marginTop: "40px" }}>
            <h2>Predicted Road Mask</h2>
            <img src={result} alt="Prediction" style={styles.image} />
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    padding: "30px",
    fontFamily: "Arial",
    background: "#f4f4f4",
    minHeight: "100vh",
  },
  button: {
    marginTop: "20px",
    padding: "12px 24px",
    cursor: "pointer",
    backgroundColor: "#222",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
  },
  image: {
    width: "50%",
    maxWidth: "400px",
    marginTop: "20px",
    borderRadius: "12px",
    border: "2px solid #ccc",
    boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
    objectFit: "contain",
  },
  resultContainer: {
    display: "flex",
    justifyContent: "center",
    gap: "40px",
    marginTop: "40px",
    flexWrap: "wrap",
  },
};

export default App;

