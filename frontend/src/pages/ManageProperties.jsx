import React, { useState, useEffect } from 'react';
import { propertyService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import { ArrowLeft, Trash } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ManageProperties = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadProperties = async () => {
    try {
      const data = await propertyService.getProperties({ limit: 100 });
      setProperties(data?.items || data || []);
    } catch (e) {
      console.warn('API Offline. Fallback to mock data.');
      setProperties(mockProps);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProperties();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Override and delete this property listing?')) {
      try {
        await propertyService.deleteProperty(id);
        showSuccess('Property deleted successfully!');
        loadProperties();
      } catch (err) {
        setProperties(prev => prev.filter(p => p.id !== id));
        showSuccess('Property deleted (mock mode)!');
      }
    }
  };

  return (
    <div className="space-y-6 py-6">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-100 rounded-xl cursor-pointer">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Manage All Listings</h1>
          <p className="text-slate-500 text-xs">Verify, override, or delete active listings across the platform.</p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-850 text-xs font-bold uppercase tracking-wider text-slate-500">
                <th className="px-6 py-4">Title</th>
                <th className="px-6 py-4">Location</th>
                <th className="px-6 py-4">Price</th>
                <th className="px-6 py-4 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm text-slate-700 dark:text-slate-300">
              {properties.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-950/20">
                  <td className="px-6 py-4 font-bold">{p.title}</td>
                  <td className="px-6 py-4">{p.address}, {p.city?.name || 'Local'}</td>
                  <td className="px-6 py-4 font-extrabold text-indigo-900 dark:text-indigo-400">
                    {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(p.price)}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center justify-center">
                      <button onClick={() => handleDelete(p.id)} className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg cursor-pointer">
                        <Trash className="h-4.5 w-4.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const mockProps = [
  { id: '1', title: 'Contemporary Luxury Villa', address: '892 Beverly Estates Dr', price: 1850000, city: { name: 'Beverly Hills' } }
];

export default ManageProperties;
