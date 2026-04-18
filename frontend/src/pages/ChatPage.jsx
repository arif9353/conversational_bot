import { useState, useEffect, useRef } from "react";
import { sendChat } from "../api/api";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [imagePopup, setImagePopup] = useState(null);

  const chatEndRef = useRef(null);

  const session_id = "session_1"; // simple for now
  const file_name = localStorage.getItem("file_name");
  const dataset_context = localStorage.getItem("dataset_context");

  // auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);
    setInput("");

    try {
      const data = await sendChat({
        query: input,
        session_id,
        file_name,
        dataset_context,
      });

      const botMessage = {
        role: "assistant",
        text: data.text,
        base64: data.base64,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      
      {/* Chat Messages */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "20px",
        background: "#f5f5f5"
      }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{
            marginBottom: "15px",
            textAlign: msg.role === "user" ? "right" : "left"
          }}>
            <div style={{
              display: "inline-block",
              padding: "10px",
              borderRadius: "10px",
              background: msg.role === "user" ? "#007bff" : "#e0e0e0",
              color: msg.role === "user" ? "#fff" : "#000",
              maxWidth: "60%"
            }}>
              {msg.text}
            </div>

            {/* Visualization Button */}
            {msg.base64 && msg.base64 !== "" && (
              <div>
                <button
                  style={{ marginTop: "5px" }}
                  onClick={() => setImagePopup(msg.base64)}
                >
                  View Visualization 📊
                </button>
              </div>
            )}
          </div>
        ))}

        <div ref={chatEndRef} />
      </div>

      {/* Input Box */}
      <div style={{
        padding: "10px",
        borderTop: "1px solid #ccc",
        display: "flex"
      }}>
        <input
          style={{ flex: 1, padding: "10px" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something about your data..."
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>

      {/* Popup Modal */}
      {imagePopup && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background: "rgba(0,0,0,0.7)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center"
        }}>
          <div style={{ background: "#fff", padding: "20px", borderRadius: "10px" }}>
            <img
              src={`data:image/png;base64,${imagePopup}`}
              alt="Visualization"
              style={{ maxWidth: "600px" }}
            />
            <br />
            <button onClick={() => setImagePopup(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}