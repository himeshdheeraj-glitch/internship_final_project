import React from 'react';
import { useAuth } from '../context/AuthContext';
import AdminDashboard from './AdminDashboard';
import AgentDashboard from './AgentDashboard';
import BuyerDashboard from './BuyerDashboard';
import Loader from '../components/Common/Loader';

const DashboardHome = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-[50vh] flex items-center justify-center bg-slate-50 dark:bg-slate-900">
        <Loader />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="p-8 text-center text-rose-500 font-bold bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl">
        Please sign in to access the dashboard.
      </div>
    );
  }

  // Dynamic rendering based on normalized role name
  const role = user.role?.toLowerCase() || 'buyer';

  switch (role) {
    case 'admin':
      return <AdminDashboard />;
    case 'agent':
      return <AgentDashboard />;
    case 'buyer':
    default:
      return <BuyerDashboard />;
  }
};

export default DashboardHome;
