import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authApi } from '../api/authApi';
import { User, AuthState } from '../types/auth';

// Initial auth state
const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  loading: true,
  error: null,
};

// Create context
const AuthContext = createContext<{
  authState: AuthState;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
}>({
  authState: initialState,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

// Provider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>(initialState);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (authApi.isAuthenticated()) {
        try {
          const user = await authApi.getCurrentUser();
          setAuthState({
            isAuthenticated: true,
            user,
            loading: false,
            error: null,
          });
        } catch (error) {
          console.error('Failed to get current user:', error);
          authApi.logout();
          setAuthState({
            isAuthenticated: false,
            user: null,
            loading: false,
            error: 'Session expired. Please login again.',
          });
        }
      } else {
        setAuthState({
          isAuthenticated: false,
          user: null,
          loading: false,
          error: null,
        });
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (username: string, password: string) => {
    try {
      setAuthState({ ...authState, loading: true, error: null });
      
      const authToken = await authApi.login({ username, password });
      authApi.setToken(authToken.access_token);
      
      const user = await authApi.getCurrentUser();
      
      setAuthState({
        isAuthenticated: true,
        user,
        loading: false,
        error: null,
      });
    } catch (error) {
      console.error('Login failed:', error);
      setAuthState({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: 'Invalid username or password',
      });
    }
  };

  // Register function
  const register = async (email: string, username: string, password: string) => {
    try {
      setAuthState({ ...authState, loading: true, error: null });
      
      await authApi.register({ email, username, password });
      
      // Login after successful registration
      await login(username, password);
    } catch (error) {
      console.error('Registration failed:', error);
      setAuthState({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: 'Registration failed. Please try again.',
      });
    }
  };

  // Logout function
  const logout = () => {
    authApi.logout();
    setAuthState({
      isAuthenticated: false,
      user: null,
      loading: false,
      error: null,
    });
  };

  return (
    <AuthContext.Provider value={{ authState, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);
