import React from 'react';
import { Link } from 'react-router-dom';
import { useFavorites } from '../../context/FavoriteContext';
import { Heart, Bed, Bath, Maximize, MapPin, Sparkles } from 'lucide-react';

const PropertyCard = ({ property }) => {
  const { toggleFavorite, isFavorite } = useFavorites();
  const isFav = isFavorite(property.id);

  // Formatting price nicely (e.g. $450,000)
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(price);
  };

  const getCoverImage = () => {
    if (property.images && property.images.length > 0) {
      const cover = property.images.find(img => img.is_cover);
      const targetImg = cover || property.images[0];
      if (targetImg.url.startsWith('http')) return targetImg.url;
      const cleanUrl = targetImg.url.startsWith('/') ? targetImg.url.substring(1) : targetImg.url;
      return `http://localhost:8000/${cleanUrl}`;
    }
    // Sophisticated real-estate fallback images based on ID hash
    const fallbackImages = [
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=800&q=80'
    ];
    const index = property.title ? property.title.charCodeAt(0) % fallbackImages.length : 0;
    return fallbackImages[index];
  };

  const handleFavoriteClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    toggleFavorite(property.id);
  };

  const isSale = property.price > 5000; // Mock selling vs renting status based on price

  return (
    <div className="group relative bg-white rounded-3xl border border-slate-150 shadow-sm hover:shadow-xl hover:-translate-y-1.5 transition-all duration-350 overflow-hidden flex flex-col h-full">
      {/* Property Image & Badges */}
      <div className="relative aspect-4/3 overflow-hidden bg-slate-100">
        <img
          src={getCoverImage()}
          alt={property.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-linear-to-t from-black/40 via-transparent to-transparent pointer-events-none" />
        
        {/* Type Badges */}
        <div className="absolute top-4 left-4 flex gap-2">
          <span className={`px-3 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider text-white shadow-md ${
            isSale ? 'bg-indigo-600 shadow-indigo-200' : 'bg-emerald-500 shadow-emerald-200'
          }`}>
            {isSale ? 'For Sale' : 'For Rent'}
          </span>
          {property.is_featured && (
            <span className="px-3 py-1.5 rounded-full text-xs font-extrabold bg-amber-500 text-white flex items-center gap-1 shadow-md shadow-amber-200">
              <Sparkles className="h-3.5 w-3.5 fill-current" />
              Featured
            </span>
          )}
        </div>

        {/* Favorites button */}
        <button
          onClick={handleFavoriteClick}
          className={`absolute top-4 right-4 p-2.5 rounded-full backdrop-blur-md shadow-md border transition-all ${
            isFav 
              ? 'bg-rose-500 text-white border-rose-500 hover:bg-rose-600' 
              : 'bg-white/80 text-slate-600 border-white/20 hover:bg-white hover:text-rose-500'
          }`}
          aria-label={isFav ? 'Remove from favorites' : 'Add to favorites'}
        >
          <Heart className={`h-5 w-5 ${isFav ? 'fill-current' : ''}`} />
        </button>
      </div>

      {/* Property Details */}
      <div className="p-5 flex flex-col grow">
        <div className="flex items-center gap-1 text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <MapPin className="h-3.5 w-3.5 text-indigo-500 shrink-0" />
          <span className="truncate">{property.city?.name || 'Local Area'}, {property.address}</span>
        </div>

        <Link to={`/properties/${property.id}`} className="block mb-2 group-hover:text-indigo-600 transition-colors">
          <h3 className="font-bold text-lg text-slate-800 line-clamp-1 leading-snug">
            {property.title}
          </h3>
        </Link>
        
        <p className="text-slate-500 text-sm line-clamp-2 mb-4 grow">
          {property.description}
        </p>

        {/* Specs footer */}
        <div className="grid grid-cols-3 gap-2 py-3 border-t border-b border-slate-100 text-xs text-slate-600 font-semibold mb-4 bg-slate-50/50 rounded-2xl px-2">
          <div className="flex items-center gap-1.5 justify-center">
            <Bed className="h-4 w-4 text-indigo-500 shrink-0" />
            <span>{property.bedrooms} Beds</span>
          </div>
          <div className="flex items-center gap-1.5 justify-center border-l border-slate-200">
            <Bath className="h-4 w-4 text-indigo-500 shrink-0" />
            <span>{property.bathrooms} Baths</span>
          </div>
          <div className="flex items-center gap-1.5 justify-center border-l border-slate-200">
            <Maximize className="h-4 w-4 text-indigo-500 shrink-0" />
            <span>{property.area} sqft</span>
          </div>
        </div>

        {/* Action / Price Row */}
        <div className="flex justify-between items-center mt-auto pt-2">
          <div className="flex flex-col">
            <span className="text-xs font-bold uppercase tracking-wide text-slate-400">Price</span>
            <span className="font-extrabold text-xl text-indigo-900">{formatPrice(property.price)}</span>
          </div>
          <Link
            to={`/properties/${property.id}`}
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-600 hover:text-white rounded-xl transition-all shadow-sm"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
