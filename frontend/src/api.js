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

export async function deleteSession(sessionId) {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`, {
    method: 'DELETE',
  });
  return response.ok;
}

export async function updateBloodTest(sessionId, testId, updatedData) {
  const response = await fetch(`${API_URL}/sessions/${sessionId}/tests/${testId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedData),
  });
  return response.json();
}
