import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useFavorites } from '../context/FavoriteContext';
import { favoritesService, propertyService } from '../services/api';
import PropertyGrid from '../components/Property/PropertyGrid';
import { Heart } from 'lucide-react';

const Favorites = () => {
  const { favorites } = useFavorites();
  const { isAuthenticated } = useAuth();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFavoriteDetails = async () => {
      setLoading(true);
      try {
        if (isAuthenticated) {
          const response = await favoritesService.getFavorites({ page: 1, size: 50 });
          const favoriteItems = response?.items || [];
          const favoriteProperties = favoriteItems
            .map((item) => item.property)
            .filter(Boolean);
          setProperties(favoriteProperties);
        } else {
          const local = localStorage.getItem('favorites');
          const ids = local ? JSON.parse(local) : [];
          if (ids.length > 0) {
            const response = await propertyService.getProperties({ limit: 100 });
            const allItems = response?.items || response || [];
            setProperties(allItems.filter(p => ids.includes(p.id)));
          } else {
            setProperties([]);
          }
        }
      } catch (err) {
        console.error(err);
        setProperties([]);
      } finally {
        setLoading(false);
      }
    };
    fetchFavoriteDetails();
  }, [isAuthenticated]);

  useEffect(() => {
    setProperties(prev => prev.filter(p => favorites.includes(p.id)));
  }, [favorites]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-indigo-900 dark:text-white tracking-tight flex items-center gap-2">
          <Heart className="h-8 w-8 text-rose-500 fill-rose-500" />
          <span>My Favorite Properties</span>
        </h1>
        <p className="text-slate-500 dark:text-slate-400 text-sm">Review your saved homes, apartments, and luxury villas.</p>
      </div>

      <PropertyGrid properties={properties} loading={loading} />
    </div>
  );
};

export default Favorites;
