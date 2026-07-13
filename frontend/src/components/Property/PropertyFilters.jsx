import React, { useState, useEffect } from 'react';
import { propertyService, locationsService } from '../../services/api';
import { Filter, RotateCcw, Bed, Bath } from 'lucide-react';

const PropertyFilters = ({ filters, onFilterChange }) => {
  const [propertyTypes, setPropertyTypes] = useState([]);
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedState, setSelectedState] = useState('');

  useEffect(() => {
    const loadMetadata = async () => {
      try {
        const [types, countryList] = await Promise.all([
          propertyService.getPropertyTypes(),
          locationsService.getCountries()
        ]);
        setPropertyTypes(types || []);
        setCountries(countryList || []);
      } catch (err) {
        console.warn('Metadata loader offline.');
      }
    };
    loadMetadata();
  }, []);

  useEffect(() => {
    const loadStates = async () => {
      if (selectedCountry) {
        try {
          const list = await locationsService.getStates(selectedCountry);
          setStates(list || []);
          setCities([]);
        } catch (e) {
          console.error(e);
        }
      } else {
        setStates([]);
        setCities([]);
      }
    };
    loadStates();
  }, [selectedCountry]);

  useEffect(() => {
    const loadCities = async () => {
      if (selectedState) {
        try {
          const list = await locationsService.getCities(selectedState);
          setCities(list || []);
        } catch (e) {
          console.error(e);
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
      search_query: '',
      purpose: undefined,
      parking: undefined,
      furnishing_status: undefined
    });
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-sm space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
        <h2 className="text-base font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <Filter className="h-4.5 w-4.5 text-indigo-600" />
          <span>Filters</span>
        </h2>
        <button
          onClick={handleReset}
          className="text-xs font-semibold text-slate-500 hover:text-indigo-650 flex items-center gap-1 cursor-pointer"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          <span>Clear All</span>
        </button>
      </div>

      {/* Purpose */}
      <div className="space-y-2">
        <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Purpose</label>
        <select
          value={filters.purpose || ''}
          onChange={(e) => handleChange('purpose', e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
        >
          <option value="">All Purposes</option>
          <option value="🏡 For Sale">🏡 For Sale</option>
          <option value="🏠 For Rent">🏠 For Rent</option>
          <option value="🏢 Lease">🏢 Lease</option>
          <option value="🌾 Land Investment">🌾 Land Investment</option>
        </select>
      </div>

      {/* Furnishing Status */}
      <div className="space-y-2">
        <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Furnishing Status</label>
        <select
          value={filters.furnishing_status || ''}
          onChange={(e) => handleChange('furnishing_status', e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
        >
          <option value="">All Statuses</option>
          <option value="Unfurnished">Unfurnished</option>
          <option value="Semi-Furnished">Semi-Furnished</option>
          <option value="Furnished">Furnished</option>
        </select>
      </div>

      {/* Parking */}
      <div className="space-y-2">
        <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Parking</label>
        <select
          value={filters.parking === undefined ? '' : filters.parking.toString()}
          onChange={(e) => handleChange('parking', e.target.value === '' ? '' : e.target.value === 'true')}
          className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
        >
          <option value="">Any Parking</option>
          <option value="true">Available</option>
          <option value="false">None</option>
        </select>
      </div>

      {/* Country */}
      <div className="space-y-2">
        <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Country</label>
        <select
          value={selectedCountry}
          onChange={(e) => setSelectedCountry(e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
        >
          <option value="">All Countries</option>
          {countries.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      {/* State */}
      {selectedCountry && (
        <div className="space-y-2">
          <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">State</label>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
          >
            <option value="">All States</option>
            {states.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
      )}

      {/* City */}
      {selectedState && (
        <div className="space-y-2">
          <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">City</label>
          <select
            value={filters.city_id || ''}
            onChange={(e) => handleChange('city_id', e.target.value)}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
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
        <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Property Type</label>
        <select
          value={filters.property_type_id || ''}
          onChange={(e) => handleChange('property_type_id', e.target.value)}
          className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-700 dark:text-slate-300 focus:outline-none"
        >
          <option value="">All Types</option>
          {propertyTypes.map((type) => (
            <option key={type.id} value={type.id}>{type.name}</option>
          ))}
        </select>
      </div>

      {/* Bedrooms */}
      <div className="space-y-2">
        <label className="block text-2xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Bedrooms</label>
        <div className="grid grid-cols-5 gap-1">
          {['', '1', '2', '3', '4+'].map((opt) => {
            const val = opt.includes('+') ? '4' : opt;
            const isSel = (opt === '' && !filters.bedrooms) || (filters.bedrooms?.toString() === val);
            return (
              <button
                key={opt}
                type="button"
                onClick={() => handleChange('bedrooms', val === '' ? '' : parseInt(val))}
                className={`py-1.5 text-xs font-bold rounded-lg border transition-all cursor-pointer ${
                  isSel
                    ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                    : 'bg-white dark:bg-slate-950 border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300'
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

export default PropertyFilters;
