import React from 'react';
import { Link } from 'react-router-dom';
import { Users, Landmark, MapPin, Grid, ShieldAlert } from 'lucide-react';

const AdminDashboard = () => {
  const cards = [
    { label: 'Manage Platform Users', path: '/dashboard/users', icon: Users, desc: 'Assign roles, activate or ban accounts.' },
    { label: 'Manage All Listings', path: '/dashboard/properties', icon: Landmark, desc: 'Verify, override or delete properties.' },
    { label: 'Manage Locations', path: '/dashboard/locations', icon: MapPin, desc: 'Add new cities, states, and countries.' },
    { label: 'Manage Amenities', path: '/dashboard/amenities', icon: Grid, desc: 'Create and configure comfort features.' },
    { label: 'Manage Property Types', path: '/dashboard/types', icon: ShieldAlert, desc: 'Add categories (e.g. villa, condo).' },
  ];

  return (
    <div className="space-y-8 py-6">
      <div>
        <h1 className="text-2xl font-black text-indigo-900 dark:text-white tracking-tight">Admin Administration</h1>
        <p className="text-slate-505 dark:text-slate-400 text-sm">Configure system endpoints, access logs, and taxonomy options.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cards.map((c, idx) => (
          <Link
            key={idx}
            to={c.path}
            className="bg-white dark:bg-slate-900 p-6 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 block"
          >
            <div className="p-3 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-650 rounded-2xl w-fit mb-4">
              <c.icon className="h-6 w-6" />
            </div>
            <h3 className="font-extrabold text-slate-800 dark:text-white text-base mb-1">{c.label}</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{c.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;
