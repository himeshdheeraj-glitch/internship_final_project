import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { favoritesService } from '../services/api';

const FavoriteContext = createContext(null);

export const FavoriteProvider = ({ children }) => {
  const [favorites, setFavorites] = useState([]);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const loadFavorites = async () => {
      if (isAuthenticated) {
        try {
          const res = await favoritesService.getFavorites();
          const items = res?.items || [];
          setFavorites(items.map(fav => fav.property_id || fav.id));
        } catch (e) {
          console.warn('Failed to load favorites from backend.', e);
        }
      } else {
        const local = localStorage.getItem('favorites');
        setFavorites(local ? JSON.parse(local) : []);
      }
    };
    loadFavorites();
  }, [isAuthenticated]);

  const toggleFavorite = async (propertyId) => {
    const isFav = favorites.includes(propertyId);
    let updated;
    if (isFav) {
      updated = favorites.filter(id => id !== propertyId);
    } else {
      updated = [...favorites, propertyId];
    }
    setFavorites(updated);

    if (isAuthenticated) {
      try {
        if (isFav) {
          await favoritesService.removeFavorite(propertyId);
        } else {
          await favoritesService.addFavorite(propertyId);
        }
      } catch (e) {
        console.error(e);
      }
    } else {
      localStorage.setItem('favorites', JSON.stringify(updated));
    }
  };

  const isFavorite = (propertyId) => favorites.includes(propertyId);

  return (
    <FavoriteContext.Provider value={{ favorites, toggleFavorite, isFavorite }}>
      {children}
    </FavoriteContext.Provider>
  );
};

export const useFavorites = () => useContext(FavoriteContext);
export default FavoriteContext;
