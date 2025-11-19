/**
 * API Client Service
 * Handles all HTTP requests to the backend API
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail?.message || error.message || 'An error occurred';
    return Promise.reject(new Error(message));
  }
);

/**
 * Fetch top headlines
 * @param {Object} params - Query parameters
 * @returns {Promise} API response
 */
export const getHeadlines = async (params = {}) => {
  return await apiClient.get('/api/headlines', { params });
};

/**
 * Search news articles
 * @param {Object} params - Query parameters
 * @returns {Promise} API response
 */
export const searchNews = async (params = {}) => {
  return await apiClient.get('/api/search', { params });
};

/**
 * Get available filter options
 * @returns {Promise} API response
 */
export const getFilters = async () => {
  return await apiClient.get('/api/filters');
};

/**
 * Check API health
 * @returns {Promise} API response
 */
export const checkHealth = async () => {
  return await apiClient.get('/health');
};

export default apiClient;
