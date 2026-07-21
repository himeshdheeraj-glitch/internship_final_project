import React, { useState, useEffect } from 'react';
import { Search, MapPin, DollarSign, Home } from 'lucide-react';

const SearchBar = ({ onSearch, initialQuery = '', initialMinPrice = '', initialMaxPrice = '' }) => {
  const [query, setQuery] = useState(initialQuery);
  const [minPrice, setMinPrice] = useState(initialMinPrice);
  const [maxPrice, setMaxPrice] = useState(initialMaxPrice);

  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  useEffect(() => {
    setMinPrice(initialMinPrice);
  }, [initialMinPrice]);

  useEffect(() => {
    setMaxPrice(initialMaxPrice);
  }, [initialMaxPrice]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({
      search_query: query,
      min_price: minPrice,
      max_price: maxPrice,
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-4xl bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border border-slate-200/60 dark:border-slate-800 rounded-3xl p-3 sm:p-4 shadow-xl flex flex-col md:flex-row items-center gap-3"
    >
      {/* Search Input */}
      <div className="w-full grow flex items-center gap-2 px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-800 rounded-2xl focus-within:border-indigo-300 transition-colors">
        <Search className="h-5 w-5 text-indigo-500 shrink-0" />
        <input
          type="text"
          placeholder="Search by city, address or title..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full bg-transparent border-0 outline-none text-slate-800 dark:text-white text-sm placeholder-slate-400 focus:ring-0 focus:outline-none"
        />
      </div>

      {/* Min Price */}
      <div className="w-full md:w-44 flex items-center gap-2 px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-800 rounded-2xl focus-within:border-indigo-300 transition-colors">
        <DollarSign className="h-5 w-5 text-emerald-500 shrink-0" />
        <input
          type="number"
          placeholder="Min Price"
          value={minPrice}
          onChange={(e) => setMinPrice(e.target.value)}
          className="w-full bg-transparent border-0 outline-none text-slate-800 dark:text-white text-sm placeholder-slate-400 focus:ring-0 focus:outline-none"
        />
      </div>

      {/* Max Price */}
      <div className="w-full md:w-44 flex items-center gap-2 px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-800 rounded-2xl focus-within:border-indigo-300 transition-colors">
        <DollarSign className="h-5 w-5 text-emerald-500 shrink-0" />
        <input
          type="number"
          placeholder="Max Price"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          className="w-full bg-transparent border-0 outline-none text-slate-800 dark:text-white text-sm placeholder-slate-400 focus:ring-0 focus:outline-none"
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        className="w-full md:w-auto px-6 py-3 font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition-colors rounded-2xl flex items-center justify-center gap-2 shadow-lg shadow-indigo-200 shrink-0"
      >
        <Search className="h-4 w-4" />
        <span>Search</span>
      </button>
    </form>
  );
};

export default SearchBar;
