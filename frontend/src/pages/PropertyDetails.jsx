import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { propertyService } from '../services/api';
import { useFavorites } from '../context/FavoriteContext';
import PropertyGallery from '../components/Property/PropertyGallery';
import PropertyFeatures from '../components/Property/PropertyFeatures';
import PropertyReviews from '../components/Property/PropertyReviews';
import { useAuth } from '../context/AuthContext';
import { Heart, MapPin, Phone, Mail, ChevronLeft, ArrowLeft } from 'lucide-react';

const PropertyDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toggleFavorite, isFavorite } = useFavorites();
  const { user } = useAuth();
  const isFav = isFavorite(id);

  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [agentForm, setAgentForm] = useState({ 
    name: user ? `${user.first_name} ${user.last_name}` : '', 
    email: user ? user.email : '', 
    message: "I'm interested in viewing this property." 
  });
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (user) {
      setAgentForm(prev => ({
        ...prev,
        name: `${user.first_name} ${user.last_name}`,
        email: user.email
      }));
    }
  }, [user]);

  useEffect(() => {
    const fetchDetails = async () => {
      setLoading(true);
      try {
        const data = await propertyService.getProperty(id);
        if (data) {
          setProperty(data);
        } else {
          setError('Property not found');
        }
      } catch (err) {
        console.warn('API Offline. Falling back to mock data.');
        const found = mockDetails.find(p => p.id === id);
        if (found) setProperty(found);
        else setError('Property not found');
      } finally {
        setLoading(false);
      }
    };
    fetchDetails();
  }, [id]);

  const handleEnquiry = (e) => {
    e.preventDefault();
    setSubmitted(true);

    const newInquiry = {
      id: Math.random().toString(36).substring(2, 9),
      property_id: property.id,
      property_title: property.title,
      property_address: property.address,
      buyer_id: user?.id || null,
      buyer_name: agentForm.name,
      buyer_email: agentForm.email,
      agent_id: property.owner_id || property.owner?.id || null,
      agent_name: property.agent_name || (property.owner?.first_name ? `${property.owner.first_name} ${property.owner.last_name}` : 'Verified Agent'),
      agent_email: property.agent_email || property.owner?.email || 'agent@estatehub.com',
      message: agentForm.message,
      created_at: new Date().toISOString()
    };

    const existing = localStorage.getItem('inquiries');
    const list = existing ? JSON.parse(existing) : [];
    list.unshift(newInquiry);
    localStorage.setItem('inquiries', JSON.stringify(list));

    setTimeout(() => {
      alert('Your request has been sent to the agent! You can track this inquiry in your dashboard.');
      setSubmitted(false);
      setAgentForm({ 
        name: user ? `${user.first_name} ${user.last_name}` : '', 
        email: user ? user.email : '', 
        message: "I'm interested in viewing this property." 
      });
    }, 1000);
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center animate-pulse">
        <div className="h-8 bg-slate-200 rounded w-1/4 mb-6" />
        <div className="h-100 bg-slate-200 rounded-3xl" />
      </div>
    );
  }

  if (error || !property) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center space-y-4">
        <h2 className="text-xl font-extrabold text-slate-800">Property Listing Not Found</h2>
        <Link to="/properties" className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl">
          <ArrowLeft className="h-4 w-4" /> Back to Listings
        </Link>
      </div>
    );
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(price);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <button onClick={() => navigate(-1)} className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-indigo-650 cursor-pointer">
          <ChevronLeft className="h-4 w-4" /> Back
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <PropertyGallery images={property.images} />
          
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-3xl space-y-4 shadow-sm">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3">
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-800 dark:text-white truncate">{property.title}</h1>
                  <button
                    onClick={() => toggleFavorite(property.id)}
                    className={`p-2 rounded-full border transition-all cursor-pointer ${
                      isFav 
                        ? 'bg-rose-500 text-white border-rose-500 hover:bg-rose-600 shadow-md shadow-rose-200' 
                        : 'bg-slate-100 hover:bg-slate-200 text-slate-600 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-700 hover:text-rose-500'
                    }`}
                    aria-label={isFav ? 'Remove from favorites' : 'Add to favorites'}
                    title={isFav ? 'Remove from favorites' : 'Add to favorites'}
                  >
                    <Heart className={`h-5 w-5 ${isFav ? 'fill-current' : ''}`} />
                  </button>
                </div>
                <p className="flex items-center gap-1 text-slate-500 dark:text-slate-400 text-sm mt-1.5">
                  <MapPin className="h-4 w-4 text-indigo-500" />
                  <span>{property.address}, {property.city?.name || 'Local Area'}</span>
                </p>
              </div>
              <div className="text-right">
                <span className="text-2xs font-extrabold uppercase text-slate-400 block">Asking Price</span>
                <span className="text-2xl font-black text-indigo-900 dark:text-indigo-400">{formatPrice(property.price)}</span>
              </div>
            </div>

            <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-sm">{property.description}</p>
          </div>

          <PropertyFeatures property={property} />

          <PropertyReviews propertyId={property.id} />
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-3xl shadow-sm space-y-6">
            <h3 className="text-base font-bold text-slate-800 dark:text-white">Contact Agent</h3>
            <div className="flex items-start gap-3 pb-4 border-b border-slate-100 dark:border-slate-800">
              <div className="h-10 w-10 rounded-xl bg-indigo-100 dark:bg-indigo-950 flex items-center justify-center text-indigo-700 dark:text-indigo-300 font-extrabold uppercase mt-1">
                {(property.agent_name || property.owner?.first_name)?.[0] || 'A'}
              </div>
              <div className="space-y-1.5 flex-1 min-w-0">
                <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200">
                  {property.agent_name || `${property.owner?.first_name || 'Agent'} ${property.owner?.last_name || 'Partner'}`}
                </h4>
                <span className="text-2xs text-indigo-650 font-bold uppercase tracking-wider block">Broker</span>
                
                {(property.agent_phone || property.owner?.phone_number) && (
                  <p className="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-400 font-medium">
                    <Phone className="h-3.5 w-3.5 text-indigo-500" />
                    <span>{property.agent_phone || property.owner?.phone_number}</span>
                  </p>
                )}
                {(property.agent_email || property.owner?.email) && (
                  <p className="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-400 font-medium">
                    <Mail className="h-3.5 w-3.5 text-indigo-500" />
                    <span className="truncate block">{property.agent_email || property.owner?.email}</span>
                  </p>
                )}
              </div>
            </div>

            <form onSubmit={handleEnquiry} className="space-y-4">
              <div className="space-y-1">
                <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Name</label>
                <input
                  type="text"
                  required
                  placeholder="Alice Smith"
                  value={agentForm.name}
                  onChange={(e) => setAgentForm({ ...agentForm, name: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
                />
              </div>

              <div className="space-y-1">
                <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Email</label>
                <input
                  type="email"
                  required
                  placeholder="alice@example.com"
                  value={agentForm.email}
                  onChange={(e) => setAgentForm({ ...agentForm, email: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
                />
              </div>

              <div className="space-y-1">
                <label className="block text-2xs font-bold text-slate-400 dark:text-slate-500 uppercase">Message</label>
                <textarea
                  rows={3}
                  required
                  value={agentForm.message}
                  onChange={(e) => setAgentForm({ ...agentForm, message: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
                />
              </div>

              <button type="submit" disabled={submitted} className="w-full py-2.5 bg-indigo-650 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-xl text-sm shadow-md cursor-pointer transition-colors">
                {submitted ? 'Sending Request...' : 'Send Message'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const mockDetails = [
  {
    id: 'f1025de4-d2e8-468b-b1a9-b1d5a71df544',
    title: 'Contemporary Luxury Villa',
    description: 'Beautiful luxury villa with sunset views and private pool.',
    price: 1850000,
    bedrooms: 5,
    bathrooms: 6,
    area: 5800,
    address: '892 Beverly Estates Dr',
    zip_code: '90210',
    city: { name: 'Beverly Hills' },
    owner: { first_name: 'Jonathan', last_name: 'Doe', email: 'jonathan.doe@antigravity.com' },
    images: [{ url: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80', is_cover: true }]
  }
];

export default PropertyDetails;
