import React, { useState, useEffect } from 'react';
import { amenitiesService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import { ArrowLeft, Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ManageAmenities = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();
  
  const [amenities, setAmenities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newAmenity, setNewAmenity] = useState({ name: '', description: '' });

  const loadAmenities = async () => {
    try {
      const data = await amenitiesService.getAmenities();
      setAmenities(data || []);
    } catch (e) {
      console.warn('API Offline. Fallback mock list.');
      setAmenities(mockAmenitiesList);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAmenities();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newAmenity.name.trim()) return;
    try {
      const added = await amenitiesService.createAmenity(newAmenity);
      showSuccess('Amenity created successfully!');
      setNewAmenity({ name: '', description: '' });
      loadAmenities();
    } catch (err) {
      // Mock addition
      const mockObj = { id: Math.random().toString(), name: newAmenity.name, description: newAmenity.description };
      setAmenities(prev => [...prev, mockObj]);
      setNewAmenity({ name: '', description: '' });
      showSuccess('Amenity created (mock mode)!');
    }
  };

  return (
    <div className="space-y-6 py-6 max-w-4xl mx-auto">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-100 rounded-xl cursor-pointer">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Manage Amenities</h1>
          <p className="text-slate-505 text-xs">Configure amenities available for property listings.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
        {/* Form */}
        <div className="md:col-span-1 bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">Add Amenity</h3>
          <form onSubmit={handleAdd} className="space-y-3">
            <div className="space-y-1">
              <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Name</label>
              <input
                type="text"
                required
                placeholder="e.g. Infinity Pool"
                value={newAmenity.name}
                onChange={(e) => setNewAmenity({ ...newAmenity, name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Description</label>
              <input
                type="text"
                placeholder="Brief description"
                value={newAmenity.description}
                onChange={(e) => setNewAmenity({ ...newAmenity, description: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-955 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>

            <button type="submit" className="w-full py-2 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1 cursor-pointer">
              <Plus className="h-4 w-4" />
              <span>Create Amenity</span>
            </button>
          </form>
        </div>

        {/* List */}
        <div className="md:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">Existing Amenities</h3>
          {loading ? (
            <div className="animate-pulse h-10 bg-slate-100 rounded-xl" />
          ) : (
            <div className="grid grid-cols-2 gap-2">
              {amenities.map((a) => (
                <div key={a.id} className="p-3 bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-850 rounded-xl">
                  <div className="font-bold text-xs text-slate-800 dark:text-white">{a.name}</div>
                  <div className="text-2xs text-slate-400 dark:text-slate-500 mt-0.5">{a.description || 'No description'}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const mockAmenitiesList = [
  { id: '1', name: 'Infinity Pool', description: 'Zero-edge high luxury pool' },
  { id: '2', name: 'Smart Home Automation', description: 'Full audio/visual and security controls' }
];

export default ManageAmenities;
