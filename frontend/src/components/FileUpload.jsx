import { useState } from "react";
import { uploadFile } from "../api/api";

export default function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
  if (!file) {
    setMessage("Please select a file");
    return;
  }

  try {
    setLoading(true);
    setMessage("");

    const data = await uploadFile(file);

    localStorage.setItem("dataset_context", data.context);
    localStorage.setItem("file_name", file.name);

    setMessage("File uploaded successfully ✅");

    // 🔥 THIS LINE IS CRITICAL
    if (onUploadSuccess) {
      onUploadSuccess();
    }

  } catch (error) {
    console.error(error);
    setMessage("Upload failed ❌");
  } finally {
    setLoading(false);
  }
};

  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "10px" }}>
      <h2>Upload Dataset</h2>

      <input type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} />

      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      <p>{message}</p>
    </div>
  );
}