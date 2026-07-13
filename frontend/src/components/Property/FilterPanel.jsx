import React, { useState, useEffect } from 'react';
import { propertyService, locationsService } from '../../services/api';
import { Filter, RotateCcw, Bed, Bath, Landmark, MapPin } from 'lucide-react';

const FilterPanel = ({ filters, onFilterChange }) => {
  const [propertyTypes, setPropertyTypes] = useState([]);
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedState, setSelectedState] = useState('');

  useEffect(() => {
    // Load metadata
    const loadMetadata = async () => {
      try {
        const [typesRes, countriesRes] = await Promise.all([
          propertyService.getPropertyTypes(),
          locationsService.getCountries(),
        ]);
        setPropertyTypes(typesRes || []);
        setCountries(countriesRes || []);
      } catch (err) {
        console.error('Failed to load filter metadata', err);
      }
    };
    loadMetadata();
  }, []);

  // Handle Country Change
  useEffect(() => {
    const loadStates = async () => {
      if (selectedCountry) {
        try {
          const res = await locationsService.getStates(selectedCountry);
          setStates(res || []);
          setCities([]);
        } catch (err) {
          console.error(err);
        }
      } else {
        setStates([]);
        setCities([]);
      }
    };
    loadStates();
  }, [selectedCountry]);

  // Handle State Change
  useEffect(() => {
    const loadCities = async () => {
      if (selectedState) {
        try {
          const res = await locationsService.getCities(selectedState);
          setCities(res || []);
        } catch (err) {
          console.error(err);
        }
      } else {
        setCities([]);
      }
    };
    loadCities();
  }, [selectedState]);

  const handleChange = (name, value) => {
    onFilterChange({
      ...filters,
      [name]: value === '' ? undefined : value,
    });
  };

  const handleReset = () => {
    setSelectedCountry('');
    setSelectedState('');
    onFilterChange({
      city_id: undefined,
      property_type_id: undefined,
      bedrooms: undefined,
      bathrooms: undefined,
      min_price: undefined,
      max_price: undefined,
    });
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm sticky top-24 space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100">
        <h2 className="text-lg font-bold text-slate-800 flex items-center gap-2">
          <Filter className="h-5 w-5 text-indigo-600" />
          <span>Filters</span>
        </h2>
        <button
          onClick={handleReset}
          className="text-xs font-semibold text-slate-500 hover:text-indigo-650 flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          <span>Reset All</span>
        </button>
      </div>

      {/* Country Selection */}
      <div className="space-y-2">
        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Country</label>
        <div className="relative">
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700 focus:outline-none focus:border-indigo-400 focus:bg-white"
          >
            <option value="">All Countries</option>
            {countries.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* State Selection */}
      {selectedCountry && (
        <div className="space-y-2">
          <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">State</label>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700 focus:outline-none focus:border-indigo-400 focus:bg-white"
          >
            <option value="">All States</option>
            {states.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
      )}

      {/* City Selection */}
      {selectedState && (
        <div className="space-y-2">
          <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">City</label>
          <select
            value={filters.city_id || ''}
            onChange={(e) => handleChange('city_id', e.target.value)}
            className="w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700 focus:outline-none focus:border-indigo-400 focus:bg-white"
          >
            <option value="">All Cities</option>
            {cities.map((city) => (
              <option key={city.id} value={city.id}>{city.name}</option>
            ))}
          </select>
        </div>
      )}

      {/* Property Type */}
      <div className="space-y-2">
        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Property Type</label>
        <select
          value={filters.property_type_id || ''}
          onChange={(e) => handleChange('property_type_id', e.target.value)}
          className="w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700 focus:outline-none focus:border-indigo-400 focus:bg-white"
        >
          <option value="">All Types</option>
          {propertyTypes.map((type) => (
            <option key={type.id} value={type.id}>{type.name}</option>
          ))}
        </select>
      </div>

      {/* Bedrooms */}
      <div className="space-y-2">
        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Bedrooms</label>
        <div className="grid grid-cols-5 gap-1.5">
          {['', '1', '2', '3', '4+'].map((opt) => {
            const val = opt.includes('+') ? '4' : opt;
            const isSel = (opt === '' && !filters.bedrooms) || (filters.bedrooms?.toString() === val);
            return (
              <button
                key={opt}
                type="button"
                onClick={() => handleChange('bedrooms', val === '' ? '' : parseInt(val))}
                className={`py-2 text-xs font-bold rounded-xl border transition-all cursor-pointer ${
                  isSel
                    ? 'bg-indigo-650 text-white border-indigo-650 shadow-sm'
                    : 'bg-white border-slate-200 text-slate-700 hover:border-indigo-300'
                }`}
              >
                {opt || 'Any'}
              </button>
            );
          })}
        </div>
      </div>

      {/* Bathrooms */}
      <div className="space-y-2">
        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Bathrooms</label>
        <div className="grid grid-cols-5 gap-1.5">
          {['', '1', '2', '3', '4+'].map((opt) => {
            const val = opt.includes('+') ? '4' : opt;
            const isSel = (opt === '' && !filters.bathrooms) || (filters.bathrooms?.toString() === val);
            return (
              <button
                key={opt}
                type="button"
                onClick={() => handleChange('bathrooms', val === '' ? '' : parseInt(val))}
                className={`py-2 text-xs font-bold rounded-xl border transition-all cursor-pointer ${
                  isSel
                    ? 'bg-indigo-650 text-white border-indigo-650 shadow-sm'
                    : 'bg-white border-slate-200 text-slate-700 hover:border-indigo-300'
                }`}
              >
                {opt || 'Any'}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;
