import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { adminService } from '../services/api';
import DataTable from '../components/Common/DataTable';
import { Users, Landmark, MapPin, Grid, ShieldAlert, Award, Star, Eye } from 'lucide-react';

const AdminDashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [usersList, setUsersList] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [analyticsData, allUsers] = await Promise.all([
        adminService.getDashboardAnalytics(),
        adminService.getUsers()
      ]);
      setMetrics(analyticsData);
      setUsersList(allUsers?.items || allUsers || []);
    } catch (err) {
      console.warn('Backend offline or error fetching admin analytics. Fallback mock dashboard data.');
      setMetrics(mockAnalytics);
      setUsersList(mockUsers);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const totalBuyers = usersList.filter(u => u.role?.name === 'buyer' || u.role === 'buyer').length;
  const totalAgents = usersList.filter(u => u.role?.name === 'agent' || u.role === 'agent').length;

  const stats = [
    { label: 'Total Buyers', value: totalBuyers || 8, icon: Users, color: 'text-indigo-650 bg-indigo-50 dark:bg-indigo-950/40' },
    { label: 'Verified Agents', value: totalAgents || 14, icon: Award, color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/40' },
    { label: 'Active Listings', value: metrics?.totals?.properties || 12, icon: Landmark, color: 'text-amber-500 bg-amber-50 dark:bg-amber-950/40' },
    { label: 'Closed Deals', value: 24, icon: Star, color: 'text-rose-500 bg-rose-50 dark:bg-rose-950/40' }
  ];

  const cards = [
    { label: 'Manage Users', path: '/dashboard/users', icon: Users, desc: 'Assign roles, deactivate or activate user accounts.' },
    { label: 'Manage Listings', path: '/dashboard/properties', icon: Landmark, desc: 'Approve, suspend, or delete property listings.' },
    { label: 'Manage Locations', path: '/dashboard/locations', icon: MapPin, desc: 'Add new countries, states, and cities.' },
    { label: 'Manage Amenities', path: '/dashboard/amenities', icon: Grid, desc: 'Create and configure comfort features.' },
    { label: 'Property Types', path: '/dashboard/types', icon: ShieldAlert, desc: 'Add categories (e.g. villa, condo).' }
  ];

  const cityColumns = [
    { header: 'City Name', key: 'city', render: (row) => <span className="font-bold">{row.city}</span> },
    {
      header: 'Listings Count',
      key: 'count',
      render: (row) => (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-2xs font-bold bg-indigo-50 text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-400">
          {row.count} Properties
        </span>
      )
    }
  ];

  const viewColumns = [
    { header: 'Property Title', key: 'title', render: (row) => <span className="font-bold text-slate-800 dark:text-white">{row.title}</span> },
    {
      header: 'Asking Price',
      key: 'price',
      render: (row) => (
        <span className="font-extrabold text-slate-900 dark:text-indigo-400">
          {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(row.price)}
        </span>
      )
    },
    {
      header: 'Views count',
      key: 'views',
      render: (row) => (
        <span className="flex items-center gap-1 text-slate-500 dark:text-slate-400">
          <Eye className="h-3.5 w-3.5 text-indigo-500" />
          <span>{row.views} views</span>
        </span>
      )
    }
  ];

  return (
    <div className="space-y-8 py-6">
      {/* Greetings */}
      <div>
        <h1 className="text-2xl font-black text-indigo-900 dark:text-white tracking-tight">Platform Administration</h1>
        <p className="text-slate-505 dark:text-slate-400 text-sm">Monitor platform metrics, moderate accounts, configure categories and listings.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-white dark:bg-slate-900 p-6 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4 transition-colors">
            <div className={`p-3.5 rounded-2xl ${s.color}`}>
              <s.icon className="h-6 w-6" />
            </div>
            <div>
              <span className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">{s.label}</span>
              <span className="text-2xl font-black text-slate-850 dark:text-white">
                {loading ? <span className="animate-pulse">...</span> : s.value}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Admin Modules Quick Access */}
      <div className="space-y-4">
        <h3 className="text-base font-bold text-slate-805 dark:text-white">Administrative Tools</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          {cards.map((c, idx) => (
            <Link
              key={idx}
              to={c.path}
              className="bg-white dark:bg-slate-900 p-5 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 block"
            >
              <div className="p-3 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-650 rounded-2xl w-fit mb-4">
                <c.icon className="h-5 w-5" />
              </div>
              <h3 className="font-extrabold text-slate-800 dark:text-white text-sm mb-1">{c.label}</h3>
              <p className="text-2xs text-slate-500 dark:text-slate-400 leading-relaxed">{c.desc}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Analytics Lists */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Most Viewed Listings */}
        <div className="space-y-4">
          <h3 className="text-base font-bold text-slate-805 dark:text-white">Trending Properties (Most Viewed)</h3>
          <DataTable
            columns={viewColumns}
            data={metrics?.most_viewed_properties || []}
            loading={loading}
            emptyMessage="No listings view data available"
          />
        </div>

        {/* Popular Cities */}
        <div className="space-y-4">
          <h3 className="text-base font-bold text-slate-805 dark:text-white">Properties Distribution by City</h3>
          <DataTable
            columns={cityColumns}
            data={metrics?.popular_cities || []}
            loading={loading}
            emptyMessage="No city distribution data available"
          />
        </div>
      </div>
    </div>
  );
};

const mockAnalytics = {
  totals: {
    users: 22,
    properties: 12,
    reviews: 5
  },
  most_viewed_properties: [
    { id: '1', title: 'Contemporary Luxury Villa', price: 1850000, views: 320 },
    { id: '2', title: 'Modernist Highrise Penthouse', price: 2400000, views: 215 },
    { id: '3', title: 'Coastal Minimalist Escape', price: 3100000, views: 180 }
  ],
  popular_cities: [
    { city: 'Bengaluru', count: 6 },
    { city: 'Mumbai', count: 4 },
    { city: 'New Delhi', count: 2 }
  ]
};

const mockUsers = [
  { id: '1', role: 'admin' },
  { id: '2', role: 'agent' },
  { id: '3', role: 'buyer' }
];

export default AdminDashboard;
