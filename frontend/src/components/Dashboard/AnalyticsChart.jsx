import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Jan', views: 4000, value: 2400 },
  { name: 'Feb', views: 3000, value: 1398 },
  { name: 'Mar', views: 2000, value: 9800 },
  { name: 'Apr', views: 2780, value: 3908 },
  { name: 'May', views: 1890, value: 4800 },
  { name: 'Jun', views: 2390, value: 3800 },
  { name: 'Jul', views: 3490, value: 4300 },
];

const AnalyticsChart = () => {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-205 dark:border-slate-800 rounded-3xl p-6 shadow-sm">
      <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Viewers & Pricing Growth</h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorViews" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#4f46e5" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            <XAxis dataKey="name" tickLine={false} axisLine={false} style={{ fontSize: '12px', fill: '#94a3b8' }} />
            <YAxis tickLine={false} axisLine={false} style={{ fontSize: '12px', fill: '#94a3b8' }} />
            <Tooltip />
            <Area type="monotone" dataKey="views" stroke="#4f46e5" strokeWidth={2.5} fillOpacity={1} fill="url(#colorViews)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AnalyticsChart;
