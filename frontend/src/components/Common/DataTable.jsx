import React from 'react';
import Loader from './Loader';

/**
 * Reusable DataTable component
 * @param {Array} columns - Array of { header: string, key: string, render: function }
 * @param {Array} data - Array of row objects
 * @param {boolean} loading - Loading state indicator
 * @param {string} emptyMessage - Custom empty message text
 */
const DataTable = ({
  columns = [],
  data = [],
  loading = false,
  emptyMessage = "No records found"
}) => {
  return (
    <div className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm transition-colors duration-300">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 text-2xs font-bold uppercase tracking-widest text-slate-400 dark:text-slate-500">
              {columns.map((col, idx) => (
                <th key={col.key || idx} className="px-6 py-4.5 font-extrabold text-left">
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm text-slate-700 dark:text-slate-350">
            {loading ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center">
                  <div className="flex flex-col items-center justify-center gap-3">
                    <Loader />
                    <span className="text-xs font-semibold text-slate-400">Loading data...</span>
                  </div>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center">
                  <span className="text-xs font-bold text-slate-450 dark:text-slate-500 uppercase tracking-wider block">
                    {emptyMessage}
                  </span>
                </td>
              </tr>
            ) : (
              data.map((row, rowIdx) => (
                <tr
                  key={row.id || rowIdx}
                  className="hover:bg-slate-50/50 dark:hover:bg-slate-950/20 transition-colors"
                >
                  {columns.map((col, colIdx) => (
                    <td key={col.key || colIdx} className="px-6 py-4.5">
                      {col.render ? col.render(row) : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
