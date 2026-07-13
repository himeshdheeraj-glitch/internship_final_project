import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/Property/SearchBar';
import PropertyCard from '../components/Property/PropertyCard';
import { propertyService } from '../services/api';
import { ArrowRight, CheckCircle2, Star, Shield, Users } from 'lucide-react';

const Home = () => {
  const [featuredProperties, setFeaturedProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFeatured = async () => {
      try {
        const res = await propertyService.getProperties({ is_featured: true, limit: 3 });
        if (res?.items && res.items.length > 0) {
          setFeaturedProperties(res.items);
        } else {
          const fallbackRes = await propertyService.getProperties({ limit: 3 });
          if (fallbackRes?.items && fallbackRes.items.length > 0) {
            setFeaturedProperties(fallbackRes.items);
          } else {
            setFeaturedProperties(mockFeaturedProperties);
          }
        }
      } catch (err) {
        console.warn('Backend offline or error. Using mock featured data.', err);
        setFeaturedProperties(mockFeaturedProperties);
      } finally {
        setLoading(false);
      }
    };
    fetchFeatured();
  }, []);

  const handleSearch = (searchParams) => {
    // Redirect to property listings page passing parameters in state
    navigate('/properties', { state: { searchParams } });
  };

  return (
    <div className="space-y-20 pb-20">
      {/* Hero Section */}
      <section className="relative min-h-[80vh] flex items-center justify-center bg-slate-950 overflow-hidden">
        {/* Background Image with Dark Overlay */}
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center opacity-40" />
        <div className="absolute inset-0 bg-linear-to-tr from-slate-950 via-slate-950/90 to-indigo-950/40" />
        
        {/* Dynamic Light Blobs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8 py-16">
          <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 uppercase tracking-widest">
            <Star className="h-3 w-3 fill-indigo-300 text-indigo-300" />
            Premium Real Estate Platform
          </span>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
            Find Your Perfect Property with <br />
            <span className="bg-linear-to-r from-emerald-400 to-indigo-400 bg-clip-text text-transparent">
              Sophisticated Simplicity
            </span>
          </h1>

          <p className="text-lg text-slate-300 max-w-2xl mx-auto font-medium">
            Discover a curated collection of premium properties tailored to your lifestyle. We connect buyers and verified agents seamlessly.
          </p>

          <div className="w-full max-w-4xl mx-auto pt-6">
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>
      </section>

      {/* Purpose & Categories Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-10">
        <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 p-8 rounded-3xl shadow-xl space-y-8">
          
          {/* Quick Purpose Filter */}
          <div className="text-center space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-600">Quick Filter by Purpose</h3>
            <div className="flex flex-wrap justify-center gap-3">
              {[
                { label: '🏡 For Sale', value: '🏡 For Sale' },
                { label: '🏠 For Rent', value: '🏠 For Rent' },
                { label: '🏢 Lease', value: '🏢 Lease' },
                { label: '🌾 Land Investment', value: '🌾 Land Investment' }
              ].map(item => (
                <button
                  key={item.value}
                  onClick={() => navigate('/properties', { state: { searchParams: { purpose: item.value } } })}
                  className="px-5 py-2.5 bg-slate-50 dark:bg-slate-950 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 border border-slate-200 dark:border-slate-800 hover:border-indigo-400 rounded-2xl text-sm font-bold text-slate-700 dark:text-slate-300 transition-all cursor-pointer"
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          <hr className="border-slate-100 dark:border-slate-800" />

          {/* Interactive Property Categories */}
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-xl font-extrabold text-slate-900 dark:text-white">Explore Property Categories</h2>
              <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">Select a category to view matching listings instantly.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
              {[
                {
                  title: 'Residential Properties',
                  icon: '🏡',
                  subtypes: ['Houses', 'Apartments/Flats', 'Villas', 'Condominiums (Condos)', 'Townhouses', 'Duplexes and Triplexes'],
                  query: 'Residential'
                },
                {
                  title: 'Commercial Properties',
                  icon: '🏢',
                  subtypes: ['Office buildings', 'Retail shops', 'Shopping malls', 'Hotels', 'Restaurants'],
                  query: 'Commercial'
                },
                {
                  title: 'Industrial Properties',
                  icon: '🏭',
                  subtypes: ['Warehouses', 'Factories', 'Manufacturing plants', 'Distribution centers'],
                  query: 'Industrial'
                },
                {
                  title: 'Land',
                  icon: '🌾',
                  subtypes: ['Residential plots', 'Commercial plots', 'Agricultural land', 'Farm land', 'Development land'],
                  query: 'Land'
                },
                {
                  title: 'Special Purpose',
                  icon: '🏛️',
                  subtypes: ['Schools', 'Hospitals', 'Hotels and resorts', 'Religious buildings', 'Sports complexes'],
                  query: 'Special'
                }
              ].map(cat => (
                <div key={cat.title} className="p-5 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-800/80 rounded-2xl flex flex-col justify-between hover:shadow-md transition-shadow">
                  <div>
                    <span className="text-3xl block mb-2">{cat.icon}</span>
                    <h4 className="font-extrabold text-sm text-slate-800 dark:text-slate-100 mb-3">{cat.title}</h4>
                    <ul className="space-y-1 text-2xs text-slate-500 dark:text-slate-400">
                      {cat.subtypes.map(sub => (
                        <li key={sub}>
                          <button
                            onClick={() => navigate('/properties', { state: { searchParams: { search_query: sub } } })}
                            className="hover:text-indigo-600 dark:hover:text-indigo-400 hover:underline text-left cursor-pointer transition-colors text-2xs"
                          >
                            • {sub}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <button
                    onClick={() => navigate('/properties', { state: { searchParams: { search_query: cat.query } } })}
                    className="mt-4 w-full text-center py-1.5 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 font-bold text-2xs rounded-lg hover:bg-indigo-100 transition-colors"
                  >
                    View All {cat.title.split(' ')[0]}
                  </button>
                </div>
              ))}
            </div>
          </div>

        </div>
      </section>

      {/* Featured Properties */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-indigo-600">Featured Listings</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-1">Our Premier Collection</h2>
          </div>
          <button
            onClick={() => navigate('/properties')}
            className="inline-flex items-center gap-2 text-sm font-bold text-indigo-600 hover:text-indigo-700 transition-colors cursor-pointer group"
          >
            <span>Browse all listings</span>
            <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[1, 2, 3].map((n) => (
              <div key={n} className="bg-white rounded-3xl border border-slate-200 p-4 space-y-4 animate-pulse">
                <div className="aspect-4/3 bg-slate-200 rounded-2xl" />
                <div className="h-4 bg-slate-200 rounded w-2/3" />
                <div className="h-4 bg-slate-200 rounded w-1/2" />
                <div className="h-10 bg-slate-200 rounded-xl" />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {featuredProperties.map((property) => (
              <PropertyCard key={property.id} property={property} />
            ))}
          </div>
        )}
      </section>

      {/* Benefits / Brand section */}
      <section className="bg-slate-100/60 border-y border-slate-200/50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-10">
          <div className="flex flex-col items-center text-center p-6 space-y-4">
            <div className="p-4 bg-white rounded-2xl shadow-sm text-indigo-600 border border-slate-200/40">
              <Shield className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-800">100% Verified Listings</h3>
            <p className="text-slate-500 text-sm">
              Every property listed on our platform undergoes a meticulous background check to protect your safety and investment.
            </p>
          </div>

          <div className="flex flex-col items-center text-center p-6 space-y-4">
            <div className="p-4 bg-white rounded-2xl shadow-sm text-emerald-500 border border-slate-200/40">
              <Users className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-800">Experienced Trusted Agents</h3>
            <p className="text-slate-500 text-sm">
              Connect with top local agents who can guide you with real market insights and detailed consultation.
            </p>
          </div>

          <div className="flex flex-col items-center text-center p-6 space-y-4">
            <div className="p-4 bg-white rounded-2xl shadow-sm text-amber-500 border border-slate-200/40">
              <CheckCircle2 className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-800">Seamless Acquisition</h3>
            <p className="text-slate-500 text-sm">
              From touring to paperwork and closing, enjoy an integrated home buying journey engineered with modern convenience.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

// Rich Mock Data fallback if API fails
const mockFeaturedProperties = [
  {
    id: 'f1025de4-d2e8-468b-b1a9-b1d5a71df544',
    title: 'Contemporary Luxury Villa',
    description: 'Stunning architectural masterpiece featuring zero-edge infinity pool, panoramic mountain views, high ceilings, automated security systems and top tier amenities.',
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
    description: 'Elevated urban luxury with 360-degree views, direct elevator access, state of the art Miele appliances, custom cabinetry and building concierge services.',
    price: 2400000,
    bedrooms: 3,
    bathrooms: 3.5,
    area: 3200,
    address: '404 Skyline Ave, Penthouse 4',
    zip_code: '10001',
    is_featured: true,
    city: { name: 'New York' },
    images: [{ url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80', is_cover: true }]
  },
  {
    id: 'c4e9d721-e325-4c07-bd83-11b3e506ab1a',
    title: 'Coastal Minimalist Escape',
    description: 'Serene beach front sanctuary featuring cedar wood construction, floor-to-ceiling windows, private beach pathway, solar energy grid, and wrap around deck.',
    price: 3100000,
    bedrooms: 4,
    bathrooms: 4,
    area: 4100,
    address: '228 Malibu Cove Blvd',
    zip_code: '90265',
    is_featured: true,
    city: { name: 'Malibu' },
    images: [{ url: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80', is_cover: true }]
  }
];

export default Home;
