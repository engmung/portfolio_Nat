const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fetchKnowledgeFiles = async () => {
  const response = await fetch(`${API_URL}/api/knowledge/files`);
  if (!response.ok) {
    throw new Error('Failed to fetch knowledge files');
  }
  return response.json();
};

export const createKnowledgeFile = async (data) => {
  const response = await fetch(`${API_URL}/api/knowledge/files`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('Failed to create knowledge file');
  }
  return response.json();
};

export const updateKnowledgeFile = async (filename, data) => {
  const response = await fetch(`${API_URL}/api/knowledge/files/${filename}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('Failed to update knowledge file');
  }
  return response.json();
};

export const deleteKnowledgeFile = async (filename) => {
  const response = await fetch(`${API_URL}/api/knowledge/files/${filename}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete knowledge file');
  }
  return response.json();
};

export const queryAI = async (query) => {
  const response = await fetch(`${API_URL}/api/ai/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  if (!response.ok) {
    throw new Error('Failed to query AI');
  }
  return response.json();
};
