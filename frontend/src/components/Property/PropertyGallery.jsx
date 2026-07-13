import React, { useState } from 'react';

const PropertyGallery = ({ images = [] }) => {
  const [activeImage, setActiveImage] = useState(0);

  const getImageUrl = (img) => {
    if (!img) return 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80';
    if (img.url.startsWith('http')) return img.url;
    const cleanUrl = img.url.startsWith('/') ? img.url.substring(1) : img.url;
    return `http://localhost:8000/${cleanUrl}`;
  };

  if (images.length === 0) {
    return (
      <div className="relative h-100 rounded-3xl overflow-hidden bg-slate-100 dark:bg-slate-800">
        <img
          src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80"
          alt="Premium Property Fallback"
          className="w-full h-full object-cover"
        />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Active Main Viewport */}
      <div className="relative 'h-122.5' rounded-3xl overflow-hidden shadow-md group bg-slate-150">
        <img
          src={getImageUrl(images[activeImage])}
          alt={`View ${activeImage + 1}`}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
        />
        <div className="absolute bottom-4 left-4 px-3 py-1 bg-black/60 text-white text-xs font-bold rounded-lg backdrop-blur-md">
          {activeImage + 1} / {images.length}
        </div>
      </div>

      {/* Thumbnails row */}
      {images.length > 1 && (
        <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-thin">
          {images.map((img, idx) => (
            <button
              key={img.id || idx}
              onClick={() => setActiveImage(idx)}
              className={`relative w-24 h-16 rounded-xl overflow-hidden shrink-0 border-2 transition-all cursor-pointer ${
                activeImage === idx ? 'border-indigo-605 shadow-md scale-95' : 'border-transparent hover:border-slate-300'
              }`}
            >
              <img
                src={getImageUrl(img)}
                alt={`Thumbnail ${idx + 1}`}
                className="w-full h-full object-cover"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default PropertyGallery;
