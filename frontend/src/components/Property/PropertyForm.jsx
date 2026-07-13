import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { propertyService, locationsService, amenitiesService } from '../../services/api';
import { Save, Upload, ArrowLeft } from 'lucide-react';

const schema = yup.object().shape({
  title: yup.string().min(3, 'Title is too short').max(255).required('Title is required'),
  description: yup.string().min(10, 'Description is too short').required('Description is required'),
  price: yup.number().positive('Price must be positive').typeError('Must be a number').required('Price is required'),
  bedrooms: yup.number().min(0, 'Must be positive').integer().required(),
  bathrooms: yup.number().min(0, 'Must be positive').integer().required(),
  area: yup.number().positive('Area must be positive').required(),
  address: yup.string().min(5, 'Address too short').required(),
  zip_code: yup.string().required(),
  city_id: yup.string().required('City selection is required'),
  property_type_id: yup.string().required('Property Type is required'),
  status: yup.string().default('published'),
  is_featured: yup.boolean().default(false),
  amenity_ids: yup.array().of(yup.string()),
  purpose: yup.string().required('Purpose is required'),
  parking: yup.boolean().default(false),
  furnishing_status: yup.string().required('Furnishing status is required'),
  agent_name: yup.string().nullable().notRequired(),
  agent_phone: yup.string().nullable().notRequired(),
  agent_email: yup.string().nullable().notRequired()
});

const PropertyForm = ({ initialData, onSubmit, submitLabel = 'Save Listing', onCancel }) => {
  const [propertyTypes, setPropertyTypes] = useState([]);
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  const [amenitiesList, setAmenitiesList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedState, setSelectedState] = useState('');

  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: initialData || {
      status: 'published',
      is_featured: false,
      amenity_ids: [],
      purpose: '🏡 For Sale',
      parking: false,
      furnishing_status: 'Unfurnished',
      agent_name: '',
      agent_phone: '',
      agent_email: ''
    }
  });

  useEffect(() => {
    const loadFormMetadata = async () => {
      try {
        const [types, countryList, amenities] = await Promise.all([
          propertyService.getPropertyTypes(),
          locationsService.getCountries(),
          amenitiesService.getAmenities()
        ]);
        setPropertyTypes(types || []);
        setCountries(countryList || []);
        setAmenitiesList(amenities || []);

        if (initialData) {
          reset(initialData);
          if (initialData.city?.state) {
            setSelectedState(initialData.city.state.id);
            if (initialData.city.state.country_id) {
              setSelectedCountry(initialData.city.state.country_id);
            }
          }
        }
        setIsInitialized(true);
      } catch (err) {
        console.warn(err);
        setIsInitialized(true);
      }
    };
    loadFormMetadata();
  }, [initialData, reset]);

  useEffect(() => {
    const loadStates = async () => {
      if (selectedCountry) {
        try {
          const list = await locationsService.getStates(selectedCountry);
          setStates(list || []);
          if (isInitialized) {
            setSelectedState('');
            setCities([]);
            setValue('city_id', '');
          }
        } catch (e) {
          console.error(e);
          setStates([]);
          if (isInitialized) {
            setSelectedState('');
            setCities([]);
            setValue('city_id', '');
          }
        }
      } else {
        setStates([]);
        if (isInitialized) {
          setSelectedState('');
          setCities([]);
          setValue('city_id', '');
        }
      }
    };
    loadStates();
  }, [selectedCountry, isInitialized, setValue]);

  useEffect(() => {
    const loadCities = async () => {
      if (selectedState) {
        try {
          const list = await locationsService.getCities(selectedState);
          setCities(list || []);
          if (isInitialized) {
            setValue('city_id', '');
          }
        } catch (e) {
          console.error(e);
          setCities([]);
        }
      } else {
        setCities([]);
        if (isInitialized) {
          setValue('city_id', '');
        }
      }
    };
    loadCities();
  }, [selectedState, isInitialized, setValue]);

  const handleFormSubmit = async (data) => {
    setLoading(true);
    try {
      await onSubmit(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Title</label>
          <input
            type="text"
            {...register('title')}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
          />
          {errors.title && <span className="text-xs text-rose-500">{errors.title.message}</span>}
        </div>

        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Property Type</label>
          <select
            {...register('property_type_id')}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
          >
            <option value="">Select Type</option>
            {propertyTypes.map((t) => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>
          {errors.property_type_id && <span className="text-xs text-rose-500">{errors.property_type_id.message}</span>}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Purpose</label>
          <select
            {...register('purpose')}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
          >
            <option value="🏡 For Sale">🏡 For Sale</option>
            <option value="🏠 For Rent">🏠 For Rent</option>
            <option value="🏢 Lease">🏢 Lease</option>
            <option value="🌾 Land Investment">🌾 Land Investment</option>
          </select>
          {errors.purpose && <span className="text-xs text-rose-500">{errors.purpose.message}</span>}
        </div>

        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Furnishing Status</label>
          <select
            {...register('furnishing_status')}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
          >
            <option value="Unfurnished">Unfurnished</option>
            <option value="Semi-Furnished">Semi-Furnished</option>
            <option value="Furnished">Furnished</option>
          </select>
          {errors.furnishing_status && <span className="text-xs text-rose-500">{errors.furnishing_status.message}</span>}
        </div>

        <div className="flex items-center space-x-2 pt-6">
          <input
            type="checkbox"
            id="parking"
            {...register('parking')}
            className="w-4.5 h-4.5 text-indigo-600 border-slate-300 rounded focus:ring-indigo-500 cursor-pointer"
          />
          <label htmlFor="parking" className="text-sm font-bold text-slate-700 dark:text-slate-300 cursor-pointer">
            Parking Available
          </label>
        </div>
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 uppercase">Description</label>
        <textarea
          rows={4}
          {...register('description')}
          className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
        />
        {errors.description && <span className="text-xs text-rose-500">{errors.description.message}</span>}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Price ($)</label>
          <input type="number" {...register('price')} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none" />
          {errors.price && <span className="text-xs text-rose-500">{errors.price.message}</span>}
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Beds</label>
          <input type="number" {...register('bedrooms')} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none" />
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Baths</label>
          <input type="number" {...register('bathrooms')} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none" />
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Area (sqft)</label>
          <input type="number" {...register('area')} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Country</label>
          <select value={selectedCountry} onChange={(e) => setSelectedCountry(e.target.value)} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none">
            <option value="">Select Country</option>
            {countries.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">State</label>
          <select value={selectedState} onChange={(e) => setSelectedState(e.target.value)} disabled={!selectedCountry} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none disabled:opacity-50">
            <option value="">Select State</option>
            {states.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">City</label>
          <select {...register('city_id')} disabled={!selectedState} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none disabled:opacity-50">
            <option value="">Select City</option>
            {cities.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          {errors.city_id && <span className="text-xs text-rose-500">{errors.city_id.message}</span>}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-3 space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Address</label>
          <input type="text" {...register('address')} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none" />
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Zip Code</label>
          <input type="text" {...register('zip_code')} className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none" />
        </div>
      </div>

      {/* Cover Image Uploader */}
      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 uppercase">Photo Upload</label>
        <input type="file" {...register('imageFile')} className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100" />
      </div>

      {/* Amenities Grid */}
      {amenitiesList.length > 0 && (
        <div className="space-y-3">
          <label className="block text-xs font-bold text-slate-500 uppercase">Amenities</label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {amenitiesList.map((a) => (
              <label key={a.id} className="flex items-center gap-2 p-2.5 border border-slate-200 rounded-xl bg-slate-50 hover:bg-white cursor-pointer text-xs font-bold text-slate-700">
                <input type="checkbox" value={a.id} {...register('amenity_ids')} className="rounded border-slate-300 text-indigo-650" />
                <span>{a.name}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      {/* Agent Details Section */}
      <div className="border-t border-slate-100 dark:border-slate-800 pt-6 space-y-4">
        <h3 className="text-sm font-bold text-slate-800 dark:text-white uppercase tracking-wider">Agent Details (Optional)</h3>
        <p className="text-2xs text-slate-500">Leave blank to use your default profile contact details.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-1">
            <label className="block text-xs font-bold text-slate-500 uppercase">Agent Name</label>
            <input
              type="text"
              {...register('agent_name')}
              placeholder="e.g. John Doe"
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
            />
          </div>
          <div className="space-y-1">
            <label className="block text-xs font-bold text-slate-500 uppercase">Contact Number</label>
            <input
              type="text"
              {...register('agent_phone')}
              placeholder="e.g. +1234567890"
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
            />
          </div>
          <div className="space-y-1">
            <label className="block text-xs font-bold text-slate-500 uppercase">Agent Email</label>
            <input
              type="email"
              {...register('agent_email')}
              placeholder="e.g. agent@example.com"
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Form Buttons */}
      <div className="flex items-center gap-3 justify-end pt-4 border-t border-slate-100">
        <button type="button" onClick={onCancel} className="px-5 py-2.5 border border-slate-200 rounded-xl text-sm font-semibold hover:bg-slate-50">Cancel</button>
        <button type="submit" disabled={loading} className="px-5 py-2.5 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl text-sm shadow-md flex items-center gap-2">
          <Save className="h-4.5 w-4.5" />
          <span>{loading ? 'Submitting...' : submitLabel}</span>
        </button>
      </div>
    </form>
  );
};

export default PropertyForm;
