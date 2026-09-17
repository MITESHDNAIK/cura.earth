const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000'
    : 'https://cura-earth.onrender.com');

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      response.statusText ||
      `Request failed (${response.status})`;

    throw new Error(detail);
  }

  return data;
}

export const apiService = {
  async sendConversationMessage(payload) {
    return request('/api/v1/conversation/conversation', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async sendChatMessage(payload) {
    return this.sendConversationMessage(payload);
  },

  async performReasoning(environmentalInput) {
    return request('/api/v1/reasoning/reason', {
      method: 'POST',
      body: JSON.stringify(environmentalInput),
    });
  },

  async runSimulation(simulationRequest) {
    return request('/api/v1/simulator/simulate', {
      method: 'POST',
      body: JSON.stringify(simulationRequest),
    });
  },

  async queryKnowledge(query, metricFilter = null) {
    return request('/api/v1/knowledge/query', {
      method: 'POST',
      body: JSON.stringify({
        query,
        metric_filter: metricFilter,
        top_k: 5,
      }),
    });
  },
};