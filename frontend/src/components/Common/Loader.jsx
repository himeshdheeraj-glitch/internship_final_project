import React from 'react';

const Loader = () => {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-3">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 border-4 border-indigo-200 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-indigo-605 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <span className="text-sm font-bold text-slate-500 tracking-wide">Loading Premium Content...</span>
    </div>
  );
};

export default Loader;
