import React from 'react';

export const PropertyCardSkeleton = () => {
  return (
    <div className="bg-white rounded-3xl border border-slate-200 p-4 space-y-4 animate-pulse">
      <div className="aspect-4/3 bg-slate-100 rounded-2xl" />
      <div className="h-4 bg-slate-150 rounded w-2/3" />
      <div className="h-4 bg-slate-150 rounded w-1/2" />
      <div className="h-8 bg-slate-150 rounded-xl" />
    </div>
  );
};

export const TableSkeleton = ({ rows = 5 }) => {
  return (
    <div className="space-y-4 animate-pulse w-full">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 items-center py-3 border-b border-slate-100">
          <div className="h-10 w-10 bg-slate-150 rounded-xl" />
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-slate-150 rounded w-1/3" />
            <div className="h-3 bg-slate-150 rounded w-1/4" />
          </div>
          <div className="h-8 w-20 bg-slate-150 rounded-lg" />
        </div>
      ))}
    </div>
  );
};

export const DetailsSkeleton = () => {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="h-400 bg-slate-150 rounded-3xl" />
      <div className="h-8 bg-slate-150 rounded w-1/3" />
      <div className="h-4 bg-slate-150 rounded w-1/2" />
      <div className="h-24 bg-slate-150 rounded-2xl" />
    </div>
  );
};
