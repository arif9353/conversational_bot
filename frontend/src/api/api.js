import axios from "axios";

const API_BASE = "http://localhost:8000"; // change if needed

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE}/ingest`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const sendChat = async (payload) => {
  const response = await axios.post(`${API_BASE}/chat`, payload);
  return response.data;
};