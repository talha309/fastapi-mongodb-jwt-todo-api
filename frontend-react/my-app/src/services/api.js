import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authService = {
  signup: (email, password) => api.post('/signup', { email, password }),
  login: (email, password) => api.post('/login', { email, password }),
};

export const todoService = {
  getAll: () => api.get('/todos'),
  getById: (id) => api.get(`/todos/${id}`),
  create: (title, description) => api.post('/todos', { title, description }),
  update: (id, title, description) => api.put(`/todos/${id}`, { title, description }),
  delete: (id) => api.delete(`/todos/${id}`),
};

export default api;
