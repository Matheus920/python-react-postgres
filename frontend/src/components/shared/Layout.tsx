import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Layout: React.FC = () => {
  const { authState, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <Link to="/">Resource Management System</Link>
            </div>
            <nav className="nav">
              <ul className="nav-list">
                <li className="nav-item">
                  <Link to="/resources">Resources</Link>
                </li>
                <li className="nav-item">
                  <Link to="/resources/create">Create Resource</Link>
                </li>
              </ul>
            </nav>
            <div className="user-menu">
              {authState.user && (
                <div className="user-info">
                  <span className="username">{authState.user.username}</span>
                  <button onClick={handleLogout} className="logout-button">
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>
      <main className="main-content">
        <div className="container">
          <Outlet />
        </div>
      </main>
      <footer className="footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} Resource Management System</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
