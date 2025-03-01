import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/shared/Layout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ResourceListPage from './pages/ResourceListPage';
import ResourceDetailPage from './pages/ResourceDetailPage';
import ResourceCreateEditPage from './pages/ResourceCreateEditPage';
import ProtectedRoute from './components/auth/ProtectedRoute';
import './App.css';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected routes */}
        <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route path="/resources" element={<ResourceListPage />} />
          <Route path="/resources/create" element={<ResourceCreateEditPage />} />
          <Route path="/resources/:id" element={<ResourceDetailPage />} />
          <Route path="/resources/:id/edit" element={<ResourceCreateEditPage />} />
          <Route path="/" element={<Navigate to="/resources" replace />} />
        </Route>
        
        {/* Redirect any unknown routes to resources */}
        <Route path="*" element={<Navigate to="/resources" replace />} />
      </Routes>
    </AuthProvider>
  );
};

export default App;
