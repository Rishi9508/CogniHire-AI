const API_BASE = '/api';

class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...options.headers,
    },
    ...options,
  };

  if (options.body && !(options.body instanceof FormData)) {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      errorData = { detail: response.statusText };
    }
    throw new ApiError(
      errorData.detail || errorData.message || `Request failed with status ${response.status}`,
      response.status,
      errorData
    );
  }

  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  }

  return response;
}

export const api = {
  // Jobs
  createJob: (data) => request('/jobs', { method: 'POST', body: data }),
  getJobs: () => request('/jobs'),
  getJob: (id) => request(`/jobs/${id}`),
  deleteJob: (id) => request(`/jobs/${id}`, { method: 'DELETE' }),

  // Candidates
  uploadCandidates: (files) => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    return request('/candidates/upload', { method: 'POST', body: formData });
  },
  getCandidates: () => request('/candidates'),
  getCandidate: (id) => request(`/candidates/${id}`),
  deleteCandidate: (id) => request(`/candidates/${id}`, { method: 'DELETE' }),

  // Rankings
  computeRankings: (jobId) => request(`/rankings/compute/${jobId}`, { method: 'POST' }),
  getRankings: (jobId) => request(`/rankings/${jobId}`),

  // Export
  exportCSV: (jobId) => request(`/export/${jobId}`),

  // Health
  healthCheck: () => request('/health'),
};

export default api;
