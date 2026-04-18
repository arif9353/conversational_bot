import UploadPage from "./pages/UploadPage";
import ChatPage from "./pages/ChatPage";
import { useState, useEffect } from "react";

function App() {
  const [uploaded, setUploaded] = useState(false);

  useEffect(() => {
    // clear on reload
    localStorage.removeItem("dataset_context");
    localStorage.removeItem("file_name");
  }, []);

  return uploaded ? (
    <ChatPage />
  ) : (
    <UploadPage onUploadSuccess={() => setUploaded(true)} />
  );
}

export default App;