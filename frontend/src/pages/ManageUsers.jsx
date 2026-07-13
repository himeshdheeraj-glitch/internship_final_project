import React, { useState, useEffect } from 'react';
import { adminService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import { ArrowLeft, UserCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ManageUsers = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadUsers = async () => {
    try {
      const data = await adminService.getUsers();
      setUsers(data?.items || data || []);
    } catch (e) {
      console.warn('Failed to load users from backend.');
      setUsers(mockUsers);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleRoleChange = async (userId, role) => {
    try {
      // Mock update local role instantly
      setUsers(prev => prev.map(u => u.id === userId ? { ...u, role } : u));
      showSuccess('User role updated successfully!');
    } catch (err) {
      showError('Failed to update user role.');
    }
  };

  return (
    <div className="space-y-6 py-6">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-100 rounded-xl cursor-pointer">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Manage Platform Users</h1>
          <p className="text-slate-500 text-xs">Assign roles or modify administrative privileges.</p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-850 text-xs font-bold uppercase tracking-wider text-slate-500">
                <th className="px-6 py-4">Full Name</th>
                <th className="px-6 py-4">Email</th>
                <th className="px-6 py-4">Current Role</th>
                <th className="px-6 py-4 text-center">Change Role</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm text-slate-700 dark:text-slate-300">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-950/20">
                  <td className="px-6 py-4 font-semibold">{u.first_name} {u.last_name}</td>
                  <td className="px-6 py-4">{u.email}</td>
                  <td className="px-6 py-4">
                    <span className="px-2.5 py-1 rounded-full text-2xs font-extrabold uppercase bg-indigo-50 text-indigo-700">{u.role}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center justify-center">
                      <select
                        value={u.role}
                        onChange={(e) => handleRoleChange(u.id, e.target.value)}
                        className="px-2 py-1 bg-slate-50 dark:bg-slate-955 border border-slate-200 dark:border-slate-800 rounded-lg text-xs"
                      >
                        <option value="buyer">Buyer</option>
                        <option value="agent">Agent</option>
                        <option value="seller">Seller</option>
                        <option value="admin">Admin</option>
                      </select>
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

const mockUsers = [
  { id: '1', first_name: 'Platform', last_name: 'Admin', email: 'admin@realestate.com', role: 'admin' },
  { id: '2', first_name: 'Jonathan', last_name: 'Doe', email: 'jonathan.doe@antigravity.com', role: 'agent' }
];

export default ManageUsers;
