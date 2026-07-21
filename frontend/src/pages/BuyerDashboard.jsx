import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useFavorites } from '../context/FavoriteContext';
import { favoritesService } from '../services/api';
import PropertyCard from '../components/Property/PropertyCard';
import DataTable from '../components/Common/DataTable';
import { Heart, Mail, Search, MessageSquare, Landmark } from 'lucide-react';
import dayjs from 'dayjs';

const BuyerDashboard = () => {
  const { user } = useAuth();
  const { favorites } = useFavorites();
  const [favoriteProps, setFavoriteProps] = useState([]);
  const [inquiries, setInquiries] = useState([]);
  const [loadingFavs, setLoadingFavs] = useState(true);
  const [activeTab, setActiveTab] = useState('favorites');

  useEffect(() => {
    const loadFavorites = async () => {
      setLoadingFavs(true);
      try {
        const response = await favoritesService.getFavorites({ page: 1, size: 50 });
        const items = response?.items || [];
        const props = items.map(item => item.property).filter(Boolean);
        setFavoriteProps(props);
      } catch (err) {
        console.warn("API offline or error fetching favorites. Using empty list.");
        setFavoriteProps([]);
      } finally {
        setLoadingFavs(false);
      }
    };
    loadFavorites();
  }, [favorites]);

  useEffect(() => {
    // Load sent inquiries from localStorage
    const localInquiries = localStorage.getItem('inquiries');
    if (localInquiries) {
      const allInquiries = JSON.parse(localInquiries);
      // Filter by current buyer's email or ID if available
      const userInquiries = allInquiries.filter(
        inq => inq.buyer_id === user?.id || inq.buyer_email === user?.email
      );
      setInquiries(userInquiries);
    }
  }, [user]);

  const stats = [
    { label: 'Saved Listings', value: favorites.length, icon: Heart, color: 'text-rose-500 bg-rose-50 dark:bg-rose-950/30' },
    { label: 'Inquiries Sent', value: inquiries.length, icon: Mail, color: 'text-indigo-650 bg-indigo-50 dark:bg-indigo-950/30' },
    { label: 'Saved Searches', value: 2, icon: Search, color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/30' }
  ];

  const inquiryColumns = [
    {
      header: 'Date & Time',
      key: 'created_at',
      render: (row) => dayjs(row.created_at).format('MMM DD, YYYY hh:mm A')
    },
    {
      header: 'Property Details',
      key: 'property_title',
      render: (row) => (
        <div>
          <span className="font-bold text-slate-800 dark:text-white block">{row.property_title}</span>
          <span className="text-xs text-slate-400">{row.property_address}</span>
        </div>
      )
    },
    {
      header: 'Agent / Broker',
      key: 'agent_name',
      render: (row) => (
        <div>
          <span className="font-bold text-slate-700 dark:text-slate-200 block">{row.agent_name || 'Verified Broker'}</span>
          <span className="text-xs text-slate-450">{row.agent_email}</span>
        </div>
      )
    },
    {
      header: 'Your Message',
      key: 'message',
      render: (row) => <p className="max-w-xs truncate text-xs text-slate-500 dark:text-slate-400">{row.message}</p>
    },
    {
      header: 'Status',
      key: 'status',
      render: () => (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-3xs font-extrabold uppercase bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-450">
          Sent
        </span>
      )
    }
  ];

  return (
    <div className="space-y-8 py-6">
      {/* Greetings */}
      <div>
        <h1 className="text-2xl font-black text-indigo-900 dark:text-white tracking-tight">
          Welcome back, {user?.first_name || 'Guest Buyer'}!
        </h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm">
          Track your favorite property listings, review agent responses, and manage saved searches.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-white dark:bg-slate-900 p-6 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4 transition-colors">
            <div className={`p-3.5 rounded-2xl ${s.color}`}>
              <s.icon className="h-6 w-6" />
            </div>
            <div>
              <span className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">{s.label}</span>
              <span className="text-2xl font-black text-slate-800 dark:text-white">{s.value}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Tabs Menu */}
      <div className="flex border-b border-slate-200 dark:border-slate-800 gap-6">
        <button
          onClick={() => setActiveTab('favorites')}
          className={`pb-3 font-extrabold text-sm border-b-2 transition-all cursor-pointer ${
            activeTab === 'favorites'
              ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
              : 'border-transparent text-slate-400 dark:text-slate-500 hover:text-slate-650'
          }`}
        >
          My Favorites ({favorites.length})
        </button>
        <button
          onClick={() => setActiveTab('inquiries')}
          className={`pb-3 font-extrabold text-sm border-b-2 transition-all cursor-pointer ${
            activeTab === 'inquiries'
              ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
              : 'border-transparent text-slate-400 dark:text-slate-500 hover:text-slate-650'
          }`}
        >
          Sent Inquiries ({inquiries.length})
        </button>
        <button
          onClick={() => setActiveTab('searches')}
          className={`pb-3 font-extrabold text-sm border-b-2 transition-all cursor-pointer ${
            activeTab === 'searches'
              ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
              : 'border-transparent text-slate-400 dark:text-slate-500 hover:text-slate-650'
          }`}
        >
          Saved Searches
        </button>
      </div>

      {/* Active Tab Panels */}
      <div>
        {activeTab === 'favorites' && (
          <div className="space-y-6">
            {loadingFavs ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[1, 2, 3].map((n) => (
                  <div key={n} className="bg-white rounded-3xl border border-slate-200 p-4 space-y-4 animate-pulse">
                    <div className="aspect-4/3 bg-slate-200 rounded-2xl" />
                    <div className="h-4 bg-slate-200 rounded w-2/3" />
                  </div>
                ))}
              </div>
            ) : favoriteProps.length === 0 ? (
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-12 text-center transition-colors">
                <Heart className="h-10 w-10 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
                <h4 className="font-extrabold text-slate-800 dark:text-white mb-1">No Favorite Properties Yet</h4>
                <p className="text-slate-500 dark:text-slate-450 text-xs mb-4">Properties you heart will show up here.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {favoriteProps.map((property) => (
                  <PropertyCard key={property.id} property={property} />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'inquiries' && (
          <DataTable
            columns={inquiryColumns}
            data={inquiries}
            emptyMessage="No inquiries sent yet. Go to Browse Properties to contact agents."
          />
        )}

        {activeTab === 'searches' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 transition-colors shadow-sm space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-extrabold text-slate-800 dark:text-white text-base">Malibu Beach Houses</h4>
                  <p className="text-slate-500 dark:text-slate-450 text-xs">Filters: Location: Malibu, Min Price: $1M, Beds: 3+</p>
                </div>
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-3xs font-extrabold uppercase bg-indigo-50 text-indigo-700 dark:bg-indigo-950/30 dark:text-indigo-400">
                  Weekly Alerts
                </span>
              </div>
              <button className="w-full text-center py-2 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 font-extrabold text-xs rounded-xl hover:bg-indigo-50 hover:text-indigo-650 transition-colors border border-slate-200 dark:border-slate-850">
                Run Search Again
              </button>
            </div>

            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 transition-colors shadow-sm space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-extrabold text-slate-800 dark:text-white text-base">Luxury Apartments Bangalore</h4>
                  <p className="text-slate-500 dark:text-slate-450 text-xs">Filters: Location: Bengaluru, Type: Apartment</p>
                </div>
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-3xs font-extrabold uppercase bg-indigo-50 text-indigo-700 dark:bg-indigo-950/30 dark:text-indigo-400">
                  Instant Alerts
                </span>
              </div>
              <button className="w-full text-center py-2 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 font-extrabold text-xs rounded-xl hover:bg-indigo-50 hover:text-indigo-650 transition-colors border border-slate-200 dark:border-slate-850">
                Run Search Again
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BuyerDashboard;
