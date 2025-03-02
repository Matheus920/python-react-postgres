import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { ApiError } from '../types/common';

// Create a custom axios instance
const axiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  // Enable automatic redirect following
  maxRedirects: 5,
  // Preserve the Authorization header during redirects
  validateStatus: (status: number) => status >= 200 && status < 400,
});

// Request interceptor for adding auth token
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = localStorage.getItem('token');
    console.log('Request interceptor - Token from localStorage:', token);
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Setting Authorization header:', `Bearer ${token}`);
      console.log('Request URL:', config.url);
      console.log('Request method:', config.method);
    } else {
      console.log('No token found in localStorage or no headers in config');
    }
    
    // Preserve Authorization header during redirects
    if (config.headers) {
      config.headers['Cache-Control'] = 'no-cache';
      // This ensures that the Authorization header is preserved during redirects
      if (!config.maxRedirects) {
        config.maxRedirects = 5;
      }
      if (!config.withCredentials) {
        config.withCredentials = true;
      }
    }
    
    return config;
  },
  (error: AxiosError): Promise<AxiosError> => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
axiosInstance.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => {
    console.log('Response successful:', response.config.url);
    return response;
  },
  (error: AxiosError): Promise<AxiosError> => {
    console.error('Response error:', error);
    console.error('Response error status:', error.response?.status);
    console.error('Response error data:', error.response?.data);
    console.error('Request URL that failed:', error.config?.url);
    console.error('Request method that failed:', error.config?.method);
    console.error('Request headers:', error.config?.headers);
    
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      console.error('401 Unauthorized error detected');
      
      // Clear token and redirect to login if not already on login page
      localStorage.removeItem('token');
      console.log('Token removed from localStorage due to 401 error');
      
      if (window.location.pathname !== '/login') {
        console.log('Redirecting to login page');
        window.location.href = '/login';
      }
    }

    // Format error for consistent handling
    const apiError: ApiError = {
      status: error.response?.status || 500,
      message: error.message || 'An unexpected error occurred',
      detail: error.response?.data && typeof error.response.data === 'object' && 'detail' in error.response.data 
        ? (error.response.data as any).detail 
        : '',
    };
    
    console.error('Formatted API error:', apiError);

    return Promise.reject(apiError);
  }
);

export default axiosInstance;
