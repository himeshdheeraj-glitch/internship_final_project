import React from 'react';
import { Bed, Bath, Maximize, Sparkles, Car, Layers, Tag } from 'lucide-react';

const PropertyFeatures = ({ property }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Bed className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Bedrooms</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100">{property.bedrooms} Beds</span>
        </div>
      </div>

      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Bath className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Bathrooms</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100">{property.bathrooms} Baths</span>
        </div>
      </div>

      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Maximize className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Floor Area</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100">{property.area} sqft</span>
        </div>
      </div>

      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Listing status</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100 capitalize">{property.status || 'Published'}</span>
        </div>
      </div>

      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Tag className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Purpose</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100">{property.purpose || 'For Sale'}</span>
        </div>
      </div>

      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Layers className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Furnishing</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100 capitalize">{property.furnishing_status || 'Unfurnished'}</span>
        </div>
      </div>

      <div className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center gap-3 shadow-sm">
        <div className="p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605">
          <Car className="h-5 w-5" />
        </div>
        <div>
          <span className="block text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wide">Parking</span>
          <span className="font-extrabold text-slate-800 dark:text-slate-100">{property.parking ? 'Available' : 'None'}</span>
        </div>
      </div>
    </div>
  );
};

export default PropertyFeatures;
