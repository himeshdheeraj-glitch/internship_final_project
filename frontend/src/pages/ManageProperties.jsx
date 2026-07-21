import React, { useState, useEffect } from 'react';
import { adminService, propertyService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import DataTable from '../components/Common/DataTable';
import { ArrowLeft, Trash, CheckCircle, AlertTriangle, Eye } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';

const ManageProperties = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadProperties = async () => {
    setLoading(true);
    try {
      const data = await adminService.getAdminProperties({ limit: 100 });
      setProperties(data?.items || data || []);
    } catch (e) {
      console.warn('API Offline. Fallback to mock listings.');
      setProperties(mockProps);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProperties();
  }, []);

  const handleUpdateStatus = async (id, statusVal) => {
    try {
      await adminService.updatePropertyStatus(id, statusVal);
      showSuccess(`Property listing status updated to ${statusVal}!`);
      loadProperties();
    } catch (err) {
      // Local state fallback update for offline mode
      setProperties(prev => prev.map(p => p.id === id ? { ...p, status: statusVal } : p));
      showSuccess(`Status updated to ${statusVal} (mock mode)!`);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Override and permanently delete this property listing from the platform?')) {
      try {
        await propertyService.deleteProperty(id);
        showSuccess('Property listing permanently deleted.');
        loadProperties();
      } catch (err) {
        setProperties(prev => prev.filter(p => p.id !== id));
        showSuccess('Property deleted (mock mode).');
      }
    }
  };

  const propertyColumns = [
    {
      header: 'Listing details',
      key: 'title',
      render: (row) => (
        <div>
          <span className="font-bold text-slate-800 dark:text-white block">{row.title}</span>
          <span className="text-xs text-slate-500">{row.address}, {row.city?.name || 'Local'}</span>
        </div>
      )
    },
    {
      header: 'Owner / Agent',
      key: 'owner',
      render: (row) => (
        <div>
          <span className="font-bold text-slate-700 dark:text-slate-200 block">
            {row.owner?.first_name ? `${row.owner.first_name} ${row.owner.last_name}` : 'Platform Seed'}
          </span>
          <span className="text-xs text-slate-450 block">{row.owner?.email || 'system@estatehub.com'}</span>
        </div>
      )
    },
    {
      header: 'Asking Price',
      key: 'price',
      render: (row) => (
        <span className="font-extrabold text-indigo-900 dark:text-indigo-400">
          {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(row.price)}
        </span>
      )
    },
    {
      header: 'Status',
      key: 'status',
      render: (row) => {
        const isPub = row.status === 'published';
        const isSusp = row.status === 'suspended';
        return (
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-2xs font-extrabold uppercase ${
            isPub
              ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400'
              : isSusp
              ? 'bg-rose-50 text-rose-700 dark:bg-rose-950/30 dark:text-rose-455'
              : 'bg-amber-50 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400'
          }`}>
            {row.status || 'published'}
          </span>
        );
      }
    },
    {
      header: 'Moderate / Moderate Status',
      key: 'actions',
      render: (row) => {
        const isPub = row.status === 'published';
        return (
          <div className="flex items-center gap-2">
            <Link
              to={`/properties/${row.id}`}
              className="p-1.5 text-slate-400 hover:text-indigo-650 hover:bg-indigo-50 rounded-lg"
              title="View Live Listing"
            >
              <Eye className="h-4.5 w-4.5" />
            </Link>
            
            {isPub ? (
              <button
                onClick={() => handleUpdateStatus(row.id, 'suspended')}
                className="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg cursor-pointer"
                title="Suspend Listing"
              >
                <AlertTriangle className="h-4.5 w-4.5" />
              </button>
            ) : (
              <button
                onClick={() => handleUpdateStatus(row.id, 'published')}
                className="p-1.5 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg cursor-pointer"
                title="Approve / Publish Listing"
              >
                <CheckCircle className="h-4.5 w-4.5" />
              </button>
            )}

            <button
              onClick={() => handleDelete(row.id)}
              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg cursor-pointer"
              title="Delete Listing"
            >
              <Trash className="h-4.5 w-4.5" />
            </button>
          </div>
        );
      }
    }
  ];

  return (
    <div className="space-y-6 py-6">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-850 rounded-xl cursor-pointer text-slate-650 dark:text-slate-350">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Moderate Listings</h1>
          <p className="text-slate-500 text-xs">Verify, suspend, or override property listings published across the platform.</p>
        </div>
      </div>

      <DataTable
        columns={propertyColumns}
        data={properties}
        loading={loading}
        emptyMessage="No property listings published on the platform."
      />
    </div>
  );
};

const mockProps = [
  {
    id: 'f1025de4-d2e8-468b-b1a9-b1d5a71df544',
    title: 'Contemporary Luxury Villa',
    address: '892 Beverly Estates Dr',
    price: 1850000,
    status: 'published',
    city: { name: 'Beverly Hills' },
    owner: { first_name: 'Jonathan', last_name: 'Doe', email: 'jonathan.doe@antigravity.com' }
  },
  {
    id: 'a8d9b1a5-cfb8-4903-bce5-8bb2d63428ff',
    title: 'Modernist Highrise Penthouse',
    address: '404 Skyline Ave',
    price: 2400000,
    status: 'pending',
    city: { name: 'New York' },
    owner: { first_name: 'Sarah', last_name: 'Conner', email: 'sarah.c@broker.com' }
  }
];

export default ManageProperties;
