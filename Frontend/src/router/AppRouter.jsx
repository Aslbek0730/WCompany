import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LandingPage from '../pages/LandingPage/LandingPage';
import Login from '../pages/Auth/Login';
import Register from '../pages/Auth/Register';
import DashboardLayout from '../layouts/DashboardLayout';
import Dashboard from '../pages/Dashboard/Dashboard';

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
};

// Public route component (redirects to dashboard if logged in)
const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }
  
  return user ? <Navigate to="/dashboard" /> : children;
};

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route 
          path="/" 
          element={
            <>
              <Header />
              <LandingPage />
              <Footer />
            </>
          } 
        />
        <Route 
          path="/login" 
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } 
        />
        <Route 
          path="/register" 
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          } 
        />

        {/* Protected dashboard routes */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="profile" element={<div>Profile Page - Coming Soon</div>} />
          <Route path="orders" element={<div>Orders Page - Coming Soon</div>} />
          <Route path="declaration" element={<div>Declaration Page - Coming Soon</div>} />
          <Route path="my-code" element={<div>My Code Page - Coming Soon</div>} />
          <Route path="notifications" element={<div>Notifications Page - Coming Soon</div>} />
          <Route path="settings" element={<div>Settings Page - Coming Soon</div>} />
        </Route>

        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;