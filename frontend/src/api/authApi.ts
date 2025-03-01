import axios from '../utils/axios';
import { AuthToken, LoginCredentials, User, UserCreate } from '../types/auth';

export const authApi = {
  /**
   * Login with username/email and password
   */
  async login(credentials: LoginCredentials): Promise<AuthToken> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await axios.post<AuthToken>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },
  
  /**
   * Register a new user
   */
  async register(userData: UserCreate): Promise<User> {
    const response = await axios.post<User>('/auth/register', userData);
    return response.data;
  },
  
  /**
   * Get the current user's profile
   */
  async getCurrentUser(): Promise<User> {
    const response = await axios.get<User>('/users/me');
    return response.data;
  },
  
  /**
   * Logout the current user (client-side only)
   */
  logout(): void {
    localStorage.removeItem('token');
  },
  
  /**
   * Check if the user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  },
  
  /**
   * Set the authentication token
   */
  setToken(token: string): void {
    localStorage.setItem('token', token);
  },
  
  /**
   * Get the authentication token
   */
  getToken(): string | null {
    return localStorage.getItem('token');
  },
};
