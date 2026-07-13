import React from 'react';
import { Landmark, Eye, Heart, DollarSign } from 'lucide-react';

const DashboardStats = ({ stats }) => {
  const items = [
    { label: 'Active Listings', value: stats?.listings || 0, icon: Landmark, color: 'text-indigo-600 bg-indigo-50 dark:bg-indigo-950/40' },
    { label: 'Total Views', value: stats?.views || 0, icon: Eye, color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/40' },
    { label: 'Favorited Count', value: stats?.favorites || 0, icon: Heart, color: 'text-rose-500 bg-rose-50 dark:bg-rose-950/40' },
    { label: 'Avg Listing Value', value: stats?.avgPrice || '$0', icon: DollarSign, color: 'text-amber-500 bg-amber-50 dark:bg-amber-950/40' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
      {items.map((item, idx) => (
        <div key={idx} className="bg-white dark:bg-slate-905 border border-slate-200 dark:border-slate-800 p-5 rounded-3xl shadow-sm flex items-center gap-4">
          <div className={`p-3 rounded-2xl ${item.color} shrink-0`}>
            <item.icon className="h-6 w-6" />
          </div>
          <div>
            <span className="block text-2xs font-extrabold uppercase tracking-wider text-slate-400">{item.label}</span>
            <span className="text-xl font-extrabold text-slate-800 dark:text-white mt-0.5 block">{item.value}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DashboardStats;
