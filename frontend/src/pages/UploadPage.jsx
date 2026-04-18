import FileUpload from "../components/FileUpload";

export default function UploadPage({ onUploadSuccess }) {
  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "100px" }}>
      <FileUpload onUploadSuccess={onUploadSuccess} />
    </div>
  );
}