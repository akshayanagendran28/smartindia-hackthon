import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to requests if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('scheme_sathi_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getMe: () => api.get('/auth/me'),
};

export const profileAPI = {
  getProfile: () => api.get('/profile'),
  updateProfile: (data) => api.put('/profile', data),
};

export const schemesAPI = {
  getAll: (params) => api.get('/schemes', { params }),
  getById: (id) => api.get(`/schemes/${id}`),
};

export const matchingAPI = {
  analyze: (data) => api.post('/matching/analyze', data),
  checkEligibility: (schemeId, data) => api.post(`/matching/eligibility/check/${schemeId}`, data),
};

export const financeAPI = {
  calculateEmi: (data) => api.post('/finance/emi', data),
};

export const documentsAPI = {
  upload: (formData) => api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserDocuments: () => api.get('/documents'),
  getStatus: (id) => api.get(`/documents/${id}/status`),
  rerunOcr: (id) => api.post(`/documents/${id}/ocr`),
  rerunValidate: (id) => api.post(`/documents/${id}/validate`),
  triggerVerify: (id) => api.post(`/documents/${id}/verify`),
  getSyntheticSamples: () => api.get('/documents/synthetic-samples'),
  loadSyntheticSample: (docKey, schemeCode) => 
    api.post(`/documents/load-synthetic/${docKey}${schemeCode ? `?scheme_code=${schemeCode}` : ''}`),
  getAuditLogs: (id) => api.get(`/documents/audit-logs/${id}`),
  deleteDocument: (id) => api.delete(`/documents/${id}`),
  runDirectPipeline: (formData) => api.post('/documents/pipeline', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getSchemeChecklist: (schemeId) => api.get(`/documents/scheme/${schemeId}/checklist`),
};

export const partnersAPI = {
  getAll: (params) => api.get('/partners', { params }),
  getRecommended: (params) => api.get('/partners/recommended', { params }),
};

export const chatAPI = {
  sendMessage: (data) => api.post('/chat/message', data),
};

export const notificationsAPI = {
  getAll: () => api.get('/notifications'),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
};

export const adminAPI = {
  getDashboard: () => api.get('/admin/dashboard'),
  createScheme: (data) => api.post('/admin/schemes', data),
  updateScheme: (id, data) => api.put(`/admin/schemes/${id}`, data),
  deleteScheme: (id) => api.delete(`/admin/schemes/${id}`),
  createRule: (data) => api.post('/admin/rules', data),
  createPartner: (data) => api.post('/admin/partners', data),
  getUsers: () => api.get('/admin/users'),
};

export default api;
