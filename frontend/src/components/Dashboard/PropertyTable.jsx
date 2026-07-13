import React from 'react';
import { Link } from 'react-router-dom';
import { Edit, Trash, Eye } from 'lucide-react';

const PropertyTable = ({ properties = [], onDelete }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(Number(price) || 0);
  };

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-850 text-xs font-bold uppercase tracking-wider text-slate-500">
              <th className="px-6 py-4">Title</th>
              <th className="px-6 py-4">Location</th>
              <th className="px-6 py-4 text-right">Price</th>
              <th className="px-6 py-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm text-slate-700 dark:text-slate-350">
            {properties.map((p) => (
              <tr key={p.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-950/20 transition-colors">
                <td className="px-6 py-4 font-bold text-slate-800 dark:text-slate-100">{p.title}</td>
                <td className="px-6 py-4">{p.address}, {p.city?.name || 'Local'}</td>
                <td className="px-6 py-4 text-right font-extrabold text-indigo-900 dark:text-indigo-400">{formatPrice(p.price)}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center justify-center gap-2">
                    <Link to={`/properties/${p.id}`} className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-slate-800 rounded-lg">
                      <Eye className="h-4.5 w-4.5" />
                    </Link>
                    <Link to={`/dashboard/properties/${p.id}/edit`} className="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-amber-50 dark:hover:bg-slate-800 rounded-lg">
                      <Edit className="h-4.5 w-4.5" />
                    </Link>
                    <button onClick={() => onDelete(p.id)} className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-slate-800 rounded-lg cursor-pointer">
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
  );
};

export default PropertyTable;
