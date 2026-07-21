import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import PropertyFilters from '../components/Property/PropertyFilters';
import PropertyGrid from '../components/Property/PropertyGrid';
import Pagination from '../components/Common/Pagination';
import SearchBar from '../components/Property/SearchBar';
import { propertyService } from '../services/api';

const PropertyListing = () => {
  const location = useLocation();
  const [properties, setProperties] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const [page, setPage] = useState(1);
  const [limit] = useState(6);
  const [filters, setFilters] = useState({
    city_id: undefined,
    property_type_id: undefined,
    min_price: undefined,
    max_price: undefined,
    bedrooms: undefined,
    bathrooms: undefined,
    search_query: '',
  });

  useEffect(() => {
    if (location.state?.searchParams) {
      setFilters((prev) => ({
        ...prev,
        ...location.state.searchParams,
      }));
    } else {
      setFilters({
        city_id: undefined,
        property_type_id: undefined,
        min_price: undefined,
        max_price: undefined,
        bedrooms: undefined,
        bathrooms: undefined,
        search_query: '',
        purpose: undefined,
        parking: undefined,
        furnishing_status: undefined
      });
    }
  }, [location.state]);

  const fetchProperties = async () => {
    setLoading(true);
    try {
      const offset = (page - 1) * limit;
      const params = {
        limit,
        offset,
        sort_by: 'created_at_desc',
        ...filters,
      };

      // Clean undefined
      Object.keys(params).forEach(k => {
        if (params[k] === undefined || params[k] === '') delete params[k];
      });

      const res = await propertyService.getProperties(params);

      if (res?.items) {
        setProperties(res.items);
        setTotal(res.total || 0);
        setTotalPages(res.pages || Math.ceil((res.total || 0) / limit) || 1);
      } else {
        setProperties(res || []);
        setTotal(res?.length || 0);
        setTotalPages(1);
      }
    } catch (e) {
      console.warn('API Offline. Using fallback mock properties.');
      setProperties(mockListingDb.slice((page - 1) * limit, page * limit));
      setTotal(mockListingDb.length);
      setTotalPages(Math.ceil(mockListingDb.length / limit) || 1);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProperties();
  }, [filters, page]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-indigo-900 dark:text-white tracking-tight">Browse Properties</h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm">Discover verified luxury estates, apartments, and land plots.</p>
      </div>

        <SearchBar 
          onSearch={(q) => { setFilters(prev => ({ ...prev, ...q })); setPage(1); }} 
          initialQuery={filters.search_query} 
          initialMinPrice={filters.min_price}
          initialMaxPrice={filters.max_price}
        />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        <div className="lg:col-span-1">
          <PropertyFilters filters={filters} onFilterChange={(f) => { setFilters(f); setPage(1); }} />
        </div>
        <div className="lg:col-span-3 flex flex-col h-full">
          <PropertyGrid properties={properties} loading={loading} />
          
          <Pagination
            currentPage={page}
            totalPages={totalPages}
            onPageChange={setPage}
            totalItems={total}
          />
        </div>
      </div>
    </div>
  );
};

const mockListingDb = [
  {
    id: 'f1025de4-d2e8-468b-b1a9-b1d5a71df544',
    title: 'Contemporary Luxury Villa',
    description: 'Stunning architectural masterpiece featuring infinity pool and panoramic mountain views.',
    price: 1850000,
    bedrooms: 5,
    bathrooms: 6,
    area: 5800,
    address: '892 Beverly Estates Dr',
    zip_code: '90210',
    is_featured: true,
    city: { name: 'Beverly Hills' },
    images: [{ url: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80', is_cover: true }]
  },
  {
    id: 'a8d9b1a5-cfb8-4903-bce5-8bb2d63428ff',
    title: 'Modernist Highrise Penthouse',
    description: 'Elevated urban luxury with 360-degree views, direct elevator access and concierge services.',
    price: 2400000,
    bedrooms: 3,
    bathrooms: 3.5,
    area: 3200,
    address: '404 Skyline Ave',
    zip_code: '10001',
    is_featured: true,
    city: { name: 'New York' },
    images: [{ url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80', is_cover: true }]
  }
];

export default PropertyListing;
