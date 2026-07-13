import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { FavoriteProvider } from './context/FavoriteContext';
import { NotificationProvider } from './context/NotificationContext';
import { ThemeProvider } from './context/ThemeContext';
import { UserProvider } from './context/UserContext';

// Layouts
import MainLayout from './layouts/MainLayout';
import DashboardLayout from './layouts/DashboardLayout';

// Pages
import Home from './pages/Home';
import PropertyListing from './pages/PropertyListing';
import PropertyDetails from './pages/PropertyDetails';
import AddProperty from './pages/AddProperty';
import EditProperty from './pages/EditProperty';
import Favorites from './pages/Favorites';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import AgentDashboard from './pages/AgentDashboard';
import ManageUsers from './pages/ManageUsers';
import ManageProperties from './pages/ManageProperties';
import ManageAmenities from './pages/ManageAmenities';
import ManageLocations from './pages/ManageLocations';
import ManagePropertyTypes from './pages/ManagePropertyTypes';
import NotFound from './pages/NotFound';

const ProtectedRoute = ({ allowedRoles = [] }) => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="h-8 w-8 border-4 border-indigo-605 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(user?.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <UserProvider>
          <FavoriteProvider>
            <NotificationProvider>
              <Router>
                <Routes>
                  <Route element={<MainLayout />}>
                    {/* Public Routes */}
                    <Route path="/" element={<Home />} />
                    <Route path="/properties" element={<PropertyListing />} />
                    <Route path="/properties/:id" element={<PropertyDetails />} />
                    <Route path="/favorites" element={<Favorites />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    
                    {/* Authenticated general consumer profile */}
                    <Route element={<ProtectedRoute allowedRoles={['buyer', 'agent', 'seller', 'admin']} />}>
                      <Route path="/profile" element={<Profile />} />
                    </Route>

                    {/* Fallback */}
                    <Route path="*" element={<NotFound />} />
                  </Route>

                  {/* Dashboard Layout - Role Protected */}
                  <Route path="/dashboard" element={<DashboardLayout />}>
                    <Route element={<ProtectedRoute allowedRoles={['agent', 'seller', 'admin']} />}>
                      <Route index element={<AgentDashboard />} />
                      <Route path="properties/new" element={<AddProperty />} />
                      <Route path="properties/:id/edit" element={<EditProperty />} />
                    </Route>
                    <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                      <Route path="users" element={<ManageUsers />} />
                      <Route path="properties" element={<ManageProperties />} />
                      <Route path="amenities" element={<ManageAmenities />} />
                      <Route path="locations" element={<ManageLocations />} />
                      <Route path="types" element={<ManagePropertyTypes />} />
                    </Route>
                  </Route>
                </Routes>
              </Router>
            </NotificationProvider>
          </FavoriteProvider>
        </UserProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
