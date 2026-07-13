import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useUser } from '../context/UserContext';
import { useNotifications } from '../context/NotificationContext';
import { User, Save, Shield } from 'lucide-react';

const Profile = () => {
  const { user } = useAuth();
  const { updateProfile, updating } = useUser();
  const { showSuccess, showError } = useNotifications();

  const [form, setForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
  });

  useEffect(() => {
    setForm({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
    });
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateProfile(form);
      showSuccess('Profile details saved!');
    } catch (err) {
      showError('Failed to update profile details.');
    }
  };

  return (
    <div className="max-w-xl mx-auto px-4 py-10 space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">Account Settings</h1>
        <p className="text-slate-505 dark:text-slate-400 text-sm">Review credentials and personal metadata.</p>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-3xl shadow-sm space-y-6">
        <div className="flex items-center gap-3 pb-4 border-b border-slate-100 dark:border-slate-850">
          <div className="p-3 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-650 rounded-2xl">
            <User className="h-6 w-6" />
          </div>
          <div>
            <h3 className="font-bold text-slate-800 dark:text-white text-sm">{user?.email}</h3>
            <span className="inline-flex items-center gap-1 text-2xs text-indigo-650 font-bold uppercase tracking-wider mt-0.5">
              <Shield className="h-3 w-3" />
              <span>{user?.role} level</span>
            </span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">First Name</label>
              <input
                type="text"
                required
                value={form.first_name}
                onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>
            
            <div className="space-y-1">
              <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Last Name</label>
              <input
                type="text"
                required
                value={form.last_name}
                onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={updating}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-sm shadow-md flex items-center justify-center gap-2 cursor-pointer transition-colors"
          >
            <Save className="h-4 w-4" />
            <span>{updating ? 'Saving...' : 'Save Settings'}</span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default Profile;
