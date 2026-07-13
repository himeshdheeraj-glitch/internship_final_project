import React, { useState, useEffect } from 'react';
import { propertyService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import { ArrowLeft, Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ManagePropertyTypes = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();
  
  const [types, setTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newType, setNewType] = useState({ name: '', description: '' });

  const loadTypes = async () => {
    try {
      const data = await propertyService.getPropertyTypes();
      setTypes(data || []);
    } catch (e) {
      console.warn('API Offline.');
      setTypes(mockTypesList);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTypes();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newType.name.trim()) return;
    try {
      await propertyService.createPropertyType(newType);
      showSuccess('Property type created successfully!');
      setNewType({ name: '', description: '' });
      loadTypes();
    } catch (err) {
      const obj = { id: Math.random().toString(), name: newType.name, description: newType.description };
      setTypes(prev => [...prev, obj]);
      setNewType({ name: '', description: '' });
      showSuccess('Property type created (mock mode)!');
    }
  };

  return (
    <div className="space-y-6 py-6 max-w-4xl mx-auto">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-100 rounded-xl cursor-pointer">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Manage Property Types</h1>
          <p className="text-slate-505 text-xs">Configure category types (e.g. villa, apartment, townhouse).</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
        {/* Form */}
        <div className="md:col-span-1 bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">Add Property Type</h3>
          <form onSubmit={handleAdd} className="space-y-3">
            <div className="space-y-1">
              <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Name</label>
              <input
                type="text"
                required
                placeholder="e.g. Villa"
                value={newType.name}
                onChange={(e) => setNewType({ ...newType, name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Description</label>
              <input
                type="text"
                placeholder="Brief description"
                value={newType.description}
                onChange={(e) => setNewType({ ...newType, description: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-955 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
              />
            </div>

            <button type="submit" className="w-full py-2 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1 cursor-pointer">
              <Plus className="h-4 w-4" />
              <span>Create Type</span>
            </button>
          </form>
        </div>

        {/* List */}
        <div className="md:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">Existing Categories</h3>
          {loading ? (
            <div className="animate-pulse h-10 bg-slate-100 rounded-xl" />
          ) : (
            <div className="grid grid-cols-2 gap-2">
              {types.map((t) => (
                <div key={t.id} className="p-3 bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-850 rounded-xl">
                  <div className="font-bold text-xs text-slate-800 dark:text-white">{t.name}</div>
                  <div className="text-2xs text-slate-400 dark:text-slate-500 mt-0.5">{t.description || 'No description'}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const mockTypesList = [
  { id: '1', name: 'Apartment', description: 'Multi-family residential unit' },
  { id: '2', name: 'Villa', description: 'High-end freestanding estate' }
];

export default ManagePropertyTypes;
