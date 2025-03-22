// api.js
const API_URL = "http://localhost:8000";

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  return response.json();
}

export async function fetchSessions() {
  const response = await fetch(`${API_URL}/sessions`);
  return response.json();
}

export async function fetchSessionDetails(sessionId) {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`);
  return response.json();
}
