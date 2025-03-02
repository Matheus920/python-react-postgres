import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { ApiError } from '../types/common';

// Create a custom axios instance
const axiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    // Disable caching by default
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Expires': '0',
  },
  // Disable automatic redirect following to handle redirects manually
  maxRedirects: 0,
  // Consider all status codes as valid to handle redirects manually
  validateStatus: (status: number) => true,
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
    
    return config;
  },
  (error: AxiosError): Promise<AxiosError> => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling redirects and errors
axiosInstance.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse | Promise<AxiosResponse> => {
    console.log('Response successful:', response.config.url);
    console.log('Response status:', response.status);
    console.log('Response data type:', typeof response.data);
    
    // For debugging resource API calls
    if (response.config.url?.includes('/resources')) {
      console.log('Resource API response:', {
        url: response.config.url,
        method: response.config.method,
        params: response.config.params,
        data: response.data
      });
    }
    
    // Handle redirects manually
    if (response.status >= 300 && response.status < 400 && response.headers.location) {
      console.log('Handling redirect to:', response.headers.location);
      
      // Create a new request to the redirect location with the same headers
      const redirectUrl = response.headers.location;
      
      // If the redirect URL is relative, prepend the baseURL
      const fullRedirectUrl = redirectUrl.startsWith('http') 
        ? redirectUrl 
        : `${axiosInstance.defaults.baseURL}${redirectUrl}`;
      
      console.log('Full redirect URL:', fullRedirectUrl);
      
      // Make a new request to the redirect location with the same headers
      return axiosInstance({
        url: fullRedirectUrl,
        method: response.config.method,
        headers: {
          ...response.config.headers,
          // Ensure cache headers are included in the redirect
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
          'Expires': '0',
        },
        params: response.config.params,
        data: response.config.data,
      });
    }
    
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
      
      // Only clear token and redirect if not on login page and not a redirect
      const isRedirect = error.config?.url?.includes('?') || error.config?.url?.endsWith('/');
      
      if (!isRedirect) {
        // Clear token and redirect to login if not already on login page
        localStorage.removeItem('token');
        console.log('Token removed from localStorage due to 401 error');
        
        if (window.location.pathname !== '/login') {
          console.log('Redirecting to login page');
          window.location.href = '/login';
        }
      } else {
        console.log('Not clearing token for redirect-related 401');
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
