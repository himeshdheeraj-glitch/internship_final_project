import React from 'react';
import { Home } from 'lucide-react';

const EmptyState = ({ title = 'No Listings Found', message = 'Try clearing some search metrics or add your own listings.', actionLink, actionLabel }) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center bg-white dark:bg-slate-900 rounded-3xl border border-dashed border-slate-300 p-8">
      <div className="p-4 bg-indigo-50 dark:bg-indigo-950 rounded-full text-indigo-650 mb-4">
        <Home className="h-8 w-8" />
      </div>
      <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-1">{title}</h3>
      <p className="text-slate-500 dark:text-slate-400 text-sm max-w-md mb-6">{message}</p>
      {actionLink && actionLabel && (
        <a
          href={actionLink}
          className="px-5 py-2.5 font-bold text-white bg-indigo-600 hover:bg-indigo-700 transition-colors rounded-xl shadow-md"
        >
          {actionLabel}
        </a>
      )}
    </div>
  );
};

export default EmptyState;
