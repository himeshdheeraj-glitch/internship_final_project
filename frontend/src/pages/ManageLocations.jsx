import React, { useState, useEffect } from 'react';
import { locationsService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import { ArrowLeft, Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ManageLocations = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();

  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);

  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedState, setSelectedState] = useState('');

  const [newCountry, setNewCountry] = useState({ name: '', code: '' });
  const [newState, setNewState] = useState({ name: '' });
  const [newCity, setNewCity] = useState({ name: '' });

  const loadCountries = async () => {
    try {
      const data = await locationsService.getCountries();
      setCountries(data || []);
    } catch (e) {
      console.warn(e);
      setCountries(mockCountries);
    }
  };

  useEffect(() => {
    loadCountries();
  }, []);

  useEffect(() => {
    const loadStates = async () => {
      if (selectedCountry) {
        try {
          const list = await locationsService.getStates(selectedCountry);
          setStates(list || []);
          setCities([]);
        } catch (e) {
          setStates(mockStates.filter(s => s.country_id === selectedCountry));
        }
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
          setCities(mockCities.filter(c => c.state_id === selectedState));
        }
      }
    };
    loadCities();
  }, [selectedState]);

  const handleCountrySubmit = async (e) => {
    e.preventDefault();
    if (!newCountry.name.trim() || !newCountry.code.trim()) return;
    try {
      await locationsService.createCountry(newCountry);
      showSuccess('Country created!');
      setNewCountry({ name: '', code: '' });
      loadCountries();
    } catch (err) {
      const obj = { id: Math.random().toString(), ...newCountry };
      setCountries(prev => [...prev, obj]);
      setNewCountry({ name: '', code: '' });
      showSuccess('Country created (mock mode)!');
    }
  };

  const handleStateSubmit = async (e) => {
    e.preventDefault();
    if (!newState.name.trim() || !selectedCountry) return;
    try {
      await locationsService.createState({ name: newState.name, country_id: selectedCountry });
      showSuccess('State created!');
      setNewState({ name: '' });
      // reload states
      const list = await locationsService.getStates(selectedCountry);
      setStates(list || []);
    } catch (err) {
      const obj = { id: Math.random().toString(), name: newState.name, country_id: selectedCountry };
      setStates(prev => [...prev, obj]);
      setNewState({ name: '' });
      showSuccess('State created (mock mode)!');
    }
  };

  const handleCitySubmit = async (e) => {
    e.preventDefault();
    if (!newCity.name.trim() || !selectedState) return;
    try {
      await locationsService.createCity({ name: newCity.name, state_id: selectedState });
      showSuccess('City created!');
      setNewCity({ name: '' });
      // reload cities
      const list = await locationsService.getCities(selectedState);
      setCities(list || []);
    } catch (err) {
      const obj = { id: Math.random().toString(), name: newCity.name, state_id: selectedState };
      setCities(prev => [...prev, obj]);
      setNewCity({ name: '' });
      showSuccess('City created (mock mode)!');
    }
  };

  return (
    <div className="space-y-6 py-6 max-w-5xl mx-auto">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/dashboard')} className="p-2 hover:bg-slate-100 rounded-xl cursor-pointer">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Manage Locations</h1>
          <p className="text-slate-505 text-xs">Configure Geographic taxonomy settings.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Country Section */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">1. Add Country</h3>
          <form onSubmit={handleCountrySubmit} className="space-y-2">
            <input
              type="text"
              required
              placeholder="Country Name (e.g. United States)"
              value={newCountry.name}
              onChange={(e) => setNewCountry({ ...newCountry, name: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
            />
            <input
              type="text"
              required
              placeholder="Code (e.g. US)"
              value={newCountry.code}
              onChange={(e) => setNewCountry({ ...newCountry, code: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
            />
            <button type="submit" className="w-full py-2 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1 cursor-pointer">
              <Plus className="h-4 w-4" /> Add Country
            </button>
          </form>

          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="w-full px-3 py-2 bg-slate-105 border border-slate-200 rounded-xl text-xs"
          >
            <option value="">Select Country to view States</option>
            {countries.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>

        {/* State Section */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">2. Add State</h3>
          <form onSubmit={handleStateSubmit} className="space-y-2">
            <input
              type="text"
              required
              disabled={!selectedCountry}
              placeholder="State Name (e.g. California)"
              value={newState.name}
              onChange={(e) => setNewState({ name: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-indigo-400 disabled:opacity-50"
            />
            <button type="submit" disabled={!selectedCountry} className="w-full py-2 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1 cursor-pointer disabled:opacity-50">
              <Plus className="h-4 w-4" /> Add State
            </button>
          </form>

          {selectedCountry && (
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full px-3 py-2 bg-slate-105 border border-slate-200 rounded-xl text-xs"
            >
              <option value="">Select State to view Cities</option>
              {states.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          )}
        </div>

        {/* City Section */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-800 dark:text-white">3. Add City</h3>
          <form onSubmit={handleCitySubmit} className="space-y-2">
            <input
              type="text"
              required
              disabled={!selectedState}
              placeholder="City Name (e.g. Beverly Hills)"
              value={newCity.name}
              onChange={(e) => setNewCity({ name: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-indigo-400 disabled:opacity-50"
            />
            <button type="submit" disabled={!selectedState} className="w-full py-2 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1 cursor-pointer disabled:opacity-50">
              <Plus className="h-4 w-4" /> Add City
            </button>
          </form>

          {selectedState && (
            <div className="max-h-40 overflow-y-auto border border-slate-100 rounded-xl p-2.5 space-y-1 bg-slate-50">
              {cities.map(c => (
                <div key={c.id} className="text-xs font-semibold text-slate-700">{c.name}</div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const mockCountries = [
  { id: 'in-id', name: 'India', code: 'IN' }
];

const mockStates = [
  { id: 'ka-id', name: 'Karnataka', country_id: 'in-id' },
  { id: 'mh-id', name: 'Maharashtra', country_id: 'in-id' },
  { id: 'dl-id', name: 'Delhi', country_id: 'in-id' },
  { id: 'tg-id', name: 'Telangana', country_id: 'in-id' }
];

const mockCities = [
  { id: 'blr-id', name: 'Bengaluru', state_id: 'ka-id' },
  { id: 'mys-id', name: 'Mysuru', state_id: 'ka-id' },
  { id: 'mum-id', name: 'Mumbai', state_id: 'mh-id' },
  { id: 'pun-id', name: 'Pune', state_id: 'mh-id' },
  { id: 'del-id', name: 'New Delhi', state_id: 'dl-id' },
  { id: 'hyd-id', name: 'Hyderabad', state_id: 'tg-id' }
];

export default ManageLocations;
